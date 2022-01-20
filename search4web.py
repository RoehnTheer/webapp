from threading import Thread
from time import sleep
from flask import Flask, render_template, request, escape, session, copy_current_request_context
from vsearch import search4letters
from checker import check_logged_in
from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError


app = Flask(__name__)
#Конфигурация веб-приложения
app.secret_key = 'GrimDark'
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': '1488',
                          'database': 'vsearchlogDB',}

# def log_request(req: 'flask_request', res: str) -> None:
#     """Сохраняет фразу, символы, результат, IP и используемый браузер в БД"""
#     sleep(15)
#     with UseDatabase(app.config['dbconfig']) as cursor:
#         #Пишем форму запроса
#         _SQL = """insert into log 
#                 (phrase, letters, ip, browser_string, results)
#                 values
#                 (%s, %s, %s, %s, %s)"""
#         #Отправляем запрос к БД
#         cursor.execute(_SQL, (req.form['phrase'],
#                             req.form['letters'],
#                             req.remote_addr,
#                             req.user_agent.browser,
#                             res,))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    """Принимает запрос, обрабатывает его, вызывает функцию сохранения в БД и выводит результат"""
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = "Result of your request: "
    results = str(search4letters(phrase, letters))

    @copy_current_request_context
    def log_request(req: 'flask_request', res: str) -> None:
        """Сохраняет фразу, символы, результат, IP и используемый браузер в БД"""
        sleep(15)
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

    try:
        #log_request(request, results)
        t = Thread(target=log_request, args=(request, results))
        t.start()
    except Exception as err:
        print('****** Ошибка:', str(err))
    return render_template('results.html',
                            the_phrase=phrase,
                            the_letters=letters,
                            the_title=title,
                            the_results=results)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    """Стартовая страница с формой для запроса"""
    return render_template('entry.html', the_title='Welcome to the search4letters on the web!')

@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    """Вытягивает из БД историю запросов и позволяет посмотреть её залогиненным юзерам"""
    # contents = [] Старая версия для записи в лог-файл
    # with open('vsearch.log') as log:
    #     for line in log:
    #         contents.append([])
    #         for item in line.split('|'):
    #             contents[-1].append(escape(item))
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results from log"""
            cursor.execute(_SQL) #Отправляем запрос к БД
            contents = cursor.fetchall() #Извлекаем данные и присваиваем их переменной contents
        titles = ('Phrase','Letters', 'Remote addr', 'User Agent', 'Results')
        return render_template('viewlog.html',
                                the_title='View log',
                                the_row_titles=titles,
                                the_data=contents,)
    except ConnectionError as err:
        print('****** Чё-то с базой данных:', str(err))
    except CredentialsError as err:
        print('****** Чё-то с именем пользователя или/и паролем:', str(err))
    except SQLError as err:
        print('****** Чё-то с запросом в БД:', str(err))
    except Exception as err:
        print('**** Что-то пошло не так ****:', str(err))

@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are logged in'

@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return ' You Logout!'

if __name__ == '__main__':
    app.run(debug=True)
