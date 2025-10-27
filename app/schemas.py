from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    role = fields.Str(validate=validate.OneOf(["user","moderator","admin"]))
    is_active = fields.Bool()
    created_at = fields.DateTime()

class UserCredentialsSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)               
    password_hash = fields.Str(load_only=True, required=True) 
    role = fields.Str(validate=validate.OneOf(["user","moderator","admin"]))

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    contenido  = fields.Str(required=True)
    fecha_creacion = fields.DateTime(dump_only=True)
    usuario_id  = fields.Int(dump_only=True)   # <- lo tomamos del JWT
    is_published = fields.Bool()
    updated_at  = fields.DateTime(dump_only=True)

class ComentarioSchema(Schema):
    id  = fields.Int(dump_only=True)
    texto = fields.Str(required=True, validate=validate.Length(min=1))
    fecha_creacion = fields.DateTime(dump_only=True)
    usuario_id = fields.Int(dump_only=True)   # <- del JWT
    post_id = fields.Int(dump_only=True)   # <- suele venir en la URL /posts/<id>/comments
    is_visible = fields.Bool()

class CategoriaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=50))

# (Si usás una ruta para vincular post-categoría, podés mantener este schema)
class PostCategoriaSchema(Schema):
    post_id  = fields.Int(required=True)
    categoria_id = fields.Int(required=True)


