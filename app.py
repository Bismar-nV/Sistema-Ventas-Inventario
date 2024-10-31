from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from Manager.EstudianteManager import EstudianteManager
from Manager.DocenteManager import DocenteManager
from Manager.CarreraManager import CarreraManager
from Manager.MateriaManager import MateriaManager
from Manager.AulaManager import AulaManager
from Manager.ClaseManager import ClaseManager
from Manager.UsuarioManager import UsuarioManager 
from Manager.AsistenciaManager import AsistenciaManager  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pyodbc
from functools import wraps
import os
import numpy as np
import os
import cv2
import imutils
import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=NOGALES\\NOGALES;'
        'DATABASE=PDI_RegistroDigital_1;'
        'UID=sa;'
        'PWD=13652938'
    )
    return conn


app = Flask(__name__)
app.secret_key = 'your_secret_key'

estudiante_manager = EstudianteManager()
docente_manager = DocenteManager()
carrera_manager = CarreraManager()
materia_manager = MateriaManager()
aula_manager = AulaManager()
clase_manager = ClaseManager()
usuario_manager = UsuarioManager()
asistencia_manager = AsistenciaManager()


# usuario login y insert y demas
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = usuario_manager.get_user(username)
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrap

@app.route('/usuarios')
@login_required
def usuarios():
    usuarios = usuario_manager.get_all_users()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/add_usuario', methods=['POST'])
@login_required
def add_usuario():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    ci = request.form['ci']
    rol = request.form['rol']
    username = request.form['username']
    password = request.form['password']
    verificacion_password = request.form['verificacion_password']
    
    if password != verificacion_password:
        flash('Las contraseñas no coinciden')
        return redirect(url_for('usuarios'))
    
    hashed_password = generate_password_hash(password)
    hashed_password1 = generate_password_hash(password)
    usuario_manager.add_user(nombre, apellido, ci, rol, username, hashed_password, hashed_password1, 1) # Estado por defecto 1 (Activo)
    flash('Usuario registrado exitosamente')
    return redirect(url_for('usuarios'))

@app.route('/update_usuario', methods=['POST'])
@login_required
def update_usuario():
    usuario_id = request.form['id']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    ci = request.form['ci']
    rol = request.form['rol']
    username = request.form['username']
    estado = request.form['estado']

    usuario_manager.update_user(usuario_id, nombre, apellido, ci, rol, username, estado)
    return redirect(url_for('usuarios'))

@app.route('/delete_usuario/<int:usuario_id>', methods=['POST'])
@login_required
def delete_usuario(usuario_id):
    usuario_manager.delete_user(usuario_id)
    return redirect(url_for('usuarios'))



# Rutas para navegar
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/estudiante')
@login_required
def estudiante():
    clases = clase_manager.get_clases()   
    docentes = docente_manager.get_docentes() 
    materias = materia_manager.get_materias()
    aulas = aula_manager.get_aulas() 
    estudiantes = estudiante_manager.get_estudiantes()
    carreras = carrera_manager.get_carreras()
    return render_template('estudiante.html', clases=clases, docentes=docentes, materias=materias, 
                            aulas=aulas, carreras=carreras,   estudiantes=estudiantes)

@app.route('/docente')
@login_required
def docente():
    clases = clase_manager.get_clases()   
    docentes = docente_manager.get_docentes() 
    materias = materia_manager.get_materias()
    aulas = aula_manager.get_aulas() 
    estudiantes = estudiante_manager.get_estudiantes()
    carreras = carrera_manager.get_carreras()
    return render_template('docente.html', clases=clases, docentes=docentes, materias=materias, 
                            aulas=aulas, carreras=carreras,   estudiantes=estudiantes)

@app.route('/carrera')
@login_required
def carrera():
    clases = clase_manager.get_clases()   
    docentes = docente_manager.get_docentes() 
    materias = materia_manager.get_materias()
    aulas = aula_manager.get_aulas() 
    estudiantes = estudiante_manager.get_estudiantes()
    carreras = carrera_manager.get_carreras()
    return render_template('carrera.html' , clases=clases, docentes=docentes, materias=materias, 
                            aulas=aulas, carreras=carreras,   estudiantes=estudiantes)

