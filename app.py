from flask import Flask, render_template
import models

app = Flask(__name__)


@app.route('/chord/<fullname>')
def chord_by_name(fullname=None):
    fullname = fullname.replace('sharp', '#')
    return render_template('chord.html',
                           chords=models.get_chords_by_fullname(fullname),
                           fullname=fullname)


@app.route('/')
def index():
    return render_template('index.html',
                           chords=models.get_all_first_chord())

if __name__ == '__main__':
    app.run(debug=True)
