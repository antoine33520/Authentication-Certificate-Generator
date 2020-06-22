#!/usr/bin/env python3
import oudjirasign as osy

# Générer une paire de clés
def generate_key():
    global privkey, pubkey
    privkey, pubkey = osy.generatersakeys() # 2048 bits par defaut

message = 'hello world'

def chiffrement():
    global privkey, pubkey, chiffre
    privkey = osy.importPrivateKey(privkey)
    pubkey = osy.importPublicKey(pubkey)
    chiffre = osy.chiffre(message, pubkey)

def dechiffrement():
    global privkey, pubkey, dechiffre
    privkey = osy.importPrivateKey(privkey)
    pubkey = osy.importPublicKey(pubkey)
    dechiffre = osy.dechiffre(message, privkey)

def signature():
    global privkey, signature
    signature = osy.signer(message, privkey)

def verif():
    global verif, signature, pubkey
    verif = osy.verifier(message, pubkey, signature)