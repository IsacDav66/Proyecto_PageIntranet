from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from src.cn.data_base_connection import get_db_connection
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Establece una clave secreta para la sesión

# Configura la carpeta de archivos
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT u.id, u.username, u.class_id, r.role_name 
                    FROM users u 
                    JOIN roles r ON u.role_id = r.id 
                    WHERE u.username=%s AND u.password=%s
                """, (username, password))
                user = cursor.fetchone()
                if user:
                    # Autenticación exitosa
                    session['user_id'] = user[0]
                    session['username'] = user[1]
                    session['class_id'] = user[2]
                    session['role'] = user[3]
                    print(f"Usuario autenticado: {session['username']}, class_id: {session['class_id']}")  # Registro de depuración
                    return redirect(url_for('portal'))
                else:
                    return render_template('login.html', error="Usuario o contraseña incorrectos")
            except Exception as e:
                print(f"Error al interactuar con la base de datos: {e}")
                return render_template('login.html', error="Error al conectar con la base de datos")
            finally:
                conn.close()

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password, role_id) VALUES (%s, %s, (SELECT id FROM roles WHERE role_name = 'administrador'))", (username, password))
                conn.commit()
                return redirect(url_for('login'))
            except Exception as e:
                print(f"Error al interactuar con la base de datos: {e}")
                return render_template('register.html', error="Error al registrar el usuario")
            finally:
                conn.close()

    return render_template('register.html')

# Ruta para el portal digital
@app.route('/portal')
def portal():
    if 'username' in session:
        return render_template('portal.html', username=session['username'], role=session['role'])
    else:
        return redirect(url_for('login'))

# Ruta para añadir estudiantes (solo administradores)
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'role' in session and session['role'] == 'administrador':
        if request.method == 'POST':
            # Lógica para crear una nueva cuenta de estudiante
            username = request.form['username']
            password = request.form['password']

            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO users (username, password, role_id) VALUES (%s, %s, (SELECT id FROM roles WHERE role_name = 'estudiante'))", (username, password))
                    conn.commit()
                    return redirect(url_for('portal'))
                except Exception as e:
                    print(f"Error al interactuar con la base de datos: {e}")
                    return render_template('add_student.html', error="Error al registrar el usuario")
                finally:
                    conn.close()
        return render_template('add_student.html')
    else:
        return redirect(url_for('portal'))

# Ruta para mostrar la lista de estudiantes (solo administradores)
@app.route('/student_list', methods=['GET', 'POST'])
def student_list():
    if 'role' in session and session['role'] == 'administrador':
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                selected_class = request.form.get('class_select')

                # Obtener la lista de clases
                cursor.execute("SELECT name FROM classes")
                classes = cursor.fetchall()

                # Obtener la lista de estudiantes con sus clases asignadas
                if selected_class:
                    # Filtrar por la clase seleccionada
                    cursor.execute("""
                        SELECT u.username, c.name AS class_name, u.class_id
                        FROM users u
                        LEFT JOIN classes c ON u.class_id = c.id
                        WHERE u.role_id = (SELECT id FROM roles WHERE role_name = 'estudiante')
                        AND c.name = %s
                    """, (selected_class,))
                else:
                    # Mostrar todos los estudiantes
                    cursor.execute("""
                        SELECT u.username, c.name AS class_name, u.class_id
                        FROM users u
                        LEFT JOIN classes c ON u.class_id = c.id
                        WHERE u.role_id = (SELECT id FROM roles WHERE role_name = 'estudiante')
                    """)
                students_with_classes = cursor.fetchall()

                return render_template('student_list.html', students_with_classes=students_with_classes, classes=classes, selected_class=selected_class)
            except Exception as e:
                print(f"Error al interactuar con la base de datos: {e}")
                return render_template('student_list.html', error="Error al obtener la lista de estudiantes")
            finally:
                conn.close()
    else:
        return redirect(url_for('login'))

# Ruta para crear una nueva clase (solo administradores)
@app.route('/create_class', methods=['POST'])
def create_class():
    if 'role' in session and session['role'] == 'administrador':
        class_name = request.form.get('class_name')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO classes (name) VALUES (%s)", (class_name,))
                conn.commit()
                return redirect(url_for('student_list'))
            except Exception as e:
                print(f"Error al interactuar con la base de datos: {e}")
                return render_template('student_list.html', error="Error al crear la clase")
            finally:
                conn.close()
    else:
        return redirect(url_for('portal'))

# Ruta para asignar un estudiante a una clase
@app.route('/assign_student', methods=['POST'])
def assign_student():
    if 'role' in session and session['role'] == 'administrador':
        student_username = request.form.get('student_username')
        class_name = request.form.get('class_name')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Obtener el ID del estudiante
                cursor.execute("SELECT id FROM users WHERE username = %s", (student_username,))
                student_id = cursor.fetchone()[0]

                # Obtener el ID de la clase
                cursor.execute("SELECT id FROM classes WHERE name = %s", (class_name,))
                class_id = cursor.fetchone()[0]

                # Asignar el estudiante a la clase
                cursor.execute("UPDATE users SET class_id = %s WHERE id = %s", (class_id, student_id))
                conn.commit()
                return redirect(url_for('student_list'))
            except Exception as e:
                print(f"Error al interactuar con la base de datos: {e}")
                return render_template('student_list.html', error="Error al asignar el estudiante a la clase")
            finally:
                conn.close()
    else:
        return redirect(url_for('portal'))

# Ruta para el Campus Digital
@app.route('/campus')
def campus():
    if 'username' in session:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Obtener la lista de cursos con su clase asociada
                cursor.execute("""
                    SELECT c.name, c.description, cl.name as class_name, cl.id as class_id
                    FROM courses c 
                    JOIN course_classes cc ON c.id = cc.course_id 
                    JOIN classes cl ON cc.class_id = cl.id
                """)
                courses_with_classes = cursor.fetchall()
                print(f"Cursos obtenidos: {courses_with_classes}")  # Registro de depuración

                # Obtener la lista de clases
                cursor.execute("SELECT name FROM classes")
                classes = cursor.fetchall()

                # Obtener la lista de estudiantes con sus clases asignadas
                cursor.execute("""
                    SELECT u.username, c.name AS class_name, u.class_id
                    FROM users u
                    LEFT JOIN classes c ON u.class_id = c.id
                    WHERE u.role_id = (SELECT id FROM roles WHERE role_name = 'estudiante')
                """)
                students_with_classes = cursor.fetchall()
                print(f"Estudiantes con clases: {students_with_classes}")  # Registro de depuración

                # Verificar si el usuario es administrador
                is_admin = session['role'] == 'administrador'
                return render_template('campus.html', courses_with_classes=courses_with_classes, classes=classes, is_admin=is_admin, students_with_classes=students_with_classes)
            except Exception as e:
                print(f"Error al interactuar con la base de datos: {e}")
                return render_template('campus.html', error="Error al obtener los cursos")
            finally:
                conn.close()
    else:
        return redirect(url_for('login'))

# Ruta para crear un nuevo curso (solo administradores)
@app.route('/create_course', methods=['POST'])
def create_course():
    if 'role' in session and session['role'] == 'administrador':
        course_name = request.form.get('course_name')
        course_description = request.form.get('course_description')
        class_name = request.form.get('class_name')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()

                # Insertar el nuevo curso
                cursor.execute("INSERT INTO courses (name, description) VALUES (%s, %s)", (course_name, course_description))
                conn.commit()

                # Obtener el ID del curso recién creado
                cursor.execute("SELECT id FROM courses WHERE name = %s", (course_name,))
                course_id = cursor.fetchone()[0]

                # Asignar la clase al curso
                if class_name:
                    cursor.execute("SELECT id FROM classes WHERE name = %s", (class_name,))
                    class_id = cursor.fetchone()[0]
                    cursor.execute("INSERT INTO course_classes (course_id, class_id) VALUES (%s, %s)", (course_id, class_id))
                    conn.commit()

                return redirect(url_for('campus'))
            except Exception as e:
                print(f"Error al interactuar con la base de datos: {e}")
                return render_template('campus.html', error="Error al crear el curso")
            finally:
                conn.close()
    else:
        return redirect(url_for('campus'))

@app.route('/add_week/<course_name>', methods=['POST'])
def add_week(course_name):
    if 'username' in session and session['role'] == 'administrador':
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()

                # Obtener el ID del curso
                cursor.execute("SELECT id FROM courses WHERE name = %s", (course_name,))
                course_id = cursor.fetchone()[0]

                # Obtener el número de semana más alto actual
                cursor.execute("SELECT MAX(week_number) FROM weeks WHERE course_id = %s", (course_id,))
                max_week_number = cursor.fetchone()[0]
                next_week_number = max_week_number + 1 if max_week_number else 1

                # Obtener los datos del formulario
                week_name = request.form['week_name']
                week_file = request.files['week_file']

                # Guardar el archivo de la semana si se proporcionó uno
                if week_file:
                    filename = secure_filename(week_file.filename)
                    week_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    # Insertar la semana en la base de datos
                    cursor.execute("INSERT INTO weeks (course_id, week_number, week_name, filename) VALUES (%s, %s, %s, %s)",
                                   (course_id, next_week_number, week_name, filename))
                    conn.commit()

                    return redirect(url_for('course_materials', course_name=course_name))

                else:
                    error = "Debes proporcionar un archivo para la semana."
                    return render_template('course_materials.html', course_name=course_name, error=error)

            except Exception as e:
                print(f"Error al interactuar con la base de datos: {e}")
                return render_template('error.html', message="Error al agregar la semana.")

            finally:
                conn.close()

    else:
        return redirect(url_for('login'))


@app.route('/course/<course_name>')
def course_materials(course_name):
    if 'username' in session:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()

                # Obtener el ID del curso
                cursor.execute("SELECT id, description FROM courses WHERE name = %s", (course_name,))
                course_data = cursor.fetchone()

                if course_data:
                    course_id = course_data[0]
                    course_description = course_data[1]

                    # Obtener el ID de la clase asociada al curso
                    cursor.execute("SELECT class_id FROM course_classes WHERE course_id = %s", (course_id,))
                    class_id = cursor.fetchone()[0]

                    # Obtener el nombre de la clase
                    cursor.execute("SELECT name FROM classes WHERE id = %s", (class_id,))
                    class_name = cursor.fetchone()[0]

                    # Obtener la lista de archivos del curso
                    cursor.execute("SELECT filename FROM course_files WHERE course_id = %s", (course_id,))
                    files = cursor.fetchall()

                    # Obtener la lista de semanas del curso
                    cursor.execute("SELECT week_number, week_name, filename FROM weeks WHERE course_id = %s", (course_id,))
                    weeks = cursor.fetchall()

                    role = session.get('role')

                    # Verificar si el usuario tiene acceso a la clase asociada al curso
                    cursor.execute("SELECT 1 FROM users WHERE class_id = %s AND id = %s", (class_id, session['user_id']))
                    has_access = cursor.fetchone()

                    if has_access or role == 'administrador':
                        return render_template('course_materials.html', course_name=course_name, course_description=course_description, class_name=class_name, files=files, weeks=weeks, role=role)
                    else:
                        return render_template('error.html', message="No tienes acceso a este curso.")

                else:
                    return render_template('error.html', message="Curso no encontrado.")

            except Exception as e:
                print(f"Error al interactuar con la base de datos: {e}")
                return render_template('error.html', message="Error al obtener la información del curso.")

            finally:
                conn.close()

    else:
        return redirect(url_for('login'))



# Ruta para subir archivos (solo administradores)
@app.route('/upload_file/<course_name>/<course_id>', methods=['POST'])
def upload_file(course_name, course_id):
    if 'role' in session and session['role'] == 'administrador':
        file = request.files['file']
        if file.filename != '':
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO course_files (course_id, filename) VALUES (%s, %s)", (course_id, filename))
                    conn.commit()
                    return redirect(url_for('course_materials', course_name=course_name))
                except Exception as e:
                    print(f"Error al interactuar con la base de datos: {e}")
                    return render_template('course_materials.html', error="Error al guardar el archivo")
                finally:
                    conn.close()
    else:
        return redirect(url_for('portal'))



# Ruta para descargar archivos
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Ruta para logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)