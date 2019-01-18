import requests

session = requests.session()
session.proxies = {}

session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'


r = session.get('https://www.facebookcorewwwi.onion/')
print(r.text)