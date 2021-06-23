from collections import deque
from threading import Lock
from PyQt5.QtCore import QObject
import logging
from logging.handlers import TimedRotatingFileHandler

class RequestThreadWorker(QObject):
    def __init__(self):
        """요청 쓰레드
        """
        super().__init__()
        self.request_queue = deque()  # 요청 큐
        self.request_thread_lock = Lock()

        # 간혹 요청에 대한 결과가 콜백으로 오지 않음
        # 마지막 요청을 저장해 뒀다가 일정 시간이 지나도 결과가 안오면 재요청
        self.retry_timer = None

        # --------------------------------------------------
        # 로거 (Logger) 준비하기
        # --------------------------------------------------
        # 로그 파일 핸들러
        fh_log = TimedRotatingFileHandler('logs/log', when='midnight', encoding='utf-8', backupCount=120)
        fh_log.setLevel(logging.DEBUG)

        # 콘솔 핸들러
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)

        # 로깅 포멧 설정
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
        fh_log.setFormatter(formatter)
        sh.setFormatter(formatter)

        # 로거 생성 및 핸들러 등록
        logger = logging.getLogger(__file__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(fh_log)
        logger.addHandler(sh)



    def retry(self, request):
        logger.debug("키움 함수 재시도: %s %s %s" % (request[0].__name__, request[1], request[2]))
        self.request_queue.appendleft(request)

    def run(self):
        while True:
            # 큐에 요청이 있으면 하나 뺌
            # 없으면 블락상태로 있음
            try:
                request = self.request_queue.popleft()
            except IndexError as e:
                time.sleep(요청주기)
                continue

            # 요청 실행
            logger.debug("키움 함수 실행: %s %s %s" % (request[0].__name__, request[1], request[2]))
            request[0](trader, *request[1], **request[2])

            # 요청에대한 결과 대기
            if not self.request_thread_lock.acquire(blocking=True, timeout=5):
                # 요청 실패
                time.sleep(요청주기)
                self.retry(request)  # 실패한 요청 재시도

            time.sleep(요청주기)  # 0.2초 이상 대기 후 마무리
