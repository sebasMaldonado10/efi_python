# 🧠 Proyecto API REST – Flask (EFI Python 2025)

Este proyecto implementa una **API REST** desarrollada con **Flask**, que gestiona usuarios, posts, comentarios y categorías.  
Incluye autenticación con **JWT (Bearer Token)** y un sistema de **roles (user, moderator, admin)** para controlar permisos.

---
## Integrantes
- Mateo Urquiza
- Sebastian Maldonado

## 🚀 Tecnologías principales
- Python 3.12  
- Flask + Flask-SQLAlchemy  
- Flask-Migrate  
- Flask-JWT-Extended  
- Passlib (bcrypt)  
- MySQL / MariaDB (XAMPP)

---

## ⚙️ Instalación y ejecución local

1️⃣ **Clonar el repositorio:**
```bash
git clone https://github.com/sebasMaldonado10/efi_python.git
cd efi_python
```

2️⃣ **Crear entorno virtual e instalar dependencias:**
```bash
python3 -m venv enviroment
source enviroment/bin/activate
pip install -r requirements.txt
```
3️⃣ **Iniciar XAMPP (necesario para el servidor MySQL):**
```bash
sudo /opt/lampp/lampp start
```

4️⃣ **Configurar variables en .env (opcional):**
```bash
SECRET_KEY=clave-secreta
JWT_SECRET_KEY=cambiame-por-env
DATABASE_URL=mysql+pymysql://root:@localhost/proyecto_blog
```

5️⃣ **Crear base de datos y cargar datos iniciales:**
```bash
flask db upgrade
python seed.py
```

⚠️ Nota: Si ya tenés la base creada localmente, podés omitir estos pasos.

6️⃣ **Iniciar la API:**
```bash
python run.py
```

📍 La API estará disponible en:

http://127.0.0.1:5000/
