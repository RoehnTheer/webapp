from flask import Flask, render_template, request, escape
from vsearch import search4letters
from DBcm import UseDatabase

app = Flask(__name__)
# Физкультпривет
#Конфигурация веб-приложения
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': '1488',
                          'database': 'vsearchlogDB',}

def log_request(req: 'flask_request', res: str) -> None:

    with UseDatabase(app.config['dbconfig']) as cursor:
        #Пишем форму запроса
        _SQL = """insert into log 
                (phrase, letters, ip, browser_string, results)
                values
                (%s, %s, %s, %s, %s)"""
        #Отправляем запрос к БД
        cursor.execute(_SQL, (req.form['phrase'],
                            req.form['letters'],
                            req.remote_addr,
                            req.user_agent.browser,
                            res,))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = "Result of your request: "
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                            the_phrase=phrase,
                            the_letters=letters,
                            the_title=title,
                            the_results=results)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to the search4letters on the web!')

@app.route('/viewlog')
def view_the_log() -> 'html':
    # contents = [] Старая версия для записи в лог-файл
    # with open('vsearch.log') as log:
    #     for line in log:
    #         contents.append([])
    #         for item in line.split('|'):
    #             contents[-1].append(escape(item))
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select phrase, letters, ip, browser_string, results from log"""
        cursor.execute(_SQL) #Отправляем запрос к БД
        contents = cursor.fetchall() #Извлекаем данные и присваиваем их переменной contents
    titles = ('Phrase','Letters', 'Remote addr', 'User Agent', 'Results')
    return render_template('viewlog.html',
                            the_title='View log',
                            the_row_titles=titles,
                            the_data=contents,)


if __name__ == '__main__':
    app.run(debug=True)