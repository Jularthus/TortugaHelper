from getpass import getpass
from consts import *
def infos():
    if mail == "" or not "@" in mail:
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
infos()