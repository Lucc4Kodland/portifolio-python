from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            mensagem TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    button_python = False
    button_discord = False
    button_html = False
    button_db = False

    if request.method == 'POST':
        if 'button_python' in request.form:
            button_python = True
        elif 'button_discord' in request.form:
            button_discord = True
        elif 'button_html' in request.form:
            button_html = True
        elif 'button_db' in request.form:
            button_db = True

    return render_template(
        'index.html',
        button_python=button_python,
        button_discord=button_discord,
        button_html=button_html,
        button_db=button_db
    )

@app.route('/feedback', methods=['POST'])
def feedback():
    email = request.form.get('email')
    text = request.form.get('text')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (email, mensagem) VALUES (?, ?)",
                   (email, text))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)