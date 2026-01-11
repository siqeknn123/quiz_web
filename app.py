from flask import Flask, render_template, request, session, redirect, url_for
from db.crud import get_quizes, get_question_after, check_right_answer, create_quiz_db, create_question_by_quiz, add_link, create_table_results, add_result, get_all_results
from random import shuffle

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678 '

def start_session(quiz_id):
    '''Створення сессії для користувача'''
    session['quiz_id'] = quiz_id
    session['last_question_id'] = 0
    session['correct_ans'] = 0
    session['wrong_ans'] = 0
    session['total'] = 0

def question_form(question): # Функцфія яка перемішує питання
    ''''''
    answers_list = [
        question[2],
        question[3],
        question[4],
        question[5]
    ]
    shuffle(answers_list)
    return render_template("test.html", question_id=question[0], quest=question[1], ans_list=answers_list)

def check_answer(question_id, selected_answer): # Перевіряє відповідь
    if check_right_answer(question_id, selected_answer): # Перевіряє чи правильна відповідь
        session["correct_ans"] += 1
    else:
        session["wrong_ans"] += 1
    session["total"] +=1
#Головна сторінка
@app.route("/", methods=['GET', 'POST']) # Створюємо головну сторінку
def index():
    if request.method == "GET": # якщо метод GET
        quizes = get_quizes() # отримуємо вікторини з БД
        start_session(-1) 
        return render_template("index.html", quizes_list=quizes)
    else: # якщо метод POST
        quiz_id = request.form.get("quiz") # отримуємо номер вибраної вікторини
        name = request.form.get("name")
        start_session(quiz_id) # створює сессію
        session['name']= name
        return redirect(url_for('test')) # перенаправлення на test

# сторінка з тестуванням
@app.route("/test", methods=["GET", "POST"]) # Створюємо сторінку де ми проходимо вікторину
def test():
    if not ("quiz_id" in session) or int(session['quiz_id']) < 0 : # Перевіряємо чи є сесія
        return redirect(url_for("index")) # Переводомо користовуча на головну сторінку
    else:
        if request.method == "POST":  # якщо метод POST
            selected_answer = request.form.get("ans") 
            question_id = int(request.form.get("quest_id"))
            check_answer(question_id, selected_answer)
            session['last_question_id'] = question_id

        new_question = get_question_after(session["quiz_id"], session['last_question_id'])
        if new_question is None:
            return redirect(url_for("result"))
        else:
            return question_form(new_question)
        
    return "<h1>Test</h1>"

@app.route("/result")
def result():
    correct = session['correct_ans']
    wrong = session['wrong_ans']
    total = session['total']
    quiz_id = session['quiz_id']
    name = session['name']
    add_result(name, correct, wrong, quiz_id, total)
    result = render_template("result.html",
                           right=correct,
                           wrong=wrong,
                           total=total)
    session.clear()
    return result


@app.route("/create-quiz", methods=["GET", "POST"])
def create_quiz():
    if request.method == "POST":
        quiz_name = request.form.get("quiz_name")
        quiz_description = request.form.get("quiz_description")
        create_quiz_db(quiz_name, quiz_description)
        return redirect(url_for("index"))
    return render_template("create_quiz.html")

@app.route("/create-question", methods=["GET", "POST"])
def create_question():
    if request.method == "POST":
        quiz_id = request.form.get("quiz_id")
        question = request.form.getlist("question[]")
        question_id= create_question_by_quiz(question)
        add_link(quiz_id, question_id)
        return redirect(url_for('index'))
    quizes = get_quizes()
    return render_template("create_question.html", quizes_list=quizes)

@app.route("/all-result")
def all_results():
    results = get_all_results()
    return render_template("all_results.html", results=results)



if __name__ == '__main__':
    app.run()

