# 🌱 BLISS

### Sistema de gestión inteligente para unidades productivas agropecuarias

BLISS es una aplicación web desarrollada para facilitar la gestión y organización de la información relacionada con unidades productivas agropecuarias.

El sistema centraliza diferentes procesos como el manejo de unidades productivas, animales y lotes, alimentación, salud animal, inventario, producción, finanzas, reportes y eventos programados.

---

## 🎯 Objetivo

Desarrollar una solución web que permita a los productores agropecuarios gestionar de manera organizada la información de sus unidades productivas, reduciendo la dependencia de registros dispersos y facilitando la consulta y seguimiento de los datos.

---

## 💡 Problema identificado

En muchas unidades productivas la información puede encontrarse distribuida entre documentos físicos, hojas de cálculo o diferentes registros.

Esto puede dificultar:

- El seguimiento de los animales.
- El control de inventarios.
- El registro de alimentación.
- El seguimiento de eventos de salud.
- El control de ingresos y gastos.
- El análisis de la producción.
- La planificación de actividades futuras.

BLISS busca centralizar esta información en una sola aplicación.

---

## 🚀 Funcionalidades principales

### 🏡 Unidades productivas

Permite registrar y administrar las unidades productivas que hacen parte del sistema.

- Crear unidades.
- Consultar unidades.
- Editar información.

### 🐄 Animales y lotes

Permite organizar los animales mediante lotes y especies.

- Registro de lotes.
- Registro de especies.
- Cantidad de animales.
- Consulta de información.

### 🌾 Alimentación

Permite registrar información relacionada con la alimentación de los animales y realizar seguimiento de los registros.

### 🩺 Salud animal

Permite llevar control de eventos relacionados con la salud.

- Eventos sanitarios.
- Tratamientos.
- Seguimiento.
- Registro de mortalidades.

### 📦 Inventario

Permite controlar los productos e insumos utilizados en las unidades productivas.

- Registro de artículos.
- Entradas.
- Salidas.
- Movimientos de inventario.

### 📈 Producción

Permite registrar y consultar información relacionada con la producción obtenida.

### 💰 Finanzas

Permite llevar un control básico de los movimientos financieros.

- Ingresos.
- Gastos.
- Descripciones.
- Fechas.
- Valores.

### 📊 Reportes

Permite consultar información consolidada de los diferentes procesos registrados en BLISS.

### 📅 Eventos y alertas

Permite programar actividades y consultar eventos próximos para facilitar el seguimiento de las tareas.

### 📋 Dashboard

El panel principal permite visualizar información general y acceder rápidamente a los diferentes módulos.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Flask | Framework web |
| MySQL | Base de datos |
| HTML5 | Estructura de las páginas |
| CSS3 | Diseño e interfaz |
| JavaScript | Interactividad |
| Git | Control de versiones |
| GitHub | Repositorio y gestión del código |

---

## 🗂️ Estructura del proyecto

```text
BLISS/
│
├── app.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── inicio.html
│   ├── login.html
│   ├── registro.html
│   ├── unidades.html
│   ├── lotes.html
│   ├── editar_lote.html
│   ├── inventario.html
│   └── ...
│
├── static/
│   ├── css/
│   └── js/
│
├── docs/
│   └── historias_usuario.md
│
└── README.md
```

---

## 👤 Historias de Usuario

BLISS fue desarrollado tomando como referencia un conjunto de Historias de Usuario orientadas a las necesidades de un productor agropecuario.

Las historias se encuentran documentadas en:

**`docs/historias_usuario.md`**

Entre las principales se encuentran:

- Registro e inicio de sesión.
- Gestión de unidades productivas.
- Gestión de animales y lotes.
- Control de alimentación.
- Gestión de salud animal.
- Gestión de inventario.
- Registro de producción.
- Control de ingresos y gastos.
- Generación de reportes.
- Programación de eventos.
- Consulta de alertas.
- Dashboard y navegación.

---

## 🗄️ Base de datos

BLISS utiliza MySQL para almacenar la información generada por la aplicación.

Entre las principales entidades utilizadas se encuentran:

- `users`
- `production_units`
- `species`
- `animal_lots`
- `inventory_items`
- `inventory_movements`
- `feeding_records`
- `health_events`
- `mortality_records`
- `production_records`
- `incomes`
- `expenses`
- `scheduled_events`
- `alerts`

La estructura permite relacionar la información de las diferentes áreas de gestión agropecuaria.

---

## ▶️ Ejecución del proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/AlejoZuleta777/BLISS.git
```

### 2. Ingresar al proyecto

```bash
cd BLISS
```

### 3. Crear y activar el entorno virtual

En Windows:

```bash
python -m venv .venv
```

Activar:

```bash
.venv\Scripts\activate
```

### 4. Instalar dependencias

Si el proyecto cuenta con un archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Configurar MySQL

Crear la base de datos correspondiente y configurar las credenciales utilizadas por la aplicación.

### 6. Ejecutar Flask

```bash
python app.py
```

Después de iniciar el servidor, acceder desde el navegador a la dirección local indicada por Flask.

---

## 🔄 Control de versiones

El proyecto utiliza Git para realizar el control de versiones.

Los cambios principales son registrados mediante commits y posteriormente enviados al repositorio remoto de GitHub.

Repositorio:

**AlejoZuleta777/BLISS**

---

## 📌 Estado del proyecto

**Estado:** Implementación final / versión académica.

BLISS cuenta con los principales módulos definidos durante el desarrollo y con documentación de las Historias de Usuario.

---

## 👨‍💻 Autor

**Maicol Alejandro Sanchez Zuleta**

Proyecto académico — Ingeniería de Software.

---

## 📚 Documentación

- [Historias de Usuario](docs/historias_usuario.md)
- Código fuente del proyecto
- Estructura de base de datos
- Control de versiones mediante Git y GitHub