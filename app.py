from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)