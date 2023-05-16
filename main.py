import requests
import json
from elasticsearch import Elasticsearch
import json
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SentinelOne:


    def __init__(self, API_TOKEN: str, url_base: str,  host: str, port: str, login_email: str, senha_email: str, destinatarios: list) -> None:

        self.API_TOKEN = API_TOKEN
        self.url_base = url_base
        

        self._headers = {
            "Authorization": "ApiToken " + self.API_TOKEN,
            "Content-Type": "application/json"
        }

        self.host = host
        self.port = port
        self.login_email = login_email
        self.senha_email = senha_email
        self.destinatarios = destinatarios

        self.now = datetime.datetime.now()
        self.now_str = self.now.strftime('%Y-%m-%d %H:%M:%S')

        # Obter a data e hora de ontem
        self.yesterday = self.now - datetime.timedelta(days=7)
        self.yesterday_str = self.yesterday.strftime('%Y-%m-%d %H:%M:%S')


    def _get_api_token_expires_date(self, user_id: str) -> str:
        self.url_base_local = self.url_base + f'/web/api/v2.1/users/{user_id}/api-token-details'
        response = requests.get(self.url_base_local, headers=self._headers)
        
        responseJson = response.json()

        try:
            expire_date = responseJson['data']['expiresAt']
            
        except:
            expire_date = responseJson['errors'][0]['detail']
            
        return expire_date
    

    def _convert_date_to_milliseconds(self, date_str: str) -> int:

        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        timestamp = int(date_obj.timestamp())

        milliseconds = timestamp * 1000

        return milliseconds


    def get_service_users(self) -> dict:
        self.url_base_local = self.url_base + f'/web/api/v2.1/service-users?limit=1000'
        response = requests.get(self.url_base_local, headers=self._headers)
        
        responseJson = response.json()

        return responseJson
    

    def get_users(self) -> dict:
        self.url_base_local = self.url_base + f'/web/api/v2.1/users?limit=1000'
        response = requests.get(self.url_base_local, headers=self._headers)
        
        responseJson = response.json()

        return responseJson
    

    def get_sites(self) -> dict:
        self.url_base_local = self.url_base + f'/web/api/v2.1/sites?limit=1000'
        response = requests.get(self.url_base_local, headers=self._headers)
        
        responseJson = response.json()

        dicionario_final = {}

        for c in responseJson['data']['sites']:
            #print(c['id'])
            #print(c['name'])
            dicionario_final[c['name']] = c['id']
            #print('\n')

        return dicionario_final
    
    '''
    def get_group_id(self, site_id: str) -> dict:
        self.url_base_local = self.url_base + f'/web/api/v2.1/groups?limit=200&siteIds={site_id}'
        response = requests.get(self.url_base_local, headers=self._headers)
        
        responseJson = response.json()

        dicionario_final = {}

        #print(responseJson)
        for c in responseJson['data']:
            #print(c)
            #print(c['id'])
            #print(c['name'])
            dicionario_final[c['name']] = c['id']
            #print('\n')

        return dicionario_final
    '''
    

    def get_groups_ids(self) -> list:
        self.url_base_local = self.url_base + f'/web/api/v2.1/groups?limit=200'
        response = requests.get(self.url_base_local, headers=self._headers)
        
        responseJson = response.json()

        lista_final = []
        for c in responseJson['data']:
            dicionario_final = {}
            dicionario_final['id'] = c['id']
            dicionario_final['name']= c['name']
            dicionario_final['siteId'] = c['siteId']
            lista_final.append(dicionario_final)


        return lista_final
    

    def get_applications(self, group_id: str, limit: int) -> str:
        print('ontem: ', self.yesterday_str)
        print('hoje: ', self.now_str)

        data1 = self._convert_date_to_milliseconds(self.yesterday_str)
        data2 = self._convert_date_to_milliseconds(self.now_str)

        print(data1)
        print(data2)

        data1_teste = '1678849200000' #15 de março de 2023   
        data2_teste = '1680145200000' #30 de março de 2023
       
        self.url_base_local = self.url_base + f'/web/api/v2.1/application-management/risks?detectionDate__between={data1}-{data2}&groupIds={group_id}&limit={limit}&severities=CRITICAL,HIGH,MEDIUM&sortBy=detectionDate&sortOrder=desc'
        response = requests.get(self.url_base_local, headers=self._headers)
        
        responseJson = response.json()
        
        print(responseJson)
        return responseJson

        
    
    def check_date_expire_api_token(self, id_user_api_token: str) -> int:
        data_atual = datetime.datetime.now().date()

        expiresAt = self._get_api_token_expires_date(id_user_api_token)

        data_obj = datetime.datetime.strptime(expiresAt, '%Y-%m-%dT%H:%M:%S.%fZ').date()
        diferenca = data_obj - data_atual

        print('aq')
        return diferenca.days



    def send_notification(self, dict_titulo_mensagem_a_enviar: dict, nome_cliente: str) -> None:

        server = smtplib.SMTP(self.host, self.port)
        server.ehlo()
        server.starttls()

        server.login(self.login_email, self.senha_email)

        palavra = ''
        for linha in dict_titulo_mensagem_a_enviar:
            palavra += f'''
                         <tr><td colspan="2" style="width: 100%; text-align: left; padding: 10px; font-family: 'Work Sans', sans-serif; color: rgba(118,113,113,1); background-color: rgba(242, 242, 242, 1); font-size: 14px;" >{linha}: {dict_titulo_mensagem_a_enviar[linha]} </td></tr>\n
                        '''


        corpo = f'''
            <table style=" width: 100%; text-align: center;">
            <tr >   
                <td style="background-color: rgba(255, 255, 255, 1); width: 100%; text-align: center; padding: 100px 0px;">
                    <table style=" width: 700px; margin: 0 auto; text-align: center; border-spacing: 0px;">
                        <tr><td colspan="2" style="width: 100%; text-align: center; padding: 20px 0px 0px 0px; font-family: 'Work Sans', sans-serif; font-style: italic; font-size: 25px; color: #FF6565;               background-color: #F2F2F2; border-radius: 5px 5px 0px 0px;"><img src="https://i.ibb.co/x7gMxZH/Imagem1.png" width="250px"></td></tr>
                        <tr><td colspan="2" style=" width: 100%; text-align: center; padding: 10px; font-family: 'Work Sans', sans-serif; font-size: 25px;  color: #F9F9F9; background-color:#e70f69;                  ">Security Operation Center</td></tr>
                        <tr><td colspan="2" style="width: 100%; text-align: center; padding: 9px; font-family: 'Work Sans', sans-serif; color: #fff; background-color: rgba(0, 173, 168, 1); font-size:                 18px;" >API TOKEN EXPIRES</td></tr>
                        <tr><td colspan="2" style="width: 100%; text-align: left; padding: 10px; font-family: 'Work Sans', sans-serif; color: rgba(118,113,113,1); background-color: rgba(242, 242, 242, 1);            font-size: 14px;" ><br><br><b>Caro responsável,</b> <br><br>Somos a equipe Bidlabs que cuida do monitoramento de incidentes de segurança da organização MV Informática.</td></tr>
                        <tr><td colspan="2" style="width: 100%; text-align: left; padding: 10px; font-family: 'Work Sans', sans-serif; color: rgba(118,113,113,1); background-color: rgba(242, 242, 242, 1); font-size: 14px;" >Nossos logs indicam um incidente em um de seus Links.</td></tr>
                        <tr><td colspan="2" style="width: 100%; text-align: left; padding: 10px; font-family: 'Work Sans', sans-serif; color: rgba(118,113,113,1); background-color: rgba(242, 242, 242, 1); font-size: 14px;" ><br><br><b>Informações do Evento:</b></td></tr>
                        <tr><td colspan="2" style="width: 100%; text-align: left; padding: 10px; font-family: 'Work Sans', sans-serif; color: rgba(118,113,113,1); background-color: rgba(242, 242, 242, 1); font-size: 14px;" >Cliente: {nome_cliente} </td></tr>
                        {palavra}
                        <tr><td colspan="2" style="width: 100%; text-align: left; padding: 10px; font-family: 'Work Sans', sans-serif; color: rgba(118,113,113,1); background-color: rgba(242, 242, 242, 1); font-size: 14px;" ><b>Caso haja novos alertas você receberá outro e-mail notificando.</b></td></tr>
                        <tr><td colspan="2" style="width: 100%; text-align: left; padding: 10px; font-family: 'Work Sans', sans-serif; color: rgba(118,113,113,1); background-color: rgba(242, 242, 242, 1); font-size: 14px;" ><br><br>Atenciosamente,<br><b>Bidweb Security IT</b></td></tr>
                        

                        <!--<tr><td colspan="2" style="font-family: 'Work Sans', sans-serif; color: #fff; background-color: #DBDBDB;; text-align: center; height: 150px;"></td></tr>-->
                    </table>

                    <table style="width: 700px; padding: 20px; border-spacing: 6px; background-color: #F2F2F2; margin: 0 auto; border-radius: 0px 0px 5px 5px; padding: 25px;">
                        <tr>
                            <td style="padding: 10px 0px 0px 0px; font-family: 'Work Sans', sans-serif; color: #fff; text-align: center; height: 150px;"> <a href="http://bidweb.com.br" target="_blank"><img src="https://i.ibb.co/ZcgXyPf/bidwebsecurityit.png" width="200px"></a>
                                <td>
                                    <p style="padding: 20px 0px 0px 0px; text-align: right; font-family: 'Work Sans', sans-serif; color: #0090A4; font-size: 14px;">
                                        <b>BID Comércio e Serviços em Tecnologia<br>da Informação Ltda.</b><br>
                                        Av. Marquês de Olinda, 296<br>
                                        4º Andar Edf. Tigre<br>
                                        Bairro do Recife 50030-000 Recife PE<br>
                                        Tel +55(81) 3032 0943/3339/3786<br>
                                        atendimento@bidweb.com.br<br>
        www.bidweb.com.br<br>
                                        CNPJ: 05.020.356/0001-00
                                    </p>
                                </td>

                            </td>
                        </tr>
                    </table>

                </td>
            </tr>
        </table>

        '''

        email_msg = MIMEMultipart()
        recipients = self.destinatarios
        email_msg['From'] = self.login_email
        email_msg['To'] = ", ".join(recipients)
        email_msg['Subject'] = f"[BL-SENTINEL] Detecção de Vencimento API TOKEN - [{nome_cliente}]"

        email_msg.attach(MIMEText(corpo, 'html'))


        # enviar email
        server.sendmail(email_msg['From'], recipients, email_msg.as_string())
        server.quit()

    # Método para chamar api, retornar a consulta e converter valores no threats.json
    # Este método retorna o nome do arquivo json gerado para ser consumido pelo método abaixo
    def generateJsonToCallAPI(self, limit) -> str:
    
        # url de filtro para incidentes unresolved, ordem decrescente de acordo com a data de criação dos incidentes
        self.url_base_local = self.url_base + f'/web/api/v2.1/threats?sortOrder=desc&sortBy=createdAt&limit={limit}&incidentStatuses=unresolved'
        #self.url_base += f'/web/api/v2.1/threats?sortOrder=desc&sortBy=createdAt&limit={self.limit}'
        response = requests.get(self.url_base_local, headers=self._headers)
        print("status code: ", response.status_code)
        responseJson = response.json()
        
        #with open(f"{_nome_arquivo_json}", "w") as outfile:
        #    json.dump(responseJson, outfile)

        return responseJson


    # método que irá receber o arquivo json criado pela chamada acima, e gerar um ndjson a partir dele
    def convertJsonToNdjson(self, outputJson, nomeArqNDJson) -> None:
        data = outputJson
        #print(data)
        

        # O retorno dos dicts sempre será dentro do json no campo data
        resultado = [json.dumps(registro) for registro in data['data']]
        #print("resultado: ", resultado)
        with open(f'{nomeArqNDJson}', 'w') as obj:
            for incidente in resultado:
                obj.write(incidente+'\n')




