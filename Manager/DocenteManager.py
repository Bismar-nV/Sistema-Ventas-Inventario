import pyodbc

class DocenteManager:
    def __init__(self):
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=NOGALES\\NOGALES;'  
            'DATABASE=PDI_RegistroDigital_1;'
            'UID=sa;'
            'PWD=13652938'
        )

    def add_docente(self, nombre, apellido, email, ci, foto, estado=1):
        query = '''INSERT INTO Docente (nombre, apellido, email, ci, foto, estado) 
                   VALUES (?, ?, ?, ?, ?, ?)'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (nombre, apellido, email, ci, foto, estado))
            self.connection.commit()
        except Exception as e:
            print(f"Error al agregar docente: {e}")
        finally:
            cursor.close()

    def get_docentes(self):
        cursor = self.connection.cursor()
        try:
            query = "SELECT * FROM Docente"
            cursor.execute(query)
            docentes = cursor.fetchall()
            return docentes
        except Exception as e:
            print(f"Error al obtener docentes: {e}")
            return []
        finally:
            cursor.close()

    def update_docente(self, docente_id, nombre, apellido, email, ci, foto, estado=1):
        cursor = self.connection.cursor()
        try:
            if foto:
                query = '''UPDATE Docente SET nombre = ?, apellido = ?, email = ?, ci = ?, foto = ?, estado = ? WHERE id = ?'''
                cursor.execute(query, (nombre, apellido, email, ci, foto, estado, docente_id))
            else:
                query = '''UPDATE Docente SET nombre = ?, apellido = ?, email = ?, ci = ?, estado = ? WHERE id = ?'''
                cursor.execute(query, (nombre, apellido, email, ci, estado, docente_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al actualizar docente: {e}")
        finally:
            cursor.close()

    def delete_docente(self, docente_id):
        query = '''UPDATE Docente SET estado = 0 WHERE id = ?'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (docente_id,))
            self.connection.commit()
        except Exception as e:
            print(f"Error al cambiar el estado del docente: {e}")
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
    docente_manager = DocenteManager()
    docentes = docente_manager.get_docentes()
    for docente in docentes:
        print(docente)
    docente_manager.close_connection()
