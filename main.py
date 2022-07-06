from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file
import pymysql
import pyqrcode
import flask
import flask_login
import pandas as pd
import shutil
from datetime import date

import os
app = Flask(__name__)
app.secret_key = 'ajbvfwje;qkfneqjoiio214812-9836'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'admin': {'password': 'admin'}}

GenerateUserNamelist = []
class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@app.route('/loginforgen', methods=['GET', 'POST'])
def loginforgen():
    if flask.request.method == 'GET':
        return render_template('login.html')

    email = flask.request.form['email']
    if email in users and flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return render_template('QrGenerate.html')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('login.html')


def getConnection():
    return pymysql.connect(
        host='localhost',
        db='qrcode_tog',
        user='root',
        password='',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )


def showUser():
    connection = getConnection()
    sql = "SELECT * FROM user ORDER BY Date, Time DESC"
    cursor = connection.cursor()
    cursor.execute(sql)
    user = cursor.fetchall()
    return user


@app.route('/')
def showuser():
    user = showUser()
    connection = getConnection()
    cursor = connection.cursor()
    re = f"SELECT Date,SUM(Van01) Van01,SUM(Van02) Van02,SUM(Van03) Van03,SUM(Van04) Van04,SUM(Van05) Van05,SUM(Van06) Van06,SUM(Van07) Van07,SUM(Van08) Van08,SUM(Van09) Van09,SUM(Van10) Van10,SUM(Bus01) Bus01,SUM(Bus02) Bus02,SUM(Bus03) Bus03,SUM(Bus04) Bus04,SUM(Bus05) Bus05 FROM result  GROUP BY Date"
    cursor = connection.cursor()
    cursor.execute(re)
    res = cursor.fetchall()
    return render_template('dashboard.html', user=user, res=res)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return showuser()


@app.route('/table')
def table():
    user = showUser()
    return render_template('table.html', user=user)


@app.route('/test01')
def test01():
    return render_template('test.html')


@app.route('/tablesearch', methods=['GET', 'POST'])
def tablesearch():
    startday = request.args.get('startdaterange')
    stopday = request.args.get('stopdaterange')
    connection = getConnection()
    u = f"SELECT * FROM user WHERE date BETWEEN '{startday}' AND '{stopday}' ORDER BY Date,user.time DESC"
    cursor = connection.cursor()
    cursor.execute(u)
    user = cursor.fetchall()
    return render_template('table.html', user=user)
#


@app.route('/chart')
def chart():
    connection = getConnection()
    cursor = connection.cursor()
    re = f"SELECT Date,SUM(Van01) Van01,SUM(Van02) Van02,SUM(Van03) Van03,SUM(Van04) Van04,SUM(Van05) Van05,SUM(Van06) Van06,SUM(Van07) Van07,SUM(Van08) Van08,SUM(Van09) Van09,SUM(Van10) Van10,SUM(Bus01) Bus01,SUM(Bus02) Bus02,SUM(Bus03) Bus03,SUM(Bus04) Bus04,SUM(Bus05) Bus05 FROM result  GROUP BY Date"
    cursor = connection.cursor()
    cursor.execute(re)
    res = cursor.fetchall()
    return render_template('charts.html', res=res)


