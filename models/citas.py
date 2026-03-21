from database import get_connection

class Cita:

    @staticmethod
    def reservar(documento, medico, tipo_cita, fecha, hora, direccion_eps, estado='Pendiente'):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO citas (documento, medico, tipo_cita, fecha, hora, direccion_eps, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (documento, medico, tipo_cita, fecha, hora, direccion_eps, estado))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def consultar(documento):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT
                pacientes.nombre,
                pacientes.apellido,
                citas.id,
                citas.medico,
                citas.tipo_cita,
                citas.fecha,
                citas.hora,
                citas.direccion_eps,
                citas.estado
            FROM pacientes
            INNER JOIN citas ON pacientes.documento = citas.documento
            WHERE pacientes.documento = %s
            ORDER BY citas.fecha ASC, citas.hora ASC
        """
        cursor.execute(sql, (documento,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    @staticmethod
    def obtener_por_id(cita_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM citas WHERE id = %s", (cita_id,))
        cita = cursor.fetchone()
        cursor.close()
        conn.close()
        return cita

    @staticmethod
    def actualizar(cita_id, medico, tipo_cita, fecha, hora, estado):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE citas
            SET medico = %s, tipo_cita = %s, fecha = %s, hora = %s, estado = %s
            WHERE id = %s
        """
        cursor.execute(sql, (medico, tipo_cita, fecha, hora, estado, cita_id))
        conn.commit()
        cursor.close()
        conn.close()
