import requests
from consts import *
from lib import *
from os import system
#NE PAS ECRIRE QUAND LA VALEUR RESTE LA MEME
try:
    system("title " + "TortugaHelper by Aqua")
except:
    pass
try:
    token = login(mail, pwd)
except:
    token = majInfos()

#DEPOT
burp0_url = "https://api.tortugacasino.com:443/common/v8/api/graphql?op=paymentTransactions"
burp0_headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/json, text/plain, */*",  "Accept-Encoding": "gzip, deflate", "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"}
burp0_json={"operationName": "paymentTransactions", "query": "query paymentTransactions($input: TransactionInput) {\n  pagedPaymentTransactions(input: $input) {\n    totalItems\n    totalPages\n    data {\n      id\n      dateTime\n      method\n      status\n      type\n      paymentMethodRef\n      amount {\n        amount\n        currency\n        __typename\n      }\n      requestedAmount {\n        amount\n        currency\n        __typename\n      }\n      receivedAmount {\n        amount\n        currency\n        __typename\n      }\n      accountDetail {\n        email\n        cardExpiry\n        cardSuffix\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n", "variables": {"input": {"paging": {"page": 0, "pageSize": 99}, "type": "deposit"}}}
pagedepot = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)

#CALCUL DEPOT
depot = float(0)
for i in pagedepot.json()['data']['pagedPaymentTransactions']['data']:
    if i['status'] == 'completed': 
        depot += i['amount']['amount']

#RETRAITS
burp0_url = "https://api.tortugacasino.com:443/common/v8/api/graphql?op=paymentTransactions"
burp0_headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate", "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"}
burp0_json={"operationName": "paymentTransactions", "query": "query paymentTransactions($input: TransactionInput) {\n  pagedPaymentTransactions(input: $input) {\n    totalItems\n    totalPages\n    data {\n      id\n      dateTime\n      method\n      status\n      type\n      paymentMethodRef\n      amount {\n        amount\n        currency\n        __typename\n      }\n      requestedAmount {\n        amount\n        currency\n        __typename\n      }\n      receivedAmount {\n        amount\n        currency\n        __typename\n      }\n      accountDetail {\n        email\n        cardExpiry\n        cardSuffix\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n", "variables": {"input": {"paging": {"page": 0, "pageSize": 99}, "type": "withdraw"}}}
pageretrait = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)

#CALCUL RETRAIT
retrait = float(0)
for i in pageretrait.json()['data']['pagedPaymentTransactions']['data']:
    if i['status'] == 'pending' or i['status'] == 'completed':
        retrait += i['amount']['amount']

#SOUS DE BASE
burp0_url = "https://api.tortugacasino.com:443/common/v8/api/graphql?op=userBalances"
burp0_headers = {"Authorization": f"Bearer {token}", "Accept-Encoding": "gzip, deflate", "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"}
burp0_json={"operationName": "userBalances", "query": "query userBalances {\n  user {\n    balances {\n      bonus {\n        amount\n        currency\n        __typename\n      }\n      total {\n        amount\n        currency\n        __typename\n      }\n      real {\n        amount\n        currency\n        __typename\n      }\n      locked {\n        amount\n        currency\n        __typename\n      }\n      withdrawable {\n        amount\n        currency\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
sous = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)

#CALCUL SOUS
argent = sous.json()['data']['user']['balances']['real']['amount']
bonus = sous.json()['data']['user']['balances']['bonus']['amount']
final = round(argent - depot + retrait, 2)
bonus = round(bonus, 2)

#DERNIERE VALEUR
consts = open('./consts.py', 'r')
if not lastvalue == final:    
    vals = []
    for i in consts:
        if i == 'lastvalue = ' + str(lastvalue):
            i = i.replace('lastvalue = '+ str(lastvalue),'lastvalue = '+ str(final))
        vals.append(i)
    print(vals)
    open('./consts.py', 'w').writelines(vals)
else:
    pareil = True

#CALCUL FINAL
plus = round(final-lastvalue,2)
moins = round(lastvalue-final,2)

if final > 0 and lastvalue<final:
    print(f'T\'es en bénéfice de {final}€ avec un bonus de {bonus}€ !\nC\'est {plus}€ de plus que la dernière fois, bien joué !')
elif final > 0 and lastvalue>final:
    print(f'T\'es en bénéfice de {final}€ avec un bonus de {bonus}€ !\nC\'est {moins}€ de moins que la dernière fois, t\'as merdé mais demain tu te refais oklm !')
elif final < 0 and lastvalue<final:
    print(f'Bon mon salaud, t\'as bien perdu tes sous là, {final}€ ça fait pas grand chose pour se nourrir...\nAu moins c\'est plus que la dernière fois, tu te rattrapes de {plus}€.')
elif final < 0 and lastvalue>final:
    print(f'Bon mon salaud, t\'as bien perdu tes sous là, {final}€ ça fait pas grand chose pour se nourrir...\nD\'ailleurs c\'est encore moins que la dernière fois, t\'as perdu {moins}€, vas postuler à Pôle Emploi dès maintenant...')
elif pareil:
    print(f'T\'as pas joué depuis la dernière fois, donc t\'es toujours à {final}€.')

input('\n\nAppuyer sur une touche pour fermer...')