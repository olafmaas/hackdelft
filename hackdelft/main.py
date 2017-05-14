from flask import Flask, jsonify, render_template, url_for
import json

app = Flask(__name__)
app.config.update(SERVER_NAME='127.0.0.1:5000')

articles = {}

with open("doc2vec/output.json") as json_file:
    articles['1'] = json.load(json_file)


with app.app_context():
    url_for('static', filename='style.css')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/articles/<term>')
def get_articles_by(term):
    return jsonify(articles[term])


@app.route('/api/articles/')
def hello_world():
    return jsonify(articles)