
# Define operaciones de usuarios
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

email_regex = re.compile(
    r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
)

nombre_regex = re.compile(r'^[a-zA-Z]{2,}$')
apellido_regex = re.compile(r'^[a-zA-Z]{2,}$')


class Usuario:

    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password_hash = data['password_hash']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Valida los datos del usuario
    @staticmethod
    def validar_usuario(usuario):
        is_valid = True

        nombre = usuario.get('nombre', '').strip()
        apellido = usuario.get('apellido', '').strip()
        email = usuario.get('email', '').strip()
        password = usuario.get('password', '')
        confirm_password = usuario.get('confirm_password', '')

        if not nombre_regex.fullmatch(nombre):
            flash(
                "El nombre debe tener al menos 2 letras.",
                "error_nombre"
            )
            is_valid = False

        if not apellido_regex.fullmatch(apellido):
            flash(
                "El apellido debe tener al menos 2 letras.",
                "error_apellido"
            )
            is_valid = False

        if not email_regex.fullmatch(email):
            flash(
                "Correo electrónico inválido.",
                "error_email"
            )
            is_valid = False

        if len(password) < 8:
            flash(
                "La contraseña debe tener al menos 8 caracteres.",
                "error_password"
            )
            is_valid = False

        if password != confirm_password:
            flash(
                "Las contraseñas no coinciden.",
                "error_confirm_password"
            )
            is_valid = False

        return is_valid

    # Guarda un usuario en la base de datos
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios
                (nombre, apellido, email, password_hash)
            VALUES
                (%(nombre)s, %(apellido)s, %(email)s, %(password_hash)s);
        """

        return connectToMySQL(
            "DonacionPeluches"
        ).query_db(query, data)

    # Obtiene un usuario por su correo
    @classmethod
    def get_by_email(cls, email):
        query = """
            SELECT *
            FROM usuarios
            WHERE email = %(email)s;
        """

        result = connectToMySQL(
            "DonacionPeluches"
        ).query_db(query, {'email': email})

        if result is False:
            return False

        if result:
            return cls(result[0])

        return None

    # Obtiene un usuario por su ID
    @classmethod
    def get_by_id(cls, id_usuario):
        query = """
            SELECT *
            FROM usuarios
            WHERE id_usuario = %(id_usuario)s;
        """

        result = connectToMySQL(
            "DonacionPeluches"
        ).query_db(query, {'id_usuario': id_usuario})

        if result is False:
            return False

        if result:
            return cls(result[0])

        return None
