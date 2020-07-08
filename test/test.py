from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import rsa

hash = "SHA-256"

def newkeys(keysize):
    random_generator = Random.new().read
    key = RSA.generate(keysize, random_generator)
    private, public = key, key.publickey()
    return public, private

def importKey(externKey):
    return RSA.importKey(externKey)



def encrypt(message, pub_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(message)

def decrypt(ciphertext, priv_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)

def main():
    msg1 = b"test"

    keysize = 2048

    (public, private) = rsa.newkeys(keysize)

    # https://docs.python.org/3/library/base64.html
    # encodes the bytes-like object s
    # returns bytes
    encrypted = b64encode(rsa.encrypt(msg1, private))
    # decodes the Base64 encoded bytes-like object or ASCII string s
    # returns the decoded bytes
    decrypted = rsa.decrypt(b64decode(encrypted), private)


    #print(private.exportKey('PEM'))
    #print(public.exportKey('PEM'))
    print("Encrypted: " + encrypted.decode('ascii'))
    print("Decrypted: '%s'" % (decrypted))

if __name__== "__main__":
    main()



































"""
def gen_binary(text):
    tab = []
    count = 0
    for char in text:
        binary = '0' + bin(ord(char))[2:]
        while count <= len(text):
            tab.append(binary)
            count += 1
        return tab

print(gen_binary(gen_certificate()))
"""