@app.route('/materia')
@login_required
def materia():
    clases = clase_manager.get_clases()   
    docentes = docente_manager.get_docentes() 
    materias = materia_manager.get_materias()
    aulas = aula_manager.get_aulas() 
    estudiantes = estudiante_manager.get_estudiantes()
    carreras = carrera_manager.get_carreras()
    return render_template('materia.html', clases=clases, docentes=docentes, materias=materias, 
                            aulas=aulas, carreras=carreras,   estudiantes=estudiantes)

@app.route('/aula')
@login_required
def aula():
    clases = clase_manager.get_clases()   
    docentes = docente_manager.get_docentes() 
    materias = materia_manager.get_materias()
    aulas = aula_manager.get_aulas() 
    estudiantes = estudiante_manager.get_estudiantes()
    carreras = carrera_manager.get_carreras()
    return render_template('aulas.html', clases=clases, docentes=docentes, materias=materias, 
                            aulas=aulas, carreras=carreras,   estudiantes=estudiantes)

@app.route('/clases')
@login_required
def clases():
    clases = clase_manager.get_clases()   
    docentes = docente_manager.get_docentes() 
    materias = materia_manager.get_materias()
    aulas = aula_manager.get_aulas() 
    estudiantes = estudiante_manager.get_estudiantes()
    carreras = carrera_manager.get_carreras()
    return render_template('clase.html', clases=clases, docentes=docentes, materias=materias, 
                            aulas=aulas, carreras=carreras,   estudiantes=estudiantes)

# Rutas para estudiantes
@app.route('/add_estudiante', methods=['POST'])
@login_required
def add_estudiante():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    ci = request.form['ci']
    # Estado siempre 1 para nuevo estudiante
    estado = 1
    # Ruta de la foto  E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_ROSTRO
    foto_path = f"E:\\getion 2024 1 univalle  trabajos\\proyectos finales\\CONTROL-DE-ASITENCIA\static\\FOTOS_ROSTRO\\{ci}_{nombre}"
    estudiante_manager.add_estudiante(nombre, apellido, email, ci, foto_path, estado)
    subprocess.Popen(["python", "E:\\getion 2024 1 univalle  trabajos\\proyectos finales\\CONTROL-DE-ASITENCIA\\Manager\\entrenandoRF.py"])
    return redirect(url_for('estudiante'))


@app.route('/delete_estudiante/<int:estudiante_id>', methods=['POST'])
@login_required
def delete_estudiante(estudiante_id):
    estudiante_manager.delete_estudiante(estudiante_id)
    return redirect(url_for('estudiante'))

@app.route('/update_estudiante', methods=['POST'])
@login_required
def update_estudiante():
    estudiante_id = request.form['id']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    ci = request.form['ci']
    estado = int(request.form['estado'])
    foto = request.form['foto']
    # Ruta de la foto
    foto = f"E:\\getion 2024 1 univalle  trabajos\\proyectos finales\\CONTROL-DE-ASITENCIA\\static\\FOTOS_ROSTRO\\{ci}_{nombre}\\rostro_10.jpg"

    if not os.path.exists(foto):
        foto = None

    estudiante_manager.update_estudiante(estudiante_id, nombre, apellido, email, ci, foto, estado)
    return redirect(url_for('estudiante'))


#rutas para docentes 
@app.route('/add_docente', methods=['POST'])
@login_required
def add_docente():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    ci = request.form['ci']
    # Estado siempre 1 para nuevo docente
    estado = 1
    # Ruta de la foto
    foto_path = f"E:\\getion 2024 1 univalle  trabajos\\proyectos finales\\CONTROL-DE-ASITENCIA\\static\\FOTOS_ROSTRO\\{ci}_{nombre}"
    docente_manager.add_docente(nombre, apellido, email, ci, foto_path, estado)
    subprocess.Popen(["python", "E:\\getion 2024 1 univalle  trabajos\\proyectos finales\\CONTROL-DE-ASITENCIA\\Manager\\entrenandoRF.py"])
    return redirect(url_for('docente'))

