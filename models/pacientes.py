from database import get_connection

class Paciente:

    @staticmethod
    def registrar(documento, nombre, apellido, telefono, correo, eps):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO pacientes (documento, nombre, apellido, telefono, correo, eps)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (documento, nombre, apellido, telefono, correo, eps))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def existe(documento):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM pacientes WHERE documento = %s", (documento,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    @staticmethod
    def obtener_por_documento(documento):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pacientes WHERE documento = %s", (documento,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
