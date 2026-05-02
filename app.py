from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'flaskuser'
app.config['MYSQL_PASSWORD'] = 'StrongPass123!'
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)

@app.route('/')
def home():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    output = '<h1>Users from Database</h1>'
    for user in users:
        output += f'<p>{user[1]} - {user[2]}</p>'
    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
