from Crypto.Publickey import RSA

# Générer une clé privée RSA
key = RSA.generate(1024) # taille de la clé en bits

# Générer une CSR (demande de signature)
# Supprimer la phrase secrète de la clé
# Générer un certificat auto-signé

## Structure d'un certificat :
#### version de X.509 à laquelle le certificat correspond
#### numéro de série du certificat
#### algorythme de chiffrement utilisé pour signer le certificat
#### nom de l'autorité de certification émettrice
#### dates de début et de fin de validité
#### objet de l'utilisation de la clé publique
#### clé publique du propriétaire du certificat
#### signature de l'émetteur du certificat