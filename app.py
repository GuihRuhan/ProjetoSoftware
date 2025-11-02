from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import IntegrityError


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
    try:
        cliente = Cliente(
            nome=request.form['nome'],
            telefone=request.form['telefone'],
            cidade=request.form['cidade'],
            rg=request.form['rg'],
            cpf=request.form['cpf']
        )
        db.session.add(cliente)
        db.session.commit()
        return redirect('/clientes')

    except IntegrityError:
        db.session.rollback()
        flash("Erro: esse RG já está cadastrado!", "error")
        return redirect('/clientes')


@app.route('/atender')
def atender():
    pacientes = Paciente.query.all()
    return render_template("atender.html", pacientes=pacientes)

@app.route('/clientes')
def clientes():
    clientes = Cliente.query.all()
    return render_template("clientes.html", clientes=clientes)

@app.route('/add_cliente', methods=['POST'])
def adicionar_cliente_novo():
    nome = request.form['nome']
    telefone = request.form['telefone']
    cidade = request.form['cidade']
    rg = request.form['rg']
    cpf = request.form['cpf']

    novo_cliente = Cliente(nome=nome, telefone=telefone, cidade=cidade, rg=rg, cpf=cpf)

    try:
        db.session.add(novo_cliente)
        db.session.commit()
        flash("Cliente cadastrado com sucesso!")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao cadastrar cliente: {e}")

    return redirect('/clientes')

# ------------------ Main ------------------

if __name__ == '__main__':
    app.run(debug=True)
