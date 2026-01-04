import sqlite3

DB_NAME = 'quizes.db'
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

def close():
    global conn, cursor
    cursor.close()
    conn.close()

def create_tables():
    open()

    cursor.execute('''CREATE TABLE IF NOT EXISTS quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR,
    description TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quetion VARCHAR,
    answer VARCHAR,
    wrong1 VARCHAR,
    wrong2 VARCHAR,
    wrong3 VARCHAR
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS quiz_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER,
    question_id INTEGER,
    FOREIGN KEY (quiz_id) REFERENCES quiz (id),
    FOREIGN KEY (question_id) REFERENCES questions (id)
    )''')
    conn.commit()
    close()

def create_table_results():
    open()
    cursor.execute('''CREATE TABLE IF NOT EXISTS results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR,
    correct INTEGER,
    wrong INTEGER,
    total INTEGER,
    quiz_id INTEGER
    )''')
    conn.commit()
    close()

def add_quizes():
    open()
    
    quizes = [
        ("Столиці", "Вгадай столиці країн світу."),
        ("Кіно", "Питання про фільми та серіали."),
        ("Наука", "Факти про винаходи й відкриття."),
        ("Музика", "Хіти різних епох і жанрів."),
        ("Україна", "Історія, культура та традиції.")
    ]

    cursor.executemany("""INSERT INTO quiz (title, description) VALUES (?, ?)""", quizes)
    conn.commit()
    close()

def add_question():
    open()

    questions = [
        # Столиці
        ("Яка столиця Франції?", "Париж", "Берлін", "Мадрид", "Рим"),
        ("Яка столиця Японії?", "Токіо", "Осака", "Кіото", "Хіросіма"),
        ("Яка столиця Канади?", "Оттава", "Торонто", "Монреаль", "Ванкувер"),
        ("Яка столиця Австралії?", "Канберра", "Сідней", "Мельбурн", "Брисбен"),
        ("Яка столиця Бразилії?", "Бразиліа", "Ріо-де-Жанейро", "Сан-Паулу", "Сальвадор"),

        # Кіно
        ("Хто зняв фільм 'Титанік'?", "Джеймс Кемерон", "Стівен Спілберг", "Крістофер Нолан", "Рідлі Скотт"),
        ("Хто зіграв Гаррі Поттера?", "Деніел Редкліфф", "Руперт Ґрінт", "Елайджа Вуд", "Том Голланд"),
        ("У якому фільмі звучить пісня 'My Heart Will Go On'?", "Титанік", "Привид", "Перл Гарбор", "Бодіґард"),
        ("Який фільм отримав 'Оскар' за найкращий фільм у 2023 році?", "Все завжди і водночас", "Аватар: Шлях води", "Топ Ган: Меверік", "Банші Інішеріна"),
        ("Хто виконує роль Джокера у фільмі 2019 року?", "Хоакін Фенікс", "Джаред Лето", "Хіт Леджер", "Джек Ніколсон"),

        # Наука
        ("Яка планета найближча до Сонця?", "Меркурій", "Венера", "Земля", "Марс"),
        ("Хто сформулював закон всесвітнього тяжіння?", "Ісаак Ньютон", "Альберт Ейнштейн", "Галілео Галілей", "Нікола Тесла"),
        ("Який газ переважає в атмосфері Землі?", "Азот", "Кисень", "Вуглекислий газ", "Аргон"),
        ("Що вимірюється в Омах?", "Опір", "Сила струму", "Потужність", "Напруга"),
        ("Хто винайшов електричну лампу?", "Томас Едісон", "Нікола Тесла", "Бенджамін Франклін", "Олександр Белл"),

        # Музика
        ("Хто виконує пісню 'Shape of You'?", "Ед Ширан", "Шон Мендес", "Бруно Марс", "Дрейк"),
        ("Яка група створила альбом 'The Dark Side of the Moon'?", "Pink Floyd", "Queen", "The Beatles", "Led Zeppelin"),
        ("Який музичний інструмент має клавіші та педалі?", "Піаніно", "Скрипка", "Флейта", "Труба"),
        ("Хто співає пісню 'Bad Guy'?", "Біллі Айліш", "Аріана Ґранде", "Тейлор Свіфт", "Селена Гомес"),
        ("Який стиль музики зародився в Ямайці?", "Реґґі", "Рок", "Джаз", "Блюз"),

        # Україна
        ("Коли Україна проголосила незалежність?", "1991", "1989", "1995", "2001"),
        ("Яке місто є столицею України?", "Київ", "Львів", "Харків", "Одеса"),
        ("Хто написав 'Заповіт'?", "Тарас Шевченко", "Іван Франко", "Леся Українка", "Пантелеймон Куліш"),
        ("Яке море омиває південні береги України?", "Чорне море", "Азовське", "Середземне", "Балтійське"),
        ("Яка страва є традиційною українською?", "Борщ", "Суші", "Піцца", "Тако")
    ]

    cursor.executemany('''INSERT INTO questions (quetion, answer, wrong1, wrong2, wrong3) VALUES (?, ?, ?, ?, ?)''', questions)
    conn.commit()
    close()

