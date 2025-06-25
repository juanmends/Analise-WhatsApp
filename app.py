from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
import os

import analise
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename.endswith('.txt'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(filepath)

            analise.analisar_conversa(filepath)

            return redirect(url_for('showresultado'))
    return render_template('upload.html')

@app.route('/resultado')
def showresultado():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    response = make_response(html)
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route('/emoji')
def showemoji():
    return send_from_directory('static/graficos', 'emoji.html')

@app.route('/dias')
def showdias():
    return send_from_directory('static/graficos', 'dias.html')

@app.route('/datas')
def showdatas():
    return send_from_directory('static/graficos', 'datas.html')

if __name__ == '__main__':
    app.run()