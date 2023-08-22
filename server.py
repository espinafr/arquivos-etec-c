#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, render_template, jsonify, send_file, url_for, redirect, session
import uuid

# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, static_folder='public', template_folder='views')

# Set the app secret key from the secret environment variables
app.secret_key = os.environ.get('SECRET')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['USERS'] = {os.environ.get('USER'): os.environ.get('SENHA')}

#def generate_unique_filename(filename):
#   ext = filename.rsplit('.', 1)[1]
#    unique_filename = "{}.{}".format(uuid.uuid4().hex, ext)
#    return unique_filename

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', files=os.listdir(app.config['UPLOAD_FOLDER']),)

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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fileInput' not in request.files:
        return "Nenhum arquivo enviado"

    files = request.files.getlist('fileInput')

    for file in files:
        if file:
            #unique_filename = generate_unique_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename) #unique_filename
            file.save(file_path)

    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


@app.route('/remove/<filename>', methods=['POST'])
def remove_file(filename):
    senha = request.form.get('senha')
    if 'username' in session and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.remove(file_path)
    return redirect(url_for('index'))
  
if __name__ == '__main__':
    app.run(debug=True)