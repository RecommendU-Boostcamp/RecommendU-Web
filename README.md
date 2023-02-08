# RecommendU-web
🎯 [FE/BE] 맞춤형 합격 자기소개서 추천 서비스 RecommendU

## 🛠 Stack
### Frontend
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=JavaScript&logoColor=white"> <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=HTML5&logoColor=white"> <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=CSS3&logoColor=white">

### Backend
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=MySQL&logoColor=white">

## 📋 DataBase ERD
![image](https://user-images.githubusercontent.com/46878756/217413934-be4973f7-1273-43ea-beb1-4ea817d8219a.png)

## ⚙ Core Functions
### 사용자 부분
  - 회원가입 및 로그인 기능 구현 (비밀번호 암호화 저장)
  - Django Authentication System을 사용한 사용자 인증
  - 회원정보 수정 기능 구현
### 자기소개서 부분
  - 사용자가 입력한 정보에 따라서 학습 모델을 통해 inference해주는 API 구현
  - 자기소개서에 대한 '좋아요','싫어요','스크랩' 체크 기능 구현
  - 사용자 별 마이 페이지 스크랩한 자기소개서 보여주기 구현
### 로그 부분
  - 답변을 제외한 사용자가 입력한 정보(회사,직무,질문)를 저장하는 로그(recommendlog) 구현
  - 추천된 자기소개서를 눌렀을 때 저장되는 로그(answerlog) 구현
  - '좋아요', '싫어요', '스크랩' 버튼을 눌렀을 때 저장되는 로그(evallog) 구현
### ML 서버 연결 부분
  - 학습에 필요한 데이터를 보내주는 API구현
  - 학습 모델을 받는 API구현
  
## 🗃 Structure
```
|-- accounts
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- models.py
|   |-- serializers.py
|   |-- templates
|   |   `-- accounts
|   |       |-- login.html
|   |       |-- mypage.html
|   |       `-- signup.html
|   |-- tests.py
|   |-- urls.py
|   `-- views.py
|-- inference
|   |-- predict.py
|   |-- preprocess.py
|   `-- similarity.py
|-- logs
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- serializers.py
|   |-- tests.py
|   |-- urls.py
|   `-- views.py
|-- manage.py
|-- recommendu
|   |-- __init__.py
|   |-- asgi.py
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
|-- requirements.txt
|-- services
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- dbinit
|   |   |-- initiation.py
|   |-- models.py
|   |-- serializers.py
|   |-- templates
|   |   `-- services
|   |       `-- main.html
|   |-- tests.py
|   |-- urls.py
|   `-- views.py
|-- static
|   |-- css
|   |   `-- style.css
|   |-- images
|   `-- js
|       `-- index.js
`-- templates
    |-- base.html
   
```

## Usage
