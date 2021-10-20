"""Extract the public key from the private key and write to a file.
"""
from Cryptodome.PublicKey import RSA


with open("private_key", "r") as src:
    private_key = RSA.importKey(src.read())

public_key = private_key.publickey()

with open('public_key.txt', 'w') as out:
    out.write(public_key.exportKey().decode('utf-8'))
