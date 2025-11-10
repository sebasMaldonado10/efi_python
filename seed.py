# seed.py
from app import create_app, db
from app.models import Categoria, Usuario, UserCredentials
from passlib.hash import bcrypt

# Crear contexto de aplicación
app = create_app()
app.app_context().push()


# CARGA DE CATEGORÍAS

categorias_iniciales = [
    "Noticias", "Reseñas", "Tutoriales", "Recetas", "Viajes",
    "Moda", "Salud y Bienestar", "Finanzas Personales", "Tecnología", "Mascotas"
]

def cargar_categorias():
    for nombre in categorias_iniciales:
        existe = Categoria.query.filter_by(nombre=nombre).first()
        if not existe:
            nueva_categoria = Categoria(nombre=nombre)
            db.session.add(nueva_categoria)
    db.session.commit()
    print("✅ Categorías cargadas correctamente.")


# ================================
#  CARGA DE USUARIOS DE PRUEBA
# ================================
usuarios_prueba = [
    ("admin", "admin@mail.com", "admin123", "admin"),
    ("mod", "mod@mail.com", "mod123", "moderator"),
    ("user", "user@mail.com", "user123", "user"),
]

def cargar_usuarios():
    for username, email, pwd, rol in usuarios_prueba:
        existe = Usuario.query.filter_by(email=email).first()
        if not existe:
            u = Usuario(username=username, email=email, role=rol)
            cred = UserCredentials(usuario=u, password_hash=bcrypt.hash(pwd))
            db.session.add_all([u, cred])
    db.session.commit()
    print("✅ Usuarios de prueba creados correctamente.")


# ================================
# 🚀 EJECUCIÓN PRINCIPAL
# ================================
if __name__ == "__main__":
    cargar_categorias()
    cargar_usuarios()
    print("\n🌱 Base de datos inicializada correctamente.")

