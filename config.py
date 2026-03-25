import os

class Config:
    MYSQL_HOST = os.getenv("MYSQLHOST")
    MYSQL_USER = os.getenv("MYSQLUSER")
    MYSQL_PASSWORD = os.getenv("MYSQLPASSWORD")
    MYSQL_PORT = int(os.getenv("MYSQLPORT", "3306"))
    MYSQL_DB = os.getenv("MYSQLDATABASE")
    SECRET_KEY = "3f82b7c6a9d4e1f50c38a29b47d6e8f15a9c2b4d7e0f3a6c9b148d5e2f7a0c3b"
