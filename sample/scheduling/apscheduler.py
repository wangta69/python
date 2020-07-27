from apscheduler.schedulers.blocking import BlockingScheduler
# 실행할 함수
def exec_interval():
    print('exec interval')
def exec_cron():
    print('exec cron')
sched = BlockingScheduler()
# 예약방식 interval로 설정, 10초마다 한번 실행
sched.add_job(exec_interval, 'interval', seconds=10)
# 예약방식 cron으로 설정, 각 5배수 분의 10, 30초마다 실행
# ex) (5분 10, 30초), (10분 10, 30초), (15분 10, 30초)
sched.add_job(exec_cron, 'cron', minute='*/5', second='10, 30')
# 스케줄링 시작
sched.start()
