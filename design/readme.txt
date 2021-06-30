# Qt Designer 설치
pip install pyqt5
pip install pyqt5designer


(base) C:\Users\myuser>designer
혹은
C:\Anaconda3-32\Library\bin\designer.exe 실행
사용법 : https://generalbulldog.tistory.com/30
https://notstop.co.kr/98/

UI 파일을 파이썬 코드로 변환하기

C:\Anaconda3-32\Lib\site-packages\PyQt5\uic 에 저장
uic 디렉터리를 선택한 후 Shift 키를 누른 상태에서 마우스 오른쪽 버튼을 클릭합니다. (이곳에서 cmd 실행)
python -m PyQt5.uic.pyuic -x [ui 파일명] -o [ to py 파일명]