from getpass import getpass
from consts import *
import requests

def getToken():
    token = ''
    while not token:
        conf = ""
        while True:
            newmail = str(input('Quel est votre adresse email Tortuga ?\n'))
            if '@' in newmail:
                while True:
                    conf = str(input(f'Votre email est-elle bien "{newmail}" ? (oui/non)\n'))[0]    
                    if conf == 'o' or conf == 'n':
                        break
            if conf == 'o':
                        break    
            else:
                print('Ceci n\'est pas une adresse email valide.')
        newpwd = ''
        conf = 'a'
        while not newpwd == conf:
            if conf != 'a':
                print('Les deux mots de passe n\'étaient pas les mêmes')
            newpwd = getpass('Quel est votre mot de passe Tortuga ? ')
            conf = getpass('Retapez votre mot de passe : ')
        consts = open('./consts.py', 'r+')
        vals = []
        for i in consts:
            if 'mail = "' in i:
                i = 'mail = ' + f'"{newmail}"\n'
            if 'pwd = "' in i:
                i = 'pwd = ' + f'"{newpwd}"\n'
            vals.append(i)
        file = open('./consts.py', 'w')
        file.writelines(vals)
# TOKEN

        try:
            burp0_url = "https://api.tortugacasino.com:443/auth/v3/api/auth/login"
            burp0_headers = {"Content-Type": "application/json", "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate", "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"}
            burp0_json={"password": pwd, "username": mail}
            login = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
            token = login.json()['token']
            print(token)
            return(token)
        except:
            print('invalide')

getToken()