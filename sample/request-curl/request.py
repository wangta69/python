import requests

url = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR'
header = {'Accept-Encoding': 'gzip', 'Content-Type':'application/json'}
data = '{"text":"Hello, World!"}'
# response=requests.post(url, headers=header, data=data)
r = requests.get(url, headers=header, data=data)
print('===========')
print(r)
print(r.json())
# print( response.text)

print('+++++++++++')
"""
#MK:만약 Proxy 서버나 Certification 등을 사용하는 경우 proxy 주소과 certification 위치를 지정해야 한다.
proxy = {"https": proxy url"}
verify = "D:\\my.crt"
r = requests.post(url, headers=header, data=data, proxies=proxy, verify=verify)
"""
