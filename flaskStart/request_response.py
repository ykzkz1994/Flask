from flask import Flask, url_for,render_template,request
#자동으로 웹브라우저 켜지게하는 임포트
import webbrowser
import threading

#템플릿폴더 경로 지정
app = Flask(__name__, template_folder='flaskStart/templates')


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')


if __name__ == '__main__':
    threading.Timer(1, open_browser).start()  # 서버 시작 후 1초 후에 브라우저가 실행됩니다.
    app.run(debug=True)

@app.route('/query')
def query_example():
    language = request.args.get('Language')
    return f"Requested language:{language}"