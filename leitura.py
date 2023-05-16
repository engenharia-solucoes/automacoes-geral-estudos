from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


#PATH = '/home/sentinel0/SentinelScript/battousai/mv/'


# lendo key
with open(f'key_cesar.bin', 'rb') as f:
    key = f.read()


# lendo user criptografada
with open(f'api_token_cesar.bin', 'rb') as f:
    iv = f.read(16)
    decrypt_data_api_token = f.read()


# decodificando senha
cipher = AES.new(key, AES.MODE_CBC, iv=iv)


decrypt_data_api_token_b = unpad(cipher.decrypt(decrypt_data_api_token), AES.block_size)


decrypt_data_api_token = decrypt_data_api_token_b.decode("utf-8")











