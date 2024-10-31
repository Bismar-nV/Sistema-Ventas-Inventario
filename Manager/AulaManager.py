import pyodbc

class AulaManager:
    def __init__(self):
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=NOGALES\\NOGALES;'  
            'DATABASE=PDI_RegistroDigital_1;'
            'UID=sa;'
            'PWD=13652938'
        )

    def add_aula(self, nombre, ubicacion, estado):
        query = '''INSERT INTO Aula (nombre, ubicacion, estado) 
                   VALUES (?, ?, ?)'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (nombre, ubicacion, estado))
            self.connection.commit()
        except Exception as e:
            print(f"Error al agregar aula: {e}")
        finally:
            cursor.close()

    def get_aulas(self):
        cursor = self.connection.cursor()
        try:
            query = "SELECT * FROM Aula"
            cursor.execute(query)
            aulas = cursor.fetchall()
            return aulas
        except Exception as e:
            print(f"Error al obtener aulas: {e}")
            return []
        finally:
            cursor.close()

    def update_aula(self, aula_id, nombre, ubicacion, estado):
        query = '''UPDATE Aula SET nombre = ?, ubicacion = ?, estado = ? WHERE id = ?'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (nombre, ubicacion, estado, aula_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al actualizar aula: {e}")
        finally:
            cursor.close()

    def delete_aula(self, aula_id):
        query = '''UPDATE Aula SET estado = ? WHERE id = ?'''
        cursor = self.connection.cursor()
        try:
            estado_inactivo = 0  # Suponiendo que el estado 0 indica "inactivo"
            cursor.execute(query, (estado_inactivo, aula_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al cambiar el estado del aula: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        try:
            self.connection.close()
            print("Conexión cerrada")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
