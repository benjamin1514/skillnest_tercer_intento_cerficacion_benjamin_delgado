
from flask_app.config.mysqlconnection import connectToMySQL


class Donacion:

    def __init__(self, data):
        self.id_donacion = data['id_donacion']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.id_usuario = data['id_usuario']

    @classmethod
    def obtener_todas(cls):
        query = """
            SELECT donaciones.*, usuarios.nombre AS donador
            FROM donaciones
            JOIN usuarios
                ON donaciones.id_usuario = usuarios.id_usuario
            ORDER BY donaciones.id_donacion DESC;
        """
        resultados = connectToMySQL("DonacionPeluches").query_db(query)

        return [cls(donacion) for donacion in resultados]

    @classmethod
    def obtener_por_id(cls, data):
        query = """
            SELECT donaciones.*, usuarios.nombre AS donador
            FROM donaciones
            JOIN usuarios
                ON donaciones.id_usuario = usuarios.id_usuario
            WHERE donaciones.id_donacion = %(id_donacion)s;
        """
        resultados = connectToMySQL("DonacionPeluches").query_db(
            query, data
        )

        if resultados:
            return cls(resultados[0])

        return None

    @staticmethod
    def crear(data):
        query = """
            INSERT INTO donaciones (nombre, descripcion, id_usuario)
            VALUES (%(nombre)s, %(descripcion)s, %(id_usuario)s);
        """
        return connectToMySQL("DonacionPeluches").query_db(query, data)

    @staticmethod
    def actualizar(data):
        query = """
            UPDATE donaciones
            SET nombre = %(nombre)s,
                descripcion = %(descripcion)s
            WHERE id_donacion = %(id_donacion)s
              AND id_usuario = %(id_usuario)s;
        """
        return connectToMySQL("DonacionPeluches").query_db(query, data)

    @staticmethod
    def eliminar(data):
        query = """
            DELETE FROM donaciones
            WHERE id_donacion = %(id_donacion)s
              AND id_usuario = %(id_usuario)s;
        """
        return connectToMySQL("DonacionPeluches").query_db(query, data)
