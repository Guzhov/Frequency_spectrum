import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import numpy as np
import librosa.display

UPLOAD_FOLDER = './files'
ALLOWED_EXTENSIONS = {'mp3'}

if not os.path.isdir("files"):
     os.mkdir("files")
if not os.path.isdir("static"):
     os.mkdir("static")

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def converting_audio_to_pic(filename):
    file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    y, sr = librosa.load(file, sr=44100)
    stft = librosa.stft(y)
    plt.figure(figsize=(14, 5))
    librosa.display.waveplot(np.abs(stft), sr=sr)
    plt.savefig("./static/{}".format(filename.rsplit('.', 1)[0].lower()) + '.png')
    os.remove(file)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            converting_audio_to_pic(filename)
            return render_template("index.html", filename=filename.rsplit('.', 1)[0].lower()+'.png')
    return render_template("index.html")


app.run()