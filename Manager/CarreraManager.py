import pyodbc

class CarreraManager:
    def __init__(self):
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=NOGALES\\NOGALES;'  
            'DATABASE=PDI_RegistroDigital_1;'
            'UID=sa;'
            'PWD=13652938'
        )

    def add_carrera(self, nombre, estado):
        query = '''INSERT INTO Carrera (nombre, estado) 
                   VALUES (?, ?)'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (nombre, estado))
            self.connection.commit()
        except Exception as e:
            print(f"Error al agregar carrera: {e}")
        finally:
            cursor.close()

    def get_carreras(self):
        cursor = self.connection.cursor()
        try:
            query = "SELECT * FROM Carrera"
            cursor.execute(query)
            carreras = cursor.fetchall()
            return carreras
        except Exception as e:
            print(f"Error al obtener carreras: {e}")
            return []
        finally:
            cursor.close()

    def update_carrera(self, carrera_id, nombre, estado):
        query = '''UPDATE Carrera SET nombre = ?, estado = ? WHERE id = ?'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (nombre, estado, carrera_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al actualizar carrera: {e}")
        finally:
            cursor.close()

    def delete_carrera(self, carrera_id):
        query = '''UPDATE Carrera SET estado = ? WHERE id = ?'''
        cursor = self.connection.cursor()
        try:
            estado_inactivo = 0  # Suponiendo que el estado 0 indica "inactivo"
            cursor.execute(query, (estado_inactivo, carrera_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al cambiar el estado de la carrera: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        try:
            self.connection.close()
            print("Conexión cerrada")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")