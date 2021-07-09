import math
import time
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import QRect
import os
import pymysql
from PyQt5.QAxContainer import QAxWidget
from PyQt5 import uic
from .financialStatementCrawling import Crawling
from PyQt5.QtCore import QThread
import threading
from dotenv import load_dotenv, dotenv_values
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import threading

# from PyQt5.QtCore import QEventLoop
# from pykrx import stock
# import datetime
#
# import matplotlib.pyplot as plt
# # 참조 : https://yobro.tistory.com/202
#
# dt_now = datetime.datetime.now()
# COM_DATE = dt_now.strftime('%Y%m%d') # 기준일자 600 거래일 전일 부터 현제까지 받아옴
form_class = uic.loadUiType("ui/stockinfo/finance.ui")[0]

class FinancialStatements(QWidget, form_class):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)  # 현재 form_class를 선택한다.
        self.LoadDataAction.clicked.connect(self.LoadDataClicked)
        self.CrawlingDataction.clicked.connect(self.CrawlingDataClicked)

    def LoadDataClicked(self):
        print('LoadData')
        pass

    def CrawlingDataClicked(self):
        crawling = Crawling()
        crawling.start()
        pass