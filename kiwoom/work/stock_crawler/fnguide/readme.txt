# consensus 값을 가져온다.
https://comp.fnguide.com/SVO2/json/data/01_06/03_' + firm_code + '.json'
https://comp.fnguide.com/SVO2/json/data/01_06/03_A005930.json

# 투자지표를 가져온다. (이부분은 회사정보에 넣는 것이 옳을 듯함 12월 기준)
https://comp.fnguide.com/SVO2/asp/SVD_Invest.asp?pGB=1&cID=&MenuYn=Y&ReportGB=D&NewMenuID=105&stkGb=701&gicode=A005930
['PER', 'PCR', 'PSR', 'PBR', '총현금흐름']

# 종가, 최고가, 수익률, 시가총액, 발생주식수(보통주 / 우선주)ㄷ탸
# 투자의견, 목표주가, EPS, PER, 추정기관수
# 이부분은 걍 연결제무재표에 넣는 것이 옳을 듯함(가장 최근 데이타를 활용한 정보)ㄷ턋;ㅁㄴㅇ
# 매출액, 영업이익, 당기순이익, 지배주주순이익, 자본총계, 자본금, 부채비율, 유보율, ROA, ROE, EPS, BPS, DPS, PER, PBR, 발행주식수

http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A005930

#
['유동비율', '부채비율', '영업이익률', 'ROA', 'ROIC']
https://comp.fnguide.com/SVO2/asp/SVD_FinanceRatio.asp?pGB=1&cID=&MenuYn=Y&ReportGB=D&NewMenuID=104&stkGb=701&gicode=' + sCode

#
https://comp.fnguide.com/SVO2/asp/SVD_Finance.asp?pGB=1&cID=&MenuYn=Y&ReportGB=D&NewMenuID=103&stkGb=701&gicode=' + sCode
['매출액', '매출총이익', '영업이익', '당기순이익']
