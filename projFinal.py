from flask import Flask, request, render_template
lAlunos = []

app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def menu():
    return render_template("index.html")

@app.route("/cadastramento.html", methods = ["GET", "POST"])
def cadastra():
    if request.method == "POST":
        nome = request.form.get("fNome")
        matricula = request.form.get("fMatricula")
        foto = request.form.get("fFoto")
        lAlunos.append([nome, matricula, foto])
        print("O aluno é " + nome + " e a matrícula dele é " + matricula + "e a foto dele é " + foto)
        return render_template("index.html")
    return render_template("cadastramento.html")

@app.route("/ver_lista.html")
def visualiza():
    return render_template("ver_lista.html")

app.run(port=5002, debug=False)

