from email.mime import application
import docx
import nltk
import nltk.data
import stop_words
import pymystem3
import pandas as pd
from flask import Flask, render_template
from lemmatizator_stem import lemmatize_all
from Preprocess import preprocess_all
from flask import jsonify
import json
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from Make_graph_from_TM import make_graph_big
import os
import shutil

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
  return render_template('index.html')

	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'File uploaded successfully. You can go back to the previous page.'

@app.route('/uploader2', methods = ['GET', 'POST'])
def upload_file2():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'File uploaded successfully. You can go back to the previous page.'

@app.route('/my-link/')
def my_link():
  print ('I got clicked!')
  lemmatize_all('interviews.txt')

  return 'Your file is lemmatized, now you can go back to the main page and click preprocess.'

@app.route('/my-preprocess/')
def my_preprocess():
  print ('I got clicked!')
  res = preprocess_all('interviews.txt', 'additional_stopwords.txt')
  res = jsonify(res.to_dict(orient='records'))
  return res



@app.route("/graph/", methods = ['POST', 'GET'])
def data():
    if request.method == 'POST':
        method = request.form['Method']
        k = request.form['Topics number']
        make_graph_big(method, k)
        shutil.move("graph.json", "static/data/graph.json")
        return render_template('make_graph.html')


if __name__ == '__main__':
  app.run(debug=True)