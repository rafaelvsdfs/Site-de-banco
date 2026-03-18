from flask import Blueprint, render_template, request, redirect, url_for
from app.database import get_conexao

bp = Blueprint('auth', __name__)

@bp.route("/")
def home():
    conn = get_conexao()
    cursor = conn.cursor()

    # Pega o cliente mais recente cadastrado
    cursor.execute("""
        SELECT c.nome, co.saldo
        FROM clientes c
        JOIN contas co ON co.cliente_id = c.id
        ORDER BY c.id DESC
        LIMIT 1
    """)
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        nome, saldo = resultado
    else:
        nome, saldo = "", 0  # vazio se não tiver cliente

    return render_template("index.html", nome=nome, saldo=saldo)

@bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]

        conn = get_conexao()
        cursor = conn.cursor()

        # Inserir cliente
        cursor.execute(
            "INSERT INTO clientes (nome, cpf) VALUES (?, ?)",
            (nome, cpf)
        )
        cliente_id = cursor.lastrowid  # pega o ID do cliente recém-criado

        # Criar conta com saldo inicial 0
        cursor.execute(
            "INSERT INTO contas (cliente_id, saldo, limite) VALUES (?, ?, ?)",
            (cliente_id, 0, 0)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("auth.home"))

    return render_template("cadastro.html")