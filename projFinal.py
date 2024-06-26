from flask import Flask, request, render_template, redirect, url_for, jsonify
from pymongo import MongoClient, ASCENDING, DESCENDING
#from pymongo.server_api import ServerApi
import os
import json 
import ast
from datetime import datetime, time


uri = "mongodb+srv://rrddamazio:vQ4lM2M1zErxlIFY@bdprojfinalmic.rgwiall.mongodb.net/?retryWrites=true&w=majority&appName=bdProjFinalMic"
cliente = MongoClient(uri, 27017)
'''
try:
    cliente = MongoClient(uri, 27017)
    banco = cliente["banco_proj_final"]
    colecao = banco["alunos"]
    print("Conexão estabelecida com sucesso.")
    for doc in colecao.find():
        print(doc)
except Exception as e:
    print(f"Erro ao conectar com MongoDB: {e}")
'''

banco = cliente["banco_proj_final"]
colecao = banco["alunos"] #colecaoALunos
colecaoDias = banco["aulas"]

#lAlunos = []

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# nome, matricula, curso, foto            

@app.route("/") #mudado
@app.route("/index.html")
def menu():    
    lAlunos = []
    for elem in colecao.find():
        lAlunos.append(elem)
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
    
@app.route("/exclui/<num>.html", methods = ["GET", "POST"]) #mudado
def exclui(num):  
    colecao.delete_one({"matricula" : num})
    return redirect(url_for("menu"))
    
@app.route("/edita/<num>.html", methods = ["GET", "POST"]) #mudado
def edita(num):
    aluno = colecao.find_one({"matricula" : num})

    lEdita = ["", "", ""]
    lEdita[0] = aluno["nome"]
    lEdita[2] = aluno["curso"]

    if request.method == "POST":
        nome = request.form.get("fNome")
        curso = request.form.get("fCurso")
        foto = request.files.get("fFoto")
        
        if foto:
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
            foto.save(foto_path)
            print({"matricula" : num}, {"nome": nome, "matricula" : num, "curso" : curso, "foto" : foto.filename, "presenca" : aluno["presenca"]})
            colecao.update_one({"matricula" : num}, {"$set":{"nome": nome, "matricula" : num, "curso" : curso, "foto" : foto.filename, "presenca" : aluno["presenca"]}})
        else:    
            print({"matricula" : num}, {"nome": nome, "matricula" : num, "curso" : curso, "foto" : None, "presenca" : aluno["presenca"]})
            colecao.update_one({"matricula" : num}, {"$set":{"nome": nome, "matricula" : num, "curso" : curso, "foto" : None, "presenca" : aluno["presenca"]}})

        return redirect(url_for("menu"))
    return render_template("edita.html", lEdita = lEdita, num = num) 

@app.route("/presenca/<num>.html", methods = ["GET", "POST"]) #mudado
def presenca(num):
    #ind = busca(num)
    aluno = colecao.find_one({"matricula" : num})
    lpresenca = aluno["presenca"]
    return render_template("presenca.html", lpresenca = lpresenca) 



@app.route("/criaAula", methods = ["GET", "POST"])
def criaAula():
    colecaoDias.insert_one({"data":"23-05-2024", "hora" : "23:00:00"})
    return "entrou no bd"

@app.route("/passaPresenca", methods = ["GET", "POST"])
def passaPresenca():
    #print("entrei na funcao")
    if request.method == "POST":
        arqJson = request.get_json()
        #arqJson = json.dumps({"data": "23-05-2024", "presencas": [{"matricula": 2210833, "hora": "23:59:05"}, {"matricula": 2210834, "hora": "22:59:05"}]})
        #print(arqJson)
            # {"data : xx-xx-xxxx, "presencas" : [{"matricula" : xxx, "hora" : "xx:xx:xx"}]}
            #{"data": "23/05/2024", "presencas": ["{"matricula": 2210833, "hora": "23:59:05"}, {"matricula": 2210834, "hora": "00:59:05"}]}
        #print("entrei aqui")   
        arqJson = json.loads(arqJson)
        #print(arqJson)
        
        lMatriculas = []
        lDatas = []
        #print(arqJson["data"])
        data = arqJson["data"]
        data= datetime.strptime(arqJson["data"], "%d-%m-%Y")
        data = data.strftime("%d-%m-%Y")
        #print(data)
        #print(arqJson["presencas"])
        for aluno in arqJson["presencas"]:
            lMatriculas.append(aluno["matricula"])
            lDatas.append(datetime.strptime(aluno["hora"], "%H:%M:%S").time())

        for aluno in colecao.find():
            presencaAluno = []
            if int(aluno["matricula"]) in lMatriculas:
                ind = lMatriculas.index(int(aluno["matricula"]))
                horaAluno = lDatas[ind]            
                horaOficial = colecaoDias.find_one({"data" : data})
                horaAula = datetime.strptime(horaOficial["hora"], "%H:%M:%S").time()
                if horaAluno <= horaAula:
                    presencaAluno = [data, "presente", "pontual"]
                else:
                    presencaAluno = [data, "presente", "atrasado"]
            else:
                presencaAluno = [data, "faltou", "-"]
            
            print(aluno["presenca"])
            lAlunoPresenca = [ast.literal_eval(item) for item in aluno["presenca"]]
            print(lAlunoPresenca)
            lAlunoPresenca.append(presencaAluno)
            print(lAlunoPresenca)

            colecao.update_one({"matricula" : aluno["matricula"]}, {"$set":{"presenca" : lAlunoPresenca}})

        return jsonify(arqJson)
    return "não foi"

@app.route("/passaInfo", methods = ["GET", "POST"])
def passaInfo():
    
#if __name__ == '__main__':
app.run(port=5002, debug=False)
