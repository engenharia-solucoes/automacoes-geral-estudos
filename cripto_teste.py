# video https://www.youtube.com/watch?v=gyPuAJfOnGk

from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


# área do cesar
# chave atual zwtz1rlMEFtNFf9e6Dqo2moid2Z2r68eCcDsAPz0j5snt4rcLZ2mLyMLBmi75GgjGx3hImmJxFpyzysv
api_token_cesar_a_criptografar = b"hgdjsadgadajdkask"



# primeiro passo será gerar uma chave

'''
#rodar esse trecho de código, copiar a simple_key e colar esse valor no salt
simple_key = get_random_bytes(32)
print(simple_key)
'''

# parâmetros utilizados para passar na key
salt = b'\xdd\x961\xd8WYB\xaf\x94\xc7\rL\x01\xf4\xc3`\xcbw;\xdc\x1f\xe1\xecC3\xeefi\xba\x1b\xf5\x89'
password = '@#OJKpT@opIFGsKl&'

# gerando a key
key_cesar = PBKDF2(password, salt, dkLen=32)


# através da chave, iremos criptografar a senha
cipher_cesar = AES.new(key_cesar, AES.MODE_CBC)


# área da mv
ciphered_api_token_cesar = cipher_cesar.encrypt(pad(api_token_cesar_a_criptografar, AES.block_size))


with open('key_cesar.bin', 'wb') as f:
    f.write(key_cesar)

# # área do cesar
with open('api_token_cesar.bin', 'wb') as f:
    f.write(cipher_cesar.iv)
    f.write(ciphered_api_token_cesar)










