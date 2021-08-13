# 참조 : https://jfun.tistory.com/199
# 참조 : https://velog.io/@kjyggg/%ED%98%95%ED%83%9C%EC%86%8C-%EB%B6%84%EC%84%9D%EA%B8%B0-Mecab-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0-A-to-Z%EC%84%A4%EC%B9%98%EB%B6%80%ED%84%B0-%EB%8B%A8%EC%96%B4-%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84-%EB%93%B1%EB%A1%9D%EA%B9%8C%EC%A7%80
# 챗봇 만들기
input_data = '판교에 지금 주문해줘'
output_data = ' '
request = {
    "intent_id": " ",
    "input_data": input_data,
    "request_type": "text",
    "story_slot_entity": {},
    "output_Data": output_data
}

# 기본 데이터 셋(DB)

intent_list = {
    "주문": ["주문", "배달"],
    "예약": ["예약", "잡아줘"],
    "정보": ["정보", "알려"]
}

story_slot_entity = {
    "주문": {"메뉴": None, "장소": None, "날짜": None},
    "예약": {"장소": None, "날짜": None},
    "정보": {"대상": None}
}

# 형태소 분석
# from konlpy tag import Mecab
# mecab = Mecab("경로/mecab-ko-dic")
# preprocessed = mecab.pos(request.get('input_data))
# print(preprocessed)
