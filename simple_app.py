from flask import Flask, session
from checker import check_logged_in


app = Flask(__name__)
app.secret_key = 'Именем Его!'

@app.route('/')
def hello() -> str:
    return 'Helooo!!!'

@app.route('/page1')
@check_logged_in
def page1() -> str:
    return 'Number 1'

@app.route('/page2')
@check_logged_in
def page2() -> str:
    return 'Number 2'

@app.route('/page3')
@check_logged_in
def page3() -> str:
    return 'Number 3'

@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are logged in'

@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return ' You Logout!'

# @app.route('/status')
# def check_status() -> str:
#     if 'logged_in' in session:
#         return 'Correctly logged'
#     return 'NOT logged!'

if __name__ == '__main__':
    app.run(debug=True)
