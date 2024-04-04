from flask import Flask, render_template
from lemmatizator_stem import lemmatize_all, lemmatize_all_eng
from Preprocess import preprocess_all
from flask import jsonify
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from Make_graph_from_TM import make_graph_big, translate_to_eng
import shutil
import pickle
import pandas as pd
from googletrans import Translator
import os
translator = Translator()
import nltk


nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('omw-1.4')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
  return render_template('index.html')

# Handle the GET request for node information
@app.route('/node-info/<node_name>', methods=['GET'])
def get_node_info(node_name):
    # Retrieve information based on the node_id (replace with your logic)
    with open('x_train_rus_alligned', 'rb') as file:
      text = pickle.load(file)
    inds = [i for i in range(len(text)) if node_name in text[i].split()]
    df = pd.read_csv('df_raw.csv')
    print(df.head())
    # output = '<br>'.join([])
    output = '<br>'.join(['Document {}: {}'.format(l, df['paragraphs'].values[l]) for l in inds])
    node_info = 'Node: <b>{node_id}</b><br>Output:<br>{output}'.format(node_id=node_name, output=output) # get_node_information(node_id)
    return node_info

	
# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'File uploaded successfully'

# @app.route('/uploader2', methods = ['GET', 'POST'])
# def upload_file2():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'File uploaded successfully'


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = secure_filename(file.filename)
        file.save(filename)
        return 'File uploaded successfully.'


@app.route('/my-link/')
def my_link():
    include_interviewer = request.args.get('includeInterviewer') == 'true'

    with open('text.txt') as f:
        first_line = f.readline()
    result = translator.translate(first_line)
    lang = result.src
    if lang == 'ru':
        lemmatize_all('text.txt', include_interviewer)
    elif lang == 'en':
        lemmatize_all_eng('text.txt', include_interviewer)

    return 'Your file is lemmatized, now you can click preprocess.'

@app.route('/my-preprocess/')
def my_preprocess():
    print('I got clicked!')
    # Assuming preprocess_all returns a pandas DataFrame or similar
    data = preprocess_all('text.txt', 'additional_stopwords.txt').to_dict(orient='records')
    return render_template('preprocess_table.html', data=data)

@app.route("/graph/", methods = ['POST', 'GET'])
def data():
    if request.method == 'POST':
        method = request.form['Method']
        k = request.form['Topics number']
        num_keywords = request.form['KeywordsNumber']
        clear_nodes, clear_links = make_graph_big(method, k, int(num_keywords))
        shutil.move("graph.json", "static/data/graph.json")
        with open(r'clear_nodes', 'w') as fp:
          for item in clear_nodes: fp.write("%s\n" % item)
          print('Done for clear_nodes')
        with open(r'clear_links', 'w') as fp:
          for item in clear_links: fp.write("%s\n" % item)
          print('Done for clear_links')
        return render_template('make_graph.html')

@app.route('/my-translate/')
def my_translate():
  import ast
  clear_nodes = []
  clear_links = []
  with open(r'clear_nodes', 'r') as fp:
      for line in fp:
          x = line[:-1]
          clear_nodes.append(ast.literal_eval(x))
  with open(r'clear_links', 'r') as fp:
      for line in fp:
          x = line[:-1]
          clear_links.append(ast.literal_eval(x))  
  translate_to_eng(clear_nodes, clear_links)
  shutil.move("graph.json", "static/data/graph.json")
  return render_template('make_graph.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080)) # Default to 8080 if PORT not set
    app.run(debug=False, host='0.0.0.0', port=port)

