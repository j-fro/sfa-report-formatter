"""Here to keep the linter from being a pain"""
import os
from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
from celery import Celery
from stacker import format_file

ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

APP = Flask(__name__)
APP.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
APP.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
APP.config['UPLOAD_FOLDER'] = 'uploads'
APP.config['SECRET_KEY'] = 'a secret key that needs to be replaced'

CELERY = Celery(APP.name, broker=APP.config['CELERY_BROKER_URL'])
CELERY.conf.update(APP.config)

def allowed_filename(filename):
    """Checks whether a file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@CELERY.task
def run_formatter(orig_filename, new_filename):
    """Formats a file and outputs a new csv"""
    flash(orig_filename, new_filename)
    format_file(orig_filename, 'config.yml', new_filename)

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
            run_formatter.delay(filename, filename.rsplit('.', 1)[0] + '.csv')
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.isdir('uploads'):
        os.mkdir('uploads')
    APP.run()
