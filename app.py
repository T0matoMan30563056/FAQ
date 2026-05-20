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
@app.route('/MakeMeAdmin', methods=['GET', 'POST'])
def MakeMeAdmin():
    db = get_db()
    cursor = db.cursor()

    username = session.get('username')
    cursor.execute("UPDATE User SET is_admin = TRUE WHERE username = %s", (username,))
    db.commit()

    cursor.close()
    db.close()
    return redirect('/Mainpage')

@app.route('/', methods=['POST','GET'])
def Login():
    session.clear()
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
    if 'username' not in session:
        return redirect('/')
        
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Question ORDER BY id DESC")
    Questions = cursor.fetchall()

    return render_template('Mainpage.html', Questions=Questions)


@app.route('/QuestionsPage', methods=['GET'])
def QuestionsPage():
    if 'username' not in session:
        return redirect('/')
    
    return render_template('AddQuestion.html')


@app.route('/AddQuestion', methods=['POST'])
def AddQuestion():
    if 'username' not in session:
        return redirect('/')
    username = session.get('username')
    question = request.form.get("Question")
    answer = request.form.get("Answer")
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO Question (username, question, answer) VALUES (%s, %s, %s)", (username, question, answer))
        db.commit()

    except Exception as e:
            print(e)
            flash('Something went wrong during INSERT')
    finally:
        cursor.close()
        db.close()

    return redirect('/Mainpage')

@app.route('/AskQuestion', methods=['POST'])
def AskQuestion():
    if 'username' not in session:
        return redirect('/')
    username = session.get('username')
    question = request.form.get("Question")  

    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO Question (username, question) VALUES (%s, %s)", (username, question,))
        db.commit()
    except Exception as e:
        print(e)
        flash('Something went wrong')

    finally:
        cursor.close()
        db.close()

    return redirect('/Mainpage')

@app.route('/Profile', methods=['GET', 'POST'])
def Profile():
    if 'username' not in session:
        return redirect('/')
    username = session.get('username')
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Question WHERE username = %s", (username,))
        comments = cursor.fetchall()
        return render_template('Profile.html', comments=comments)

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        db.close()

@app.route('/DeleteUser', methods=['GET', 'POST'])
def DeleteUser():
    if 'username' not in session:
        return redirect('/')
    username = session.get('username')
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("UPDATE User SET username = 'Deleted_User' WHERE username = %s", (username,))
        db.commit()
        return redirect('/')

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        db.close()


@app.route('/Delete/<int:id>', methods=['POST'])
def DeleteQuestiont(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Question WHERE id = %s", (id,))
    db.commit()
    db.close()
    return redirect('/Mainpage')