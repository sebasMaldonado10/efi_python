import os
#configuracion de la base de datos

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-secreta')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/proyecto_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
