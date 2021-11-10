[에러]
AttributeError: module 'tweepy' has no attribute 'StreamListener'
[솔루션]
import tweepy
print(tweepy.__version__)

만일 3.7.0~3.10.0 버전이 아닐 경우, 아래의 코드로 tweepy 버전을 바꿔준다
pip install tweepy==3.10.0


[에러]
java.nio.file.InvalidPathException: Illegal char <*> at index 64: C:\Anaconda3-64\envs\deeplearning\Lib\site-packages\konlpy\java\*

[해결]
https://daewonyoon.tistory.com/386
pip install -U "jpype1<1.1"