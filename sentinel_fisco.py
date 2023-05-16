from xml.dom import NotFoundErr
import requests
import json
from elasticsearch import Elasticsearch
import json
import os
import datetime
import warnings
from credenciais import credenciais

api_token = credenciais.get('api_token')
url = credenciais.get('url')

warnings.filterwarnings("ignore")

# This API token will expire on 3/5/23

class SentinelOne:


    def __init__(self, API_TOKEN: str = api_token, url_base: str = url, limit: int =100) -> None:

        self.API_TOKEN = API_TOKEN
        self.url_base = url_base
        self.limit = limit
        

        self._headers = {
            "Authorization": "ApiToken " + self.API_TOKEN,
            "Content-Type": "application/json"
        }

        

        

    # Método para chamar api, retornar a consulta e converter valores no threats.json
    # Este método retorna o nome do arquivo json gerado para ser consumido pelo método abaixo
    def generateJsonToCallAPI(self) -> str:
    
        # url de filtro para incidentes unresolved, ordem decrescente de acordo com a data de criação dos incidentes
        self.url_base += f'/web/api/v2.1/threats?sortOrder=desc&sortBy=createdAt&limit={self.limit}&incidentStatuses=unresolved'
        #self.url_base += f'/web/api/v2.1/threats?sortOrder=desc&sortBy=createdAt&limit={self.limit}'
        response = requests.get(self.url_base, headers=self._headers)
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
    def __init__(self, url: str = 'https://10.83.201.181:9200', login: str = 'bidlabs', senha: str = 'Otce3cd@m+d'):
        self.url = url
        self.login = login
        self.senha = senha
        self.verify_certs = False

        self.es = Elasticsearch(
            self.url,
            http_auth=(self.login, self.senha),
            verify_certs=self.verify_certs
        )

    
    def send_json_to_elk(self, file_name, index_name):
        try:
            with open(file_name) as fp:
                for line in fp:
                    line = line.replace("\n", "")

                    # pegando os threats id (cada evento tem um id unico) para setar eles como id no index, impedindo que haja duplicação de dados
                    linha_json = json.loads(line)
                    #print(linha_json['id'])

                    try:
                        obter = self.es.get(index=index_name, id=linha_json['threatInfo']['threatId'])
                    except:
                       
                        jdoc = {"data": linha_json, "timefield": datetime.datetime.utcnow().isoformat(), "Cliente": "Fisco Saude"}
                        self.es.index(index=index_name, doc_type='_doc', body=jdoc, id=linha_json['threatInfo']['threatId'])


                    #self.es.indices.refresh(index=index_name)

            #print(self.es.get(index=index_name, id=linha_json['threatInfo']['threatId']))
            #print(type(self.es.get(index=index_name, id=linha_json['threatInfo']['threatId'])))
            #print(self.es.get(index=index_name, id=linha_json['threatInfo']['threatId'])['_id'])
            print(f"Finished upload: {index_name}")
        except Exception as e:
            print(e)



if __name__ == "__main__":
    
    # altere limite para resultado de quantos incidentes desejar
    # chamando sentinel para gerar arquivo de threats em ndson
    
    sentinel = SentinelOne(limit=1000)

    nome_arquivo_json = sentinel.generateJsonToCallAPI()

    #sentinel.convertJsonToNdjson(nome_arquivo_json, "/home/sentinel0/SentinelScript/battousai/threatsNDJson.json")
    sentinel.convertJsonToNdjson(nome_arquivo_json, "arquivo.json")
    
    '''
    # criando instancia do elasticsearch e passando por parametro o ndjson acima
    es = ElasticSiem()

    #es.send_json_to_elk("/home/sentinel0/SentinelScript/battousai/threatsNDJson.json", "my-index-gabriel", "sentinel_test")
    es.send_json_to_elk("threatsNDJson-FiscoGustavo.json", "gustavo_teste")
    '''
