from flask import Flask, request, render_template, redirect, url_for
import os

lAlunos = []

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# nome, matricula, curso, foto
def busca(matricula):
    for (i, elem) in enumerate(lAlunos):
        if elem[1] == matricula:
            return i
    return None


@app.route("/")
@app.route("/index.html")
def menu():    
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
            lAlunos.append([nome, matricula,curso, foto.filename])        
        else:
            lAlunos.append([nome, matricula, curso, None])
        return redirect(url_for("menu"))
    else:
        return render_template("cadastramento.html", lCadastro = lCadastro)
    
@app.route("/ver_lista.html")
def visualiza():
    return render_template("ver_lista.html", lAlunos = lAlunos)

@app.route("/exclui.html", methods = ["GET", "POST"])
def exclui():    
    sExclui = ""
    if request.method == "POST":
        matricula = request.form.get("fMatricula")
        ind = busca(matricula)
        if ind == None:
            return render_template("exclui.html", error = True, sExcluiu = sExclui)
        
        lAlunos.pop(ind)
        return redirect(url_for("menu"))
    else:
        return render_template("exclui.html", sExcluiu = sExclui)
    
@app.route("/edita.html", methods = ["GET", "POST"])
def edita():
    lEdita = ["", "", ""]
    if request.method == "POST":
        nome = request.form.get("fNome")
        matricula = request.form.get("fMatricula")
        curso = request.form.get("fCurso")
        foto = request.files.get("fFoto")

        ind = busca(matricula)
        if ind == None:
            lEdita[0] = nome
            lEdita[1] = matricula
            lEdita[2] = curso              
            return render_template("edita.html", error = True, lEdita = lEdita)
        elif foto:
            # Salvar a foto no diretório de uploads
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
            foto.save(foto_path)
            lAlunos[ind][3] = foto.filename
        else:    
            lAlunos[ind][3] = None
        lAlunos[ind][0] = nome
        lAlunos[ind][2] = curso
        return redirect(url_for("menu"))
    else:
        return render_template("edita.html", lEdita = lEdita)




        




app.run(port=5002, debug=False)

