import sys
from kiwoom.kiwoom import *
from PyQt5.QtWidgets import *
import logging
from logging.handlers import TimedRotatingFileHandler

class Main():
    def __init__(self):
        print("메인 클래스입니다.")

        self.app = QApplication(sys.argv) # QApplication 객체 생성.
        self.kiwoom = Kiwoom()
        self.app.exec_() # 이벤트 루프 실행.

if __name__ == "__main__":
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

    Main()