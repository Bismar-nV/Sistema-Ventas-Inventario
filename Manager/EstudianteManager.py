import pyodbc

class EstudianteManager:
    def __init__(self):
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=NOGALES\\NOGALES;'  
            'DATABASE=PDI_RegistroDigital_1;'
            'UID=sa;'
            'PWD=13652938'
        )

    def add_estudiante(self, nombre, apellido, email, ci, foto, estado=1):
        query = '''INSERT INTO Estudiante (nombre, apellido, email, ci, foto, estado) 
                   VALUES (?, ?, ?, ?, ?, ?)'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (nombre, apellido, email, ci, foto, estado))
            self.connection.commit()
        except Exception as e:
            print(f"Error al agregar estudiante: {e}")
        finally:
            cursor.close()

    def get_estudiantes(self):
        cursor = self.connection.cursor()
        try:
            query = "SELECT * FROM Estudiante"
            cursor.execute(query)
            estudiantes = cursor.fetchall()
            return estudiantes
        except Exception as e:
            print(f"Error al obtener estudiantes: {e}")
            return []
        finally:
            cursor.close()

    def update_estudiante(self, estudiante_id, nombre, apellido, email, ci, foto, estado=1):
        cursor = self.connection.cursor()
        try:
            if foto:
                query = '''UPDATE Estudiante SET nombre = ?, apellido = ?, email = ?, ci = ?, foto = ?, estado = ? WHERE id = ?'''
                cursor.execute(query, (nombre, apellido, email, ci, foto, estado, estudiante_id))
            else:
                query = '''UPDATE Estudiante SET nombre = ?, apellido = ?, email = ?, ci = ?, estado = ? WHERE id = ?'''
                cursor.execute(query, (nombre, apellido, email, ci, estado, estudiante_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al actualizar estudiante: {e}")
        finally:
            cursor.close()

    def delete_estudiante(self, estudiante_id):
        query = '''UPDATE Estudiante SET estado = 0 WHERE id = ?'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (estudiante_id,))
            self.connection.commit()
        except Exception as e:
            print(f"Error al cambiar el estado del estudiante: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        try:
            self.connection.close()
            print("Conexión cerrada")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    estudiante_manager = EstudianteManager()
    estudiantes = estudiante_manager.get_estudiantes()
    for estudiante in estudiantes:
        print(estudiante)
    estudiante_manager.close_connection()
