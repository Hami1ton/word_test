import sqlite3
from flask import request, session, g, redirect, url_for, \
     render_template, flash
from contextlib import closing

from app_factory import create_app
from app_urls import LOGOUT_URL, WORD_TEST_URL, WELCOME_URL, LOGIN_URL, TEST_RESULT_URL
from problems_creator import ProblemsCreator

NUMBER_OF_QUESTIONS = 5
app = create_app("app_config.py")

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read().decode('utf-8'))

        # データを挿入
        with open("db/Words.txt", mode="r") as f:
            word_list = [s.strip() for s in f.readlines()]

        with open("db/Meanings.txt", mode="r") as g:
            meaning_list = [s.strip() for s in g.readlines()]

        for i in range(len(word_list)-1):
            db.execute('insert into english_words_and_meanings (word, meaning) values (?, ?)',
                       [word_list[i], meaning_list[i]])
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route(WELCOME_URL, methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        return redirect(url_for('start_test'))
    return render_template('welcome.html')


@app.route(LOGIN_URL, methods=['GET', 'POST'])
# ログイン画面
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('welcome'))
    return render_template('login.html', error=error)


@app.route(LOGOUT_URL)
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route(WORD_TEST_URL)
def start_test():
    # TODO 問題数を変えられるようにしたい
    # problem_listは[[英単語,[選択肢1, 2, 3]], [], [],...,[]]で指定
    creator = ProblemsCreator(NUMBER_OF_QUESTIONS)
    session["problem_list"] = creator.create_question_list()
    return render_template('start_test.html', problem_list=session["problem_list"])


@app.route(TEST_RESULT_URL, methods=['POST'])
def show_result():
    answer_list = [int(request.form[problem[0]]) for problem in session["problem_list"]]
    # 答え合わせ
    count = 0
    # 選択肢番号からユーザの選んだ英単語の"意味"のリストを作成する
    users_answer = [session["problem_list"][i][1][answer_list[i]]
                    if answer_list[i] != 3 else None for i in range(NUMBER_OF_QUESTIONS)]
    for i in range(NUMBER_OF_QUESTIONS):
        # 答えとユーザの選んだ意味が合致していれば点数を加算する
        if session["problem_words_and_meanings_list"][i][1] == users_answer[i]:
            count += 1
    return render_template('result.html', point=count)


if __name__ == '__main__':
    init_db()
    app.run()
    # print(app.config["PASSWORD"])
