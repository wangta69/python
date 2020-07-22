import requests

url="http://chanceball.com"
header={"Accept-Encoding": "gzip", "Content-Type":"application/json"}
data='{"message":"hello"}'
response=requests.post(url, headers=header, data=data)

print('===========')
print(response)
print('+++++++++++')
"""
#MK:만약 Proxy 서버나 Certification 등을 사용하는 경우 proxy 주소과 certification 위치를 지정해야 한다.
proxy = {"https": "https://mkblog.co.kr:port"}
verify="D:\\mkblog\\mkblog.crt"
response=requests.post(url, headers=header, data=data, proxies=proxy, verify=verify)
"""
