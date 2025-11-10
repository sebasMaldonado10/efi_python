import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost/proyecto_blog")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT (consigna: 24 horas)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "cambiame-por-env")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # (Opcional, pero útil)
    JSON_AS_ASCII = False           # para acentos/ñ en JSON
    PROPAGATE_EXCEPTIONS = True     # deja pasar errores (útil con JWT)
