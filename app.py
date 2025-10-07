from flask import Flask, render_template, request, redirect, url_for, flash
import heapq
from datetime import datetime

app = Flask(__name__)
app.secret_key = "chave_super_secreta"

# Banco de dados fake em memória (pode trocar por SQLite depois)
clientes = []

# Lista de pacientes (usando heap para priorizar)
pacientes = []
contador = 0  # Para desempate (ordem de chegada)


# Função para definir prioridade
def definir_prioridade(idade, urgencia, convenio):
    if urgencia == "emergencia":
        return 1
    elif urgencia == "urgencia":
        return 2
    elif idade >= 60:
        return 3
    elif convenio == "sim":
        return 4
    else:
        return 5


@app.route("/")
def index():
    # Converte heap em lista ordenada (sem remover da heap)
    fila_ordenada = sorted(pacientes, key=lambda x: (x[0], x[1]))
    return render_template("index.html", pacientes=fila_ordenada)


@app.route("/add", methods=["POST"])
def add_paciente():
    global contador
    nome = request.form["nome"]
    idade = int(request.form["idade"])
    urgencia = request.form["urgencia"]
    convenio = request.form["convenio"]

    prioridade = definir_prioridade(idade, urgencia, convenio)

    # Adiciona na heap: (prioridade, ordem chegada, dados)
    heapq.heappush(pacientes, (prioridade, contador, {
        "nome": nome,
        "idade": idade,
        "urgencia": urgencia,
        "convenio": convenio,
        "hora": datetime.now().strftime("%H:%M:%S")
    }))
    contador += 1

    flash(f"Paciente {nome} adicionado à fila!", "success")
    return redirect(url_for("index"))


@app.route("/atender")
def atender_paciente():
    if pacientes:
        paciente = heapq.heappop(pacientes)[2]  # Pega os dados do paciente
        return render_template("atender.html", paciente=paciente)
    return render_template("atender.html", paciente=None)



# Rotas de clientes
@app.route("/clientes")
def lista_clientes():
    return render_template("clientes.html", clientes=clientes)


@app.route("/adicionar", methods=["POST"])
def adicionar_cliente():
    codigo = request.form.get("codigo")
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")
    cidade = request.form.get("cidade")

    if not codigo or not nome:
        flash("Código e Nome são obrigatórios!", "error")
        return redirect(url_for("lista_clientes"))

    cliente = {"codigo": codigo, "nome": nome, "telefone": telefone, "cidade": cidade}
    clientes.append(cliente)

    flash("Cliente adicionado com sucesso!", "success")
    return redirect(url_for("lista_clientes"))


@app.route("/deletar/<codigo>")
def deletar_cliente(codigo):
    global clientes
    clientes = [c for c in clientes if c["codigo"] != codigo]
    flash("Cliente removido!", "info")
    return redirect(url_for("lista_clientes"))


if __name__ == "__main__":
    app.run(debug=True)
