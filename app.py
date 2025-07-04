from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Create DB
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY, email TEXT, password TEXT)''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS exams 
                    (id INTEGER PRIMARY KEY, title TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS questions 
                    (id INTEGER PRIMARY KEY, exam_id INTEGER, question TEXT, a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS results 
                    (id INTEGER PRIMARY KEY, user_id INTEGER, exam_id INTEGER, score INTEGER)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS posts 
                    (id INTEGER PRIMARY KEY, user_id INTEGER, content TEXT, filename TEXT)''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS exams 
                    (id INTEGER PRIMARY KEY, title TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS questions 
                    (id INTEGER PRIMARY KEY, exam_id INTEGER, question TEXT, a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS results 
                    (id INTEGER PRIMARY KEY, user_id INTEGER, exam_id INTEGER, score INTEGER)''')

    conn.close()

init_db()

# Routes
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        
    conn.execute('''CREATE TABLE IF NOT EXISTS exams 
                    (id INTEGER PRIMARY KEY, title TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS questions 
                    (id INTEGER PRIMARY KEY, exam_id INTEGER, question TEXT, a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS results 
                    (id INTEGER PRIMARY KEY, user_id INTEGER, exam_id INTEGER, score INTEGER)''')

    conn.close()
        return redirect('/')
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    conn = sqlite3.connect('database.db')
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
    
    conn.execute('''CREATE TABLE IF NOT EXISTS exams 
                    (id INTEGER PRIMARY KEY, title TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS questions 
                    (id INTEGER PRIMARY KEY, exam_id INTEGER, question TEXT, a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS results 
                    (id INTEGER PRIMARY KEY, user_id INTEGER, exam_id INTEGER, score INTEGER)''')

    conn.close()
    if user:
        session['user_id'] = user[0]
        return redirect('/dashboard')
    return 'Login Failed'

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    conn = sqlite3.connect('database.db')
    posts = conn.execute('SELECT * FROM posts').fetchall()
    
    conn.execute('''CREATE TABLE IF NOT EXISTS exams 
                    (id INTEGER PRIMARY KEY, title TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS questions 
                    (id INTEGER PRIMARY KEY, exam_id INTEGER, question TEXT, a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS results 
                    (id INTEGER PRIMARY KEY, user_id INTEGER, exam_id INTEGER, score INTEGER)''')

    conn.close()
    return render_template('dashboard.html', posts=posts)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if 'user_id' not in session:
        return redirect('/')
    if request.method == 'POST':
        content = request.form['content']
        file = request.files['file']
        filename = None
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn = sqlite3.connect('database.db')
        conn.execute('INSERT INTO posts (user_id, content, filename) VALUES (?, ?, ?)', (session['user_id'], content, filename))
        conn.commit()
        
    conn.execute('''CREATE TABLE IF NOT EXISTS exams 
                    (id INTEGER PRIMARY KEY, title TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS questions 
                    (id INTEGER PRIMARY KEY, exam_id INTEGER, question TEXT, a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS results 
                    (id INTEGER PRIMARY KEY, user_id INTEGER, exam_id INTEGER, score INTEGER)''')

    conn.close()
        return redirect('/dashboard')
    return render_template('post.html')

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/exam_list')
def exam_list():
    conn = sqlite3.connect('database.db')
    exams = conn.execute('SELECT * FROM exams').fetchall()
    
    conn.execute('''CREATE TABLE IF NOT EXISTS exams 
                    (id INTEGER PRIMARY KEY, title TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS questions 
                    (id INTEGER PRIMARY KEY, exam_id INTEGER, question TEXT, a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS results 
                    (id INTEGER PRIMARY KEY, user_id INTEGER, exam_id INTEGER, score INTEGER)''')

    conn.close()
    return render_template('exam_list.html', exams=exams)

@app.route('/take_exam/<int:exam_id>')
def take_exam(exam_id):
    conn = sqlite3.connect('database.db')
    exam = conn.execute('SELECT * FROM exams WHERE id = ?', (exam_id,)).fetchone()
    questions = conn.execute('SELECT * FROM questions WHERE exam_id = ?', (exam_id,)).fetchall()
    
    conn.execute('''CREATE TABLE IF NOT EXISTS exams 
                    (id INTEGER PRIMARY KEY, title TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS questions 
                    (id INTEGER PRIMARY KEY, exam_id INTEGER, question TEXT, a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS results 
                    (id INTEGER PRIMARY KEY, user_id INTEGER, exam_id INTEGER, score INTEGER)''')

    conn.close()
    return render_template('take_exam.html', exam=exam, questions=questions)

@app.route('/submit_exam', methods=['POST'])
def submit_exam():
    exam_id = request.form['exam_id']
    conn = sqlite3.connect('database.db')
    questions = conn.execute('SELECT * FROM questions WHERE exam_id = ?', (exam_id,)).fetchall()
    score = 0
    for q in questions:
        selected = request.form.get(f'q{q[0]}')
        if selected == q[7]:
            score += 1
    conn.execute('INSERT INTO results (user_id, exam_id, score) VALUES (?, ?, ?)', (session['user_id'], exam_id, score))
    conn.commit()
    
    conn.execute('''CREATE TABLE IF NOT EXISTS exams 
                    (id INTEGER PRIMARY KEY, title TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS questions 
                    (id INTEGER PRIMARY KEY, exam_id INTEGER, question TEXT, a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS results 
                    (id INTEGER PRIMARY KEY, user_id INTEGER, exam_id INTEGER, score INTEGER)''')

    conn.close()
    return f'You scored {score} out of {len(questions)}'

@app.route('/admin/create_exam', methods=['GET', 'POST'])
def create_exam():
    if request.method == 'POST':
        title = request.form['title']
        conn = sqlite3.connect('database.db')
        conn.execute('INSERT INTO exams (title) VALUES (?)', (title,))
        conn.commit()
        
    conn.execute('''CREATE TABLE IF NOT EXISTS exams 
                    (id INTEGER PRIMARY KEY, title TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS questions 
                    (id INTEGER PRIMARY KEY, exam_id INTEGER, question TEXT, a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS results 
                    (id INTEGER PRIMARY KEY, user_id INTEGER, exam_id INTEGER, score INTEGER)''')

    conn.close()
        return redirect('/exam_list')
    return render_template('create_exam.html')

@app.route('/admin/add_question/<int:exam_id>', methods=['GET', 'POST'])
def add_question(exam_id):
    conn = sqlite3.connect('database.db')
    exam = conn.execute('SELECT * FROM exams WHERE id = ?', (exam_id,)).fetchone()
    if request.method == 'POST':
        question = request.form['question']
        a = request.form['a']
        b = request.form['b']
        c = request.form['c']
        d = request.form['d']
        correct = request.form['correct']
        conn.execute('''INSERT INTO questions (exam_id, question, a, b, c, d, correct)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                     (exam_id, question, a, b, c, d, correct))
        conn.commit()
        return redirect(f'/admin/add_question/{exam_id}')
    return render_template('add_question.html', exam=exam)


# ----- Exams Functionality -----

@app.route('/exams')
def exams():
    if 'user_id' not in session:
        return redirect('/')
    conn = sqlite3.connect('database.db')
    exams = conn.execute('SELECT * FROM exams').fetchall()
    conn.close()
    return render_template('exam_list.html', exams=exams)

@app.route('/take_exam/<int:exam_id>')
def take_exam(exam_id):
    if 'user_id' not in session:
        return redirect('/')
    conn = sqlite3.connect('database.db')
    exam = conn.execute('SELECT * FROM exams WHERE id = ?', (exam_id,)).fetchone()
    questions = conn.execute('SELECT * FROM questions WHERE exam_id = ?', (exam_id,)).fetchall()
    conn.close()
    return render_template('take_exam.html', exam=exam, questions=questions)

@app.route('/submit_exam/<int:exam_id>', methods=['POST'])
def submit_exam(exam_id):
    score = 0
    conn = sqlite3.connect('database.db')
    questions = conn.execute('SELECT * FROM questions WHERE exam_id = ?', (exam_id,)).fetchall()
    for q in questions:
        selected = request.form.get(f'q{q[0]}')
        if selected == q[7]:
            score += 1
    conn.execute('INSERT INTO results (user_id, exam_id, score) VALUES (?, ?, ?)', (session['user_id'], exam_id, score))
    conn.commit()
    conn.close()
    return f"Your score: {score}/{len(questions)}"

@app.route('/admin/create_exam', methods=['GET', 'POST'])
def create_exam():
    if request.method == 'POST':
        title = request.form['title']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO exams (title) VALUES (?)', (title,))
        exam_id = cur.lastrowid
        for i in range(1, 4):
            question = request.form.get(f'q{i}')
            a = request.form.get(f'a{i}')
            b = request.form.get(f'b{i}')
            c = request.form.get(f'c{i}')
            d = request.form.get(f'd{i}')
            ans = request.form.get(f'ans{i}')
            cur.execute('INSERT INTO questions (exam_id, question, a, b, c, d, correct) VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (exam_id, question, a, b, c, d, ans))
        conn.commit()
        conn.close()
        return redirect('/exams')
    return render_template('create_exam.html')
