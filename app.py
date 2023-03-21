from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import utils.SQLiteDB as dbHandler
import utils.preprocessing
import os

app = Flask(__name__)


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


@app.route("/login", methods=['POST', 'GET'])
def home():
    dbHandler.createTableIfNotExist()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dbHandler.insertUser(username, password)
        users = dbHandler.retrieveUsers()
        return render_template('index.html', users=users)
    else:
        return render_template('index.html')


@app.route("/user")
def users():
    return dbHandler.retrieveUsers()


@app.route("/register", methods=['POST', 'GET'])
def registerUsers():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        return dbHandler.registerUsers(username, email, password)
    else:
        return render_template('signup.html')


@app.route("/userWithUsername", methods=['POST', 'GET'])
def userWithUsername():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    return dbHandler.retrieveUsersWithUsername(username)


@app.route("/predict", methods=['POST'])
def prediction():
    data = request.get_data()
    print(data)
    # print('Vectorized Input:')
    pred = utils.preprocessing.getPrediction(data)

    if pred[0] == 0:
        print("It seems to be safe input")
        dbresponse = dbHandler.executeQuery(data.decode())
        print("DB Response =", dbresponse)
        return "It seems to be safe input"
    else:
        print("ALERT :::: This can be SQL injection")
        return "ALERT :::: This can be SQL injection"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
