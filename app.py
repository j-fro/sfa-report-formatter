"""Here to keep the linter from being a pain"""
import os
from flask import Flask, request, render_template, flash, redirect, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from stacker import FormatThread

ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

APP = Flask(__name__, static_url_path='')
APP.config['UPLOAD_FOLDER'] = 'uploads'
APP.config['SECRET_KEY'] = 'a secret key that needs to be replaced'

def allowed_filename(filename):
    """Checks whether a file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@APP.route('/', methods=['GET', 'POST'])
def index():
    """Base url"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_filename(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
            thread.file_name = os.path.join(APP.config['UPLOAD_FOLDER'], filename)
            thread.start()
            APP.config['FILE_NAME'] = filename.rsplit('.', 1)[0]
        return render_template('uploaded.html')
    else:
        return render_template('index.html')

@APP.route('/poll', methods=['GET'])
def poll():
    """Route for polling the server on the status of the file transformation"""
    return jsonify({
        'status': thread.status,
        'outputFile': thread.output_file
    })

@APP.route('/download', methods=['GET'])
def download():
    """Route to serve the transformed file back to the user"""
    return send_from_directory('', thread.output_file)


if __name__ == '__main__':
    if not os.path.isdir('uploads'):
        os.mkdir('uploads')
    thread = FormatThread(1, 'format thread')
    APP.run()
