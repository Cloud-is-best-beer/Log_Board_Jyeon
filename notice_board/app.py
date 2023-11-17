from flask import Flask, session, request, render_template, redirect, url_for, flash
import sqlite3
import datetime
from mine import *

app = Flask(__name__)
app.secret_key = "1234"

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method =='GET':
        return render_template('signup.html')
    
    else:
        userid = request.form['userid']
        password = request.form['password']
        username = request.form['username']
        password_check = request.form['password_check']

        password = hashing(password)
        password_check = hashing(password_check)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #id가 이미 존재하는 id 일 때
        if cursor.execute('SELECT (userid) FROM user WHERE userid = ?',(userid,)).fetchone():
            flash('이미 아이디가 존재합니다. 새로운 아이디를 입력해주세요.',category='existed_id')
            conn.close()
            return redirect(url_for('signup'))
        else:
            if password == password_check:
                cursor.execute('INSERT INTO user (userid,password,username) VALUES (?,?,?)' ,(userid,password,username))
                conn.commit()
                conn.close()
                return redirect(url_for('login'))
            else:
                flash('패스워드가 일치하지 않습니다.',category='password_check')
                return redirect(url_for('signup'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    else:
        userid = request.form['userid']
        password = request.form['password']
        
        password = hashing(password)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT (userid) FROM user WHERE userid = ?',(userid,))

        if cursor.fetchone() == None:
            flash('로그인 정보가 일치하지 않습니다.',category='login_fail')
            return redirect(url_for('login'))
        
        else:
            cursor.execute('SELECT (password) FROM user WHERE userid = ?',(userid,))
            pw_confirm = cursor.fetchone()[0]

            if password == pw_confirm:
                session['userid'] = userid
                return redirect(url_for('index'))
            
            else:
                flash('로그인 정보가 일치하지 않습니다.',category='login_fail')
                return redirect(url_for('login'))
        

@app.route('/board_list',methods=['GET','POST'])
def board_list():
    #page = request.args.get('page',1,type=int) # page당 10개의 글 목록을 보여줄거임.
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM board')
    lists = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('board_list.html',lists = lists)


@app.route('/board',methods=['GET','POST'])
def board():
    if request.method == 'GET':
        return render_template('board.html')
    
    else:
        if 'userid' in session:
            title = request.form['title']
            body = request.form['body']
            time = datetime.datetime.now()
            userid = session['userid']
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO board (title,body,time,userid) VALUES (?,?,?,?)',(title,body,time,userid))
            
            conn.commit()
            conn.close()
            return redirect(url_for('board_list'))
        else:
            flash('로그인이 필요합니다',category='need_login')
            return redirect(url_for('login'))


@app.route('/board/<int:id>',methods=['GET','POST'])
def board_detail(id):
    if request.method =='GET':    
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM board WHERE id = ?', (id,))
        post = cursor.fetchone()
        conn.close()

        if post is None:
            return "게시물이 존재하지 않습니다."
    
    else:
        if 'delete' in request.form:
            delete_board(id)
            return redirect(url_for('index'))
        
    return render_template('board_detail.html', post=post)


def delete_board(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM board WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def edit_board():
    pass

@app.route('/mypage', methods=['GET','POST'])
def mypage():
    if request.method == 'GET':
        if 'userid' in session:
            userid = session['userid']
            conn = sqlite3.connect('database.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM board WHERE userid = ?',(userid,))
            my_info = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return render_template('mypage.html',my_info = my_info)
        
        else:
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('userid',None)
    return redirect(url_for('index'))



if __name__ =='__main__':
    init_db()
    app.run(debug=True)
    

    #conn.row_factory = sqlite3.Row 이런식으로 하면
    #딕셔너리 형태로 가져올 수 있음.