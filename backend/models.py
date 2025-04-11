from backend import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.LargeBinary, nullable=False)
    tokens = db.relationship('Token', backref='usuario', lazy=True)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    token = db.Column(db.Text, nullable=False)
