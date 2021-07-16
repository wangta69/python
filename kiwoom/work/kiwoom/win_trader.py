import os
from PyQt5.QtCore import QEventLoop, QTimer, QTime
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic
from dotenv import load_dotenv
from kiwoom.worker import Worker
from utils.telegram import Telegram

form_class = uic.loadUiType("ui/kiwoom/trader.ui")[0]

class TraderWindow(QWidget, form_class):
    def __init__(self, kiwoom=None):
        super().__init__()
        self.setupUi(self)

        self.kiwoom = kiwoom
        self.isLogin = kiwoom.is_login()

        self.timer = QTimer(self)
        self.timer.start(500)
        self.timer.timeout.connect(self.timeout)

        # 테레그램 세팅
        load_dotenv()
        self.sns_message = ""
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_BOT_CHAT_ID')
        self.telegram = Telegram()

        # 조건검색식 관련 (GetConditionLoad())
        self.worker = Worker()
        self.worker.signal_receive_condition_ver.connect(self.signal_ver)
        self.worker.signal_receive_tr_condition.connect(self.signal_tr)  # 1회성
        self.worker.signal_receive_real_condition.connect(self.signal_real)  # 실시간

        # # 조건검색식 관련
        self.kiwoom.OnReceiveConditionVer.connect(self.worker.on_receive_condition_ver)
        self.kiwoom.OnReceiveTrCondition.connect(self.worker.on_receive_tr_condition)
        self.kiwoom.OnReceiveRealCondition.connect(self.worker.receive_real_condition)

        # ui 관련 처리
        self.checkBox_cond.setChecked(True)
        self.pushButton_cond.clicked.connect(self.start_cond)
        self.lineEdit.textChanged.connect(self.code_changed)
        self.pushButton.clicked.connect(self.send_order)

        self.init()

    def init(self):
        if self.isLogin != 1:
            QMessageBox.about(self, 'Alert', "먼저 로그인 해 주세요")
            pass
        else:
            accouns_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
            accounts = self.kiwoom.get_login_info("ACCNO")

            accounts_list = accounts.split(';')[0:accouns_num]
            self.comboBox.addItems(accounts_list)

            # 조건검색식 호출
            self.condition_load()

    def code_changed(self):
        code = self.lineEdit.text()
        name = self.kiwoom.get_master_code_name(code)
        self.lineEdit_2.setText(name)

    def send_order(self):
        pass
        order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
        hoga_lookup = {'지정가': "00", '시장가': "03"}

        account = self.comboBox.currentText()
        order_type = self.comboBox_2.currentText()
        code = self.lineEdit.text()
        hoga = self.comboBox_3.currentText()
        num = self.spinBox.value()
        price = self.spinBox_2.value()

        print("send_order_req", "0101", account, order_type_lookup[order_type], code, num, price,
                                hoga_lookup[hoga], "")

        # self.kiwoom.send_order("send_order_req", "0101", account, order_type_lookup[order_type], code, num, price,
        #                        hoga_lookup[hoga], "")

    def timeout(self):
        current_time = QTime.currentTime()
        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        # state = self.kiwoom.is_login()
        # if state == 1:
        #     state_msg = "서버 연결 중"
        # else:
        #     state_msg = "서버 미 연결 중"

        # self.statusbar.showMessage(state_msg + " | " + time_msg)

        # if self.sns_message:
        #     # 텔레그램
        #     if self.checkBox_cond.isChecked():
        #         self.telegram.send_message(self.sns_message)
        #     self.textEdit_cond.append(self.sns_message)
        #     self.sns_message = ""

    def signal_ver(self, receive, msg):
        """
        getConditionLoad() 메서드의 조건식 목록 요청에 대한 응답 이벤트

        :param receive: int - 응답결과(1: 성공, 나머지 실패)
        :param msg: string - 메세지
        """
        print('signal_ver', receive, msg)
        cond_list = []
        try:
            if not receive:
                print('not receive')
                return

            dic = self.kiwoom.getConditionNameList()
            print('dic', dic)

            for key in dic.keys():
                print('key', key)
                cond_list.append("{};{}".format(key, dic[key]))
            print('cond_list', cond_list)
            # 콤보박스에 조건식 목록 추가
            self.comboBox_cond.addItems(cond_list)

        except Exception as e:
            print(e)

        finally:
            print('signal_ver finally')
            # pass
            # self.condition_serarch_event_loop.exit()


    def signal_tr(self, screen_no, codes, condition_name, condition_index, inquiry):
        """
        (1회성, 실시간) 종목 조건검색 요청시 발생되는 이벤트
        :param screen_no:
        :type screen_no: str
        :param codes: - 종목코드 목록(각 종목은 세미콜론으로 구분됨)
        :param condition_name: 조건식 이름
        :type condition_name: str
        :param condition_index: 조건식 인덱스
        :type condition_index: int
        :param inquiry: 조회구분(0: 남은데이터 없음, 2: 남은데이터 있음)
        :type inquiry: int
        :return:
        """
        print('screen_no: ', screen_no, 'codes: ', codes, 'condition_name: ', condition_name, 'condition_index: ', condition_index, 'inquiry: ', inquiry)
        try:
            if codes == "":
                return

            codeList = codes.split(';')
            del codeList[-1]

            print(codeList)
            print("종목개수: ", len(codeList))

            # 로그용
            msg = ""
            for code in codeList:
                msg += "{} {}\n".format(code, self.kiwoom.get_master_code_name(code))

            self.sns_message += msg
        finally:
            pass

    #
    #
    def signal_real(self, code, event, condition_name, condition_index):
        """
        실시간 종목 조건검색 요청시 발생되는 이벤트
        :param code: string - 종목코드
        :param event: string - 이벤트종류("I": 종목편입, "D": 종목이탈)
        :param condition_name: string - 조건식 이름
        :param condition_index: string - 조건식 인덱스(여기서만 인덱스가 string 타입으로 전달됨)
        :return:
        """
        print('signal_real')
        print('receive_real_condition', code, event, condition_name, condition_index)
        print("종목코드: {}, 종목명: {}".format(code, self.kiwoom.get_master_code_name(code)))
        print("이벤트: ", "종목편입" if event == "I" else "종목이탈")
        msg = "{} {} {}\n".format("종목편입" if event == "I" else "종목이탈", code, self.kiwoom.get_master_code_name(code))
        self.sns_message += msg

    ## 조건검색식 관련 추가
    def condition_load(self):
        """
        조건식 목록 요청 메서드: 사용자가 만든 컨디션 목록을 가져온다.
        현재 창에 접근시 자동실행
        :return:
        """
        # 조건식 실행 (signal_ver())로 결과 전달
        self.kiwoom.dynamicCall("GetConditionLoad()")

    def start_cond(self):
        condition_name = self.comboBox_cond.currentText().split(';')[1]
        condition_index = self.comboBox_cond.currentText().split(';')[0]

        if self.pushButton_cond.text() == "적용":

            try:
                self.kiwoom.send_condition("0", condition_name, int(condition_index), 1)
                self.pushButton_cond.setText("해제")
                self.comboBox_cond.setEnabled(False)
                self.checkBox_cond.setEnabled(False)
                print("{} activated".format(condition_name))
                msg = "{} 실행\n".format(condition_name)
                self.sns_message += msg
            except Exception as e:
                print(e)

        else:
            self.sendConditionStop("0", condition_name, condition_index)
            self.pushButton_cond.setText("적용")
            self.comboBox_cond.setEnabled(True)
            self.checkBox_cond.setEnabled(True)

    def sendConditionStop(self, screen_no, condition_name, condition_index):
        self.kiwoom.send_condition_stop(screen_no, condition_name, condition_index)

        msg = "{} 중지\n".format(condition_name)
        self.sns_message += msg

