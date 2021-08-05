# Rule-Based(규칙 기반) 챗봇 만들기
# 참조 : https://needjarvis.tistory.com/639


import pandas as pd
chatbot_data = pd.read_excel("./chatbot_data.xlsx")
# rule의 데이터를 split하여 list형태로 변환 후, index값과 함께 dictionary 형태로 저장

chat_dic = {}
row = 0
for rule in chatbot_data['rule']:
    chat_dic[row] = rule.split('|')
    row += 1

def chat(request):
    for k, v in chat_dic.items():
        index = -1
        for word in v:
            try:
                if index == -1:
                    index = request.index(word)
                else: # 이전 index 값은 현재 index값보다 이전이어야 한다.
                    if index < request.index(word, index):
                        index = request.index(word, index)
                    else: # index 값이 이상할 경우 과감하게 break를 한다
                        index = -1
                        break
            except ValueError:
                index = -1
                break

        if index > -1:
            return chatbot_data['response'][k]
    return '무슨 말인지 모르겠어요'

while True:
    req = input('대화를 입력해보세요.')
    if req == 'exit':
        break
    else:
        print('jarvis : ', chat(req))