class ElasticSiem:
    def __init__(self, url_elastic: str, login_elastic: str, senha_elastic: str):
        self.url = url_elastic
        self.login = login_elastic
        self.senha = senha_elastic
        self.verify_certs = False

        self.es = Elasticsearch(
            self.url,
            http_auth=(self.login, self.senha),
            verify_certs=self.verify_certs
        )

    
    def send_json_to_elk(self, file_name, index_name, tipo_envio, nome_cliente, site_name="", group_name=""):
        try:
            with open(file_name) as fp:
                for line in fp:
                    line = line.replace("\n", "")

                    # pegando os threats id (cada evento tem um id unico) para setar eles como id no index, impedindo que haja duplicação de dados
                    linha_json = json.loads(line)
                    #print(linha_json['id'])

                    if tipo_envio == 'threat':
                        id_envio = linha_json['threatInfo']['threatId']

                        try:
                            obter = self.es.get(index=index_name, id=id_envio)
                        except:
                        
                            jdoc = {"data": linha_json, "timefield": datetime.datetime.utcnow().isoformat(), "Cliente": f"{nome_cliente}"}
                            self.es.index(index=index_name, doc_type='_doc', body=jdoc, id=id_envio)
                    
                    elif tipo_envio == 'application':
                        id_envio = linha_json['id']

                        try:
                            obter = self.es.get(index=index_name, id=id_envio)
                        except:
                        
                            jdoc = {"data": linha_json, "timefield": datetime.datetime.utcnow().isoformat(), "Cliente": f"{nome_cliente}", "site_name" : f"{site_name}", "group_name" : f"{group_name}"}
                            self.es.index(index=index_name, doc_type='_doc', body=jdoc, id=id_envio)

                    

        

            print(f"Finished upload: {index_name}")
        except Exception as e:
            print(e)


    
    

    
    
