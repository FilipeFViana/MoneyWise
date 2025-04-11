from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.auth import validar_dados, criar_usuario, verificar_login
from backend.models import Token, Usuario
from backend.extensions import db
import requests
import os

bp = Blueprint("routes", __name__)

@bp.route("/")
def home():
    return render_template("index.html")

@bp.route("/login-page")
def login_page():
    return render_template("login.html")

@bp.route("/register-page")
def register_page():
    return render_template("register.html")

@bp.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

@bp.route("/perfil")
def profile_page():
    return render_template("profile.html")

@bp.route("/register", methods=["POST"])
def register():
    dados = request.json
    erro = validar_dados(
        dados.get("nome"),
        dados.get("email"),
        dados.get("cpf"),
        dados.get("senha")
    )

    if erro:
        return jsonify({"erro": erro}), 400

    criar_usuario(dados["nome"], dados["email"], dados["cpf"], dados["senha"])
    return jsonify({"mensagem": "Usuário registrado com sucesso!"}), 201

@bp.route("/login", methods=["POST"])
def login():
    dados = request.json
    usuario = verificar_login(dados["email"], dados["senha"])

    if not usuario:
        return jsonify({"erro": "E-mail ou senha inválidos"}), 401

    token = create_access_token(identity=usuario.email)
    token_db = Token(usuario_id=usuario.id, token=token)
    db.session.add(token_db)
    db.session.commit()

    return jsonify({
        "mensagem": "Login bem-sucedido!",
        "token": token,
        "usuario": {
            "nome": usuario.nome,
            "email": usuario.email,
            "cpf": usuario.cpf
        }
    }), 200

@bp.route("/dashboard-data", methods=["GET"])
@jwt_required()
def dashboard_data():
    usuario_logado = get_jwt_identity()
    simbolos = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "BBAS3.SA"]
    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    ativos = []

    for simbolo in simbolos:
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={simbolo}&apikey={api_key}"
            response = requests.get(url)
            data = response.json().get("Global Quote", {})
            preco = data.get("05. price", "0.00")
            variacao = data.get("10. change percent", "0.00%")
            ativos.append({
                "simbolo": simbolo,
                "preco": round(float(preco), 2),
                "variacao": variacao.replace("%", "").strip()
            })
        except:
            continue

    return jsonify({
        "mensagem": f"Bem-vindo ao seu painel, {usuario_logado}!",
        "ativos": ativos
    })

@bp.route("/perfil-dados", methods=["GET"])
@jwt_required()
def perfil_dados():
    email = get_jwt_identity()
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify({
        "nome": usuario.nome,
        "email": usuario.email,
        "cpf": usuario.cpf
    })
