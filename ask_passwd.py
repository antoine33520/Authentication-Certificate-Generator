import getpass, sys

def get_passwd():
    passwd = getpass.getpass(prompt = 'Veuillez entrer un mot de passe svp (q pour quitter):\n')
    if passwd == 'q':
        sys.exit()
    passwd_bis = getpass.getpass(prompt = 'Veuillez confimer le mot de passe svp (q pour quitter): ')
    if passwd_bis == 'q':
        sys.exit()
    while passwd != passwd_bis :
        print('Veuillez réessayer.')
        passwd = getpass.getpass(prompt = 'Veuillez entrer un mot de passe svp (q pour quitter): ')
        if passwd == 'q':
            sys.exit()
        passwd_bis = getpass.getpass(prompt = 'Veuillez confimer le mot de passe svp (q pour quitter): ')
        if passwd_bis == 'q':
            sys.exit()
    else:
        print('Mot de passe enregistré !')
    return passwd
        
        

get_passwd()