
import os
import mysql.connector

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Cargar variables de entorno
load_dotenv()

# Configuración de Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# ==========================================
# CONEXIÓN CON MYSQL
# ==========================================

def conectar_bd():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# ==========================================
# PROTECCIÓN DE RUTAS
# ==========================================

def login_requerido(funcion):
    @wraps(funcion)
    def decorada(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión para continuar.", "error")
            return redirect(url_for("login"))

        return funcion(*args, **kwargs)

    return decorada


# ==========================================
# PÁGINA DE INICIO
# ==========================================

@app.route("/")
def inicio():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return render_template("inicio.html")


# ==========================================
# HU01 - REGISTRO DE USUARIOS
# ==========================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip().lower()
        telefono = request.form.get("telefono", "").strip()
        contrasena = request.form.get("contrasena", "")
        confirmar = request.form.get("confirmar", "")

        if not nombre or not correo or not contrasena:
            flash("Completa todos los campos obligatorios.", "error")
            return redirect(url_for("registro"))

        if contrasena != confirmar:
            flash("Las contraseñas no coinciden.", "error")
            return redirect(url_for("registro"))

        if len(contrasena) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error")
            return redirect(url_for("registro"))

        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT id FROM users WHERE email = %s",
                (correo,)
            )

            if cursor.fetchone():
                flash("Este correo ya está registrado.", "error")
                return redirect(url_for("registro"))

            password_hash = generate_password_hash(contrasena)

            cursor.execute(
                """
                INSERT INTO users (full_name, email, password_hash, phone)
                VALUES (%s, %s, %s, %s)
                """,
                (nombre, correo, password_hash, telefono)
            )

            conexion.commit()

            flash("¡Cuenta creada correctamente! Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("login"))

        except mysql.connector.Error as error:
            conexion.rollback()
            print("Error en el registro:", error)
            flash("No fue posible completar el registro.", "error")

        finally:
            cursor.close()
            conexion.close()

    return render_template("registro.html")


# ==========================================
# HU02 - INICIO DE SESIÓN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        correo = request.form.get("correo", "").strip().lower()
        contrasena = request.form.get("contrasena", "")

        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT id, full_name, email, password_hash
                FROM users
                WHERE email = %s
                """,
                (correo,)
            )

            usuario = cursor.fetchone()

            if usuario and check_password_hash(
                usuario["password_hash"], contrasena
            ):

                session.clear()
                session["user_id"] = usuario["id"]
                session["user_name"] = usuario["full_name"]

                flash("¡Bienvenido a BLISS!", "success")
                return redirect(url_for("dashboard"))

            flash("Correo o contraseña incorrectos.", "error")

        except mysql.connector.Error as error:
            print("Error en el inicio de sesión:", error)
            flash("No fue posible iniciar sesión.", "error")

        finally:
            cursor.close()
            conexion.close()

    return render_template("login.html")


# ==========================================
# CERRAR SESIÓN
# ==========================================

@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente.", "success")
    return redirect(url_for("login"))


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
@login_requerido
def dashboard():

    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT COUNT(*) AS total FROM production_units WHERE user_id = %s",
            (session["user_id"],)
        )
        total_unidades = cursor.fetchone()["total"]

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM inventory_items i
            INNER JOIN production_units u ON i.unit_id = u.id
            WHERE u.user_id = %s
            """,
            (session["user_id"],)
        )
        total_insumos = cursor.fetchone()["total"]

        return render_template(
            "dashboard.html",
            total_unidades=total_unidades,
            total_insumos=total_insumos
        )

    finally:
        cursor.close()
        conexion.close()


# ==========================================
# EJECUTAR APLICACIÓN
# ==========================================