@app.route('/chart_DWMY', methods=['GET', 'POST'])
def chart_DWMY():
    times = request.args.get('type')
    print(times)
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    date_times = date_time.strftime("%Y-%m-%d,%H:%M:%S")
    day, time = date_times.split(',')
    y, m, d = day.split('-')
    connection = getConnection()
    cursor = connection.cursor()
    c = ''
    print(y)
    if times == 'All':  # pass
        c = "SELECT Date,SUM(Van01) Van01,SUM(Van02) Van02,SUM(Van03) Van03,SUM(Van04) Van04,SUM(Van05) Van05,SUM(Van06) Van06,SUM(Van07) Van07,SUM(Van08) Van08,SUM(Van09) Van09,SUM(Van10) Van10,SUM(Bus01) Bus01,SUM(Bus02) Bus02,SUM(Bus03) Bus03,SUM(Bus04) Bus04,SUM(Bus05) Bus05 FROM result  GROUP BY Date"
    if times == 'Daily':
        c = f"SELECT date_format(date, "'"%d/%m"'") Date,SUM(Van01) Van01,SUM(Van02) Van02,SUM(Van03) Van03,SUM(Van04) Van04,SUM(Van05) Van05,SUM(Van06) Van06,SUM(Van07) Van07,SUM(Van08) Van08,SUM(Van09) Van09,SUM(Van10) Van10,SUM(Bus01) Bus01,SUM(Bus02) Bus02,SUM(Bus03) Bus03,SUM(Bus04) Bus04,SUM(Bus05) Bus05 FROM result  where year(Date) LIKE year(CURDATE()) GROUP BY Day(Date)"
        print(c)
    if times == 'Monthly':  # pass
        c = f"SELECT date_format(date, "'"%m-%y"'") Date,SUM(Van01) Van01,SUM(Van02) Van02,SUM(Van03) Van03,SUM(Van04) Van04,SUM(Van05) Van05,SUM(Van06) Van06,SUM(Van07) Van07,SUM(Van08) Van08,SUM(Van09) Van09,SUM(Van10) Van10,SUM(Bus01) Bus01,SUM(Bus02) Bus02,SUM(Bus03) Bus03,SUM(Bus04) Bus04,SUM(Bus05) Bus05 FROM result where year(Date) LIKE year(CURDATE()) GROUP BY month(Date)"
        print(c)
    if times == 'Yearly':  # pass
        c = "SELECT year(Date) Date,SUM(Van01) Van01,SUM(Van02) Van02,SUM(Van03) Van03,SUM(Van04) Van04,SUM(Van05) Van05,SUM(Van06) Van06,SUM(Van07) Van07,SUM(Van08) Van08,SUM(Van09) Van09,SUM(Van10) Van10,SUM(Bus01) Bus01,SUM(Bus02) Bus02,SUM(Bus03) Bus03,SUM(Bus04) Bus04,SUM(Bus05) Bus05 FROM result GROUP BY Year(Date)"
    if times == 'Weekly':  # pass
        c = f"SELECT date_format(date, "'"wk%U"'") Date, SUM(Van01) Van01,SUM(Van02) Van02,SUM(Van03) Van03,SUM(Van04) Van04,SUM(Van05) Van05,SUM(Van06) Van06,SUM(Van07) Van07,SUM(Van08) Van08,SUM(Van09) Van09,SUM(Van10) Van10,SUM(Bus01) Bus01,SUM(Bus02) Bus02,SUM(Bus03) Bus03,SUM(Bus04) Bus04,SUM(Bus05) Bus05 FROM result GROUP BY YEARWEEK(Date, 2) ORDER BY YEARWEEK(Date, 2)"

    cursor = connection.cursor()
    cursor.execute(c)
    res = cursor.fetchall()
    return render_template('charts.html', res=res)


@app.route('/chartsearch', methods=['GET', 'POST'])
def chartsearch():
    startday = request.args.get('startdaterange')
    stopday = request.args.get('stopdaterange')
    connection = getConnection()
    cursor = connection.cursor()
    re = f"SELECT * FROM result WHERE date BETWEEN '{startday}' AND '{stopday}' GROUP BY Date"
    cursor = connection.cursor()
    cursor.execute(re)
    res = cursor.fetchall()
    return render_template('charts.html', res=res)


@app.route('/table_DWMY', methods=['GET', 'POST'])
def table_DWMY():
    times = request.args.get('type')
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    date_times = date_time.strftime("%Y-%m-%d,%H:%M:%S")
    day, time = date_times.split(',')
    y, m, d = day.split('-')
    connection = getConnection()
    cursor = connection.cursor()
    u = ''

    if times == 'All':
        u = "SELECT * FROM user ORDER BY Date,user.time DESC"
    elif times == 'Daily':
        u = f"SELECT * FROM user WHERE Date LIKE '%{y}-{m}-{d}' ORDER BY Date,user.time DESC"
    elif times == 'Monthly':
        u = f"SELECT * FROM user WHERE Date LIKE '%{y}-{m}-%' ORDER BY Date,user.time DESC"
    elif times == 'Yearly':
        u = f"SELECT * FROM user WHERE Date LIKE '{y}%' ORDER BY Date,user.time DESC"
    elif times == 'Weekly':
        u = f"SELECT * FROM user WHERE week(Date) = week(now()) ORDER BY Date,user.time DESC"

    cursor = connection.cursor()
    cursor.execute(u)
    user = cursor.fetchall()
    return render_template('table.html', user=user)


@app.route('/home', methods=['GET', 'POST'])
def login():
    username = request.args.get('username')
    print(username)
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    date_times = date_time.strftime("%Y-%m-%d,%H:%M:%S")
    day, time = date_times.split(',')
    return render_template('index.html', username=username, day=day, time=time)


