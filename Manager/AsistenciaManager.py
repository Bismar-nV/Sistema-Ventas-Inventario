import pyodbc

class AsistenciaManager:
    def __init__(self):
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=NOGALES\\NOGALES;'  
            'DATABASE=PDI_RegistroDigital_1;'
            'UID=sa;'
            'PWD=13652938'
        )

    def get_all_asistencias(self):
        query = '''
        SELECT Asistencia.id, Clase.nombre AS clase_nombre, Asistencia.nombre, Asistencia.tipo_persona, Asistencia.fecha, Asistencia.hora, Asistencia.presente, Asistencia.estado
        FROM Asistencia
        JOIN Clase ON Asistencia.clase_id = Clase.id
        '''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            asistencias = cursor.fetchall()
            results = []
            for asistencia in asistencias:
                results.append({
                    'id': asistencia.id,
                    'clase_nombre': asistencia.clase_nombre,
                    'nombre': asistencia.nombre,
                    'tipo_persona': asistencia.tipo_persona,
                    'fecha': asistencia.fecha.strftime('%Y-%m-%d'),
                    'hora': asistencia.hora.strftime('%H:%M:%S'),  # Asegúrate de que la hora está en el formato correcto
                    'presente': asistencia.presente,
                    'estado': asistencia.estado
                })
            return results
        except Exception as e:
            print(f"Error al obtener asistencias: {e}")
            return []
        finally:
            cursor.close()

    def get_asistencia(self):
        cursor = self.connection.cursor()
        try:
            query = "SELECT * FROM Asistencia"
            cursor.execute(query)
            asistencia = cursor.fetchall()
            return asistencia
        except Exception as e:
            print(f"Error al obtener Asistencia: {e}")
            return []
        finally:
            cursor.close()

    def add_asistencia(self, clase_id, persona_id, tipo_persona, fecha, hora, presente):
        cursor = self.connection.cursor()
        try:
            query = '''
            EXEC InsertarAsistencia @clase_id = ?, @persona_id = ?, @tipo_persona = ?, @fecha = ?, @hora = ?, @presente = ?, @estado = 1
            '''
            cursor.execute(query, (clase_id, persona_id, tipo_persona, fecha, hora, presente))
            self.connection.commit()
        except Exception as e:
            print(f"Error al agregar asistencia: {e}")
        finally:
            cursor.close()

    def update_asistencia(self, asistencia_id, presente, estado):
        query = '''
        UPDATE Asistencia SET presente = ?, estado = ?
        WHERE id = ?
        '''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (presente, estado, asistencia_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al actualizar asistencia: {e}")
        finally:
            cursor.close()

    def delete_asistencia(self, asistencia_id):
        query = '''
        UPDATE Asistencia SET estado = 0 WHERE id = ?
        '''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (asistencia_id,))
            self.connection.commit()
        except Exception as e:
            print(f"Error al cambiar el estado de la asistencia: {e}")
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
    asistencia_manager = AsistenciaManager()
    asistencias = asistencia_manager.get_all_asistencias()
    for asistencia in asistencias:
        print(asistencia)
    asistencia_manager.close_connection()
