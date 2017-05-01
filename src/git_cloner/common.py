from base64 import b64encode
from http.client import HTTPSConnection


def connect_with_auth(site, port=443, path='/', login='', password=''):
    c = HTTPSConnection(site, port)

    # Need to base 64 encode it
    # and then decode it to acsii as python 3 stores it as a byte string.
    user_and_pass = b64encode('{}:{}'.format(login, password).encode('utf-8')).decode('ascii')
    headers = {
        'User-Agent': 'Repo downloader'
    }

    if login:
        headers['Authorization'] = 'Basic {}'.format(user_and_pass)

    # Connect.
    c.request('GET', path, headers=headers)
    res = c.getresponse()
    data = res.read()

    return data
