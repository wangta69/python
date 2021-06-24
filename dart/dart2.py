from konfig import Config
import requests
from io import BytesIO
import zipfile
import xmltodict
import json

cc = Config("./conf.ini")
crtfc_key = cc.get_map("app")['OPENDARTAPI']

## 종목명 및 종목 코드 가져오기 (corp_name, stock_code)
api = 'https://opendart.fss.or.kr/api/corpCode.xml'
res = requests.get(api, params={'crtfc_key': crtfc_key})
z = zipfile.ZipFile(BytesIO(res.content))
print(z.namelist()) # ['CORPCODE.xml']
data_xml = z.read('CORPCODE.xml').decode('utf-8')
data_odict = xmltodict.parse(data_xml)
data_dict = json.loads(json.dumps(data_odict))
data = data_dict.get('result', {}).get('list')

for item in data:
    if item['corp_name'] in ["삼성전자", "SK하이닉스", "NAVER"]:
        print(item) # {'corp_code': '00164779', 'corp_name': 'SK하이닉스', 'stock_code': '000660', 'modify_date': '20210511'}

## 기업개황 (이때는 corp_code 사용)
res = requests.get('https://opendart.fss.or.kr/api/company.json?crtfc_key=' + crtfc_key + '&corp_code=00126380')
item = json.loads(res.text)
print(item)
