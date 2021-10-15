import numpy as np #벡터와 행렬 계산을 위한 함수 라이브러리
import pandas as pd #데이터 분석을 위한 라이브러리
import quandl, math #주가 데이터를 가져오기 위한 라이브러리
# from sklearn import cross_validation #학습과 테스트를 위한 데이터 분리
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression #회귀분석 라이브러리

#구글 주가 데이터를 가져와 Quandl데이터 셋 구성
#Quandl 데이터셋에는 일단위 시가, 종가, 고가, 저가, 거래량 등이 포함되어 있음
df = quandl.get('WIKI/GOOGL')

df['Close3'] = df['Close'].shift(3)
df['Close2'] = df['Close'].shift(2)
df['Close1'] = df['Close'].shift(1)
df.dropna(inplace=True)

X = np.array(df[['Close3', 'Close2', 'Close1']]) #회귀분석 라이브러리 활용을 위한 데이터셋 구성
y = np.array(df['Close']) #타겟  구성

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2) #데이터 분리

clf = LinearRegression() #회귀 분석 객체 생성
clf.fit(X_train, y_train) #회귀 분석 학습

#만약 Close3: 812 ~Close1: 799일 경우 종가 예측 방법
clf.predict([[812, 813, 807]])