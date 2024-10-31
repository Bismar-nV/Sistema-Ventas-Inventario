import pyodbc

class UsuarioManager:
    def __init__(self):
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=NOGALES\\NOGALES;'  
            'DATABASE=PDI_RegistroDigital_1;'
            'UID=sa;'
            'PWD=13652938'
        )

    def get_user(self, username):
        cursor = self.connection.cursor()
        try:
            query = "SELECT * FROM Usuario WHERE username = ?"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
            return None
        finally:
            cursor.close()

    def get_all_users(self):
        cursor = self.connection.cursor()
        try:
            query = "SELECT * FROM Usuario"
            cursor.execute(query)
            users = cursor.fetchall()
            return users
        except Exception as e:
            print(f"Error al obtener los usuarios: {e}")
            return []
        finally:
            cursor.close()

    def add_user(self, nombre, apellido, ci, rol, username, password, verificacion_password, estado):
        cursor = self.connection.cursor()
        try:
            query = '''
                INSERT INTO Usuario (nombre, apellido, ci, rol, username, password, verificacion_password, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(query, (nombre, apellido, ci, rol, username, password, verificacion_password, estado))
            self.connection.commit()
        except Exception as e:
            print(f"Error al agregar usuario: {e}")
        finally:
            cursor.close()

    def update_user(self, usuario_id, nombre, apellido, ci, rol, username, estado):
        cursor = self.connection.cursor()
        try:
            query = '''
                UPDATE Usuario SET nombre = ?, apellido = ?, ci = ?, rol = ?, username = ?, estado = ?
                WHERE id = ?
            '''
            cursor.execute(query, (nombre, apellido, ci, rol, username, estado, usuario_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
        finally:
            cursor.close()

    def delete_user(self, usuario_id):
        cursor = self.connection.cursor()
        try:
            query = "UPDATE Usuario SET estado = 0 WHERE id = ?"
            cursor.execute(query, (usuario_id,))
            self.connection.commit()
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
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
    usuario_manager = UsuarioManager()
    usuarios = usuario_manager.get_all_users()
    for usuario in usuarios:
        print(usuario)
    usuario_manager.close_connection()
