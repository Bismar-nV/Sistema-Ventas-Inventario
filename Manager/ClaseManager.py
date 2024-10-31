import pyodbc

class ClaseManager:
    def __init__(self):
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=NOGALES\\NOGALES;'  
            'DATABASE=PDI_RegistroDigital_1;'
            'UID=sa;'
            'PWD=13652938'
        )

    def add_clase(self, materia_id, docente_id, aula_id, horario, estado):
        query = '''INSERT INTO Clase (materia_id, docente_id, aula_id, horario, estado) 
                   VALUES (?, ?, ?, ?, ?)'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (materia_id, docente_id, aula_id, horario, estado))
            self.connection.commit()
        except Exception as e:
            print(f"Error al agregar clase: {e}")
        finally:
            cursor.close()

    def get_clases(self):
        cursor = self.connection.cursor()
        try:
            query = '''SELECT c.id, c.materia_id, m.nombre as materia_nombre, 
                              c.docente_id, d.nombre as docente_nombre, 
                              c.aula_id, a.nombre as aula_nombre, 
                              c.horario, c.estado
                       FROM Clase c
                       LEFT JOIN Materia m ON c.materia_id = m.id
                       LEFT JOIN Docente d ON c.docente_id = d.id
                       LEFT JOIN Aula a ON c.aula_id = a.id'''
            cursor.execute(query)
            clases = cursor.fetchall()
            return clases
        except Exception as e:
            print(f"Error al obtener clases: {e}")
            return []
        finally:
            cursor.close()

    def update_clase(self, clase_id, materia_id, docente_id, aula_id, horario, estado):
        query = '''UPDATE Clase SET materia_id = ?, docente_id = ?, aula_id = ?, horario = ?, estado = ? WHERE id = ?'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (materia_id, docente_id, aula_id, horario, estado, clase_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al actualizar clase: {e}")
        finally:
            cursor.close()

    def delete_clase(self, clase_id):
        query = '''UPDATE Clase SET estado = ? WHERE id = ?'''
        cursor = self.connection.cursor()
        try:
            estado_inactivo = 0  # Suponiendo que el estado 0 indica "inactivo"
            cursor.execute(query, (estado_inactivo, clase_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al cambiar el estado de la clase: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        try:
            self.connection.close()
            print("Conexión cerrada")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")