@app.route('/delete_docente/<int:docente_id>', methods=['POST'])
@login_required
def delete_docente(docente_id):
    docente_manager.delete_docente(docente_id)
    return redirect(url_for('docente'))

@app.route('/update_docente', methods=['POST'])
@login_required
def update_docente():
    docente_id = request.form['id']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    ci = request.form['ci']
    estado = int(request.form['estado'])
    foto = f"E:\\getion 2024 1 univalle  trabajos\\proyectos finales\\CONTROL-DE-ASITENCIA\\static\FOTOS_ROSTRO\\{ci}_{nombre}\\rostro_10.jpg"

    if not os.path.exists(foto):
        foto = None

    docente_manager.update_docente(docente_id, nombre, apellido, email, ci, foto, estado)
    return redirect(url_for('docente'))

#capturar foto
@app.route('/capture_photo', methods=['POST'])
@login_required
def capture_photo():
    data = request.json
    ci = data['ci']
    nombre = data['nombre']
    person_name = f"{ci}_{nombre}"
    data_path = r'E:\\getion 2024 1 univalle  trabajos\\proyectos finales\\CONTROL-DE-ASITENCIA\\static\\FOTOS_ROSTRO'
    person_path = os.path.join(data_path, person_name)

    if not os.path.exists(person_path):
        os.makedirs(person_path)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0

    # Crear una ventana con la propiedad de estar al frente
    cv2.namedWindow('frame', cv2.WND_PROP_TOPMOST)
    cv2.setWindowProperty('frame', cv2.WND_PROP_TOPMOST, 1)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aux_frame = frame.copy()

        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rostro = aux_frame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(os.path.join(person_path, f'rostro_{count}.jpg'), rostro)
            count += 1

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1)
        if k == 27 or count >= 50:  # Captura una sola imagen
            break

    cap.release()
    cv2.destroyAllWindows()
    return jsonify(success=True)


# carrera funciona
@app.route('/add_carrera', methods=['POST'])
@login_required
def add_carrera():
    nombre = request.form['nombre']
    estado = request.form['estado']
    carrera_manager.add_carrera(nombre, estado)
    return redirect(url_for('carrera'))

@app.route('/delete_carrera/<int:carrera_id>', methods=['POST'])
@login_required
def delete_carrera(carrera_id):
    carrera_manager.delete_carrera(carrera_id)
    return redirect(url_for('carrera'))

@app.route('/update_carrera', methods=['POST'])
@login_required
def update_carrera():
    carrera_id = request.form['id']
    nombre = request.form['nombre']
    estado = request.form['estado']
    carrera_manager.update_carrera(carrera_id, nombre, estado)
    return redirect(url_for('carrera'))


#materi 
@app.route('/add_materia', methods=['POST'])
@login_required
def add_materia():
    nombre = request.form['nombre']
    carrera_id = request.form['carrera_id']
    estado = request.form['estado']
    materia_manager.add_materia(nombre, carrera_id, estado)
    return redirect(url_for('materia'))

@app.route('/delete_materia/<int:materia_id>', methods=['POST'])
@login_required
def delete_materia(materia_id):
    materia_manager.delete_materia(materia_id)
    return redirect(url_for('materia'))

@app.route('/update_materia', methods=['POST'])
@login_required
def update_materia():
    materia_id = request.form['id']
    nombre = request.form['nombre']
    carrera_id = request.form['carrera_id']
    estado = request.form['estado']
    materia_manager.update_materia(materia_id, nombre, carrera_id, estado)
    return redirect(url_for('materia'))


# aulas 
@app.route('/add_aula', methods=['POST'])
@login_required
def add_aula():
    nombre = request.form['nombre']
    ubicacion = request.form['ubicacion']
    estado = request.form['estado']
    aula_manager.add_aula(nombre, ubicacion, estado)
    return redirect(url_for('aula'))

