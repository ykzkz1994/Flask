from flask import Flask  # Flask 애플리케이션 객체를 생성하기 위해 사용. 애플리케이션을 시작하는 핵심 클래스.
from flask import render_template  # HTML 템플릿 파일을 렌더링하고 브라우저로 전송하기 위해 사용. 템플릿과 데이터를 결합해서 웹 페이지 생성.
from flask import request  # 클라이언트로부터 받은 HTTP 요청 데이터를 다루기 위해 사용. 폼 데이터, 쿼리 스트링, 헤더 등을 처리할 수 있음.
from flask import jsonify  # 파이썬 데이터를 JSON 형식으로 변환하여 HTTP 응답으로 전송하기 위해 사용. 주로 API 응답을 보낼 때 사용.
from flask import abort  # 특정 HTTP 에러 상태 코드를 반환하기 위해 사용. 예를 들어, 권한이 없거나 리소스를 찾을 수 없을 때 404 또는 403 같은 상태 코드 반환.


from flask_login import LoginManager  # Flask 애플리케이션에 로그인 관리 기능을 추가하는 객체. 사용자를 인증, 로그아웃 등 로그인 흐름 관리.
from flask_login import UserMixin  # 사용자의 클래스를 정의할 때 상속하는 믹스인 클래스. 사용자 모델에 필요한 속성과 메서드를 제공함.
from flask_login import login_user  # 사용자를 로그인 처리하는 함수. 사용자를 인증하고 세션에 저장하여 로그인이 유지되도록 함.
from flask_login import logout_user  # 현재 로그인한 사용자를 로그아웃 처리하는 함수. 세션을 종료하여 사용자의 인증 상태를 해제.
from flask_login import login_required  # 특정 뷰 함수에 적용하여 로그인된 사용자만 접근할 수 있도록 제한하는 데코레이터.
from flask_login import current_user  # 현재 로그인한 사용자의 정보를 제공하는 객체. 로그인한 사용자의 정보를 접근할 때 사용.


from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime #컬럼에 사용될  시간 설정 import

import webbrowser
import threading

from werkzeug.security import generate_password_hash  # 비밀번호를 안전하게 해시(암호화)하기 위한 함수. 데이터베이스에 평문 비밀번호를 저장하는 대신 해시된 값을 저장하여 보안성을 높임.
from werkzeug.security import check_password_hash  # 사용자가 입력한 비밀번호와 데이터베이스에 저장된 해시된 비밀번호를 비교하여 일치 여부를 확인하는 함수. 로그인 시 비밀번호를 검증할 때 사용.


app = Flask(__name__)

login_manager = LoginManager()  # LoginManager 객체를 생성. 로그인과 관련된 기능들을 관리하기 위한 객체.
login_manager.init_app(app)  # 생성한 LoginManager 객체를 Flask 애플리케이션(app)에 연결하여 로그인 관리 기능을 사용할 수 있도록 할당.
login_manager.login_view = 'login'  # 로그인이 필요한 페이지에 접근할 때 사용자를 리다이렉트할 로그인 페이지의 뷰 함수 이름을 지정.


#데이터베이스 설정 (데이터 베이스 종류+사용할 드라이버://사용자이름:비밀번호@서버주소/연결할 데이터베이스 이름)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://todoproject:1234@localhost/solo_todo'
#SQLAlchemy의 수정 추적 기능을 비활성화(성능상의 이유로 권장)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#세션 및 쿠키에 대한 보안향상을 위한 비밀 키를 설정
app.config['SECRET_KEY'] = 'password'
db=SQLAlchemy(app)


#데이터 모델 정의
#파스칼케이스
class User(UserMixin,db.Model):
    no = db.Column(db.Integer,primary_key=True) #회원번호 프리이머리키
    id = db.Column(db.String(14),unique=True,nullable=False) #로그인 아이디 고유값,null불가
    password_hash =db.Column(db.String(512),nullable=False) #비밀번호 null불가
    email = db.Column(db.String(50),nullable=False) # 이메일 null불가능
    nickname = db.Column ( db.String(10),unique=True,nullable=True) # 닉네임 중복방지를위해 유니크 하지만 설정 안할수도 있음
    name = db.Column (db.String(30),nullable=False) #실제 이름  알파벳 고려 길게 그러나 null은 불가
    birth = db.Column (db.Integer,nullable=False) #출생년도  null불가


    def set_password(self,password): #입력받은 패스워드를 암호화시켜주는 함수인듯?
        self.password_hash = generate_password_hash(password)

    def check_password(self,password): #사용자가 입력한 평문 비밀번호와 DB의 해시비밀번호가 일치하는지 확인하는 함수
        #사용자가 입력한 평문 비밀번호를 해시화해서 DB의 해시 비밀번호와 대조하는 방식
        return check_password_hash(self.password_hash,password)




