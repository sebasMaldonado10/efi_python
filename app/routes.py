from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Post, Usuario, Comentario, Categoria, db
from app.forms import RegistroForm, LoginForm, ComentarioForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def home():
    posts = Post.query.order_by(Post.fecha_creacion.desc()).all()
    return render_template('home.html', posts=posts)

@main.route('/categoria/<int:categoria_id>')
def filtrar_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    posts = categoria.posts.order_by(Post.fecha_creacion.desc()).all()
    return render_template('posts_por_categoria.html', posts=posts, categoria=categoria)


#GET para mostrar el formulario vacio
#POST para recibir los datos del formulario cuando se envia
@main.route('/crear_post',methods=['GET','POST'])
@login_required
def crear_post():
    if request.method =='POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        categorias_ids = request.form.getlist('categorias')  # Lista de IDs seleccionados

        nuevo_post = Post(titulo=titulo, contenido=contenido, usuario_id=current_user.id) #Asocia el post al usuario creado
        
        if categorias_ids:
            categorias_seleccionadas = Categoria.query.filter(Categoria.id.in_(categorias_ids)).all()
            nuevo_post.categorias = categorias_seleccionadas
            
        db.session.add(nuevo_post)
        db.session.commit()

        flash('Post creado!')
        return redirect(url_for('main.home'))
    
    return render_template('crear_post.html')

@main.route('/editar_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.titulo = request.form['titulo']
        post.contenido = request.form['contenido']
        db.session.commit()
        flash('¡Post editado con éxito!')
        return redirect(url_for('main.home'))

    return render_template('editar_post.html', post=post)


@main.route('/eliminar_post/<int:post_id>', methods=[ 'POST'])
@login_required
def eliminar_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.usuario_id != current_user.id:
        flash('No tenés permiso para eliminar este post')
        return redirect(url_for('main.home'))
     
    db.session.delete(post)
    db.session.commit()
    flash('Post eliminado con éxito.')
    return redirect(url_for('main.home'))

@main.route('/registro',methods=['GET','POST'])
def registro():
    form = RegistroForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)

        nuevo_usuario = Usuario(username=username, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('¡Registro exitoso!')
        return redirect(url_for('main.home'))
    
    return render_template('registro.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if form.validate_on_submit():
            print(f"Email ingresado: {form.email.data}")
            usuario = Usuario.query.filter_by(email=form.email.data).first()
            print(f"Usuario encontrado: {usuario}")
    
        if usuario:
            print(f"Contraseña en DB (hash): {usuario.password}")
            print(f"Contraseña ingresada: {form.password.data}")
            print(f"¿Coinciden?: {check_password_hash(usuario.password, form.password.data)}")

        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            print("Login exitoso")
            return redirect(url_for('main.home'))
        else:
            flash('Email o contraseña incorrectos')

    return render_template('login.html', form=form)

@main.route('/crear_post')
@login_required
def settings():
    return render_template('crear_post.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('sesion cerrada')
    return redirect(url_for('main.home'))


@main.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def ver_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = ComentarioForm() #creamos una instancia del formulario

    if form.validate_on_submit():
        nuevo_comentario = Comentario(
            texto=form.texto.data,
            autor=current_user,
            post=post
        )

        db.session.add(nuevo_comentario)#subimos el comentario a la BD
        db.session.commit()

        flash('Comentario agregado.')
        return redirect(url_for('main.ver_post', post_id=post.id))

    return render_template('ver_post.html', post=post, form=form)



