from flask import Flask, render_template, url_for, redirect, request,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
import yaml
import psycopg2
import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="krishna",
    database="studentGradeBook",
    port="3306"
)
app = Flask(__name__)

# config sql
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
        if 'email' in session:
          return render_template('login.html')
        return render_template('index.html')

@app.route('/viewstudent.html', methods=['GET', 'POST'])
def viewstudent():
    if request.method == 'POST':
        studentname = request.form['studentname']
        cur = conn.cursor()
        cur.execute("SELECT * FROM student WHERE studentname = %s", (studentname,))
        student = cur.fetchall()
        cur.close()
        return render_template('viewstudent.html', student=student)
    return render_template('viewstudent.html')
conn.close()


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pswd = request.form['pswd']
        cur = mysql.connection.cursor()
        cur.execute("SELECT email, pswd FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        if user and pswd == user[1]:
            session['email'] = email
            return redirect(url_for('/'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/registration.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # fetching data
        registerDetails = request.form
        firstname = registerDetails['firstname']
        lastname = registerDetails['lastname']
        email = registerDetails['email']
        phone = registerDetails['phone']
        pswd = registerDetails['pswd']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users(firstname, lastname, email, phone, pswd) VALUES(%s, %s, %s, %s, %s)", (firstname, lastname, email, phone, pswd))
        mysql.connection.commit()
        cursor.close()
        return 'success'
    return render_template('registration.html')

@app.route('/main4.html', methods=['GET','POST'])
def main4():
    return render_template('main4.html')

@app.route('/course.html', methods=['GET','POST'])
def course():
    if request.method == 'POST':
        courses = request.form
        coursename = courses['coursename']
        coursecode = courses['coursecode']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO course(coursename, coursecode) VALUES(%s, %s)", (coursename, coursecode))
        mysql.connection.commit()
        cursor.close()
        return 'Success'
    return render_template('course.html')

@app.route('/result.html', methods=['GET','POST'])
def result():
    return render_template('result.html')

@app.route('/student.html', methods=['GET','POST'])
def student():
    if request.method == 'POST' :
        students = request.form
        studentname = students['studentname']
        studentid = students['studentid']
        course = students['course']
        teacher = students['teacher']
        grade = students['grade']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO student(studentname, studentid, course, teacher, grade) VALUES(%s, %s, %s, %s, %s)",(studentname, studentid, course, teacher, grade))
        mysql.connection.commit()
        cursor.close()
        return 'success'
    return render_template('student.html')


if __name__ == '__main__':
    app.run(debug=True)