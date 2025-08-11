from app import create_app, db
from app.models import Categoria

app = create_app()
app.app_context().push()

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
    print("Categorías cargadas correctamente.")

if __name__ == "__main__":
    cargar_categorias()
