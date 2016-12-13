"""Here to keep the linter from being a pain"""
import os
from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
from stacker import format_file
from threading import Thread

ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

APP = Flask(__name__)
APP.config['UPLOAD_FOLDER'] = 'uploads'
APP.config['SECRET_KEY'] = 'a secret key that needs to be replaced'

def allowed_filename(filename):
    """Checks whether a file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@APP.route('/', methods=['GET', 'POST'])
def index():
    """Base url"""
    flash('Hit base URL')
    if request.method == 'POST':
        flash('Post request')
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
            thread = FormatThread(1, 'poo', os.path.join(APP.config['UPLOAD_FOLDER'], filename))
            thread.start()
            # run_formatter.delay(filename, filename.rsplit('.', 1)[0] + '.csv')
    return render_template('index.html')

class FormatThread(Thread):
    def __init__(self, threadID, name, file_name):
        Thread.__init__(self)
        self.name = name
        self.threadID = threadID
        self.file_name = file_name

    def run(self):
        format_file(self.file_name, 'config.yml', 'test.csv')

if __name__ == '__main__':
    if not os.path.isdir('uploads'):
        os.mkdir('uploads')
    APP.run()
