from flask import Flask, request, render_template, abort
from jinja2 import TemplateNotFound

app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def menu():
    return render_template("index.html")

@app.route('/cadastramento.html')
def cadastra():
    return render_template("cadastramento.html")

@app.route('/ver_lista.html')
def visualiza():
    return render_template("ver_lista.html")
    

app.run(port=5002, debug=False)

