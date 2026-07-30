from flask import Blueprint, render_template, request
from database import mysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, redirect, url_for 
from database import mysql

acceso = Blueprint("acceso", __name__)

# Ruta de inicio
@acceso.route("/")
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total = cursor.fetchone()
    cursor.close()
    return render_template("acceso/index.html", total_usuarios=total[0])

# Ruta de registro
@acceso.route("/registro", methods=["GET", "POST"])
def registro():
    mensaje = ""
    tipo_mensaje = ""

    if request.method == "POST":
        cedula = request.form["cedula"]
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        telefono = request.form["telefono"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()

        # Validar si la cédula ya existe
        cursor.execute("SELECT id FROM usuarios WHERE cedula = %s", (cedula,))
        usuario = cursor.fetchone()

        if usuario:
            mensaje = "La cédula ya está registrada."
            tipo_mensaje = "danger"
        else:
            password_encriptado = generate_password_hash(password)
            sql = """INSERT INTO usuarios
                     (cedula,nombres,apellidos,telefono,password,rol)
                     VALUES (%s,%s,%s,%s,%s,'Cliente')"""
            cursor.execute(sql, (cedula, nombres, apellidos, telefono, password_encriptado))
            mysql.connection.commit()

            mensaje = "Usuario registrado correctamente."
            tipo_mensaje = "success"

        cursor.close()

    return render_template("acceso/registro.html", mensaje=mensaje, tipo_mensaje=tipo_mensaje)

# Ruta de iniciar sesión
@acceso.route("/iniciar_sesion", methods=["GET","POST"])
def iniciar_sesion():
    mensaje = ""

    if request.method == "POST":
        cedula = request.form["cedula"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT id,nombres,apellidos,password,rol 
                          FROM usuarios WHERE cedula=%s""", (cedula,))
        usuario = cursor.fetchone()

        if usuario:
            password_bd = usuario[3]
            if check_password_hash(password_bd, password):
                # Guardar datos en sesión
                session["id"] = usuario[0]
                session["nombre"] = usuario[1]
                session["rol"] = usuario[4]

                cursor.close()

                # Redirigir según rol
                if usuario[4] == "Administrador":
                    return redirect(url_for("administrador.dashboard"))
                else:
                    return redirect(url_for("cliente.dashboard"))
            else:
                mensaje = "Contraseña incorrecta."
        else:
            mensaje = "La cédula no está registrada."

        cursor.close()

    return render_template("acceso/login.html", mensaje=mensaje)

# Ruta de cierre de sesión
@acceso.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear()  # elimina todos los datos guardados en la sesión
    return redirect(url_for("acceso.index"))  # redirige al inicio
