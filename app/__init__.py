from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager

#Este archivo inicializa Flask, configura la base de datos y registra rutas.

db = SQLAlchemy()  # Creamos una instancia de SQLAlchemy para manejar la base de datos 
migrate = Migrate()  # Creamos una instancia de Migrate para manejar las migraciones de la base de datos

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    from app.models import Usuario, Post, Comentario, Categoria

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    @app.context_processor
    def inyectar_categorias():
        categorias = Categoria.query.all()
        return dict(categorias=categorias)

    from .routes import main
    app.register_blueprint(main)

    return app