def add_links():
    open()
    cursor.execute("PRAGMA foreign_keys=on")
    action = input("Додати зв'язок? (y/n)")
    while action != "n":
        quiz_id = int(input("Введіть номер вікторини"))
        question_id = int(input("Введіть номер запитання"))
        cursor.execute('''INSERT INTO quiz_questions (quiz_id, question_id) VALUES (?, ?)''', [quiz_id, question_id])
        conn.commit()
        action = input("Додати зв'язок? (y/n)")
    close()

def get_quizes():
    open()
    cursor.execute("SELECT * FROM quiz")
    quizes = cursor.fetchall()
    close()
    return quizes
    
def get_question_after(quiz_id=1, question_id=0):
   '''Повертає наступне питання до вибраної вікторини'''
   open()
   cursor.execute("""SELECT questions.id, questions.quetion, questions.answer, questions.wrong1, questions.wrong2, questions.wrong3
                  FROM questions, quiz_questions
                  WHERE quiz_questions.quiz_id = ? AND
                  quiz_questions.question_id > ? AND
                  quiz_questions.question_id = questions.id
                  ORDER BY quiz_questions.id""", (quiz_id, question_id))
  
   question = cursor.fetchone()
   close()
   return question

def check_right_answer(question_id, selected_answer):
    open()
    cursor.execute("""SELECT answer FROM questions WHERE id = ?""", [question_id])
    right_answer = cursor.fetchone()[0]
    close()
    if selected_answer == right_answer:
        return True
    else:
        return False
    
def create_quiz_db(title, description):
    open()
    cursor.execute("""INSERT INTO quiz (title, description) VALUES (?, ?)""", [title, description])
    conn.commit()
    close()
    
def create_question_by_quiz(question: list[str]) -> int:
    open()
    cursor.execute("""INSERT INTO questions (quetion, answer, wrong1, wrong2, wrong3) 
    VALUES (?, ?, ?, ?, ?)
    RETURNING id""", question)
    question_id = cursor.fetchone()[0]
    conn.commit()
    close()
    return question_id

def add_link(quiz_id: int, question_id: int) -> None:
    """Створення зв'язку вікторини з питанням"""
    open()
    cursor.execute("""INSERT INTO  quiz_questions (quiz_id, question_id) VALUES(?, ?)""", [quiz_id, question_id])
    conn.commit()
    close()

def add_result(name, correct, wrong, total, quiz_id):
    open()
    cursor.execute('''INSERT INTO results (name, correct, wrong, total, quiz_id)
    VALUES(?, ?, ?, ?, ?)''', [name, correct, wrong, total, quiz_id])
    conn.commit()
    close()




