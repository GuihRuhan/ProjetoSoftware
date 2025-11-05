from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ------------------ Models ------------------

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.String(10))
    rg = db.Column(db.String(20))
    cpf = db.Column(db.String(20))
    urgencia = db.Column(db.String(20))
    convenio = db.Column(db.String(50))
    hora_chegada = db.Column(db.String(20))

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    cidade = db.Column(db.String(100))
    rg = db.Column(db.String(20))  # ✅ REMOVIDO unique=True
    cpf = db.Column(db.String(20))

# ------------------ Rotas ------------------

@app.route('/')
def index():
    pacientes = Paciente.query.all()
    return render_template("index.html", pacientes=pacientes)

@app.route('/add_cliente', methods=['POST'])
def adicionar_cliente():
    nome = request.form['nome']
    telefone = request.form['telefone']
    cidade = request.form['cidade']
    rg = request.form['rg']
    cpf = request.form['cpf']

    cliente = Cliente(nome=nome, telefone=telefone, cidade=cidade, rg=rg, cpf=cpf)

    try:
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente cadastrado com sucesso!", "success")
    except IntegrityError:
        db.session.rollback()
        flash("Erro: esse RG já está cadastrado!", "error")

    return redirect('/clientes')


@app.route('/atender')
def atender():
    paciente = Paciente.query.all()
    return render_template("atender.html", paciente=paciente)

@app.route('/clientes')
def clientes():
    clientes = Cliente.query.all()
    return render_template("clientes.html", clientes=clientes)

@app.route('/add_paciente', methods=['POST'])
def add_paciente():
    nome = request.form.get("nome")
    idade = request.form.get("idade")
    rg = request.form.get("rg")
    cpf = request.form.get("cpf")
    convenio = request.form.get("convenio")
    urgencia = request.form.get("urgencia")
    hora_chegada = datetime.now().strftime("%H:%M:%S")

    novo = Paciente(
        nome=nome,
        idade=idade,
        rg=rg,
        cpf=cpf,
        convenio=convenio,
        urgencia=urgencia,
        hora_chegada=hora_chegada
    )
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/deletar_cliente/<int:id>')
def deletar_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        flash("Cliente removido com sucesso!", "success")
    else:
        flash("Cliente não encontrado!", "error")

    return redirect('/clientes')


# ------------------ Main ------------------

if __name__ == '__main__':
    app.run(debug=True)
