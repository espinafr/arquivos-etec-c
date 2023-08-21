#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, render_template, jsonify, send_file, url_for
import test

# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, static_folder='public', template_folder='views')

# Set the app secret key from the secret environment variables
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FILES'] = {}

def generate_unique_filename(filename):
    ext = filename.rsplit('.', 1)[1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return unique_filename

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', qntd = len(os.listdir(app.config['UPLOAD_FOLDER'])), files=os.listdir(app.config['UPLOAD_FOLDER']))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fileInput' not in request.files:
        return "Nenhum arquivo enviado"

    files = request.files.getlist('fileInput')

    for file in files:
        if file:
            unique_filename = generate_unique_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            app.config['FILES'][unique_filename] = file.filename

    return "Arquivos enviados com sucesso!"

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


@app.route('/remove/<filename>')
def remove_file(filename):
    if filename in app.config['FILES']:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.remove(file_path)
        del app.config['FILES'][filename]
    return redirect(url_for('index'))
  
if __name__ == '__main__':
    app.run(debug=True)