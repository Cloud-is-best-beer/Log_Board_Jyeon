from flask import Flask, session, request, render_template, redirect, url_for, flash
import sqlite3
import datetime
from mine import *
from user import user_bp
from board import board_bp


app = Flask(__name__)
app.secret_key = "1234"

@app.route('/')
def index():
    return render_template("index.html")

app.register_blueprint(user_bp)
app.register_blueprint(board_bp)



if __name__ =='__main__':
    init_db()
    app.run(debug=True)
    
