from datetime import datetime
from . import db
from flask_login import UserMixin

# Tabla intermedia para relación muchos a muchos
post_categoria = db.Table('post_categoria',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('categoria_id', db.Integer, db.ForeignKey('categorias.id'), primary_key=True)
) #un post puede tener varias categorias y una categoria puede estar en muchos posts(m a m).

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    posts = db.relationship('Post', backref='autor', lazy=True)
    comentarios = db.relationship('Comentario', backref='autor', lazy=True)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    comentarios = db.relationship('Comentario', backref='post', lazy=True)
    categorias = db.relationship('Categoria', secondary=post_categoria, backref=db.backref('posts', lazy='dynamic'), lazy='dynamic')

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)







    
