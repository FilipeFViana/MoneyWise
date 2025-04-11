from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///moneywise.db"
    JWT_SECRET_KEY = "supersecreto"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
