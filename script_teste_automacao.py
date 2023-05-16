import random

client_name_input = input('informe o nome do cliente: ')
api_key_input = input('informe a chave de api do cliente: ')

password = random.randint(1, 100)

salt = b"\xdd\x961\xd8WYB\xaf\x94\xc7\rL\x01\xf4\xc3`\xcbw;\xdc\x1f\xe1\xecC3\xeefi\xba\x1b\xf5\x89"



valor = f'''

# video https://www.youtube.com/watch?v=gyPuAJfOnGk

from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


# área do cesar
# chave atual zwtz1rlMEFtNFf9e6Dqo2moid2Z2r68eCcDsAPz0j5snt4rcLZ2mLyMLBmi75GgjGx3hImmJxFpyzysv
api_token_{client_name_input}_a_criptografar = b"{api_key_input}"

# gerando a key
salt = {salt}
key_{client_name_input} = PBKDF2({password}, salt, dkLen=32)


# através da chave, iremos criptografar a senha
cipher_{client_name_input} = AES.new(key_{client_name_input}, AES.MODE_CBC)


# área da mv
ciphered_api_token_{client_name_input} = cipher_{client_name_input}.encrypt(pad(api_token_{client_name_input}_a_criptografar, AES.block_size))


with open('key_{client_name_input}.bin', 'wb') as f:
    f.write(key_{client_name_input})

# # área do cesar
with open('api_token_{client_name_input}.bin', 'wb') as f:
    f.write(cipher_{client_name_input}.iv)
    f.write(ciphered_api_token_{client_name_input})

'''

print(valor)













