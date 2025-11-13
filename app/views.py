from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError
from functools import wraps

#IMPORTAMOS LO NECESARIO
from passlib.hash import bcrypt
from flask_jwt_extended import (
    jwt_required, verify_jwt_in_request,
    create_access_token, get_jwt, get_jwt_identity
)

from app import db
from app.models import Usuario, UserCredentials, Post, Comentario, Categoria

from app.schemas import (
    RegisterSchema, LoginSchema, UsuarioSchema, PostSchema, ComentarioSchema, CategoriaSchema
)

# =========================
#    RBAC / Ownership
# =========================
def role_required(*allowed_roles: str):
    """Exige que el claim 'role' del JWT esté en allowed_roles."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            role = get_jwt().get("role")
            if role not in allowed_roles:
                return jsonify({"msg": "No tenés permiso para realizar esta acción."}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def is_admin() -> bool:
    return get_jwt().get("role") == "admin"

def owns(owner_id: int) -> bool:
    try:
        uid = int(get_jwt_identity())  # lo pasamos a int para comparar
    except (TypeError, ValueError):
        uid = get_jwt_identity()
    return is_admin() or owner_id == uid

# =======================
#          AUTH
# =======================
class RegisterAPI(MethodView):
    def post(self):
        try:
            data = RegisterSchema().load(request.get_json() or {})
            print("📩 Datos recibidos:", data)
        except ValidationError as err:
            print("❌ Errores de validación:", err.messages)
            return jsonify({"errors": err.messages}), 422

        # Verificar si ya existe usuario o email
        existe = Usuario.query.filter(
            (Usuario.username == data["username"]) | (Usuario.email == data["email"])
        ).first()
        if existe:
            return jsonify({"msg": "El nombre de usuario o email ya existe."}), 409

        # Crear usuario con el rol correspondiente
        u = Usuario(
            username=data["username"],
            email=data["email"],
            role=data.get("role", "user"),
            is_active=True,
        )

        # Crear credenciales (sin role, solo el hash)
        cred = UserCredentials(usuario=u, password_hash=bcrypt.hash(data["password"]))

        db.session.add_all([u, cred])
        db.session.commit()

        print("✅ Usuario creado correctamente:", u.username, "-", u.role)
        return UsuarioSchema().dump(u), 201



class LoginAPI(MethodView):
    def post(self):
        try:
            data = LoginSchema().load(request.get_json() or {})
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 422

        usuario = Usuario.query.filter_by(email=data["email"]).first()
        if not usuario or not usuario.is_active or not usuario.credenciales:
            return jsonify({"msg": "Credenciales inválidas."}), 401
        if not bcrypt.verify(data["password"], usuario.credenciales.password_hash):
            return jsonify({"msg": "Credenciales inválidas."}), 401

        # identity como string (el ID del usuario)
        identity = str(usuario.id) 
        claims   = {
            "role": usuario.role,
            "email": usuario.email,
            "username": usuario.username
        }

        access_token = create_access_token(
            identity=identity,
            additional_claims=claims
        )
        return jsonify(access_token=access_token), 200



class MeAPI(MethodView):
    @jwt_required()
    def get(self):
        uid = int(get_jwt_identity())
        u = Usuario.query.get(uid)
        if not u:
            return jsonify({"msg": "Usuario no encontrado"}), 404
        return UsuarioSchema().dump(u), 200


# =======================
#          POSTS
# =======================
class PostListAPI(MethodView):
    # Público: listar solo publicados
    def get(self):
        posts = Post.query.filter_by(is_published=True).order_by(Post.fecha_creacion.desc()).all()
        return jsonify(PostSchema(many=True).dump(posts)), 200

    # user+: crear
    @jwt_required()
    def post(self):
        try:
            data = PostSchema().load(request.get_json() or {})
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 422

        uid = int(get_jwt_identity())

        nuevo_post = Post(
            titulo=data["titulo"],
            contenido=data["contenido"],
            usuario_id=uid,
            is_published=data.get("is_published", True)
        )
        db.session.add(nuevo_post)
        db.session.commit()
        return PostSchema().dump(nuevo_post), 201


class PostDetailAPI(MethodView):
    # Público: ver un post (si no publicado, solo admin)
    def get(self, post_id: int):
        p = Post.query.get(post_id)
        if not p or (not p.is_published and not is_admin()):
            return jsonify({"msg": "No encontrado"}), 404
        return PostSchema().dump(p), 200

    # Autor o admin: editar
    @jwt_required()
    def put(self, post_id: int):
        post = Post.query.get_or_404(post_id)
        if not owns(post.usuario_id):
            return jsonify({"msg": "No tenés permiso para editar este post."}), 403

        try:
            data = PostSchema().load(request.get_json() or {}, partial=True)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 422

        for field in ("titulo", "contenido", "is_published"):
            if field in data:
                setattr(post, field, data[field])
        db.session.commit()
        return PostSchema().dump(post), 200

    # Autor o admin: eliminar
    @jwt_required()
    def delete(self, post_id: int):
        post = Post.query.get_or_404(post_id)
        if not owns(post.usuario_id):
            return jsonify({"msg": "No tenés permiso para eliminar este post."}), 403
        db.session.delete(post)
        db.session.commit()
        return "", 204
    
# ======== COMENTARIOS ========

class CommentListAPI(MethodView):
    # Público: listar comentarios de un post
    def get(self, post_id: int):
        post = Post.query.get_or_404(post_id)
        qs = Comentario.query.filter_by(post_id=post.id, is_visible=True)\
                             .order_by(Comentario.fecha_creacion.asc()).all()
        return jsonify(ComentarioSchema(many=True).dump(qs)), 200

    # user+: crear comentario en un post
    @jwt_required()
    def post(self, post_id: int):
        post = Post.query.get_or_404(post_id)
        try:
            data = ComentarioSchema().load(request.get_json() or {})
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 422

        uid = int(get_jwt_identity())

        com = Comentario(
            texto=data["texto"],
            usuario_id=uid,
            post_id=post.id,
            is_visible=True
        )
        db.session.add(com); db.session.commit()
        return ComentarioSchema().dump(com), 201


class CommentDeleteAPI(MethodView):
    # Autor del comentario, moderator o admin
    @jwt_required()
    def delete(self, comment_id: int):
        c = Comentario.query.get_or_404(comment_id)
        role = get_jwt().get("role")
        uid = int(get_jwt_identity())


        if not (c.usuario_id == uid or role in ("moderator", "admin")):
            return jsonify({"msg": "No tenés permiso para eliminar este comentario."}), 403

        db.session.delete(c); db.session.commit()
        return "", 204
    
class CommentUpdateAPI(MethodView):
    @jwt_required()
    def put(self, comment_id):
        c = Comentario.query.get_or_404(comment_id)
        uid = int(get_jwt_identity())
        role = get_jwt().get("role")

        # Solo autor, moderator o admin pueden editar
        if c.usuario_id != uid and role not in ("moderator", "admin"):
            return jsonify({"msg": "No autorizado"}), 403

        data = request.get_json() or {}
        c.texto = data.get("texto", c.texto)
        db.session.commit()
        return ComentarioSchema().dump(c), 200


# ======== CATEGORÍAS ========

class CategoryListAPI(MethodView):
    # Público
    def get(self):
        cats = Categoria.query.order_by(Categoria.nombre.asc()).all()
        return jsonify(CategoriaSchema(many=True).dump(cats)), 200

    # moderator+ crea
    @jwt_required()
    @role_required("moderator", "admin")
    def post(self):
        try:
            data = CategoriaSchema().load(request.get_json() or {})
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 422

        if Categoria.query.filter_by(nombre=data["nombre"]).first():
            return jsonify({"msg": "La categoría ya existe"}), 409

        cat = Categoria(nombre=data["nombre"])
        db.session.add(cat); db.session.commit()
        return CategoriaSchema().dump(cat), 201


class CategoryDetailAPI(MethodView):
    # moderator+ edita
    @jwt_required()
    @role_required("moderator", "admin")
    def put(self, category_id: int):
        cat = Categoria.query.get_or_404(category_id)
        try:
            data = CategoriaSchema().load(request.get_json() or {}, partial=True)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 422

        if "nombre" in data:
            # evitar duplicado
            if Categoria.query.filter(Categoria.nombre == data["nombre"],
                                      Categoria.id != cat.id).first():
                return jsonify({"msg": "La categoría ya existe"}), 409
            cat.nombre = data["nombre"]

        db.session.commit()
        return CategoriaSchema().dump(cat), 200

    # admin borra
    @jwt_required()
    @role_required("admin")
    def delete(self, category_id: int):
        cat = Categoria.query.get_or_404(category_id)
        db.session.delete(cat); db.session.commit()
        return "", 204


# ======== USUARIOS (ADMIN) ========
class UserListAPI(MethodView):
    @role_required("admin")
    def get(self):
        users = Usuario.query.order_by(Usuario.created_at.desc()).all()
        return jsonify(UsuarioSchema(many=True).dump(users)), 200


class UserDetailAPI(MethodView):
    @jwt_required()
    def get(self, user_id: int):
        u = Usuario.query.get_or_404(user_id)
        uid = int(get_jwt_identity())

        if not (is_admin() or uid == u.id):
            return jsonify({"msg": "Forbidden"}), 403
        return UsuarioSchema().dump(u), 200

    # admin: cambiar rol y/o activar/desactivar
    @role_required("admin")
    def patch(self, user_id: int):
        u = Usuario.query.get_or_404(user_id)
        data = request.get_json() or {}

        if "role" in data:
            new_role = data["role"]
            if new_role not in ("user", "moderator", "admin"):
                return jsonify({"msg": "Rol inválido"}), 400
            u.role = new_role
            if u.credenciales:
                u.credenciales.role = new_role

        if "is_active" in data:
            u.is_active = bool(data["is_active"])

        db.session.commit()
        return UsuarioSchema().dump(u), 200

    # admin: desactivar (soft delete)
    @role_required("admin")
    def delete(self, user_id: int):
        u = Usuario.query.get_or_404(user_id)
        u.is_active = False
        db.session.commit()
        return "", 204


# ======== STATS (moderator+ / admin extra campo) ========
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models import Comentario as _Comentario, Post as _Post, Usuario as _Usuario

class StatsAPI(MethodView):
    @jwt_required()
    @role_required("moderator", "admin")
    def get(self):
        resp = {
            "total_posts":      db.session.scalar(db.select(func.count()).select_from(_Post)) or 0,
            "total_comments":   db.session.scalar(db.select(func.count()).select_from(_Comentario)) or 0,
            "total_users":      db.session.scalar(db.select(func.count()).select_from(_Usuario)) or 0,
        }
        if get_jwt().get("role") == "admin":
            week_ago = datetime.now() - timedelta(days=7)
            posts_last_week = db.session.scalar(
                db.select(func.count()).select_from(_Post).where(_Post.fecha_creacion >= week_ago)
            ) or 0
            resp["posts_last_week"] = posts_last_week
        return jsonify(resp), 200

# ====REVIEWS====
class ReviewsAllAPI(MethodView):
    @jwt_required()
    @role_required("admin", "moderator")
    def get(self):
        reviews = Comentario.query.order_by(Comentario.fecha_creacion.desc()).all()
        return jsonify(ComentarioSchema(many=True).dump(reviews)), 200

