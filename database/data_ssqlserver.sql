-- Crear la base de datos
CREATE DATABASE PDI_RegistroDigital_1;
GO

-- Usar la base de datos
USE PDI_RegistroDigital_1;
GO

-- Tabla de estudiantes
CREATE TABLE Estudiante (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    apellido NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) NOT NULL,
    ci INT NOT NULL, -- Cédula de Identidad
    foto NVARCHAR(255), -- Dirección de la foto almacenada
    estado INT,
    CONSTRAINT UQ_Estudiante_CI UNIQUE (ci) -- Asegura que la CI sea única
);
GO

-- Tabla de docentes
CREATE TABLE Docente (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    apellido NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) NOT NULL,
    ci INT NOT NULL, -- Cédula de Identidad
    foto NVARCHAR(255), -- Dirección de la foto almacenada
    estado INT,
    CONSTRAINT UQ_Docente_CI UNIQUE (ci) -- Asegura que la CI sea única
);
GO

-- Tabla de Carreras
CREATE TABLE Carrera (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    estado INT
);
GO

-- Tabla de Materias
CREATE TABLE Materia (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    carrera_id INT,
    estado INT,
    FOREIGN KEY (carrera_id) REFERENCES Carrera(id)
);
GO

-- Tabla de Aulas
CREATE TABLE Aula (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    ubicacion NVARCHAR(255) NOT NULL,
    estado INT
);
GO

-- Tabla de Clases
CREATE TABLE Clase (
    id INT PRIMARY KEY IDENTITY(1,1),
    materia_id INT,
    docente_id INT,
    aula_id INT,
    horario NVARCHAR(100),
    estado INT,
    FOREIGN KEY (materia_id) REFERENCES Materia(id) ON DELETE CASCADE,
    FOREIGN KEY (docente_id) REFERENCES Docente(id) ON DELETE CASCADE,
    FOREIGN KEY (aula_id) REFERENCES Aula(id) ON DELETE CASCADE
);
GO

-- Tabla de ClaseEstudiante para asociar estudiantes con clases
CREATE TABLE ClaseEstudiante (
    clase_id INT,
    estudiante_id INT,
    PRIMARY KEY (clase_id, estudiante_id), -- Clave primaria compuesta
    FOREIGN KEY (clase_id) REFERENCES Clase(id) ON DELETE CASCADE, -- Relación con la tabla Clase
    FOREIGN KEY (estudiante_id) REFERENCES Estudiante(id) ON DELETE CASCADE -- Relación con la tabla Estudiante
);
GO


-- Tabla de asistencias
CREATE TABLE Asistencia (
    id INT PRIMARY KEY IDENTITY(1,1),
    clase_id INT,
    persona_id INT,
    tipo_persona NVARCHAR(50), -- Puede ser 'Estudiante' o 'Docente'
    nombre NVARCHAR(100),
    fecha DATE,
    hora TIME, -- Nueva columna para almacenar la hora
    presente BIT,
    estado INT,
    FOREIGN KEY (clase_id) REFERENCES Clase(id) ON DELETE CASCADE
);
GO


-- Tabla de Usuarios (Ejemplo)
CREATE TABLE Usuario (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    apellido NVARCHAR(100) NOT NULL,
    ci NVARCHAR(20) NOT NULL,
    rol NVARCHAR(50) NOT NULL, -- Rol del usuario
    username NVARCHAR(100) NOT NULL,
    password NVARCHAR(MAX) NOT NULL,
    verificacion_password NVARCHAR(MAX) NOT NULL,
    estado INT
);
GO

-- Procedimiento almacenado para insertar asistencia
CREATE PROCEDURE InsertarAsistencia1
    @clase_id INT,
    @persona_id INT,
    @tipo_persona NVARCHAR(50),
    @fecha DATE,
    @hora TIME, -- Nueva parámetro para la hora
    @presente BIT,
    @estado INT
