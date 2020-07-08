from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from base64 import b64encode, b64decode
import rsa

def newkeys():
    key = RSA.generate(2048)
    private, public = key, key.publickey()
    return public, private

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

    private = rsa.newkeys(2048)

    encrypted = b64encode(rsa.encrypt(msg1, private))
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

ou

''.join(format(ord(i), 'b') for i in data)
"""