@app.route('/delete_aula/<int:aula_id>', methods=['POST'])
@login_required
def delete_aula(aula_id):
    aula_manager.delete_aula(aula_id)
    return redirect(url_for('aula'))

@app.route('/update_aula', methods=['POST'])
@login_required
def update_aula():
    aula_id = request.form['id']
    nombre = request.form['nombre']
    ubicacion = request.form['ubicacion']
    estado = request.form['estado']
    aula_manager.update_aula(aula_id, nombre, ubicacion, estado)
    return redirect(url_for('aula'))

#clase 
@app.route('/add_clase', methods=['POST'])
@login_required
def add_clase():
    materia_id = request.form['materia_id']
    docente_id = request.form['docente_id']
    aula_id = request.form['aula_id']
    horario = request.form['horario']
    estado = request.form['estado']
    clase_manager.add_clase(materia_id, docente_id, aula_id, horario, estado)
    return redirect(url_for('clases'))

@app.route('/delete_clase/<int:clase_id>', methods=['POST'])
@login_required
def delete_clase(clase_id):
    clase_manager.delete_clase(clase_id)
    return redirect(url_for('clases'))

@app.route('/update_clase', methods=['POST'])
@login_required
def update_clase():
    clase_id = request.form['id']
    materia_id = request.form['materia_id']
    docente_id = request.form['docente_id']
    aula_id = request.form['aula_id']
    horario = request.form['horario']
    estado = request.form['estado']
    clase_manager.update_clase(clase_id, materia_id, docente_id, aula_id, horario, estado)
    return redirect(url_for('clases'))

#asistencia 
@app.route('/asistencia')
@login_required
def asistencia():
    clases = clase_manager.get_clases() 
    docentes = docente_manager.get_docentes() 
    materias = materia_manager.get_materias()
    aulas = aula_manager.get_aulas() 
    estudiantes = estudiante_manager.get_estudiantes()
    carreras = carrera_manager.get_carreras()
    asistencias = asistencia_manager.get_asistencia()
    return render_template('asistencia.html', asistencias=asistencias, clases=clases, docentes=docentes, materias=materias, 
                            aulas=aulas, carreras=carreras,   estudiantes=estudiantes)


@app.route('/add_asistencia', methods=['POST'])
@login_required
def add_asistencia():
    clase_id = request.form['clase_id']
    persona_id = request.form['persona_id']
    tipo_persona = request.form['tipo_persona']
    fecha = request.form['fecha']
    hora = request.form['hora']
    presente = 'presente' in request.form  # Verifica si el checkbox 'presente' está marcado
    asistencia_manager.add_asistencia(clase_id, persona_id, tipo_persona, fecha, hora, presente)
    return redirect(url_for('asistencia'))

@app.route('/update_asistencia', methods=['POST'])
@login_required
def update_asistencia():
    asistencia_id = request.form['id']
    presente = 1 if 'presente' in request.form else 0
    estado = int(request.form['estado'])
    asistencia_manager.update_asistencia(asistencia_id, presente, estado)
    return redirect(url_for('asistencia'))


@app.route('/delete_asistencia/<int:asistencia_id>', methods=['POST'])
@login_required
def delete_asistencia(asistencia_id):
    asistencia_manager.delete_asistencia(asistencia_id)
    return redirect(url_for('asistencia'))



@app.route('/reconocimiento_facial', methods=['POST'])
@login_required
def reconocimiento_facial_route():
    try:
        subprocess.Popen(["python", "E:\\getion 2024 1 univalle  trabajos\\proyectos finales\\CONTROL-DE-ASITENCIA\\Manager\\reconocimiento_facial.py"])
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'error': str(e)})
    
@app.route('/entrenar_reconocedor', methods=['POST'])
@login_required
def entrenar_reconocedor():
    try:
        subprocess.Popen(["python", "E:\\getion 2024 1 univalle  trabajos\\proyectos finales\\CONTROL-DE-ASITENCIA\\Manager\\entrenandoRF.py"])
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