AS
BEGIN
    DECLARE @nombre NVARCHAR(100);

    IF @tipo_persona = 'Estudiante'
    BEGIN
        SELECT @nombre = CONCAT(nombre, ' ', apellido)
        FROM Estudiante
        WHERE id = @persona_id;
    END
    ELSE IF @tipo_persona = 'Docente'
    BEGIN
        SELECT @nombre = CONCAT(nombre, ' ', apellido)
        FROM Docente
        WHERE id = @persona_id;
    END

    INSERT INTO Asistencia (clase_id, persona_id, tipo_persona, nombre, fecha, hora, presente, estado)
    VALUES (@clase_id, @persona_id, @tipo_persona, @nombre, @fecha, @hora, @presente, @estado);
END;
GO




-- Usar la base de datos
USE PDI_RegistroDigital;
GO

-- Insertar datos en la tabla Estudiante con la ruta de la foto incluyendo el ci y el nombre
INSERT INTO Estudiante (nombre, apellido, email, ci, foto, estado) VALUES
('Juan', 'Pérez', 'juan.perez@example.com', 123456789, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\123456789_Juan.jpg', 1),
('Maria', 'González', 'maria.gonzalez@example.com', 987654321, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\987654321_María.jpg', 1),
('Carlos', 'Sánchez', 'carlos.sanchez@example.com', 567891234, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\567891234_Carlos.jpg', 1),
('Ana', 'Martínez', 'ana.martinez@example.com', 432198765, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\432198765_Ana.jpg', 1),
('Lucia', 'Fernández', 'lucia.fernandez@example.com', 678123459, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\678123459_Lucía.jpg', 1),
('Pedro', 'Díaz', 'pedro.diaz@example.com', 159753468, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\159753468_Pedro.jpg', 1),
('Elena', 'Gómez', 'elena.gomez@example.com', 951357486, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\951357486_Elena.jpg', 1),
('Jorge', 'López', 'jorge.lopez@example.com', 753159846, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\753159846_Jorge.jpg', 1),
('Laura', 'Morales', 'laura.morales@example.com', 357951486, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\357951486_Laura.jpg', 1),
('Roberto', 'Navarro', 'roberto.navarro@example.com', 258456357, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\258456357_Roberto.jpg', 1);
GO
-- Actualizar la columna 'foto' de la tabla Estudiante
USE PDI_RegistroDigital;
GO

UPDATE Estudiante
SET foto = 'E:\\proyectos finales\\CONTROL-DE-ASITENCIA\\static\\FOTOS_ROSTRO\\' + CAST(ci AS NVARCHAR(10)) + '_' + nombre + '.jpg'
WHERE id IN (SELECT id FROM Estudiante);
GO


UPDATE Estudiante
SET 
    nombre = 'Lucia', -- Reemplaza 'NuevoNombre' con el nombre real deseado
    foto = 'E:\\proyectos finales\\CONTROL-DE-ASITENCIA\\static\\FOTOS_ROSTRO\\' + CAST(ci AS NVARCHAR(10)) + '_NuevoNombre.jpg'
WHERE id = 5; -- Asumiendo que quieres actualizar el estudiante con id 1
GO



-- Insertar datos en la tabla Docente con la ruta de la foto incluyendo el ci y el nombre
INSERT INTO Docente (nombre, apellido, email, ci, foto, estado) VALUES
('Isabel', 'Romero', 'isabel.romero@example.com', 123789456, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\123789456_Isabel.jpg', 1),
('Miguel', 'Ortiz', 'miguel.ortiz@example.com', 789123456, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\789123456_Miguel.jpg', 1),
('Claudia', 'Méndez', 'claudia.mendez@example.com', 456789123, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\456789123_Claudia.jpg', 1),
('Antonio', 'Herrera', 'antonio.herrera@example.com', 321654987, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\321654987_Antonio.jpg', 1),
('Fernando', 'Vega', 'fernando.vega@example.com', 987321654, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\987321654_Fernando.jpg', 1),
('Patricia', 'Suárez', 'patricia.suarez@example.com', 654987321, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\654987321_Patricia.jpg', 1),
('David', 'Paredes', 'david.paredes@example.com', 789456123, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\789456123_David.jpg', 1),
('Marta', 'Rubio', 'marta.rubio@example.com', 123654789, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\123654789_Marta.jpg', 1),
('Susana', 'Campos', 'susana.campos@example.com', 654123789, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\654123789_Susana.jpg', 1),
('Luis', 'Rodríguez', 'luis.rodriguez@example.com', 321789654, 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\321789654_Luis.jpg', 1);
GO
-- Actualizar la columna 'foto' de la tabla Docente
UPDATE Docente
SET foto = 'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO\' + CAST(ci AS NVARCHAR(10)) + '_' + nombre + '.jpg'
WHERE id IN (SELECT id FROM Docente);
GO

-- Insertar datos en la tabla Carrera
INSERT INTO Carrera (nombre, estado) VALUES
('Ingeniería Informática', 1),
('Ingeniería Civil', 1),
('Medicina', 1),
('Derecho', 1),
('Administración de Empresas', 1),
('Psicología', 1),
('Arquitectura', 1),
('Biología', 1),
('Física', 1),
('Ingeniería de Sistemas', 1),
('Ingeniería en Robótica', 1),
('Química', 1);
GO

-- Insertar datos en la tabla Materia
INSERT INTO Materia (nombre, carrera_id, estado) VALUES
('Programación', 1, 1),
('Estructuras', 2, 1),
('Anatomía', 3, 1),
('Derecho Constitucional', 4, 1),
('Contabilidad', 5, 1),
('Psicología General', 6, 1),
('Diseño Arquitectónico', 7, 1),
('Genética', 8, 1),
('Física Cuántica', 9, 1),
('Química Orgánica', 10, 1),
('Programación Avanzada', 1, 1),
('Estructuras de Datos', 1, 1),
('Inteligencia Artificial', 1, 1),
('Desarrollo de Software', 1, 1),
('Redes y Seguridad', 1, 1),
('Fundamentos de Robótica', 2, 1),
('Robótica Aplicada', 2, 1),
('Sistemas de Control', 2, 1),
('Visión por Computadora', 2, 1),
('Automatización y Mecatrónica', 2, 1);
GO

-- Insertar datos en la tabla Aula
INSERT INTO Aula (nombre, ubicacion, estado) VALUES
('Aula 101', 'Edificio A, Planta Baja', 1),
('Aula 102', 'Edificio A, Planta Alta', 1),
('Laboratorio de Física', 'Edificio B, Planta Baja', 1),
('Laboratorio de Química', 'Edificio B, Planta Alta', 1),
('Aula de Diseño', 'Edificio C, Planta Baja', 1),
('Aula de Psicología', 'Edificio C, Planta Alta', 1),
('Aula 201', 'Edificio D, Planta Baja', 1),
('Aula 202', 'Edificio D, Planta Alta', 1),
('Aula de Derecho', 'Edificio E, Planta Baja', 1),
('Aula de Medicina', 'Edificio E, Planta Alta', 1),
('Aula 101', 'Edificio Principal, Planta Baja', 1),
('Aula 102', 'Edificio Principal, Planta Alta', 1),
('Laboratorio de Programación', 'Edificio de Ingeniería, Planta Baja', 1),
('Laboratorio de Redes', 'Edificio de Ingeniería, Planta Baja', 1),
('Laboratorio de IA', 'Edificio de Ingeniería, Planta Alta', 1),
('Sala de Diseño de Software', 'Edificio de Ingeniería, Planta Alta', 1),
('Laboratorio de Robótica 1', 'Edificio de Robótica, Planta Baja', 1),
('Laboratorio de Robótica 2', 'Edificio de Robótica, Planta Baja', 1),
('Sala de Sistemas de Control', 'Edificio de Robótica, Planta Alta', 1),
('Laboratorio de Visión por Computadora', 'Edificio de Robótica, Planta Alta', 1);
GO

-- Insertar datos en la tabla Clase
INSERT INTO Clase (materia_id, docente_id, aula_id, horario, estado) VALUES
(1, 1, 1, 'Lunes 09:00-11:00', 1),
(2, 2, 2, 'Martes 09:00-11:00', 1),
(3, 3, 3, 'Miércoles 09:00-11:00', 1),
(4, 4, 4, 'Jueves 09:00-11:00', 1),
(5, 5, 5, 'Viernes 09:00-11:00', 1),
(6, 6, 6, 'Lunes 12:00-14:00', 1),
(7, 7, 7, 'Martes 12:00-14:00', 1),
(8, 8, 8, 'Miércoles 12:00-14:00', 1),
(9, 9, 9, 'Jueves 12:00-14:00', 1),
(10, 10, 10, 'Viernes 12:00-14:00', 1);
GO

-- Insertar datos en la tabla ClaseEstudiante
INSERT INTO ClaseEstudiante (clase_id, estudiante_id) VALUES
(1, 21), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
(2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 10),
(3, 7), (3, 8), (3, 9), (3, 1), (3, 2), (3, 6),
(4, 10), (4, 1), (4, 2), (4, 3), (4, 7), (4, 9),
(5, 3), (5, 4), (5, 5), (5, 8), (5, 9), (5, 10),
(6, 6), (6, 7), (6, 8), (6, 1), (6, 2), (6, 3),
(7, 9), (7, 10), (7, 1), (7, 4), (7, 5), (7, 6),
(8, 2), (8, 3), (8, 4), (8, 7), (8, 8), (8, 10),
(9, 5), (9, 6), (9, 7), (9, 9), (9, 10), (9, 1),
(10, 8), (10, 9), (10, 10), (10, 2), (10, 3), (10, 4);
GO


SELECT Asistencia.id, Clase.nombre AS clase_nombre, Asistencia.nombre, Asistencia.tipo_persona, Asistencia.fecha, Asistencia.presente, Asistencia.estado
FROM Asistencia
JOIN Clase ON Asistencia.clase_id = Clase.id



-- Ejemplo de inserciones en la tabla Usuario
INSERT INTO Usuario (nombre, apellido, ci, rol, username, password, verificacion_password, estado)
VALUES 
('Juan', 'Pérez', '12345678', 'Administrador', 'jperez', 'hashed_password_1', 'hashed_password_1', 1),
('Ana', 'Gómez', '87654321', 'Vendedor', 'agomez', 'hashed_password_2', 'hashed_password_2', 1),
('Carlos', 'Sánchez', '11223344', 'Inventario', 'csanchez', 'hashed_password_3', 'hashed_password_3', 1),
('María', 'Lopez', '99887766', 'Cajero', 'mlopez', 'hashed_password_4', 'hashed_password_4', 0),
('Bismar', 'Nogales', '99887799', 'Administrador', 'nogales', 'scrypt:32768:8:1$DDWmzk7pFbw6G3Fq$d19af030784c424c77862808fe34a8858534b90ee558020f7ce91a622405904d15ccaade62bf122e700dd7937a89b3b3d45d513c92f6f9031d9e79a3b26f409e', 'scrypt:32768:8:1$DDWmzk7pFbw6G3Fq$d19af030784c424c77862808fe34a8858534b90ee558020f7ce91a622405904d15ccaade62bf122e700dd7937a89b3b3d45d513c92f6f9031d9e79a3b26f409e', 1),
('Luis', 'Rodríguez', '55667788', 'Supervisor', 'lrodriguez', 'hashed_password_5', 'hashed_password_5', 1);
GO


select *from Usuario

username:mmm 
password:12345