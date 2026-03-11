import mysql.connector
from domain.ports import AccesoRepository
from domain.models import Acceso
from typing import List

class MySQLAccesoRepository(AccesoRepository):
    def __init__(self, host, user, password, database):
        self.config = {'host': host, 'user': user, 'password': password, 'database': database}
        self._init_db()

    def _init_db(self):
        """Crea la tabla automáticamente si no existe"""
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accesos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                empleado VARCHAR(255) NOT NULL,
                area VARCHAR(255) NOT NULL,
                hora VARCHAR(255) NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()

    def save(self, acceso: Acceso) -> Acceso:
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()
        query = "INSERT INTO accesos (empleado, area, hora) VALUES (%s, %s, %s)"
        cursor.execute(query, (acceso.empleado, acceso.area, acceso.hora))
        conn.commit()
        acceso.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return acceso

    def get_all(self) -> List[Acceso]:
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM accesos")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Acceso(**row) for row in rows]