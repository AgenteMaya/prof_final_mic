from flask import Flask, request, render_template
import os

lAlunos = []

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
@app.route("/index.html")
def menu():
    return render_template("index.html")

@app.route("/cadastramento.html", methods = ["GET", "POST"])
def cadastra():
    if request.method == "POST":
        nome = request.form.get("fNome")
        matricula = request.form.get("fMatricula")
        foto = request.files.get("fFoto")

        if foto:
            # Salvar a foto no diretório de uploads
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
            foto.save(foto_path)
            lAlunos.append([nome, matricula, foto.filename])
        
        else:
            lAlunos.append([nome, matricula, None])
        #print("O aluno é " + nome + " e a matrícula dele é " + matricula + "e a foto dele é " + str(type(foto)))
        #print(lAlunos)
        return render_template("index.html")
    return render_template("cadastramento.html")

@app.route("/ver_lista.html")
def visualiza():
    return render_template("ver_lista.html", lAlunos = lAlunos)

app.run(port=5002, debug=False)

