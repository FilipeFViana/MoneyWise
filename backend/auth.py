import re
import bcrypt
from backend.models import Usuario
from backend import db

def validar_dados(nome, email, cpf, senha):
    if not nome or not email or not cpf or not senha:
        return "Todos os campos são obrigatórios!"

    if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", nome):
        return "O nome deve conter apenas letras."

    if not re.match(r"^\d{11}$", cpf):
        return "O CPF deve conter exatamente 11 números."

    if Usuario.query.filter_by(email=email).first():
        return "E-mail já cadastrado."

    if Usuario.query.filter_by(cpf=cpf).first():
        return "CPF já cadastrado."

    return None

def criar_usuario(nome, email, cpf, senha):
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    novo_usuario = Usuario(nome=nome, email=email, cpf=cpf, senha=senha_hash)
    db.session.add(novo_usuario)
    db.session.commit()

def verificar_login(email, senha):
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario.senha):
        return usuario
    return None
