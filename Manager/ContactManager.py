import pyodbc

class AdministradorDeContactos:
    def __init__(self):
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=NOGALES\\BISMAR;'  
            'DATABASE=PDI_RegistroDigital_1;'
            'UID=sa;'
            'PWD=13652938'
        )
    
    def agregar_aula(self, nombre, ubicacion):
        consulta = '''INSERT INTO Aula (nombre, ubicacion) 
                      VALUES (?, ?)'''
        cursor = self.connection.cursor()
        cursor.execute(consulta, (nombre, ubicacion))
        self.connection.commit()

    def obtener_aulas(self):
        consulta = "SELECT * FROM Aula"
        cursor = self.connection.cursor()
        cursor.execute(consulta)
        return cursor.fetchall()

    def actualizar_aula(self, aula_id, nombre, ubicacion):
        consulta = '''UPDATE Aula SET nombre = ?, ubicacion = ? WHERE id = ?'''
        cursor = self.connection.cursor()
        cursor.execute(consulta, (nombre, ubicacion, aula_id))
        self.connection.commit()

    def eliminar_aula(self, aula_id):
        consulta = "DELETE FROM Aula WHERE id = ?"
        cursor = self.connection.cursor()
        cursor.execute(consulta, (aula_id,))
        self.connection.commit()
