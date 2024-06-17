from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient, ASCENDING, DESCENDING
import os

#cliente = MongoClient("localhost", 27017)
#banco = cliente["banco_proj_final"]
#colecao = banco["alunos"]
lAlunos = []

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# nome, matricula, curso, foto
def busca(matricula):
    for (i, elem) in enumerate(lAlunos):
        if elem["matricula"] == matricula:
            return i
    return None

def busca(matricula):
    for (i, elem) in enumerate(lAlunos):
        if elem["matricula"] == matricula:
            return i
    return None


@app.route("/")
@app.route("/index.html")
def menu():    
    print(lAlunos)
    return render_template("index.html", lAlunos = lAlunos)

@app.route("/cadastramento.html", methods = ["GET", "POST"])
def cadastra():
    lCadastro = ["", "", ""]
    if request.method == "POST":
        nome = request.form.get("fNome")
        matricula = request.form.get("fMatricula")
        curso = request.form.get("fCurso")
        foto = request.files.get("fFoto")

        ind = busca(matricula)
        if ind != None:           
            lCadastro[0] = nome
            lCadastro[1] = matricula
            lCadastro[2] = curso
            return render_template("cadastramento.html", error = True, lCadastro = lCadastro)

        elif foto:
            # Salvar a foto no diretório de uploads
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
            foto.save(foto_path)    
            lAlunos.append({"nome":nome, "matricula" : matricula, "curso" : curso, "foto" : foto.filename})        
            #colecao.insert({"nome":nome, "matricula" : matricula, "curso" : curso, "foto" : foto.filename})
        else:
            lAlunos.append({"nome":nome, "matricula" : matricula, "curso" : curso, "foto" : None})
            #colecao.insert({"nome":nome, "matricula" : matricula, "curso" : curso, "foto" : None})
        return redirect(url_for("menu"))
    else:
        return render_template("cadastramento.html", lCadastro = lCadastro)
    
@app.route("/ver_lista.html")
def visualiza():
    return render_template("ver_lista.html", lAlunos = lAlunos)

@app.route("/exclui/<num>.html", methods = ["GET", "POST"])
def exclui(num):    
    
    ind = busca(num)
    lAlunos.pop(ind)
        
    return redirect(url_for("menu"))
    
@app.route("/edita/<num>.html", methods = ["GET", "POST"])
def edita(num):
    print(num)
    ind = busca(num)
    lEdita = ["", "", ""]
    lEdita[0] = lAlunos[ind]["nome"]
    lEdita[2] = lAlunos[ind]["curso"]

    if request.method == "POST":
        nome = request.form.get("fNome")
        curso = request.form.get("fCurso")
        foto = request.files.get("fFoto")

        lAlunos[ind]["nome"] = nome
        lAlunos[ind]["curso"] = curso
        if foto:
            # Salvar a foto no diretório de uploads
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
            foto.save(foto_path)
            lAlunos[ind]["foto"] = foto.filename
        else:    
            lAlunos[ind]["foto"] = None
        return redirect(url_for("menu"))
    return render_template("edita.html", lEdita = lEdita, num = num) 
    #return redirect(url_for("edita"))  
app.run(port=5002, debug=False)

