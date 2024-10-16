from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@host/db_name'
db = SQLAlchemy(app)

class User (db.Model):

    #테이블명 지정 코드 이걸 생략시 기본적으로 클래스이름을 소문자화시킨 'user'가 됨
    __tablename__ = 'users'

    #id 라는 컬럼 정수형,프라이머리키
    id = db.Column(db.Integer,primary_key=True)
    #username 이라는 컬럼 문자열 80자까지,유일,null허용
    username = db.Column(db.String(80),unique=True,nullable=True)
