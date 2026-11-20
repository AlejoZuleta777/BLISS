# BLISS — Historias de Usuario

## 1. Descripción

BLISS es una aplicación web para la gestión de unidades productivas agropecuarias. El sistema permite centralizar información relacionada con unidades productivas, animales, lotes, alimentación, salud animal, inventario, producción, finanzas, reportes y eventos programados.

Las siguientes Historias de Usuario representan las principales necesidades identificadas para el desarrollo del sistema.

---

## 2. Historias de Usuario

### HU01 — Registro e inicio de sesión

**Como** administrador o usuario del sistema,  
**quiero** registrarme e iniciar sesión,  
**para** acceder de manera segura a las funcionalidades de BLISS.

**Criterio de aceptación:**
- El usuario puede registrarse.
- El usuario puede iniciar sesión con sus credenciales.
- El sistema permite acceder al panel principal después de autenticarse.

**Estado:** Implementada.

---

### HU02 — Crear unidades productivas

**Como** productor agropecuario,  
**quiero** registrar unidades productivas,  
**para** organizar las fincas o espacios donde realizo mis actividades productivas.

**Criterio de aceptación:**
- Se puede registrar una nueva unidad.
- Se pueden almacenar sus datos principales.
- La unidad queda disponible dentro del sistema.

**Estado:** Implementada.

---

### HU03 — Editar unidades productivas

**Como** productor agropecuario,  
**quiero** editar la información de una unidad productiva,  
**para** mantener sus datos actualizados.

**Criterio de aceptación:**
- Se puede seleccionar una unidad existente.
- Se pueden modificar sus datos.
- Los cambios quedan almacenados.

**Estado:** Implementada.

---

### HU04 — Registrar animales y lotes

**Como** productor agropecuario,  
**quiero** registrar animales y lotes,  
**para** organizar y controlar la población de mi unidad productiva.

**Criterio de aceptación:**
- Se pueden registrar lotes.
- Se puede indicar la especie correspondiente.
- Se puede registrar la cantidad de animales.
- Los registros quedan asociados a la unidad productiva.

**Estado:** Implementada.

---

### HU05 — Consultar lotes

**Como** productor agropecuario,  
**quiero** consultar la información de mis lotes,  
**para** conocer su composición y estado.

**Criterio de aceptación:**
- El sistema muestra los lotes registrados.
- Se puede consultar la información de cada lote.
- La información se presenta de manera organizada.

**Estado:** Implementada.

---

### HU06 — Registrar alimentación

**Como** productor agropecuario,  
**quiero** registrar la alimentación de los animales,  
**para** llevar control de los recursos utilizados en su alimentación.

**Criterio de aceptación:**
- Se pueden registrar datos de alimentación.
- La información queda almacenada.
- Los registros pueden consultarse posteriormente.

**Estado:** Implementada.

---

### HU07 — Registrar eventos de salud

**Como** productor agropecuario,  
**quiero** registrar eventos relacionados con la salud animal,  
**para** mantener un historial sanitario.

**Criterio de aceptación:**
- Se pueden registrar eventos de salud.
- El evento queda asociado a la información correspondiente.
- Se puede consultar el historial registrado.

**Estado:** Implementada.

---

### HU08 — Registrar tratamientos

**Como** productor agropecuario,  
**quiero** registrar tratamientos realizados a los animales,  
**para** realizar seguimiento de las intervenciones sanitarias.

**Criterio de aceptación:**
- Se pueden registrar tratamientos.
- Se puede almacenar la información correspondiente.
- Los registros quedan disponibles para consulta.

**Estado:** Implementada.

---

### HU09 — Gestionar inventario

**Como** productor agropecuario,  
**quiero** registrar productos e insumos,  
**para** conocer los recursos disponibles en mi unidad productiva.

**Criterio de aceptación:**
- Se pueden registrar artículos.
- Se puede consultar el inventario.
- Los productos pueden identificarse mediante su información registrada.

**Estado:** Implementada.

---

### HU10 — Registrar movimientos de inventario

**Como** productor agropecuario,  
**quiero** registrar entradas y salidas de inventario,  
**para** controlar el movimiento de los insumos y productos.

**Criterio de aceptación:**
- Se pueden registrar movimientos.
- Se identifica el tipo de movimiento.
- El sistema conserva el historial de movimientos.

**Estado:** Implementada.

---

### HU11 — Registrar producción

**Como** productor agropecuario,  
**quiero** registrar la producción obtenida,  
**para** llevar seguimiento de los resultados productivos.

**Criterio de aceptación:**
- Se pueden registrar producciones.
- Se pueden almacenar cantidades y fechas.
- Los registros quedan asociados a la unidad correspondiente.

