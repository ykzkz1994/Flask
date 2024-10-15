from flask import Flask, url_for
#자동으로 웹브라우저 켜지게하는 임포트
import webbrowser
import threading

app = Flask(__name__)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.route('/int/<int:var>')
def int_type(var:int):
    return  f'Integer:{var}'

@app.route('/float/<float:var>')
def float_type(var:float):
    return  f'Float:{var}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return  f'Subpath:{subpath}'

@app.route('/uuid/<uuid:some_id>')
def show_uuid(some_id):
    return  f'UUID:{some_id}'




#홈페이지
@app.route('/')
def index():

    #여기서는  인덱스를 호출
    return f'홈페이지:{url_for("index")}'


#뷰함수-사용자 프로필
@app.route('/user/<username>')
def profile(username):
    return f'{username}의 프로필 페이지입니다. 홈으로 가기: {url_for("user_profile",username=username)}'


#정적 파일 테스트를 위한 경로
@app.route('/static-example')
def static_example():
    #여기서는 스테틱 파일네임 스타일 css를 롷출
    return f'정적파일 유알엘 {url_for("static",filename="style.css")}'

#절대 url 테스트
@app.route('/absolute')
def absolute():
    return f'외부절대 url {url_for("index",_external=True)}'

#Https와 절대 URL테스트
@app.route('/https')
def https():
    return f'HTTPs절대 url {url_for("index",_scheme="https",_external=True)}'


#뷰함수-게시물
@app.route('/post/<year>/<month>/<day>')
def show_post(year,month,day):
    #실제로는 날짜에 해당하는 게시물을 보여주는 로직이 위치해아함
    return f'Post for{year}/{month}/{day}날짜 보여주는 메서드'

#타입힌트
def greet(name:str)->str:
    return  f"Hello,{name}"

def add(a:int,b:int)->int:
    return 1
print(add("string",2))

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()  # 서버 시작 후 1초 후에 브라우저가 실행됩니다.
    app.run(debug=True)
