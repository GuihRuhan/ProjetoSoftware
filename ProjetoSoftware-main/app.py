from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)

# ==============================
# DADOS TEMPORÁRIOS
# ==============================
fila_pacientes = []
paciente_em_atendimento = None

# Caminho do arquivo de clientes
DATA_FILE = "data/clientes.json"


# ==============================
# FUNÇÕES AUXILIARES
# ==============================
def carregar_clientes():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_clientes(clientes):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(clientes, f, ensure_ascii=False, indent=4)


# ==============================
# ROTA PRINCIPAL — FILA DE ATENDIMENTO
# ==============================
@app.route("/")
def index():
    return render_template("index.html", pacientes=fila_pacientes)



@app.route("/add_paciente", methods=["POST"])
def add_paciente():
    nome = request.form["nome"]
    idade = request.form["idade"]
    urgencia = request.form["urgencia"]
    convenio = request.form["convenio"]
    hora = datetime.now().strftime("%H:%M:%S")

    novo_paciente = {
        "nome": nome,
        "idade": idade,
        "urgencia": urgencia,
        "convenio": convenio,
        "hora": hora
    }

    # Prioriza emergências, depois urgências, depois comuns
    prioridade = {"emergencia": 1, "urgencia": 2, "comum": 3}
    fila_pacientes.append(novo_paciente)
    fila_pacientes.sort(key=lambda p: prioridade[p["urgencia"]])

    return redirect(url_for("index"))


@app.route("/atender")
def atender_paciente():
    global paciente_em_atendimento
    if fila_pacientes:
        paciente_em_atendimento = fila_pacientes.pop(0)
    else:
        paciente_em_atendimento = None
    return render_template("atender.html", paciente=paciente_em_atendimento)


# ==============================
# GESTÃO DE CLIENTES
# ==============================
@app.route("/clientes")
def lista_clientes():
    clientes = carregar_clientes()
    return render_template("clientes.html", clientes=clientes)


@app.route("/add_cliente", methods=["POST"])
def adicionar_cliente():
    codigo = request.form["codigo"]
    nome = request.form["nome"]
    telefone = request.form.get("telefone", "")
    cidade = request.form.get("cidade", "")

    clientes = carregar_clientes()
    clientes.append({
        "codigo": codigo,
        "nome": nome,
        "telefone": telefone,
        "cidade": cidade
    })
    salvar_clientes(clientes)

    return redirect(url_for("lista_clientes"))


@app.route("/delete_cliente/<codigo>")
def deletar_cliente(codigo):
    clientes = carregar_clientes()
    clientes = [c for c in clientes if c["codigo"] != codigo]
    salvar_clientes(clientes)
    return redirect(url_for("lista_clientes"))


# ==============================
# EXECUÇÃO
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
