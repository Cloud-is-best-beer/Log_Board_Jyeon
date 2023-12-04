from flask import Blueprint,render_template,redirect,url_for,request,flash, session
import sqlite3
from mine import hashing,val_password

user_bp = Blueprint('user',__name__,url_prefix='/user')

@user_bp.route('/signup',methods=['GET','POST'])
def signup():
    if request.method =='GET':
        return render_template('user/signup.html')
    
    else:
        userid = request.form['userid']
        password = request.form['password']
        username = request.form['username']
        password_check = request.form['password_check']
        if val_password(password):
        
            password = hashing(password)
            password_check = hashing(password_check)

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            #id가 이미 존재하는 id 일 때
            if cursor.execute('SELECT (userid) FROM user WHERE userid = ?',(userid,)).fetchone():
                flash('이미 아이디가 존재합니다. 새로운 아이디를 입력해주세요.',category='existed_id')
                conn.close()
                return redirect(url_for('user.signup'))
            else:
                if password == password_check:
                    cursor.execute('INSERT INTO user (userid,password,username) VALUES (?,?,?)' ,(userid,password,username))
                    conn.commit()
                    conn.close()
                    return redirect(url_for('user.login'))
                else:
                    flash('패스워드가 일치하지 않습니다.',category='password_check')
                    return redirect(url_for('user.signup'))
        else:
            flash('비밀번호를 특수기호와 숫자를 포함한 8자 이상으로 설정해주세요.',category='password_pattern')
            return redirect(url_for('user.signup'))

@user_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method =='GET':
        return render_template('user/login.html')
    else:
        userid = request.form['userid']
        password = request.form['password']
        
        password = hashing(password)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT (userid) FROM user WHERE userid = ?',(userid,))

        if cursor.fetchone() == None:
            flash('로그인 정보가 일치하지 않습니다.',category='login_fail')
            return redirect(url_for('user.login'))
        
        else:
            cursor.execute('SELECT (password) FROM user WHERE userid = ?',(userid,))
            pw_confirm = cursor.fetchone()[0]

            if password == pw_confirm:
                session['userid'] = userid
                return redirect(url_for('index'))
            
            else:
                flash('로그인 정보가 일치하지 않습니다.',category='login_fail')
                return redirect(url_for('user.login'))


@user_bp.route('/mypage', methods=['GET','POST'])
def mypage():
    if request.method == 'GET':
        if 'userid' in session:
            userid = session['userid']
            conn = sqlite3.connect('database.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM board WHERE userid = ?',(userid,))
            infos = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return render_template('user/mypage.html',infos=infos)
        
        else:
            return redirect(url_for('user.login'))
    
    else:
        return redirect(url_for('user.unregister'))


@user_bp.route('/unregister',methods=['GET','POST'])
def unregister():
    if request.method == 'GET':
        return render_template('user/unregister.html')
    
    else:
        if 'userid' in session:
            password = request.form['password']
            password = hashing(password)
    
            userid = session['userid']
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT (password) FROM user where userid = ?',(userid,))
            stored_password = cursor.fetchone()
            
            if password == stored_password[0]:
                cursor.execute('DELETE FROM board WHERE userid = ?',(userid,))
                cursor.execute('DELETE FROM user WHERE userid = ?',(userid,))
                conn.commit()
                conn.close()
                session.pop('userid',None)
                session.clear()
                return redirect(url_for('index'))
            else:
                flash('패스워드가 일치하지 않습니다.',category='password_check')
                return redirect(url_for('user.unregister'))
        else:
            redirect(url_for('index'))


@user_bp.route('/logout')
def logout():
    print('before logout : ',session)
    session.pop('userid',None)
    print('after logout : ',session)

    return redirect(url_for('index'))
