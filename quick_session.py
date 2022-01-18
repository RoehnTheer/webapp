from flask import Flask, session


app = Flask(__name__)
app.secret_key = 'For The Emperor!'

@app.route('/setuser/<user>')
def setuser(user: str) -> str:
    session['user'] = user
    return 'Имя изера: ' + session['user']


@app.route('/getuser')
def getuser() -> str:
    return 'Наш юзер: ' + session['user']



if __name__ == '__main__':
    app.run(debug=True)
