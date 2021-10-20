import base64
import os

from Cryptodome.Hash import SHA256
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.PublicKey import RSA

dir_list = ["sub_dir"]
data_dir = os.path.abspath("./card_segmentation/datasets")
sign_dir = os.path.abspath("./card_segmentation/signature")

verify_flag = True

for dir in dir_list:
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

        sig = open(os.path.join(sign_dir, dir, f'{".".join(f.split(".")[:-1])}.txt'), "r")
        sig_txt = sig.readline()
        sig = bytes.fromhex(sig_txt)  # # convert string to bytes object

        # Load public key (not private key) and verify signature
        public_key = RSA.importKey(open("public_key.txt").read())
        verifier = PKCS1_v1_5.new(public_key)
        verified = verifier.verify(digest, sig)

        if not verified:
            verify_flag = False
            break
        else:
            print(f'{f} is valid!')

    if not verify_flag:
        break

if verify_flag:
    print("Signature is valid!")
else:
    print("FAILED! Data is edited by human!")

print("Done!")
