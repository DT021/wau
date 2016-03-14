WAU(Where Are U)
=======================

프로젝트 WAU(Where Are U)는 Social Media에 올라온 location information이 없는 포스트에 대하여 그 내용으로부터 장소를 추출하는 extraction engine과 그에 대한 위치 기반 social media application으로 구성되어 있다.

기술 요약
-----------

1. Extraction engine은 다양한 Social Media로부터 포스트를 수집하는 crawler, 포스트 내 location information들과 ‘Naver Map’을 통하여 구축된 location dictionary, 수집 된 데이터를 통하여 학습을 하는 learing module로 구성되어 있다. 
2. Map based social media application은 입력된 포스트 내용을 input으로 Extraction engine을 통해 나온 결과를 user에게 추천하여 지도 상에 포스트를 남기는 위치 기반 Social media application이다.
[졸업프로젝트 결과 보고서]


배경
-----------
Facebook, Instagram 등 기존의 Social media들은 이미 포스팅에  location information을 추가하는 기능을 제공하고 있지만 추가적인 행동을 요구하는 interface, 배터리에 부담을 주는 GPS로 인하여 그 사용률이 현저히 낮은 실정이다. 
WAU는 location information이 없는 포스트에 location information을 추가하고 더 나아가 location based social media를 제작하여 포스팅 단계에서 location을 추천하여 information 사용을 유도한다. 이를 통하여 추가된 포스트 location information은 포스트의 추가적인 feature로서 location information을 필요로 하는 여러분야에서 이용 될 가능성이 매우 높다.
 본 프로젝트의 서비스인 MAPIA는 Facebook, Instagram, Twitter 등의 대표적인 SNS와 경쟁하기 이전에 이들 서비스가 효과적으로 제공하지 못하던 장소라는 가치를 차별성 있게 제공함으로써 보완적인 역할로서 사용자들에게 접근할 수 있다. 기존의 SNS와의 파트너로서 인맥과 시간이 아닌 장소를 기반으로 소통의 주체를 옮겨옴과 동시에 이들 SNS를 적극활용하여 초기부터 컨텐츠를 확보할 수 있으며 색다른 가치를 제공한다. 이로써 이들 SNS의 사용자들이 장소에 대해 기록하고 공유할 때 유용하게 사용할 수 있도록 하여  사용자를 빠르게 확보할 수 있도록 하였다.


개발 기술
===========

API Server
-----------
 AWS의 EC2 Instance(Tokyo)에 Ubuntu 서버를 생성하여 Android와 Web을 위한 API 서버를 개발하였다. nginx 웹서버 및 uwsgi 미들웨어를 붙인 Flask 기반 API 서버로서 안드로이드, 웹에 대한 API를 Service 한다. 내부적으로는 DB, Machine Learning Module, Resource Server, Data Collector 등 다른 서버와 통신한다. 
 *[첨부1]MAPIA_api_specification


DB
-----------
 AWS RDS에 2D Indexing 기능을 제공하는 오픈소스 RDBMS인 PostgreSQL을 활용하여 데이터베이스를 구축하였다. Object-Relation-Mapper인 SQLAlchemy를 활용하였으며 ORM 구조는 아래와 같다. 로그인 정보와 메시지 정보는 memory db인 redis를 사용하여 구현하였다.
Resource
-----------
지도 기반 SNS를 개발하면서 사용자들이 업로드하는 사진, 동영상 파일들을 AWS S3에 저장하여 리소스 서버를 생성하고 Android 또는 Web에서 API를 통해 받아볼 수 있도록 구성하였다. 
Analysis(Recommend) Server
-----------
Machine Learning을 활용한 분석 엔진이다. 본 프로젝트에서는 사용자의 연동된 다른 SNS와 MAPIA에 업로드한 게시글을 활용하여 Text to Place 엔진을 개발하였다. Falcon API 서버(REST API용 데이터 관리 서버)를 활용하여 Analysis Server를 구축하고 Data Collector를 이용하여 장소 및 포스팅 데이터를 수집하였다.
 이를 이용하여 Place Dictionary, Tag Relationship Dictionay와 Training dataset을 만들고 3일동안 AWS EC2 Instance m4.4xlarge type(16cpu, 64Gib Memory)을 대여하여 학습을 진행하였다. Analysis 모듈 개발은 대여 서버에 ipython notebook을 구축하여 진행하였으며 학습 및 평가가 끝난 clf을 통해 Text to Place 엔진 및 Falcon API 서버를 구축하였다. Input은 포스트이며 output은 게시글에서 의미하는 장소 벡터이다.
 Learning module에선 입력된 post의 content를 자연어 처리하여 tag들의 집합으로 구성하고, 텍스트로 작성되어 있는 tag들을 학습할 수 있도록 (x, y)의 형태로 바꾸는데 수식으로 바꾸는 과정은 다음과 같다.

이를 이용하여 python maching learing library인 scikit-learn을 통하여 1차원 SVM모델을 통하여 학습을 하였다.
Data Collector
-----------
 Instagram, Twitter의 게시글 데이터를 open API를 활용하여 수집하였다(Instagram 16,000,000개 - tag search api를 이용하여 수집, 데이터 크기는 Instagram API call 차단 Threshold인 80,000건 * 20일, Facebook은 정책 변경으로 게시글 수집 불가). python 기반 크롤러인 Scrapy를 이용하여 naver map crawling(place id 기준 crawling 821,000건).
Visualization Module
-----------
ELK 스택을 활용하여 서비스 분석을 위한 Visualization Module을 개발하였다. 서버에 남는 Android 및 Web의 request API와 Analysis API의 로그를 기록하여 Fluent라는 Log collector를 활용하여 정형화 시켜 ELK 서버로 전송하고 Elasticsearch라는 루씬 검색엔진 기반 NoSQL 데이터베이스에 저장한다. 이를 Kibana라는 Elasticsearch 기반 시각화 엔진을 이용하여 MAPIA 사용자들의 사용 흐름 시각화 및 기계학습 분류 결과 시각화를 하였다. 

참고문헌
-----------
http://www.scipy-lectures.org/
http://scikit-learn.org/stable/modules/clustering.html
Terrence S. Furey, Nello Cristianini, Nigel Duffy, David W. Bednarski, Michel Schummer and David Haussler (2000) Support vector machine classification and validation of cancer tissue samples using microarray expression data
