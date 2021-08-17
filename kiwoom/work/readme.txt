1. - 기본 회사정보를 입력 / update  (kind.krx.co.kr 에서 회사 데이타 구함)
    krx/ex1.py corporation.update() 실행


2. roa, roic 등을 구하고 per, pcr, psr, pbr 등을 구해 재무적으로 단단한 업체들을 고른다. (comp.fnguide.com 에서 제공하는 데이타 가져옮)
    quant > db-type > ex1.py
      # 포괄 손익계산서, 재무상태료, 현금흐름표를 구함
    - quant.createFinancialStatements()
      # 유동비율, 부채비율, 영업이익율 roa, roic 등을 구함
    - quant.createFinancialRatio()
       # 투자지표를 구한다. (per, pcr, psr, pbr, 총현금흐름)
    - quant.createInvestmentIndiators()

    종합점수를 계산한다.
    # pbr, per, pcr, psr에 대한 순위를 매긴다.
    rank.setOrder(202106)

    # 종합점수를 계산한다. (score_total 가 3인 것만을 기준으로 구매를 한다, 이때 위에서 계산한 종합점수를 참조한다)
    rank.makescore()
    score_net_income = IF(net_income > 0, 1, 0), ' \
    score_cashflow_operating = IF(cashflow_operating  > 0, 1, 0), ' \
    score_diff = IF(cashflow_operating >  net_income, 1, 0), ' \
    score_total = score_net_income +  score_cashflow_operating + score_diff ' \


3. investing 에서 재무재표 관련 정보를 가져온다.
    investing에서는 예산 재무재표를 제공함으로 이것을 참조로 하여 시장보다 빠르게 대응하기위해 참조한다.
    investing > ex1.py

    1. 필요한 회사이름을 현재 db와 매치 시킨다.
        investing.updateInvestingCompName()
    2. earnings 을 스크롤 한다.
        investing.earnings()

3. naver에서 현재 주가를 가져온다. (per을 이용하여 현재 주가 및 적정 주가를 확인하기 위함)
    naver > ex1.py



