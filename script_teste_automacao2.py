# video https://www.youtube.com/watch?v=gyPuAJfOnGk

from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


# área do cesar
# chave atual zwtz1rlMEFtNFf9e6Dqo2moid2Z2r68eCcDsAPz0j5snt4rcLZ2mLyMLBmi75GgjGx3hImmJxFpyzysv
api_token_gabriel_a_criptografar = b"12345"

# gerando a key
salt = b'\xdd\x961\xd8WYB\xaf\x94\xc7\rL\x01\xf4\xc3`\xcbw;\xdc\x1f\xe1\xecC3\xeefi\xba\x1b\xf5\x89'     
key_gabriel = PBKDF2(70, salt, dkLen=32)


# através da chave, iremos criptografar a senha
cipher_gabriel = AES.new(key_gabriel, AES.MODE_CBC)


# área da mv
ciphered_api_token_gabriel = cipher_gabriel.encrypt(pad(api_token_gabriel_a_criptografar, AES.block_size))


with open('key_gabriel.bin', 'wb') as f:
    f.write(key_gabriel)

# # área do cesar
with open('api_token_gabriel.bin', 'wb') as f:
    f.write(cipher_gabriel.iv)
    f.write(ciphered_api_token_gabriel)