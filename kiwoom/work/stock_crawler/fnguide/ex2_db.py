# from stock_crawler.connMysql import Mysql
#
#
# class Ranking():
#     def __init__(self, parent=None):
#         super().__init__()
#         self.mysql = Mysql()
#
#
#     def setOrder(self, date):
#         '''
#         저평가된 항목을 찾기 위해 분기별 정렬을 처리한다.
#         :return:
#         '''
#         self.mysql.updateOrder(date, 'order_pbr', 'pbr')
#         self.mysql.updateOrder(date, 'order_per', 'per')
#         self.mysql.updateOrder(date, 'order_pcr', 'pcr')
#         self.mysql.updateOrder(date, 'order_psr', 'psr')
#
#     def makescore(self):
#         '''
#         각각의 score를 매기고 종합점수를 매긴다.
#         :return:
#         '''
#         self.mysql.updateScore('202106')
#         pass
#
#
# rank = Ranking()
# rank.setOrder(202106)
# rank.makescore()
#
# # option
# pd.set_option('chained', None)
#
#
# # 저평가 데이터프레임과 F-score 데이터프레임 만들기 (CH4. 전략 구현하기.ipynb)
# date = '2020/12'
# value = MagicUtil.make_value_combo(['PER', 'PBR', 'PSR', 'PCR'], invest_df, date, None)
# quality = MagicUtil.get_fscore(fs_df, date, None)
#
# # print('value', value)
# # print('quality', quality)
#
# # # index 주식 코드 기준 병합
# value_quality = pd.merge(value, quality, how='outer', left_index=True, right_index=True)
# # print(value_quality)
# # print(len(value_quality)) # 2263
# # # #
# value_quality.to_excel('순위All.xlsx')
# value_quality_filtered = value_quality[value_quality['종합점수'] == 3]
# # print(value_quality_filtered)
# # print(len(value_quality_filtered)) # 428
#
# vq_df = value_quality_filtered.sort_values(by='종합순위')
# # print(vq_df)
# # vq_df.to_excel('순위.xlsx')
# # print(len(vq_df)) #
#



