from flask import Flask, render_template, session, redirect, url_for
import urllib.parse

app = Flask(__name__)

app.secret_key = "cinthia_carimbos"

produtos = [
    {
        "id": 1,
        "nome": "Carimbo Automático",
        "preco": 35.00,
        "descricao": "Carimbo automático de alta qualidade."
    },
    {
        "id": 2,
        "nome": "Carimbo de Madeira",
        "preco": 20.00,
        "descricao": "Carimbo tradicional de madeira."
    },
    {
        "id": 3,
        "nome": "Carimbo Datador",
        "preco": 45.00,
        "descricao": "Carimbo com data ajustável."
    }
]

@app.route("/")
def inicio():
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
    for produto in produtos:
        if produto["id"] == id:
            if "carrinho" not in session:
                session["carrinho"] = []

            session["carrinho"].append(produto)
            session.modified = True

            return redirect(url_for("carrinho"))

    return "Produto não encontrado!"

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
        mensagem += f"• {produto['nome']} - R$ {produto['preco']:.2f}%0A"
        total += produto["preco"]

    mensagem += f"%0A💰 Total: R$ {total:.2f}"

    mensagem = urllib.parse.quote(mensagem)

    numero = "5585987967624" # Substitua pelo número de telefone desejado

    return redirect(
        f"https://wa.me/message/HDQBGH3SCFO5H1?text={mensagem}"
    )

if __name__ == "__main__":
    app.run(debug=True)