@app.route("/unidades", methods=["GET", "POST"])
@login_requerido
def unidades():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        tipo = request.form.get("tipo", "").strip().upper()
        ubicacion = request.form.get("ubicacion", "").strip()

        tipos_permitidos = [
            "GANADERIA",
            "AVICULTURA",
            "PISCICULTURA",
            "PORCICULTURA",
            "EQUINOS",
            "OTRA"
        ]

        if not nombre or tipo not in tipos_permitidos:
            flash("Ingresa un nombre y un tipo de producción válido.", "error")
            return redirect(url_for("unidades"))

        conexion = None
        cursor = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO production_units
                (user_id, name, production_type, location)
                VALUES (%s, %s, %s, %s)
            """, (
                session["user_id"],
                nombre,
                tipo,
                ubicacion or None
            ))

            conexion.commit()
            flash("¡Unidad productiva registrada correctamente!", "success")

        except mysql.connector.Error as error:
            if conexion:
                conexion.rollback()
            print("Error al registrar unidad:", error)
            flash("No fue posible registrar la unidad productiva.", "error")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

        return redirect(url_for("unidades"))

    conexion = None
    cursor = None

    try:
        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, name, production_type, location, created_at
            FROM production_units
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (session["user_id"],))

        lista_unidades = cursor.fetchall()

        return render_template(
            "unidades.html",
            unidades=lista_unidades
        )

    except mysql.connector.Error as error:
        print("Error al consultar unidades:", error)
        flash("No fue posible cargar tus unidades productivas.", "error")
        return render_template("unidades.html", unidades=[])

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()




@app.route("/inventario", methods=["GET", "POST"])
@login_requerido
def inventario():
    if request.method == "POST":
        unidad_id = request.form.get("unidad_id", "").strip()
        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "").strip().upper()
        cantidad = request.form.get("cantidad", "").strip()
        unidad_medida = request.form.get("unidad_medida", "").strip()
        cantidad_minima = request.form.get("cantidad_minima", "").strip()
        costo = request.form.get("costo", "").strip()
        vencimiento = request.form.get("vencimiento", "").strip()

        categorias_permitidas = [
            "ALIMENTO", "MEDICAMENTO", "HERRAMIENTA",
            "LIMPIEZA", "OTRO"
        ]
        medidas_permitidas = [
            "kg", "litros", "unidades", "bultos", "sacos"
        ]

        try:
            unidad_id = int(unidad_id)
            cantidad = float(cantidad)
            cantidad_minima = float(cantidad_minima)
            costo = float(costo)

            if (
                not nombre
                or categoria not in categorias_permitidas
                or unidad_medida not in medidas_permitidas
                or cantidad < 0
                or cantidad_minima < 0
                or costo < 0
            ):
                raise ValueError("Datos inválidos.")

        except (ValueError, TypeError):
            flash("Revisa los datos del insumo. No se permiten valores negativos.", "error")
            return redirect(url_for("inventario"))

        conexion = None
        cursor = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor(dictionary=True)

            # Comprobar que la unidad pertenezca al usuario
            cursor.execute("""
                SELECT id
                FROM production_units
                WHERE id = %s AND user_id = %s
            """, (unidad_id, session["user_id"]))

            if not cursor.fetchone():
                flash("La unidad productiva seleccionada no es válida.", "error")
                return redirect(url_for("inventario"))

            cursor.execute("""
                INSERT INTO inventory_items (
                    unit_id, name, category, quantity,
                    measurement_unit, minimum_quantity,
                    unit_cost, expiration_date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                unidad_id,
                nombre,
                categoria,
                cantidad,
                unidad_medida,
                cantidad_minima,
                costo,
                vencimiento or None
            ))

            conexion.commit()
            flash("¡Insumo registrado correctamente!", "success")

        except mysql.connector.Error as error:
            if conexion:
                conexion.rollback()
            print("Error al registrar insumo:", error)
            flash("No fue posible guardar el insumo.", "error")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

        return redirect(url_for("inventario"))

    conexion = None
    cursor = None

    try:
        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, name
            FROM production_units
            WHERE user_id = %s
            ORDER BY name
        """, (session["user_id"],))

        lista_unidades = cursor.fetchall()

        cursor.execute("""
            SELECT
                i.id,
                i.name,
                i.category,
                i.quantity,
                i.measurement_unit,
                i.minimum_quantity,
                i.unit_cost,
                u.name AS unit_name
            FROM inventory_items i
            INNER JOIN production_units u ON i.unit_id = u.id
            WHERE u.user_id = %s
            ORDER BY i.created_at DESC
        """, (session["user_id"],))

        lista_inventario = cursor.fetchall()

        return render_template(
            "inventario.html",
            unidades=lista_unidades,
            inventario=lista_inventario
        )

    except mysql.connector.Error as error:
        print("Error al consultar inventario:", error)
        flash("No fue posible cargar el inventario.", "error")
        return render_template(
            "inventario.html",
            unidades=[],
            inventario=[]
        )

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()




@app.route("/lotes", methods=["GET", "POST"])
@login_requerido
def lotes():
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)

    try:
        if request.method == "POST":
            unidad_id = request.form.get("unidad_id")
            especie_id = request.form.get("especie_id")
            nombre = request.form.get("nombre", "").strip()
            cantidad = request.form.get("cantidad")
            fecha_ingreso = request.form.get("fecha_ingreso")

            if not all([unidad_id, especie_id, nombre, cantidad, fecha_ingreso]):
                flash("Completa todos los campos obligatorios.", "error")
                return redirect(url_for("lotes"))

            try:
                cantidad = int(cantidad)
                unidad_id = int(unidad_id)
                especie_id = int(especie_id)

                if cantidad <= 0:
                    raise ValueError()
            except ValueError:
                flash("Verifica la cantidad y los datos seleccionados.", "error")
                return redirect(url_for("lotes"))

            # Verificar que la unidad pertenezca al usuario
            cursor.execute("""
                SELECT id, production_type
                FROM production_units
                WHERE id = %s AND user_id = %s
            """, (unidad_id, session["user_id"]))

            unidad = cursor.fetchone()

            if not unidad:
                flash("La unidad productiva seleccionada no es válida.", "error")
                return redirect(url_for("lotes"))

            # Verificar que la especie exista y corresponda al tipo de producción
            cursor.execute("""
                SELECT id
                FROM species
                WHERE id = %s AND production_type = %s
            """, (especie_id, unidad["production_type"]))

            especie = cursor.fetchone()

            if not especie:
                flash("La especie no corresponde al tipo de producción.", "error")
                return redirect(url_for("lotes"))

            cursor.execute("""
                INSERT INTO animal_lots
                (unit_id, species_id, name, quantity, entry_date, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                unidad_id,
                especie_id,
                nombre,
                cantidad,
                fecha_ingreso,
                "ACTIVO"
            ))

            conexion.commit()
            flash("¡Lote registrado correctamente!", "success")
            return redirect(url_for("lotes"))

        # Consultar únicamente las unidades del usuario
        cursor.execute("""
            SELECT id, name
            FROM production_units
            WHERE user_id = %s
            ORDER BY name
        """, (session["user_id"],))

        unidades = cursor.fetchall()

        # Consultar especies disponibles
        cursor.execute("""
            SELECT id, name, production_type
            FROM species
            ORDER BY name
        """)

        especies = cursor.fetchall()

        # Consultar lotes de las unidades del usuario
        cursor.execute("""
            SELECT
                l.id,
                l.name,
                l.quantity,
                l.entry_date,
                l.status,
                s.name AS especie,
                u.name AS unidad
            FROM animal_lots l
            INNER JOIN species s ON l.species_id = s.id
            INNER JOIN production_units u ON l.unit_id = u.id
            WHERE u.user_id = %s
            ORDER BY l.created_at DESC
        """, (session["user_id"],))

        lista_lotes = cursor.fetchall()

        return render_template(
            "lotes.html",
            unidades=unidades,
            especies=especies,
            lotes=lista_lotes
        )

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error en el módulo de lotes:", error)
        flash("No fue posible completar la operación.", "error")
        return redirect(url_for("lotes"))

    finally:
        cursor.close()
        conexion.close()



