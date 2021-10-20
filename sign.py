#from base64 import (b64encode, b64decode)
import base64
import os

from Cryptodome.Hash import SHA256
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.PublicKey import RSA

dir_list = ["sub_dir"]
data_dir = os.path.abspath("./card_segmentation/datasets")
sign_dir = os.path.abspath("./card_segmentation/signature")

for dir in dir_list:
    if not os.path.exists(sign_dir):
        os.mkdir("./card_segmentation/signature")
    if not os.path.exists(os.path.join(sign_dir, dir)):
        os.mkdir(os.path.join(sign_dir, dir))

    file_list = os.listdir(os.path.join(data_dir, dir))

    for f in file_list:
        # Open image
        image = open(os.path.join(data_dir, dir, f), 'rb')
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)  # encodestring also works aswell as decodestring
        image.close()

        # Encoding
        digest = SHA256.new()
        digest.update(image_64_encode)

        # Load private key previouly generated
        with open("private_key", "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        # Sign the message
        signer = PKCS1_v1_5.new(private_key)
        sig = signer.sign(digest)

        txt_name = f'{".".join(f.split(".")[:-1])}.txt'
        with open(os.path.join(os.path.join(sign_dir, dir, txt_name)), "w") as sign_f:
            sign_f.write(sig.hex())
        sign_f.close()

        # sig is bytes object, so convert to hex string.
        # (could convert using b64encode or any number of ways)
        print("Signature:")
        print(sig.hex())

print("Done!")