**Estado:** Implementada.

---

### HU12 — Registrar ingresos

**Como** productor agropecuario,  
**quiero** registrar los ingresos obtenidos,  
**para** conocer el dinero generado por mi actividad productiva.

**Criterio de aceptación:**
- Se pueden registrar ingresos.
- Se almacena el valor correspondiente.
- Se puede consultar la información financiera registrada.

**Estado:** Implementada.

---

### HU13 — Registrar gastos

**Como** productor agropecuario,  
**quiero** registrar los gastos realizados,  
**para** controlar los costos de mi actividad productiva.

**Criterio de aceptación:**
- Se pueden registrar gastos.
- Se almacena el valor correspondiente.
- Los gastos quedan disponibles para consulta.

**Estado:** Implementada.

---

### HU14 — Consultar reportes

**Como** productor agropecuario,  
**quiero** consultar reportes de la información registrada,  
**para** analizar el comportamiento de mi actividad productiva.

**Criterio de aceptación:**
- El sistema presenta información consolidada.
- Los datos pueden consultarse de manera organizada.
- Los reportes permiten apoyar el análisis de la información.

**Estado:** Implementada.

---

### HU15 — Programar eventos

**Como** productor agropecuario,  
**quiero** programar eventos,  
**para** organizar actividades futuras de mi unidad productiva.

**Criterio de aceptación:**
- Se pueden registrar eventos.
- Se puede establecer una fecha.
- El evento queda almacenado para su posterior consulta.

**Estado:** Implementada.

---

### HU16 — Consultar alertas y eventos próximos

**Como** productor agropecuario,  
**quiero** identificar eventos próximos,  
**para** recordar actividades importantes y actuar oportunamente.

**Criterio de aceptación:**
- El sistema identifica eventos próximos.
- La información se muestra al usuario.
- Las fechas permiten realizar seguimiento de las actividades.

**Estado:** Implementada.

---

### HU17 — Registrar mortalidades

**Como** productor agropecuario,  
**quiero** registrar las mortalidades ocurridas,  
**para** mantener actualizado el control de los animales.

**Criterio de aceptación:**
- Se puede registrar una mortalidad.
- Se puede almacenar la fecha y la información relacionada.
- El registro queda disponible para consulta.

**Estado:** Implementada.

---

### HU18 — Consultar el dashboard

**Como** productor agropecuario,  
**quiero** visualizar un panel principal con información resumida,  
**para** tener una visión general de mi unidad productiva.

**Criterio de aceptación:**
- El sistema presenta un panel principal.
- Se muestran datos relevantes del sistema.
- El usuario puede acceder desde el dashboard a los diferentes módulos.

**Estado:** Implementada.

---

### HU19 — Navegación sencilla

**Como** usuario de BLISS,  
**quiero** navegar fácilmente entre los módulos,  
**para** utilizar el sistema sin complicaciones.

**Criterio de aceptación:**
- Los módulos principales son accesibles desde la interfaz.
- Los botones y enlaces permiten desplazarse entre las funcionalidades.
- La navegación mantiene una estructura organizada.

**Estado:** Implementada.

---

### HU20 — Persistencia de la información

**Como** administrador del sistema,  
**quiero** que la información registrada sea almacenada en una base de datos,  
**para** conservar los datos y consultarlos posteriormente.

**Criterio de aceptación:**
- La información se almacena en MySQL.
- Los registros pueden recuperarse posteriormente.
- La información permanece disponible entre sesiones.

**Estado:** Implementada.

---

## 3. Tecnologías utilizadas

BLISS fue desarrollado utilizando principalmente:

- **Python**
- **Flask**
- **MySQL**
- **HTML5**
- **CSS3**
- **JavaScript**
- **Git**
- **GitHub**

---

## 4. Relación entre Historias de Usuario y módulos

| Módulo | Historias relacionadas |
|---|---|
| Usuarios | HU01 |
| Dashboard | HU18 |
| Unidades productivas | HU02, HU03 |
| Animales y lotes | HU04, HU05 |
| Alimentación | HU06 |
| Salud animal | HU07, HU08, HU17 |
| Inventario | HU09, HU10 |
| Producción | HU11 |
| Finanzas | HU12, HU13 |
| Reportes | HU14 |
| Eventos y alertas | HU15, HU16 |
| Interfaz y navegación | HU19 |
| Base de datos | HU20 |

---

## 5. Estado general del proyecto

Las Historias de Usuario definidas para BLISS fueron utilizadas como referencia para desarrollar las funcionalidades principales de la aplicación.

**Estado general:** Proyecto implementado y documentado.