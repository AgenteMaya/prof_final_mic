from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.server_api import ServerApi
import os



uri = "mongodb+srv://rrddamazio:vQ4lM2M1zErxlIFY@bdprojfinalmic.rgwiall.mongodb.net/?retryWrites=true&w=majority&appName=bdProjFinalMic"
cliente = MongoClient(uri, 27017)
"""
try:
    cliente.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
"""
banco = cliente["banco_proj_final"]
colecao = banco["alunos"]

#lAlunos = []

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# nome, matricula, curso, foto
"""
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
"""

@app.route("/") #mudado
@app.route("/index.html")
def menu():    
    print(colecao.find())
    lAlunos = []
    print(lAlunos)
    for elem in colecao.find():
        print(elem)
        lAlunos.append(elem)
    print(lAlunos)
    return render_template("index.html", lAlunos = lAlunos)

@app.route("/cadastramento.html", methods = ["GET", "POST"]) #mudado
def cadastra():
    lCadastro = ["", "", ""]
    if request.method == "POST":
        nome = request.form.get("fNome")
        matricula = request.form.get("fMatricula")
        curso = request.form.get("fCurso")
        foto = request.files.get("fFoto")

        #ind = busca(matricula)
        ind = colecao.find_one({"matricula" : matricula})
        print(ind)
        print(type(ind))
        if ind != None:           
            lCadastro[0] = nome
            lCadastro[1] = matricula
            lCadastro[2] = curso
            return render_template("cadastramento.html", error = True, lCadastro = lCadastro)

        elif foto:
            # Salvar a foto no diretório de uploads
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
            foto.save(foto_path)    
            #lAlunos.append({"nome":nome, "matricula" : matricula, "curso" : curso, "foto" : foto.filename, "presenca" : []})        
            colecao.insert_one({"nome":nome, "matricula" : matricula, "curso" : curso, "foto" : foto.filename, "presenca" : []})
        else:
            #lAlunos.append({"nome":nome, "matricula" : matricula, "curso" : curso, "foto" : None, "presenca" : []})
            colecao.insert_one({"nome":nome, "matricula" : matricula, "curso" : curso, "foto" : None, "presenca" : []})
        return redirect(url_for("menu"))
    else:
        return render_template("cadastramento.html", lCadastro = lCadastro)
    
"""
@app.route("/ver_lista.html") #mudado
def visualiza():
    print(colecao.find())
    lAlunos = []
    print(lAlunos)
    for elem in colecao.find():
        print(elem)
        lAlunos.append(elem)
    print(lAlunos)

    return render_template("ver_lista.html", lAlunos = lAlunos)
"""

@app.route("/exclui/<num>.html", methods = ["GET", "POST"]) #mudado
def exclui(num):    
    
    #ind = busca(num)
    #lAlunos.pop(ind)
    colecao.delete_one({"matricula" : num})

    return redirect(url_for("menu"))
    
@app.route("/edita/<num>.html", methods = ["GET", "POST"]) #mudado
def edita(num):
    print(num)
    aluno = colecao.find_one({"matricula" : num})

    lEdita = ["", "", ""]
    lEdita[0] = aluno["nome"]
    lEdita[2] = aluno["curso"]

    if request.method == "POST":
        nome = request.form.get("fNome")
        curso = request.form.get("fCurso")
        foto = request.files.get("fFoto")

        
        if foto:
            # Salvar a foto no diretório de uploads
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
            foto.save(foto_path)
            colecao.update_one({"matricula" : num}, {"nome": nome, "matricula" : num, "curso" : curso, "foto" : foto.filename, "presenca" : aluno["presenca"]})
        else:    
            colecao.update_one({"matricula" : num}, {"nome": nome, "matricula" : num, "curso" : curso, "foto" : None, "presenca" : aluno["presenca"]})

        return redirect(url_for("menu"))
    return render_template("edita.html", lEdita = lEdita, num = num) 
    #return redirect(url_for("edita"))  

@app.route("/presenca/<num>.html") #mudado
def presenca(num):
    #ind = busca(num)
    aluno = colecao.find_one({"matricula" : num})
    return render_template("presenca.html", lPresenca = aluno["presenca"]) 

app.run(port=5002, debug=False)
