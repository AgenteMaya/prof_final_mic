from flask import Flask, request, render_template, redirect, url_for
import os

lAlunos = []

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def busca(matricula):
    for (i, elem) in enumerate(lAlunos):
        if elem[1] == matricula:
            return i
    return None


@app.route("/")
@app.route("/index.html")
def menu():
    print("passei aqui")    
    
    return render_template("index.html", lAlunos = lAlunos)

@app.route("/cadastramento.html", methods = ["GET", "POST"])
def cadastra():
    if request.method == "POST":
        nome = request.form.get("fNome")
        matricula = request.form.get("fMatricula")
        curso = request.form.get("fCurso")
        foto = request.files.get("fFoto")

        ind = busca(matricula)
        if ind != None:           
           return render_template("cadastramento.html", error = True)

        if foto:
            # Salvar a foto no diretório de uploads
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
            foto.save(foto_path)
            lAlunos.append([nome, matricula,curso, foto.filename])
        
        else:
            lAlunos.append([nome, matricula, curso, None])
        #print("O aluno é " + nome + " e a matrícula dele é " + matricula + "e a foto dele é " + str(type(foto)))
        #print(lAlunos)
        return redirect(url_for("menu"))
    else:
        return render_template("cadastramento.html")
    
@app.route("/ver_lista.html")
def visualiza():
    return render_template("ver_lista.html", lAlunos = lAlunos)


app.run(port=5002, debug=False)

