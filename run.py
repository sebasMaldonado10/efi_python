from app import create_app

app = create_app() #funcion create_app

from app.models import Usuario, Post, Comentario, Categoria

if __name__ == '__main__':
    app.run(debug=True) #activamos el modo debug 