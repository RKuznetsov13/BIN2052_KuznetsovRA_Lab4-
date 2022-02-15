import requests
from flask import Flask, render_template, request
import psycopg2

# Создаем приложение
app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="postgres",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if str(username) == '' or str(password) == '':
        return render_template('login.html', login_error='Invalid username or password')
    else:
        cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
        records = list(cursor.fetchall())
        if len(records) == 0:
            return render_template('login.html', login_error='User does not exist')
        else:
            return render_template('account.html', full_name=records[0][1], name=username, passwd=password)


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')
