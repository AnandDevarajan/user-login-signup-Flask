from flask import Flask, request, render_template, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3

location = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    con = sqlite3.Connection(location+"\stackqueue.db")
    cursor = con.cursor()
    rows1 = cursor.execute("SELECT password from users where email=?", [email])
    hpass = rows1.fetchone()
    finalHash = hpass[0]
    print(finalHash, password)
    if(check_password_hash(hpass[0], password) == True):
        params2 = (email, hpass[0])
        query2 = "SELECT email, password from users where email = ? and password = ?"
        cursor.execute(query2, params2)
        rows = cursor.execute(query2, params2)
        rows = rows.fetchall()
        print(rows)
        if(len(rows) == 1):
            # Here remove check.html put the first page user sees after logged
            return render_template('check.html')
        else:
            return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        con = sqlite3.Connection(location+'\stackqueue.db')
        cursor = con.cursor()
        con.execute(
            "CREATE TABLE IF NOT EXISTS users(name TEXT NOT NULL,email TEXT NOT NULL,password TEXT NOT NULL)")
        hashpassword = generate_password_hash(password)
        params = (name, email, hashpassword)
        query1 = "INSERT into users values(?,?,?)"
        cursor.execute(query1, params)
        con.commit()
        return redirect('/')
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
