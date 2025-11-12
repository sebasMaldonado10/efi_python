# app/routes.py
from app.views import (
    # Auth
    RegisterAPI, LoginAPI, MeAPI,
    # Posts
    PostListAPI, PostDetailAPI,
    # Comentarios
    CommentListAPI, CommentDeleteAPI,
    # Categorías
    CategoryListAPI, CategoryDetailAPI,
    # Usuarios (admin)
    UserListAPI, UserDetailAPI,
    # Stats
    StatsAPI
)

def register_routes(app):
    # ---- Auth ----
    app.add_url_rule("/api/register", view_func=RegisterAPI.as_view("register"))
    app.add_url_rule("/api/login", view_func=LoginAPI.as_view("login"))
    app.add_url_rule("/api/me", view_func=MeAPI.as_view("me"))

    # ---- Posts ----
    app.add_url_rule("/api/posts", view_func=PostListAPI.as_view("post_list"))
    app.add_url_rule("/api/posts/<int:post_id>", view_func=PostDetailAPI.as_view("post_detail"))

    # ---- Comentarios ----
    app.add_url_rule("/api/posts/<int:post_id>/comments", view_func=CommentListAPI.as_view("comment_list"))
    app.add_url_rule("/api/comments/<int:comment_id>", view_func=CommentDeleteAPI.as_view("comment_delete"))

    # ---- Categorías ----
    app.add_url_rule("/api/categories", view_func=CategoryListAPI.as_view("category_list"))
    app.add_url_rule("/api/categories/<int:category_id>", view_func=CategoryDetailAPI.as_view("category_detail"))

    # ---- Usuarios (admin) ----
    app.add_url_rule("/api/users", view_func=UserListAPI.as_view("user_list"))
    app.add_url_rule("/api/users/<int:user_id>", view_func=UserDetailAPI.as_view("user_detail"))

    # ---- Stats ----
    app.add_url_rule("/api/stats", view_func=StatsAPI.as_view("stats"))

