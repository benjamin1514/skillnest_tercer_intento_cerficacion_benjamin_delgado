# Controlador de usuarios
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_app import app, bcrypt



# Mostrar registro e inicio de sesión
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')

    return render_template('index.html')


# Registrar un usuario
@app.route('/registrar', methods=['POST'])
def registrar():
    datos = {
        'nombre': request.form.get('nombre', '').strip(),
        'apellido': request.form.get('apellido', '').strip(),
        'email': request.form.get('email', '').strip().lower(),
        'password': request.form.get('password', ''),
        'confirm_password': request.form.get('confirm_password', '')
    }

    # Validar los campos mediante el modelo
    if not Usuario.validar_usuario(datos):
        return redirect('/')

    # Comprobar si el correo ya está registrado
    usuario_existente = Usuario.get_by_email(datos['email'])

    if usuario_existente is False:
        flash('Error al consultar la base de datos.', 'error')
        return redirect('/')

    if usuario_existente is not None:
        flash('Este correo electrónico ya está registrado.', 'error_email')
        return redirect('/')

    # Generar hash de la contraseña
    password_hash = bcrypt.generate_password_hash(
        datos['password']
    ).decode('utf-8')

    # Guardar usuario
    resultado = Usuario.save({
        'nombre': datos['nombre'],
        'apellido': datos['apellido'],
        'email': datos['email'],
        'password_hash': password_hash
    })

    # Comprobar que el registro se haya realizado
    if resultado is False or resultado is None or resultado == 0:
        flash('No se pudo registrar el usuario.', 'error')
        return redirect('/')

    # Iniciar sesión solo después de guardar correctamente
    session.clear()
    session['user_id'] = resultado
    session['usuario_nombre'] = datos['nombre']

    flash('Registro exitoso. ¡Bienvenido!', 'success')
    return redirect('/dashboard')


# Iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    if not email or not password:
        flash('Ingresa tu correo y contraseña.', 'error')
        return redirect('/')

    usuario = Usuario.get_by_email(email)

    if usuario is False:
        flash('Error al consultar la base de datos.', 'error')
        return redirect('/')

    if usuario is None:
        flash('Correo o contraseña incorrectos.', 'error')
        return redirect('/')

    # Verificar la contraseña con Bcrypt
    if not bcrypt.check_password_hash(
        usuario.password_hash, password
    ):
        flash('Correo o contraseña incorrectos.', 'error')
        return redirect('/')

    # Crear sesión
    session.clear()
    session['user_id'] = usuario.id_usuario
    session['usuario_nombre'] = usuario.nombre

    return redirect('/dashboard')


# Cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect('/')
