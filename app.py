
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

# ==========================================
# HU06 / HU07 - ALIMENTACIÓN
# ==========================================

@app.route("/alimentacion", methods=["GET", "POST"])
@login_requerido
def alimentacion():

    conexion = None
    cursor = None

    try:
        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True)

        # ==================================
        # REGISTRAR ALIMENTACIÓN
        # ==================================

        if request.method == "POST":

            lote_id = request.form.get("lote_id", "").strip()
            alimento = request.form.get("alimento", "").strip()
            cantidad = request.form.get("cantidad", "").strip()
            unidad_medida = request.form.get("unidad_medida", "").strip()
            precio_unitario = request.form.get("precio_unitario", "").strip()
            fecha_alimentacion = request.form.get("fecha_alimentacion", "").strip()
            observaciones = request.form.get("observaciones", "").strip()

            try:
                lote_id = int(lote_id)
                cantidad = float(cantidad)
                precio_unitario = float(precio_unitario)

                if (
                    not alimento
                    or not unidad_medida
                    or not fecha_alimentacion
                    or cantidad <= 0
                    or precio_unitario < 0
                ):
                    raise ValueError()

            except (ValueError, TypeError):
                flash("Verifica los datos de la alimentación.", "error")
                return redirect(url_for("alimentacion"))

            # ==================================
            # VERIFICAR LOTE
            # ==================================

            cursor.execute("""
                SELECT
                    l.id,
                    l.name,
                    l.unit_id,
                    u.name AS unit_name
                FROM animal_lots l
                INNER JOIN production_units u
                    ON l.unit_id = u.id
                WHERE l.id = %s
                  AND u.user_id = %s
            """, (
                lote_id,
                session["user_id"]
            ))

            lote = cursor.fetchone()

            if not lote:
                flash("El lote seleccionado no es válido.", "error")
                return redirect(url_for("alimentacion"))

            # ==================================
            # CALCULAR COSTO TOTAL
            # ==================================

            total_cost = cantidad * precio_unitario

            # ==================================
            # BUSCAR ALIMENTO EN INVENTARIO
            # ==================================

            cursor.execute("""
                SELECT
                    id,
                    name,
                    quantity,
                    measurement_unit
                FROM inventory_items
                WHERE unit_id = %s
                  AND LOWER(name) = LOWER(%s)
                LIMIT 1
            """, (
                lote["unit_id"],
                alimento
            ))

            inventario = cursor.fetchone()

            if not inventario:
                flash(
                    f"El alimento '{alimento}' no existe en el inventario "
                    f"de la unidad '{lote['unit_name']}'.",
                    "error"
                )
                return redirect(url_for("alimentacion"))

            # ==================================
            # VALIDAR UNIDAD DE MEDIDA
            # ==================================

            if inventario["measurement_unit"] != unidad_medida:
                flash(
                    f"La unidad de medida del inventario es "
                    f"'{inventario['measurement_unit']}', "
                    f"pero estás registrando '{unidad_medida}'.",
                    "error"
                )
                return redirect(url_for("alimentacion"))

            # ==================================
            # VALIDAR EXISTENCIA
            # ==================================

            cantidad_disponible = float(inventario["quantity"])

            if cantidad > cantidad_disponible:
                flash(
                    f"No hay suficiente inventario. "
                    f"Disponible: {cantidad_disponible:g} "
                    f"{inventario['measurement_unit']}.",
                    "error"
                )
                return redirect(url_for("alimentacion"))

            # ==================================
            # GUARDAR ALIMENTACIÓN
            # ==================================

            cursor.execute("""
                INSERT INTO feeding_records (
                    lot_id,
                    feed_name,
                    quantity,
                    measurement_unit,
                    unit_price,
                    total_cost,
                    feeding_date,
                    notes
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                lote_id,
                alimento,
                cantidad,
                unidad_medida,
                precio_unitario,
                total_cost,
                fecha_alimentacion,
                observaciones or None
            ))

            # ==================================
            # DESCONTAR DEL INVENTARIO
            # ==================================

            nueva_cantidad = cantidad_disponible - cantidad

            cursor.execute("""
                UPDATE inventory_items
                SET quantity = %s
                WHERE id = %s
            """, (
                nueva_cantidad,
                inventario["id"]
            ))

            # ==================================
            # REGISTRAR MOVIMIENTO
            # ==================================

            nota_movimiento = (
                f"Consumo de alimentación - "
                f"Lote: {lote['name']}"
            )

            cursor.execute("""
                INSERT INTO inventory_movements (
                    item_id,
                    movement_type,
                    quantity,
                    notes
                )
                VALUES (%s, %s, %s, %s)
            """, (
                inventario["id"],
                "SALIDA",
                cantidad,
                nota_movimiento
            ))

            # ==================================
            # CONFIRMAR TODA LA OPERACIÓN
            # ==================================

            conexion.commit()

            flash(
                f"¡Alimentación registrada correctamente! "
                f"Costo total: ${total_cost:,.0f}. "
                f"Inventario actualizado: {nueva_cantidad:g} "
                f"{unidad_medida} disponibles.",
                "success"
            )

            return redirect(url_for("alimentacion"))

        # ==================================
        # CARGAR LOTES ACTIVOS
        # ==================================

        cursor.execute("""
            SELECT
                l.id,
                l.name,
                s.name AS especie,
                u.name AS unidad
            FROM animal_lots l
            INNER JOIN species s
                ON l.species_id = s.id
            INNER JOIN production_units u
                ON l.unit_id = u.id
            WHERE u.user_id = %s
              AND l.status = 'ACTIVO'
            ORDER BY l.name
        """, (session["user_id"],))

        lotes = cursor.fetchall()

        # ==================================
        # HISTORIAL DE ALIMENTACIÓN
        # ==================================

        cursor.execute("""
            SELECT
                f.id,
                f.feed_name,
                f.quantity,
                f.measurement_unit,
                f.unit_price,
                f.total_cost,
                f.feeding_date,
                f.notes,
                l.name AS lote,
                s.name AS especie,
                u.name AS unidad
            FROM feeding_records f
            INNER JOIN animal_lots l
                ON f.lot_id = l.id
            INNER JOIN species s
                ON l.species_id = s.id
            INNER JOIN production_units u
                ON l.unit_id = u.id
            WHERE u.user_id = %s
            ORDER BY f.feeding_date DESC, f.id DESC
        """, (session["user_id"],))

        registros = cursor.fetchall()

        return render_template(
            "alimentacion.html",
            lotes=lotes,
            registros=registros
        )

    except mysql.connector.Error as error:

        if conexion:
            conexion.rollback()

        print("Error en el módulo de alimentación:", error)

        flash(
            "No fue posible completar la operación de alimentación.",
            "error"
        )

        return redirect(url_for("dashboard"))

    finally:

        if cursor:
            cursor.close()

        if conexion:
            conexion.close()



# ==========================================
# SALUD ANIMAL
# ==========================================

@app.route("/salud", methods=["GET", "POST"])
@login_requerido
def salud():

    conexion = None
    cursor = None

    try:
        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True)

        # ==================================
        # REGISTRAR EVENTO SANITARIO
        # ==================================

        if request.method == "POST":

            lote_id = request.form.get("lote_id", "").strip()
            event_type = request.form.get("event_type", "").strip()
            product_used = request.form.get("product_used", "").strip()
            event_date = request.form.get("event_date", "").strip()
            description = request.form.get("description", "").strip()

            tipos_permitidos = [
                "VACUNACIÓN",
                "TRATAMIENTO",
                "CONTROL",
                "DESPARASITACIÓN",
                "OTRO"
            ]

            if (
                not lote_id
                or not event_type
                or not event_date
                or event_type not in tipos_permitidos
            ):
                flash("Completa los campos obligatorios del evento sanitario.", "error")
                return redirect(url_for("salud"))

            try:
                lote_id = int(lote_id)

                if not product_used:
                    product_used = None

                if not description:
                    description = None

            except (ValueError, TypeError):
                flash("Los datos ingresados no son válidos.", "error")
                return redirect(url_for("salud"))

            # ==================================
            # VERIFICAR QUE EL LOTE PERTENEZCA
            # AL USUARIO ACTUAL
            # ==================================

            cursor.execute("""
                SELECT
                    l.id,
                    l.name,
                    s.name AS especie,
                    u.name AS unidad
                FROM animal_lots l
                INNER JOIN species s
                    ON l.species_id = s.id
                INNER JOIN production_units u
                    ON l.unit_id = u.id
                WHERE l.id = %s
                  AND u.user_id = %s
                  AND l.status = 'ACTIVO'
            """, (
                lote_id,
                session["user_id"]
            ))

            lote = cursor.fetchone()

            if not lote:
                flash("El lote seleccionado no es válido.", "error")
                return redirect(url_for("salud"))

            # ==================================
            # GUARDAR EVENTO SANITARIO
            # ==================================

            cursor.execute("""
                INSERT INTO health_events (
                    lot_id,
                    event_type,
                    product_used,
                    event_date,
                    description
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                lote_id,
                event_type,
                product_used,
                event_date,
                description
            ))

            conexion.commit()

            flash(
                f"¡Evento sanitario registrado para el lote '{lote['name']}'!",
                "success"
            )

            return redirect(url_for("salud"))

        # ==================================
        # CARGAR LOTES ACTIVOS
        # ==================================

        cursor.execute("""
            SELECT
                l.id,
                l.name,
                s.name AS especie,
                u.name AS unidad
            FROM animal_lots l
            INNER JOIN species s
                ON l.species_id = s.id
            INNER JOIN production_units u
                ON l.unit_id = u.id
            WHERE u.user_id = %s
              AND l.status = 'ACTIVO'
            ORDER BY l.name
        """, (session["user_id"],))

        lotes = cursor.fetchall()

        # ==================================
        # HISTORIAL SANITARIO
        # ==================================

        cursor.execute("""
            SELECT
                h.id,
                h.event_type,
                h.product_used,
                h.event_date,
                h.description,
                l.name AS lote,
                s.name AS especie,
                u.name AS unidad
            FROM health_events h
            INNER JOIN animal_lots l
                ON h.lot_id = l.id
            INNER JOIN species s
                ON l.species_id = s.id
            INNER JOIN production_units u
                ON l.unit_id = u.id
            WHERE u.user_id = %s
            ORDER BY h.event_date DESC, h.id DESC
        """, (session["user_id"],))

        registros = cursor.fetchall()

        return render_template(
            "salud.html",
            lotes=lotes,
            registros=registros
        )

    except mysql.connector.Error as error:

        if conexion:
            conexion.rollback()

        print("Error en el módulo de salud animal:", error)

        flash(
            "No fue posible completar la operación de salud animal.",
            "error"
        )

        return redirect(url_for("dashboard"))

    finally:

        if cursor:
            cursor.close()

        if conexion:
            conexion.close()

           
