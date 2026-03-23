import mysql.connector
from config import Config

def migrate():
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
        
        # Verificar si la columna 'estado' ya existe
        cursor.execute("DESCRIBE citas")
        columns = [column[0] for column in cursor.fetchall()]
        
        if 'estado' not in columns:
            print("Agregando la columna 'estado' a la tabla 'citas'...")
            cursor.execute("ALTER TABLE citas ADD COLUMN estado VARCHAR(20) DEFAULT 'Pendiente'")
            conn.commit()
            print("¡Migración completada exitosamente!")
        else:
            print("La columna 'estado' ya existe. No se requiere migración.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error durante la migración: {str(e)}")

if __name__ == "__main__":
    migrate()
