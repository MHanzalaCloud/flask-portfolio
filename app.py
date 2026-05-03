from flask import Flask, request, redirect
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
    output = '<h1>Users</h1>'
    output += '<a href="/add">Add New User</a><br><br>'
    for user in users:
        output += f'<p>{user[1]} - {user[2]} '
        output += f'<a href="/edit/{user[0]}">Edit</a> '
        output += f'<a href="/delete/{user[0]}">Delete</a></p>'
    return output

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, role) VALUES (%s, %s)", (username, role))
        mysql.connection.commit()
        cursor.close()
        return redirect('/')
    return '''
        <h1>Add User</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Username"><br><br>
            <input type="text" name="role" placeholder="Role"><br><br>
            <button type="submit">Add User</button>
        </form>
    '''

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        cursor.execute("UPDATE users SET username=%s, role=%s WHERE id=%s", (username, role, id))
        mysql.connection.commit()
        cursor.close()
        return redirect('/')
    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    user = cursor.fetchone()
    cursor.close()
    return f'''
        <h1>Edit User</h1>
        <form method="POST">
            <input type="text" name="username" value="{user[1]}"><br><br>
            <input type="text" name="role" value="{user[2]}"><br><br>
            <button type="submit">Update</button>
        </form>
    '''

@app.route('/delete/<int:id>')
def delete_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