# ==================================
        # Produccion
        # ==================================

@app.route("/produccion", methods=["GET", "POST"])
@login_requerido
def produccion():
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    user_id = session["user_id"]

    if request.method == "POST":
        lot_id = request.form.get("lot_id")
        quantity = request.form.get("quantity")
        measurement_unit = request.form.get("measurement_unit")
        production_date = request.form.get("production_date")
        notes = request.form.get("notes")

        if not lot_id or not quantity or not production_date:
            flash("Completa los campos obligatorios.", "danger")
            cursor.close()
            conn.close()
            return redirect(url_for("produccion"))

        try:
            # Verificar que el lote pertenezca al usuario
            cursor.execute("""
                SELECT l.id, l.name, l.quantity, s.name AS species
                FROM animal_lots l
                INNER JOIN production_units u ON l.unit_id = u.id
                INNER JOIN species s ON l.species_id = s.id
                WHERE l.id = %s AND u.user_id = %s
            """, (lot_id, user_id))

            lote = cursor.fetchone()

            if not lote:
                flash("El lote seleccionado no es válido.", "danger")
            else:
                cursor.execute("""
                    INSERT INTO production_records
                    (lot_id, quantity, measurement_unit, production_date, notes)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    lot_id,
                    quantity,
                    measurement_unit,
                    production_date,
                    notes
                ))

                conn.commit()
                flash("Producción registrada correctamente.", "success")

        except Exception as e:
            conn.rollback()
            flash(f"Error al registrar la producción: {str(e)}", "danger")

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("produccion"))

    # Lotes del usuario
    cursor.execute("""
        SELECT 
            l.id,
            l.name,
            l.quantity,
            s.name AS species,
            u.name AS unit_name
        FROM animal_lots l
        INNER JOIN production_units u ON l.unit_id = u.id
        INNER JOIN species s ON l.species_id = s.id
        WHERE u.user_id = %s
        ORDER BY l.name
    """, (user_id,))

    lotes = cursor.fetchall()

    # Historial de producción
    cursor.execute("""
        SELECT
            p.id,
            p.quantity,
            p.measurement_unit,
            p.production_date,
            p.notes,
            l.name AS lot_name,
            s.name AS species
        FROM production_records p
        INNER JOIN animal_lots l ON p.lot_id = l.id
        INNER JOIN species s ON l.species_id = s.id
        INNER JOIN production_units u ON l.unit_id = u.id
        WHERE u.user_id = %s
        ORDER BY p.production_date DESC, p.id DESC
    """, (user_id,))

    producciones = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "produccion.html",
        lotes=lotes,
        producciones=producciones
    )

# ==================================
        # Finanzas
        # ==================================

@app.route("/finanzas")
def finanzas():
    conexion = None
    cursor = None

    try:
        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True)

        # Unidades productivas
        cursor.execute("""
            SELECT id, name
            FROM production_units
            ORDER BY name
        """)
        unidades = cursor.fetchall()

        # Ingresos
        cursor.execute("""
            SELECT
                i.id,
                i.unit_id,
                i.lot_id,
                i.concept,
                i.amount,
                i.income_date,
                i.description
            FROM incomes i
            ORDER BY i.income_date DESC, i.id DESC
        """)
        ingresos = cursor.fetchall()

        # Gastos
        cursor.execute("""
            SELECT 
                e.id,
                e.unit_id,
                e.lot_id,
                e.concept,
                e.category,
                e.amount,
                e.expense_date,
                e.description
            FROM expenses e
            ORDER BY e.expense_date DESC, e.id DESC
        """)
        gastos = cursor.fetchall()

        # Totales
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM incomes
        """)
        total_ingresos = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM expenses
        """)
        total_gastos = cursor.fetchone()["total"]

        saldo = total_ingresos - total_gastos

        return render_template(
            "finanzas.html",
            ingresos=ingresos,
            gastos=gastos,
            total_ingresos=total_ingresos,
            total_gastos=total_gastos,
            saldo=saldo
        )

    except Exception as e:
        print("ERROR EN FINANZAS:", e)
        flash("No fue posible cargar el módulo de finanzas.", "error")
        return redirect(url_for("dashboard"))

    finally:
        if cursor:
            cursor.close()


@app.route("/finanzas/ingreso", methods=["POST"])
def registrar_ingreso():
    conexion = None
    cursor = None

    try:
        unit_id = request.form.get("unit_id")
        lot_id = request.form.get("lot_id") or None
        concept = request.form.get("concept")
        amount = request.form.get("amount")
        income_date = request.form.get("income_date")
        description = request.form.get("description")

        if not unit_id or not concept or not amount or not income_date:
            flash("Completa los campos obligatorios del ingreso.", "error")
            return redirect(url_for("finanzas"))

        conexion = mysql.connection
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO incomes
            (unit_id, lot_id, concept, amount, income_date, description)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            unit_id,
            lot_id,
            concept,
            amount,
            income_date,
            description
        ))

        conexion.commit()

        flash("Ingreso registrado correctamente.", "success")

    except Exception as e:
        if conexion:
            conexion.rollback()

        print("ERROR REGISTRANDO INGRESO:", e)
        flash("No fue posible registrar el ingreso.", "error")

    finally:
        if cursor:
            cursor.close()

    return redirect(url_for("finanzas"))


@app.route("/finanzas/gasto", methods=["POST"])
def registrar_gasto():
    conexion = None
    cursor = None

    try:
        unit_id = request.form.get("unit_id")
        lot_id = request.form.get("lot_id") or None
        concept = request.form.get("concept")
        category = request.form.get("category")
        amount = request.form.get("amount")
        expense_date = request.form.get("expense_date")
        description = request.form.get("description")

        if not unit_id or not concept or not category or not amount or not expense_date:
            flash("Completa los campos obligatorios del gasto.", "error")
            return redirect(url_for("finanzas"))

        conexion = mysql.connection
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO expenses
            (unit_id, lot_id, concept, category, amount, expense_date, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            unit_id,
            lot_id,
            concept,
            category,
            amount,
            expense_date,
            description
        ))

        conexion.commit()

        flash("Gasto registrado correctamente.", "success")

    except Exception as e:
        if conexion:
            conexion.rollback()

        print("ERROR REGISTRANDO GASTO:", e)
        flash("No fue posible registrar el gasto.", "error")

    finally:
        if cursor:
            cursor.close()

    return redirect(url_for("finanzas"))
            

# ==========================================
# REPORTES
# ==========================================

@app.route("/reportes")
@login_requerido
def reportes():

    conexion = None
    cursor = None

    try:
        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True)

        # ==================================
        # RESUMEN GENERAL
        # ==================================

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM production_units
            WHERE user_id = %s
        """, (session["user_id"],))

        total_unidades = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM animal_lots l
            INNER JOIN production_units u
                ON l.unit_id = u.id
            WHERE u.user_id = %s
              AND l.status = 'ACTIVO'
        """, (session["user_id"],))

        total_lotes = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COALESCE(SUM(l.quantity), 0) AS total
            FROM animal_lots l
            INNER JOIN production_units u
                ON l.unit_id = u.id
            WHERE u.user_id = %s
              AND l.status = 'ACTIVO'
        """, (session["user_id"],))

        total_animales = cursor.fetchone()["total"]

        # ==================================
        # FINANZAS
        # ==================================

        cursor.execute("""
            SELECT COALESCE(SUM(i.amount), 0) AS total
            FROM incomes i
            INNER JOIN production_units u
                ON i.unit_id = u.id
            WHERE u.user_id = %s
        """, (session["user_id"],))

        total_ingresos = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COALESCE(SUM(e.amount), 0) AS total
            FROM expenses e
            INNER JOIN production_units u
                ON e.unit_id = u.id
            WHERE u.user_id = %s
        """, (session["user_id"],))

        total_gastos = cursor.fetchone()["total"]

        saldo = total_ingresos - total_gastos

        # ==================================
        # PRODUCCIÓN
        # ==================================

        cursor.execute("""
            SELECT
                COALESCE(SUM(p.quantity), 0) AS total
            FROM production_records p
            INNER JOIN animal_lots l
                ON p.lot_id = l.id
            INNER JOIN production_units u
                ON l.unit_id = u.id
            WHERE u.user_id = %s
        """, (session["user_id"],))

        total_produccion = cursor.fetchone()["total"]

        # ==================================
        # MORTALIDAD
        # ==================================

        cursor.execute("""
            SELECT
                COALESCE(SUM(m.quantity), 0) AS total
            FROM mortality_records m
            INNER JOIN animal_lots l
                ON m.lot_id = l.id
            INNER JOIN production_units u
                ON l.unit_id = u.id
            WHERE u.user_id = %s
        """, (session["user_id"],))

        total_mortalidad = cursor.fetchone()["total"]

        # ==================================
        # PRODUCCIÓN POR UNIDAD
        # ==================================

        cursor.execute("""
            SELECT
                u.name AS unidad,
                COALESCE(SUM(p.quantity), 0) AS produccion
            FROM production_units u
            LEFT JOIN animal_lots l
                ON l.unit_id = u.id
            LEFT JOIN production_records p
                ON p.lot_id = l.id
            WHERE u.user_id = %s
            GROUP BY u.id, u.name
            ORDER BY produccion DESC
        """, (session["user_id"],))

        produccion_unidades = cursor.fetchall()

        # ==================================
        # GASTOS POR CATEGORÍA
        # ==================================

        cursor.execute("""
            SELECT
                e.category,
                COALESCE(SUM(e.amount), 0) AS total
            FROM expenses e
            INNER JOIN production_units u
                ON e.unit_id = u.id
            WHERE u.user_id = %s
            GROUP BY e.category
            ORDER BY total DESC
        """, (session["user_id"],))

        gastos_categoria = cursor.fetchall()

        # ==================================
        # ÚLTIMOS MOVIMIENTOS FINANCIEROS
        # ==================================

        cursor.execute("""
            SELECT
                i.concept,
                i.amount,
                i.income_date,
                u.name AS unidad
            FROM incomes i
            INNER JOIN production_units u
                ON i.unit_id = u.id
            WHERE u.user_id = %s
            ORDER BY i.income_date DESC, i.id DESC
            LIMIT 5
        """, (session["user_id"],))

        ultimos_ingresos = cursor.fetchall()

        cursor.execute("""
            SELECT
                e.concept,
                e.amount,
                e.expense_date,
                e.category,
                u.name AS unidad
            FROM expenses e
            INNER JOIN production_units u
                ON e.unit_id = u.id
            WHERE u.user_id = %s
            ORDER BY e.expense_date DESC, e.id DESC
            LIMIT 5
        """, (session["user_id"],))

        ultimos_gastos = cursor.fetchall()

        return render_template(
            "reportes.html",
            total_unidades=total_unidades,
            total_lotes=total_lotes,
            total_animales=total_animales,
            total_ingresos=total_ingresos,
            total_gastos=total_gastos,
            saldo=saldo,
            total_produccion=total_produccion,
            total_mortalidad=total_mortalidad,
            produccion_unidades=produccion_unidades,
            gastos_categoria=gastos_categoria,
            ultimos_ingresos=ultimos_ingresos,
            ultimos_gastos=ultimos_gastos
        )

    except mysql.connector.Error as error:

        print("ERROR EN REPORTES:", error)

        flash(
            "No fue posible cargar el módulo de reportes.",
            "error"
        )

        return redirect(url_for("dashboard"))

    finally:

        if cursor:
            cursor.close()

        if conexion:
            conexion.close()


if __name__ == "__main__":
    app.run(debug=True)