#데이터 모델 정의하기
#python에서 카멜이아니라 파스칼케이스를 사용하는게 관례
class Todo(db.Model):
    no = db.Column(db.Integer, primary_key=True) #프라이머리키 정수타입
    title = db.Column(db.String(100), nullable=False) #제목 급하게 작성 할 수도 있으니 내용을 제목에 기입 할 수도 있음 null불가
    description = db.Column(db.Text, nullable=True) #내용 제한없는 가변길이에 급하게 작성시 제목에 작성 할 수 있으니 null가능
    completed = db.Column(db.Boolean, default=False) #완료여부 디폴트는 false, True=완료된거
    created_date = db.Column(db.DateTime, default=datetime.utcnow) # 컬럼이 생성될 때 현재의 UTC 시간을 기본 값으로 자동 저장
    deadline = db.Column(db.DateTime, nullable=True) #마감기한
    priority = db.Column(db.Integer, default=5) #할 일의 우선순위 1이 가장 높은 우선순위이고 숫자가 클수록 낮은 우선순위
    category = db.Column(db.String(10), nullable=True) #카테고리 구현 할 때 뷰에서 버튼 클릭하면 밸류 들어가는식으로 구현
    important = db.Column(db.Boolean, default=False) #해당 할 일이 중요한지 여부
    recurring = db.Column(db.Boolean, default=False) #반복 일정
    assigned_to = db.Column(db.String(100), nullable=True) #할당된사람 /협업상황시에 유용 null 허용
    progress = db.Column(db.Integer, default=0) #진척률/할 일의 진행 상황을 백분율(%)로 표시

    ##테이블 제약조건도 나중에 추가하기

    def __repr__(self):
        return f'<Todo {self.title}>'


#Flask-login이 현재 로그인상태인 사용자를 로드 할 수 있도록 회원번호로
@login_manager.user_loader
def load_user(user_no):
    return User.query.get(int(user_no))

# 라우트 정의를 서버 시작 전에 위치시킵니다.
@app.route('/')
def Home():
    return render_template('home.html')

#로그인 페이지리턴 및 기능추가
@app.route('/signup',methods=['GET','POST'])
def signup ():
    #요청메서드가 포스트방식인 경우엔
    if request.method == 'POST':
        #자동생성 프라이머리키를 제외한 폼
        id = request.form['id']#이렇게만 쓰면 컬럼타입에 맞는 폼을 알아서 불러오나?
        password = request.form ['password'] # 비밀번호 입력
        email = request.form ['email']
        nickname = request.form ['nickname']
        name = request.form ['name']
        birth = request.form ['birth']

        user = User(id=id,email=email,nickname=nickname,name=name,birth=birth)
        user.set_password(password)#비밀번호는 해시화

        db.session.add(user)#추가
        db.session.commit()#커밋

        #가입문구와 상태코드를 리턴
        return jsonify({'메세지': '회원가입을 축하합니다'}),201
    return render_template('signup.html')

#로그인을 위한 라우트
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='POST':
        user = User.query.filter_by(no=request.form['no']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return  jsonify({'message':'로그인성공'}),200
        return abort(401,description="invalid credentials")
    return render_template('login.html')

#로그아웃을 위한 라우트
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message':'로그아웃 성공'}),200


@app.route('/first')
def first():
    return "첫번째 페이지 "

@app.route('/todo')
def todo():
    return render_template('todo.html')# todohtml

#Todo생성
@app.route('/todo/add',methods=['post'])
def add_todo():
    title = request.json['title']
    description = request.json['description']
    completed= request.json['completed']
    created_date = request.json['created_date']
    deadline = request.json['deadline']
    priority = request.json['priority']
    category = request.json['category']
    important = request.json['important']
    recurring = request.json['recurring']
    assigned_to = request.json['assigned_to']
    progress = request.json['progress']

    new_todo = Todo(title=title,description=description,completed=completed,created_date=created_date,deadline=deadline,priority=priority,category=category,important=important,recurring=recurring,assigned_to=assigned_to,progress=progress)
    db.session.add(new_todo) #new_todo객체를 db에 추가
    db.session.commit() #commit으로 변경사항 저장

    return jsonify({'message':'Todo create'}),201


# Todo 조회
@app.route('/todo/list', methods=['GET'])
def list_todo():
    todos = Todo.query.all()
    return jsonify([
        {
            'no': todo.no,
            'title': todo.title,
            'description': todo.description,
            'completed': todo.completed,
            'deadline': todo.deadline.strftime('%Y-%m-%dT%H:%M:%S') if todo.deadline else None,
            'priority': todo.priority,
            'category': todo.category,
            'important': todo.important,
            'recurring': todo.recurring,
            'assigned_to': todo.assigned_to,
            'progress': todo.progress
        } for todo in todos
    ]), 200


#Todo수정
@app.route('/todo/edit/<int:no>',methods=['PUT'])
def edit_todo(no): #no를 기준으로 db에서 수정하는 메서드
    todo = Todo.query.filter_by(no=no).first()
    if todo:
        todo.title = request.json['title']
        todo.description = request.json['description']
        # todo.completed = (todo.progress = 100 )=True,(todo.progress != 100)=False 일단 주석처리 나중에 다시 코드 건드려야함  요청을 동시에 하면 안될 것 같음
        todo.deadline = request.json['deadline']
        todo.priority = request.json['priority']
        todo.category = request.json['category']
        todo.important = request.json['important']
        todo.recurring = request.json['recurring']
        todo.assigned_to = request.json['assigned_to']
        todo.progress = request.json['progress']

        db.session.commit()#저장
    else:
        abort(404,description="유효하지 않은 요청입니다 잠시 후에 다시 시도해주세요 ")

#Todo삭제
@app.route('/todo/delete/<int:no>',methods=['DELETE']) #no로 판별하여 todo를 삭제하는 메서드
def delete_todo(no):
    todo = Todo.query.filter_by(no=no).first()
    if todo:#삭제처리를 한 후 커밋 그리고 삭제완료라는 메세지와 처리상태코드를 리턴함 
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'message':'삭제 완료'}),200
    else:#오류코드인 404코드와 메세지를 보냄
        abort(404,description="정상적인 요청이 아닙니다 잠시 후 다시 시도해주세요")




#데이터 베이스 생성
with app.app_context():
    db.create_all()


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')#브라우저 실행시 켜질 초기 경로

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
