from credenciais import credenciais
from main import SentinelOne, ElasticSiem

host = credenciais.get('host')
port = credenciais.get('port')
login_email = credenciais.get('login_email')
senha_email = credenciais.get('senha_email')
api_token = credenciais.get('api_token')
url_sentinel = credenciais.get('url_sentinel')
url_elastic = credenciais.get('url_elastic')
login_elastic = credenciais.get('login_elastic')
senha_elastic = credenciais.get('senha_elastic')


# passa dados referentes ao provedor de envio de email, quem irá receber as notificações 
sentinel = SentinelOne(API_TOKEN=api_token, url_base=url_sentinel, host=host, port=port, login_email=login_email, senha_email=senha_email, destinatarios=['gabriel.vasconcelos@bidweb.com.br'])

try:
    data_api = sentinel.check_date_expire_api_token('1642148365526354102')

    if data_api < 10:
        sentinel.send_notification(dict_titulo_mensagem_a_enviar={'Dias restantes até o API TOKEN expirar' : f'{data_api} dias', 'Mensagem' : 'Por favor atualize a chave de api e repasse para o desenvolvedor responsável.'}, nome_cliente='MV')
        print('Notificação de vencimento de chave de api enviada')

except TypeError as err:
    sentinel.send_notification(dict_titulo_mensagem_a_enviar={'Error' : 'Sua chave de API expirou'}, nome_cliente='MV')
    print('errro de chave -> email enviado')
    print(err)
except Exception as err:
    sentinel.send_notification(dict_titulo_mensagem_a_enviar={'Error' : err}, nome_cliente='MV')
    print('errroooo exceção genérica -> email enviado')
    print(err)


try:
    sites = sentinel.get_sites()

    groups = sentinel.get_groups_ids()

    for c in groups:
        for v in sites:
            if sites[v] == c['siteId']:
                c['site_name'] = v

    # criando instancia do elasticsearch e passando por parametro o ndjson acima
    es = ElasticSiem(url_elastic=url_elastic, login_elastic=login_elastic, senha_elastic=senha_elastic)

    for c in groups:
        nome_arquivo_json = sentinel.get_applications(group_id=c['id'], limit=1000)

        sentinel.convertJsonToNdjson(nome_arquivo_json, f"MVapplicationsNDJson-{c['site_name']}-{c['name']}.json")

        es.send_json_to_elk(file_name=f"MVapplicationsNDJson-{c['site_name']}-{c['name']}.json", index_name="mv-sentinel-application-teste-novo", tipo_envio="application", nome_cliente="MV", site_name=c['site_name'], group_name=c['name'])

except Exception as err:
        sentinel.send_notification(dict_titulo_mensagem_a_enviar={'Error NDJSON' : err}, nome_cliente='MV')
        print('errro no ndjson ou elastic')
        print(err)









