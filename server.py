#env/Scripts/activate
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, render_template, send_file, url_for, redirect, session
from werkzeug.exceptions import HTTPException
from datetime import datetime
import sqlite3
import uuid

app = Flask(__name__, static_folder='public', template_folder='views')

app.secret_key = os.environ.get('SECRET')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['USERS'] = {os.environ.get('USER'): os.environ.get('SENHA')}

def generate_unique_filename(filename):
    ext = filename.rsplit('.', 1)[1]
    unique_filename = "{}.{}".format(uuid.uuid4().hex, ext)
    return unique_filename

@app.route('/', methods=['GET'])
def index():
    files = access_db('SELECT unique_filename, original_filename, data FROM files', (), 'f')
    return render_template('index.html', files=files, username=session.get('username'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e

    return render_template("500.html", erro=e), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in app.config['USERS'] and app.config['USERS'][username] == password:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')  

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

def access_db(command: str, params, method: str):
    conn = sqlite3.connect('file_manager.db')
    cursor = conn.cursor()
    cursor.execute(command, params)
    results = cursor.fetchall() if method=='f' else conn.commit()
    conn.close()
    return results

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fileInput' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('fileInput')

    for file in files:
        if file:
            unique_filename = generate_unique_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            access_db('INSERT INTO files (original_filename, unique_filename, data) VALUES (?, ?, ?)', (file.filename, unique_filename, datetime.now().strftime("%d/%m/%Y às %H:%M")), 'c')

    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    name = access_db('SELECT original_filename FROM files WHERE unique_filename == (?) LIMIT 1', (filename,), 'f')
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), download_name=name[0][0], as_attachment=True)


@app.route('/remove/<filename>', methods=['POST'])
def remove_file(filename):
    if 'username' in session and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        access_db('DELETE FROM files WHERE unique_filename = ?', (filename,), 'c')
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.remove(file_path)
    return redirect(url_for('index'))
  
if __name__ == '__main__':
    access_db('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            original_filename TEXT,
            unique_filename TEXT,
            data INTEGER
        )
    ''', (), 'c') # criando a table
    app.run(debug=True)