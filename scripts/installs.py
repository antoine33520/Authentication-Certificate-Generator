#!/usr/bin/env python3
import os, sys


os_type = sys.platform.lower()

if "win" in os_type:
    python = ""

elif "linux" in os_type:
    python = "sudo apt-get install python3.6"
    pip = "sudo apt-get insatll python3-pip"
    getmac = "sudo pip install getmac"
    pycrypto = "sudo pip install pycrypto"
    datetime = "sudo pip install datetime"
    hashlib = "sudo pip install hashlib"
    getpass = "sudo pip install getpass"

elif "darwin" in os_type:
    python = "brew install python"

else :
    print('Erreur: Je ne suis pas en mesure d\'identifier votre OS.')

install_python = os.popen(python).read().replace("\n","").replace("	","").replace(" ","")
install_pip = os.popen(pip).read().replace("\n","").replace("	","").replace(" ","")
install_getmac = os.popen(getmac).read().replace("\n","").replace("	","").replace(" ","")
install_pycrypto = os.popen(pycrypto).read().replace("\n","").replace("	","").replace(" ","")
install_datetime = os.popen(datetime).read().replace("\n","").replace("	","").replace(" ","")
install_hashlib = os.popen(hashlib).read().replace("\n","").replace("	","").replace(" ","")
install_getpass = os.popen(getpass).read().replace("\n","").replace("	","").replace(" ","")