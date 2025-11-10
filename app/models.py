from datetime import datetime
from . import db #importamos la instancia de SQLAlchemy creada en __init__.py
from passlib.hash import bcrypt

# Tabla intermedia para relación muchos a muchos
post_categoria = db.Table('post_categoria',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('categoria_id', db.Integer, db.ForeignKey('categorias.id'), primary_key=True)
    ) 
#un post puede tener varias categorias y una categoria puede estar en muchos posts(m a m).

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(20), default='user') #roles: user, admin, moderator
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    #Relación uno a muchos con UserCredential, Post y Comentario
    credenciales = db.relationship("UserCredentials", uselist=False, back_populates="usuario")
    posts = db.relationship("Post", backref="autor", cascade="all,delete-orphan")
    comentarios = db.relationship("Comentario", backref="autor", cascade="all,delete-orphan")

# Tabla para credenciales adicionales
class UserCredentials(db.Model):
    __tablename__ = 'user_credentials'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    usuario = db.relationship("Usuario", back_populates="credenciales")

    @staticmethod
    def hash_pwd(password):
        return bcrypt.hash(password)

    def check_pwd(self, password):
        return bcrypt.verify(password, self.password_hash)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    is_published = db.Column(db.Boolean, default=True) #Indica si el post está publicado o en borrador 
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now) #Fecha de última actualización

    comentarios = db.relationship('Comentario', backref='post', lazy=True, cascade='all, delete-orphan')
    categorias = db.relationship('Categoria', secondary=post_categoria, backref=db.backref('posts', lazy='dynamic'), lazy='dynamic')

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    is_visible = db.Column(db.Boolean, default=True) #Indica si el comentario es visible públicamente

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)







    
