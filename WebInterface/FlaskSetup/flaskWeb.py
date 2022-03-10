from __future__ import print_function
from flask import Flask, redirect, url_for, render_template, request, flash, session
from gensim.parsing.preprocessing import remove_stopwords
from nltk.stem import PorterStemmer
from flask_session import Session
from forms import SearchForm
import sys
import string

app = Flask(__name__)
porter = PorterStemmer()
sess = Session()
clickCount = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=['GET', 'POST'])
def lucene():
    global clickCount
    search = SearchForm(request.form)
    search_string = search.data['search']
    if request.method == 'POST':
        if clickCount == 0:
            return redirect('/lucene_output')
        elif clickCount == 2:
            return redirect('/hadoop_output')
    return render_template('lucene.html', form=search)

@app.route("/lucene_results", methods=['POST'])
def lucene_results(search):
    results = []
    search_string = search.data['search']
    #before pre-processing
    #print(search_string, file=sys.stdout)
    #remove punctuation
    search_string = ' '.join(word.strip(string.punctuation) for word in search_string.split())
    search_string = remove_stopwords(search_string)
    search_string = porter.stem(search_string)
    #after pre-processing
    #print(search_string, file=sys.stdout)
    
    if search.data['search'] == '':
        flash('Please enter a search query. Try again?')
        return redirect('/lucene')
    if not results:
        flash('No results found. Try again?')
        return redirect('/lucene')
    else:
        return redirect('/lucene')

@app.route('/lucene_output', methods=['GET'])     
def lucene_output1():
    global clickCount
    clickCount = 2
    return render_template('lucene_output1.html')

@app.route("/hadoop", methods=['GET', 'POST'])
def hadoop():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return hadoop_results(search)

    return render_template("hadoop.html", form=search)

@app.route("/hadoop_results", methods=['GET'])
def hadoop_results(search):
    results = []
    search_string = search.data['search']
    #print(search.data['search'], file=sys.stdout)
    if search.data['search'] == '':
        flash('Please enter a search query. Try again?')
        return redirect('/hadoop')
    if not results:
        flash('No results found. Try again?')
        return redirect('/hadoop')
    else:
        #display results
        return render_template('hadoop_results.html', output=results)

@app.route('/hadoop_output', methods=['GET'])     
def hadoop_output1():   
    return render_template('hadoop_output1.html')

if __name__ == "__main__":
    app.secret_key = 'ooga booga'
    app.config['SESSION_TYPE'] = 'filesystem'

    #sess.init_app(app)

    app.run(debug=True)
