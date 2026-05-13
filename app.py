from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import mysql.connector
from dotenv import find_dotenv, load_dotenv

app = Flask(__name__)
app.secret_key = "6767676767676767"

def get_db():
    return mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        use_pure = True
    )

@app.route('/', methods=['POST','GET'])
def Login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']

        db = get_db()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], password):
                session['username'] = username
                return redirect('Mainpage')
            else:
                flash('Invalid username or password')

        except Exception as e:
            print(e)
            flash('Something went wrong, try again.')

        finally:
            cursor.close()
            db.close()
    return render_template('Login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['Username']
        password = generate_password_hash(request.form['Password'])

        db = get_db()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("SELECT id FROM User WHERE username = %s", (username,))
            User = cursor.fetchone()

            if User:
                flash('Username already taken.')
                return render_template('Register.html')

            cursor.execute(
                "INSERT INTO User (username, password) VALUES (%s, %s)",
                (username, password)
            )
            db.commit()
            session['username'] = username
            return redirect('Mainpage')
                            
        except Exception as e:
            print(e)
            flash('Something went wrong during registration.')

        finally:
            cursor.close()
            db.close()

    return render_template('Register.html')

@app.route('/Mainpage', methods=['GET'])
def mainpage():
    db = get_db()
    cursor = db.cursor()


    return render_template('Mainpage.html')