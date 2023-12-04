from flask import Blueprint, render_template, redirect, url_for, request, session, flash
import sqlite3
import datetime
from mine import hashing

board_bp = Blueprint('board', __name__, url_prefix='/board')


@board_bp.route('/board',methods=['GET','POST'])
def board():
    if request.method == 'GET':
        return render_template('board/board.html')
    
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
            return redirect(url_for('board.board_list'))
        else:
            flash('로그인이 필요합니다',category='need_login')
            return redirect(url_for('user.login'))
        

@board_bp.route('/board_list',methods=['GET','POST'])
def board_list():
    #page = request.args.get('page',1,type=int) # page당 10개의 글 목록을 보여줄거임. 일단 이거는 남겨두고.
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM board')
    lists = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('board/board_list.html',lists = lists)


@board_bp.route('/board/<int:id>',methods=['GET','POST'])
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
        elif 'update' in request.form:
            return redirect(url_for('board.board.edit_board'),post['userid']) 
        
    return render_template('board/board_detail.html', post=post)


def delete_board(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM board WHERE id = ?', (id,))
    conn.commit()
    conn.close()


@board_bp.route('/board/<int:id>/edit',methods=['GET','POST'])
def edit_board(id):
    if request.method =='GET':
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM board WHERE id = ?', (id,))
        post = cursor.fetchone()
        conn.close()
        return render_template('/board/board_edit.html',post=post)
       

    else:
        title = request.form['new_title']
        body = request.form['new_body']
        time = datetime.datetime.now()
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('UPDATE board SET title = ?, body = ?, time = ? WHERE id = ?',(title,body,time,id,))
        conn.commit()
        conn.close()

        return redirect(url_for('board.board_list'))

