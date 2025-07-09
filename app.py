from flask import Flask, request, render_template_string
import sqlite3
import hashlib

app = Flask(__name__)
DB_NAME = 'usuarios.db'

# Crear tabla si no existe
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

# Función para hashear contraseña
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Agregar usuario a la base de datos
def add_user(nombre, password):
    password_hash = hash_password(password)
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)', (nombre, password_hash))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Validar usuario y contraseña
def validate_user(nombre, password):
    password_hash = hash_password(password)
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM usuarios WHERE nombre=? AND password_hash=?', (nombre, password_hash))
        return c.fetchone() is not None

# Página principal con formulario de login
@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ''
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        password = request.form.get('password')
        if validate_user(nombre, password):
            mensaje = f'Bienvenido, {nombre}!'
        else:
            mensaje = 'Usuario o contraseña incorrectos.'
    return render_template_string('''
        <h2>Login Examen</h2>
        <form method="POST">
            Nombre: <input type="text" name="nombre" required><br>
            Contraseña: <input type="password" name="password" required><br>
            <input type="submit" value="Ingresar">
        </form>
        <p>{{mensaje}}</p>
    ''', mensaje=mensaje)

if __name__ == '__main__':
    init_db()
    # Carga automática de los usuarios tomas y brandon
    add_user("tomas", "clave123")
    add_user("brandon", "clave456")
    app.run(port=5800)