@app.route('/savecontainer', methods=['GET', 'POST'])
def savecontainer():
    username = request.args.get('username')
    day = request.args.get('day')
    time = request.args.get('time')
    container = request.args.get('container')
    print(container, username, day, time)
    connection = getConnection()
    Van01, Van02, Van03, Van04, Van05, Van06, Van07, Van08, Van09, Van10, Bus01, Bus02, Bus03, Bus04, Bus05 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    if username != "":
        if username != "None":
            if container == 'Van01':
                Van01 = 1
            elif container == 'Van02':
                Van02 = 1
            elif container == 'Van03':
                Van03 = 1
            elif container == 'Van04':
                Van04 = 1
            elif container == 'Van05':
                Van05 = 1
            elif container == 'Van06':
                Van06 = 1
            elif container == 'Van07':
                Van07 = 1
            elif container == 'Van08':
                Van08 = 1
            elif container == 'Van09':
                Van09 = 1
            elif container == 'Van10':
                Van10 = 1
            elif container == 'Bus01':
                Bus01 = 1
            elif container == 'Bus02':
                Bus02 = 1
            elif container == 'Bus03':
                Bus03 = 1
            elif container == 'Bus04':
                Bus04 = 1
            elif container == 'Bus05':
                Bus05 = 1
            sql = "INSERT INTO user(Username, Container, Time ,Date) VALUES('%s', '%s', '%s', '%s')" % (username,
                                                                                                        container, time, day)
            ins = "INSERT  INTO result(Date,Van01,Van02,Van03,Van04,Van05,Van06,Van07,Van08,Van09,Van10,Bus01,Bus02,Bus03,Bus04,Bus05) VALUES('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                day, Van01, Van02, Van03, Van04, Van05, Van06, Van07, Van08, Van09, Van10, Bus01, Bus02, Bus03, Bus04, Bus05)
            cursor = connection.cursor()
            cursor.execute(sql)
            cursor.execute(ins)
            connection.commit()

    return redirect(url_for('resultsave'))


@app.route('/resultsave')
def resultsave():
    a = request.url
    print(a)
    print("tab closed")
    return render_template('index2.html')

def choicesave(username,name,department,factory):
    if factory == 'TOG':
        connection = getConnection()
        sql = f"INSERT INTO employee(user, name, address) VALUES('%s', '%s', '%s')" % (username,name, department)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return "TOG"
    
    if factory == 'TOC':
        connection = getConnection()
        sql = f"INSERT INTO employeetoc(user, name, address) VALUES('%s', '%s', '%s')" % (username,name, department)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return "TOC"
    



@app.route('/genqr', methods=['GET', 'POST'])
def genqr():
    name = request.args.get('name')
    username = request.args.get('username')
    department = request.args.get('department')
    factory = request.args.get('factory')
    dir = 'qrcode/test'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
        
    print(GenerateUserNamelist)
    if username not in GenerateUserNamelist:
        GenerateUserNamelist.append(username)
        save = choicesave(username,name,department,factory)
        print(save)
        print("ไม่มีในระบบ")
        url = "http://localhost:5000/"
        qr = pyqrcode.create(url+"/home?username="+username)
        qrcode = qr.png("qrcode.png", scale=6)
        return send_file("qrcode.png", mimetype='image/png', attachment_filename=f'{username}.png', as_attachment=True)
    
    return redirect('/protected')


@app.route('/long')
def main():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    UPLOAD_FOLDER = "./"
    if request.method == 'POST':
        f = request.files['file']
        factoryexcel = request.args.get('factoryexcel')
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        df = pd.read_excel(f.filename, usecols="A,B,C")
        print(len(df))        

        dir = 'qrcode/qrcode'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        for i in range(len(df)):
            username = df['รหัสพนักงาน'][i]
            name = df['ชื่อ-สกุล'][i]
            agency = df['แผนก'][i]
            if username not in GenerateUserNamelist:
                GenerateUserNamelist.append(username)
                connection = getConnection()
                sql =''
                if factoryexcel == 'TOG':
                    sql = f"INSERT INTO employee(user, name, address) VALUES('%s', '%s', '%s')" % (username,
                     name, agency)
                if factoryexcel == 'TOC':
                    sql = f"INSERT INTO employeetoc(user, name, address) VALUES('%s', '%s', '%s')" % (username,
                     name, agency)
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()
                url = "http://203.146.249.6/"
                qr = pyqrcode.create(url+"/home?username="+str(username))
                qrcode = qr.png("qrcode/test/"+str(username)+".png", scale=6)
        today = date.today()
        day = today.strftime("%d %m %Y")
        shutil.make_archive('qrcode/qrcode', 'zip', 'qrcode/test')
        
        print("generate finish")

        return send_file("qrcode/qrcode.zip", mimetype='application/zip', attachment_filename=f'{day}.rar', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host="203.146.249.6", port=80)
