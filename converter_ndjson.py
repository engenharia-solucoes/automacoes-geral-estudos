import json

def ler_json(arq_json):
    with open(arq_json, 'r', encoding='utf8') as f:
        return json.load(f)
    
def convertJsonToNdjson(outputJson, nomeArqNDJson) -> None:
        data = outputJson
        #print(data)
        

        # O retorno dos dicts sempre será dentro do json no campo data
        resultado = [json.dumps(registro) for registro in data['data']]
        #print("resultado: ", resultado)
        with open(f'{nomeArqNDJson}', 'w') as obj:
            for incidente in resultado:
                obj.write(incidente+'\n')
    
ler = ler_json('arquivo.json')
convertJsonToNdjson(ler, 'aquiii.json')