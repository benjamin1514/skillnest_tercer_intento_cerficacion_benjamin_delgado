
# Controlador de donaciones
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.donacion import Donacion


# Mostrar todos los peluches
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    donaciones = Donacion.obtener_todas()

    if donaciones is False:
        flash('Error al cargar los peluches.', 'error')
        donaciones = []

    return render_template(
        'dashboard.html',
        donaciones=donaciones
    )


# Mostrar formulario para crear una donación
@app.route('/nueva')
def nueva_donacion():
    if 'user_id' not in session:
        return redirect('/')

    return render_template('nueva.html')


# Crear una donación
@app.route('/crear', methods=['POST'])
def crear_donacion():
    if 'user_id' not in session:
        return redirect('/')

    nombre = request.form.get('nombre', '').strip()
    descripcion = request.form.get('descripcion', '').strip()

    # Validar campos obligatorios
    if len(nombre) < 2:
        flash('El nombre debe tener al menos 2 caracteres.', 'error')
        return redirect('/nueva')

    if not descripcion:
        flash('La descripción no puede estar vacía.', 'error')
        return redirect('/nueva')

    # Crear donación
    resultado = Donacion.crear({
        'nombre': nombre,
        'descripcion': descripcion,
        'id_usuario': session['user_id']
    })

    if resultado is False or not resultado:
        flash('No se pudo crear la donación.', 'error')
        return redirect('/nueva')

    flash('¡Pel uche donado correctamente!'.replace('Pel uche', 'Peluche'), 'success')
    return redirect('/dashboard')


# Ver los detalles de un peluche
@app.route('/ver/<int:id_donacion>')
def ver_donacion(id_donacion):
    if 'user_id' not in session:
        return redirect('/')

    donacion = Donacion.obtener_por_id({
        'id_donacion': id_donacion
    })

    if donacion is False:
        flash('Error al consultar el peluche.', 'error')
        return redirect('/dashboard')

    if donacion is None:
        flash('El peluche no existe.', 'error')
        return redirect('/dashboard')

    return render_template('ver.html', donacion=donacion)


# Mostrar formulario de edición
@app.route('/editar/<int:id_donacion>')
def editar_donacion(id_donacion):
    if 'user_id' not in session:
        return redirect('/')

    donacion = Donacion.obtener_por_id({
        'id_donacion': id_donacion
    })

    if donacion is False:
        flash('Error al consultar el peluche.', 'error')
        return redirect('/dashboard')

    if donacion is None:
        flash('El peluche no existe.', 'error')
        return redirect('/dashboard')

    if donacion.id_usuario != session['user_id']:
        flash('Solo puedes editar tus propias donaciones.', 'error')
        return redirect('/dashboard')

    return render_template('editar.html', donacion=donacion)


# Actualizar una donación
@app.route('/actualizar/<int:id_donacion>', methods=['POST'])
def actualizar_donacion(id_donacion):
    if 'user_id' not in session:
        return redirect('/')

    donacion = Donacion.obtener_por_id({
        'id_donacion': id_donacion
    })

    if donacion is False:
        flash('Error al consultar el peluche.', 'error')
        return redirect('/dashboard')

    if donacion is None or donacion.id_usuario != session['user_id']:
        flash('No puedes editar esta donación.', 'error')
        return redirect('/dashboard')

    nombre = request.form.get('nombre', '').strip()
    descripcion = request.form.get('descripcion', '').strip()

    if len(nombre) < 2:
        flash('El nombre debe tener al menos 2 caracteres.', 'error')
        return redirect(f'/editar/{id_donacion}')

    if not descripcion:
        flash('La descripción no puede estar vacía.', 'error')
        return redirect(f'/editar/{id_donacion}')

    resultado = Donacion.actualizar({
        'id_donacion': id_donacion,
        'nombre': nombre,
        'descripcion': descripcion,
        'id_usuario': session['user_id']
    })

    if resultado is False or resultado is None:
        flash('No se pudo actualizar el peluche.', 'error')
        return redirect(f'/editar/{id_donacion}')

    flash('Donación actualizada correctamente.', 'success')
    return redirect('/dashboard')


# Eliminar una donación
@app.route('/eliminar/<int:id_donacion>', methods=['POST'])
def eliminar_donacion(id_donacion):
    if 'user_id' not in session:
        return redirect('/')

    donacion = Donacion.obtener_por_id({
        'id_donacion': id_donacion
    })

    if donacion is False:
        flash('Error al consultar el peluche.', 'error')
        return redirect('/dashboard')

    if donacion is None or donacion.id_usuario != session['user_id']:
        flash('No puedes eliminar esta donación.', 'error')
        return redirect('/dashboard')

    resultado = Donacion.eliminar({
        'id_donacion': id_donacion,
        'id_usuario': session['user_id']
    })

    if resultado is False or resultado is None:
        flash('No se pudo eliminar el peluche.', 'error')
        return redirect('/dashboard')

    flash('Donación eliminada correctamente.', 'success')
    return redirect('/dashboard')
