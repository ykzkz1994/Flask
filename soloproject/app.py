from flask import Flask #플라스크
from flask import render_template #
from flask import request
from flask import jsonify
from flask import abort
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime #컬럼에 사용될  시간 설정 import
import webbrowser
import threading

app = Flask(__name__)


#데이터베이스 설정 (데이터 베이스 종류+사용할 드라이버://사용자이름:비밀번호@서버주소/연결할 데이터베이스 이름)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://todoproject:1234@localhost/solo_todo'
db=SQLAlchemy(app)

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

# 라우트 정의를 서버 시작 전에 위치시킵니다.
@app.route('/')
def Home():
    return render_template('home.html')

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
        #completed는 진행률이 100이되면 바뀌게 설정할것
        todo.deadline = request.json['deadline']
        todo.priority = request.json['priority']
        todo.category = request.json['category']
        todo.important =
        
    else:
        abort(404,message="유효하지 않은 요청입니다 잠시 후에 다시 시도해주세요 ")






#데이터 베이스 생성
with app.app_context():
    db.create_all()


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')#브라우저 실행시 켜질 초기 경로

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
