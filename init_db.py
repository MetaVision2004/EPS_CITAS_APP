import mysql.connector
from config import Config
import re

def init_db():
    try:
        print("Conectando a la base de datos...")
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=Config.MYSQL_PORT,
            database=Config.MYSQL_DB
        )
        cursor = conn.cursor()
        
        print("Leyendo archivo SQL...")
        with open('eps_citas_db.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
        # Remover comentarios
        sql_content = re.sub(r'--.*?\n', '', sql_content)
        sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
        
        # Separar por punto y coma (;) cuidando de no romper bloques internos
        # Pero los comandos de creación son sencillos aquí
        commands = sql_content.split(';')
        
        print("Ejecutando comandos SQL...")
        for command in commands:
            cmd = command.strip()
            if cmd:
                try:
                    cursor.execute(cmd)
                    print(f"Ejecutado: {cmd[:50]}...")
                except Exception as ex:
                    print(f"Error en comando: {str(ex)}")
        
        conn.commit()
        print("¡Base de datos inicializada exitosamente!")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")

if __name__ == "__main__":
    init_db()
