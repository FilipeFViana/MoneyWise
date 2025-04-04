from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import re
import bcrypt

app = Flask(__name__, template_folder="templates", static_folder="static")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moneywise.db"
app.config["JWT_SECRET_KEY"] = "supersecreto"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Criação do usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.LargeBinary, nullable=False)  # Armazena senha criptografada
    tokens = db.relationship('Token', backref='usuario', lazy=True)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    token = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

# Rotas HTML
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login-page")
def login_page():
    return render_template("login.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/dashboard", methods=["GET"])
def dashboard_page():
    return render_template("dashboard.html")

# Registro de usuário
@app.route("/register", methods=["POST"])
def register():
    dados = request.json
    nome = dados.get("nome", "").strip()
    email = dados.get("email", "").strip()
    cpf = dados.get("cpf", "").strip()
    senha = dados.get("senha", "").strip()

    if not nome or not email or not cpf or not senha:
        return jsonify({"erro": "Todos os campos são obrigatórios!"}), 400

    if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", nome):
        return jsonify({"erro": "O nome deve conter apenas letras."}), 400

    if not re.match(r"^\d{11}$", cpf):
        return jsonify({"erro": "O CPF deve conter exatamente 11 números."}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"erro": "E-mail já cadastrado"}), 400

    if Usuario.query.filter_by(cpf=cpf).first():
        return jsonify({"erro": "CPF já cadastrado"}), 400

    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    novo_usuario = Usuario(nome=nome, cpf=cpf, email=email, senha=senha_hash)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário registrado com sucesso!"}), 201

# Login e geração de token
@app.route("/login", methods=["POST"])
def login_user():
    dados = request.json
    email = dados.get("email")
    senha = dados.get("senha")

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not bcrypt.checkpw(senha.encode('utf-8'), usuario.senha):
        return jsonify({"erro": "E-mail ou senha inválidos"}), 401

    token = create_access_token(identity=email, expires_delta=timedelta(minutes=30))

    # Salva o token no banco
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

# Dashboard protegida 
@app.route("/dashboard-data", methods=["GET"])
@jwt_required()
def dashboard_data():
    current_user = get_jwt_identity()
    return jsonify({"mensagem": f"Bem-vindo ao seu painel, {current_user}!"})

if __name__ == "__main__":
    app.run(debug=True)
