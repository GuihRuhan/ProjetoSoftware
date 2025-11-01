from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

# Caminho do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ===== MODELOS =====
class Cliente(db.Model):
    codigo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    cidade = db.Column(db.String(50))

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    urgencia = db.Column(db.String(20))
    convenio = db.Column(db.String(10))
    hora = db.Column(db.String(10), default=lambda: datetime.now().strftime("%H:%M"))

# ===== ROTAS =====

@app.route('/')
def index():
    pacientes = Paciente.query.all()
    # return render_template('index.html', pacientes=enumerate(pacientes))
    return render_template('index.html', pacientes=list(enumerate(pacientes)))


@app.route('/add_paciente', methods=['POST'])
def add_paciente():
    nome = request.form['nome']
    idade = request.form['idade']
    urgencia = request.form['urgencia']
    convenio = request.form['convenio']
    novo = Paciente(nome=nome, idade=idade, urgencia=urgencia, convenio=convenio)
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/atender')
def atender_paciente():
    paciente = Paciente.query.first()
    if paciente:
        db.session.delete(paciente)
        db.session.commit()
        return render_template('atender.html', paciente=paciente)
    else:
        return render_template('atender.html', paciente=None)

# === CLIENTES ===
@app.route('/clientes')
def lista_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/add_cliente', methods=['POST'])
def adicionar_cliente():
    codigo = request.form['codigo']

    if Cliente.query.filter_by(codigo=codigo).first():
        flash("Código já existente! Escolha outro.")
        return redirect('/clientes')

    nome = request.form['nome']
    telefone = request.form['telefone']
    cidade = request.form['cidade']
    novo = Cliente(codigo=codigo, nome=nome, telefone=telefone, cidade=cidade)
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('lista_clientes'))


@app.route('/deletar/<int:codigo>')
def deletar_cliente(codigo):
    cliente = Cliente.query.get_or_404(codigo)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('lista_clientes'))

# ===== EXECUÇÃO =====
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)