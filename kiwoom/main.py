import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication

class SyncRequestDecorator:
    '''키움 API 동기화 데코레이터
    '''
    @staticmethod
    def kiwoom_sync_request(func):
        def func_wrapper(self, *args, **kwargs):
            self.request_thread_worker.request_queue.append((func, args, kwargs))
        return func_wrapper

    @staticmethod
    def kiwoom_sync_callback(func):
        def func_wrapper(self, *args, **kwargs):
            logger.debug("키움 함수 콜백: %s %s %s" % (func.__name__, args, kwargs))
            func(self, *args, **kwargs)  # 콜백 함수 호출
            if self.request_thread_worker.request_thread_lock.locked():
                self.request_thread_worker.request_thread_lock.release()  # 요청 쓰레드 잠금 해제
        return func_wrapper

class SysTrader(QObject):
    def __init__():
        """자동투자시스템 메인 클래스
        """
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.OnEventConnect.connect(self.kiwoom_OnEventConnect)  # 로그인 결과를 받을 콜백함수 연결

    # -------------------------------------
    # 로그인 관련함수
    # -------------------------------------
    @SyncRequestDecorator.kiwoom_sync_request
    def kiwoom_CommConnect(self):
        """로그인 요청
        키움증권 로그인창 띄워주고, 자동로그인 설정시 바로 로그인 진행됨.
        OnEventConnect()으로 콜백 전달됨.
        :param kwargs:
        :return: 1: 로그인 요청 성공, 0: 로그인 요청 실패
        """
        lRet = self.kiwoom.dynamicCall("CommConnect()")
        return lRet

    @SyncRequestDecorator.kiwoom_sync_callback
    def kiwoom_OnEventConnect(self, nErrCode):
        """로그인 결과 수신
        :param nErrCode: 0: 로그인 성공, 100: 사용자 정보교환 실패, 101: 서버접속 실패, 102: 버전처리 실패
        :param kwargs:
        :return:
        """
        if nErrCode == 0:
            logger.debug("로그인 성공")
        elif nErrCode == 100:
            logger.debug("사용자 정보교환 실패")
        elif nErrCode == 101:
            logger.debug("서버접속 실패")
        elif nErrCode == 102:
            logger.debug("버전처리 실패")


if __name__ == "__main__":
    # (중략)
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

    # --------------------------------------------------
    # 자동투자시스템 시작
    # --------------------------------------------------
    app = QApplication(sys.argv)  # Qt 애플리케이션 생성
    trader = SysTrader()  # QObject를 상속하는 자동투자시스템 객체 생성
    trader.kiwoom_CommConnect()  # 로그인
    sys.exit(app.exec_())