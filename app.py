"""Here to keep the linter from being a pain"""
import os
from threading import Thread
from flask import Flask, request, render_template, flash, redirect, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from stacker import FormatThread

ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = 'uploads'

def allowed_filename(filename):
    """Checks whether a file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    """Base url"""
    if request.method == 'POST':
        clear_uploads(app.config['UPLOAD_FOLDER'])
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_filename(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            thread.file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            thread.thread = Thread(target=thread.run)
            thread.thread.start()
            app.config['FILE_NAME'] = filename.rsplit('.', 1)[0]
        return render_template('uploaded.html')
    else:
        return render_template('index.html')

@app.route('/poll', methods=['GET'])
def poll():
    """Route for polling the server on the status of the file transformation"""
    return jsonify({
        'status': thread.status,
        'outputFile': thread.output_file
    })

@app.route('/download', methods=['GET'])
def download():
    """Route to serve the transformed file back to the user"""
    return send_from_directory('', thread.output_file)

def clear_uploads(upload_dir):
    for file_name in os.listdir(upload_dir):
        os.remove(os.path.join(upload_dir, file_name))

if __name__ == '__main__':
    if not os.path.isdir('uploads'):
        os.mkdir('uploads')
    thread = FormatThread()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port)
    app.run()
