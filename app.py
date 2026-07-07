from flask import Flask, render_template, session, redirect, url_for, request

from models.produto import Produto, db

from config import Config

import urllib.parse

from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config.from_object(Config)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "img")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db.init_app(app)

@app.route("/limpar-carrinho")
def limpar_carrinho():
    session["carrinho"] = []
    session.modified = True
    return redirect(url_for("carrinho"))

@app.route("/admin/editar/<int:id>", methods=["GET", "POST"])
def editar_produto(id):
    if not session.get("admin_logado"):
        return redirect(url_for("login"))
    
    produto = Produto.query.get(id)

    if not produto:
        return "Produto não encontrado!"

    if request.method == "POST":
        produto.nome = request.form["nome"]
        produto.descricao = request.form["descricao"]
        produto.preco = float(request.form["preco"])
        produto.imagem = request.form["imagem"]

        db.session.commit()

        return redirect(url_for("admin"))

    return render_template("editar_produto.html", produto=produto)
 
@app.route("/")
def inicio():
     produtos = Produto.query.all()
    
     return render_template("index.html", produtos=produtos)


@app.route("/carrinho")
def carrinho():
    carrinho = session.get("carrinho", [])
    total = 0

    for produto in carrinho:
        total += produto["preco"]

    return render_template("carrinho.html", carrinho=carrinho, total=total)

@app.route("/adicionar/<int:id>")
def adicionar(id):
    produto = Produto.query.get(id)

    if produto:
        if "carrinho" not in session:
            session["carrinho"] = []

        item = {
    "id": produto.id,
    "nome": produto.nome,
    "descricao": produto.descricao,
    "preco": produto.preco,
    "imagem": produto.imagem
}

        session["carrinho"].append(item)
        session.modified = True

        return redirect(url_for("carrinho"))

    return "Produto não encontrado!"

@app.route("/admin/excluir/<int:id>")
def excluir_produto(id):
    if not session.get("admin_logado"):
        return redirect(url_for("login"))
    
    produto = Produto.query.get(id)

    if produto:
        db.session.delete(produto)
        db.session.commit()

    return redirect(url_for("admin"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == "admin" and senha == "1234":
            session["admin_logado"] = True
            return redirect(url_for("admin"))

        return "Usuário ou senha incorretos!"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin_logado", None)
    return redirect(url_for("login"))
 
@app.route("/remover/<int:id>")
def remover(id):
    carrinho = session.get("carrinho", [])

    for produto in carrinho:
        if produto["id"] == id:
            carrinho.remove(produto)
            break

    session["carrinho"] = carrinho
    session.modified = True

    return redirect(url_for("carrinho"))

@app.route("/finalizar")
def finalizar():
    carrinho = session.get("carrinho", [])

    mensagem = "Olá! Gostaria de fazer o seguinte pedido:%0A%0A"
    total = 0

    for produto in carrinho:
        mensagem += f"- {produto['nome']} - R$ {produto['preco']:.2f}%0A"
        total += produto["preco"]

    mensagem += f"%0A Total: R$ {total:.2f}"

    mensagem = urllib.parse.quote(mensagem)

    numero = "5585987967624"

    return redirect(f"https://wa.me/message/HDQBGH3SCFO5H1?text={mensagem}")

@app.route("/produto/<int:id>")
def produto(id):
    produto = Produto.query.get(id)
    if produto:
        return render_template("produto.html", produto=produto)

@app.route("/admin")
def admin():
    if not session.get("admin_logado"):
        return redirect(url_for("login"))
    
    produtos = Produto.query.all()
    return render_template("admin.html", produtos=produtos)

@app.route("/admin/novo-produto", methods=["POST"])
def novo_produto():
    if not session.get("admin_logado"):
        return redirect(url_for("login"))

    nome = request.form["nome"]
    descricao = request.form["descricao"]
    preco = float(request.form["preco"])

    arquivo = request.files["imagem"]

    if arquivo and arquivo.filename != "":
        nome_imagem = secure_filename(arquivo.filename)

        caminho = os.path.join(
            app.config["UPLOAD_FOLDER"],
            nome_imagem
        )

        arquivo.save(caminho)
    else:
        nome_imagem = ""

    produto = Produto(
        nome=nome,
        descricao=descricao,
        preco=preco,
        imagem=nome_imagem
    )

    db.session.add(produto)
    db.session.commit()

    return redirect(url_for("admin"))



if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)