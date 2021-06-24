import dart_fss as dart
from konfig import Config
cc = Config("./conf.ini")
print(cc.get_map("app")['OPENDARTAPI'])

# Open DART API KEY 설정
api_key = cc.get_map("app")['OPENDARTAPI']
dart.set_api_key(api_key=api_key)

# DART 에 공시된 회사 리스트 불러오기
corp_list = dart.get_corp_list()

print('==================')
print(corp_list) # Number of companies: 87113
print('==================')

# # 삼성전자 검색
# samsung = corp_list.find_by_corp_name('삼성전자', exactly=True)[0]
#
# # 2012년부터 연간 연결재무제표 불러오기
# fs = samsung.extract_fs(bgn_de='20120101')
#
# # 재무제표 검색 결과를 엑셀파일로 저장 ( 기본저장위치: 실행폴더/fsdata )
# fs.save()