@app.route("/lotes/editar/<int:lote_id>", methods=["GET", "POST"])
@login_requerido
def editar_lote(lote_id):

    conexion = None
    cursor = None

    try:
        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True)

        # Comprobar que el lote pertenezca al usuario
        cursor.execute("""
            SELECT
                l.id,
                l.name,
                l.quantity,
                l.entry_date,
                l.status,
                s.name AS especie,
                u.name AS unidad
            FROM animal_lots l
            INNER JOIN production_units u ON l.unit_id = u.id
            INNER JOIN species s ON l.species_id = s.id
            WHERE l.id = %s AND u.user_id = %s
        """, (lote_id, session["user_id"]))

        lote = cursor.fetchone()

        if not lote:
            flash("No se encontró el lote solicitado.", "error")
            return redirect(url_for("lotes"))

        if request.method == "POST":

            nombre = request.form.get("nombre", "").strip()
            cantidad = request.form.get("cantidad", "").strip()
            fecha_ingreso = request.form.get("fecha_ingreso", "").strip()

            try:
                cantidad = int(cantidad)

                if not nombre or len(nombre) > 120:
                    raise ValueError()

                if cantidad <= 0:
                    raise ValueError()

                from datetime import datetime
                datetime.strptime(fecha_ingreso, "%Y-%m-%d")

            except (ValueError, TypeError):
                flash("Verifica el nombre, la cantidad y la fecha.", "error")
                return render_template("editar_lote.html", lote=lote)

            cursor.execute("""
                UPDATE animal_lots
                SET name = %s,
                    quantity = %s,
                    entry_date = %s
                WHERE id = %s
            """, (
                nombre,
                cantidad,
                fecha_ingreso,
                lote_id
            ))

            conexion.commit()

            flash("¡Lote actualizado correctamente!", "success")
            return redirect(url_for("lotes"))

        return render_template("editar_lote.html", lote=lote)

    except mysql.connector.Error as error:
        if conexion:
            conexion.rollback()

        print("Error al editar lote:", error)
        flash("No fue posible actualizar el lote.", "error")
        return redirect(url_for("lotes"))

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


if __name__ == "__main__":
    app.run(debug=True)
