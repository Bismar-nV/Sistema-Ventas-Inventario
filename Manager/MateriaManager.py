import pyodbc

class MateriaManager:
    def __init__(self):
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=NOGALES\\NOGALES;'  
            'DATABASE=PDI_RegistroDigital_1;'
            'UID=sa;'
            'PWD=13652938'
        )

    def add_materia(self, nombre, carrera_id, estado):
        query = '''INSERT INTO Materia (nombre, carrera_id, estado) 
                   VALUES (?, ?, ?)'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (nombre, carrera_id, estado))
            self.connection.commit()
        except Exception as e:
            print(f"Error al agregar materia: {e}")
        finally:
            cursor.close()

    def get_materias(self):
        cursor = self.connection.cursor()
        try:
            query = '''SELECT m.id, m.nombre, m.carrera_id, c.nombre as carrera_nombre, m.estado
                       FROM Materia m
                       LEFT JOIN Carrera c ON m.carrera_id = c.id'''
            cursor.execute(query)
            materias = cursor.fetchall()
            return materias
        except Exception as e:
            print(f"Error al obtener materias: {e}")
            return []
        finally:
            cursor.close()

    def update_materia(self, materia_id, nombre, carrera_id, estado):
        query = '''UPDATE Materia SET nombre = ?, carrera_id = ?, estado = ? WHERE id = ?'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (nombre, carrera_id, estado, materia_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al actualizar materia: {e}")
        finally:
            cursor.close()

    def delete_materia(self, materia_id):
        query = '''UPDATE Materia SET estado = ? WHERE id = ?'''
        cursor = self.connection.cursor()
        try:
            estado_inactivo = 0  # Suponiendo que el estado 0 indica "inactivo"
            cursor.execute(query, (estado_inactivo, materia_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al cambiar el estado de la materia: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        try:
            self.connection.close()
            print("Conexión cerrada")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
