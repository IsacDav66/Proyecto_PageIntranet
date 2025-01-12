# Resumen del Proyecto: Plataforma Educativa Web "Autismo +"


![image](https://github.com/user-attachments/assets/52b25c20-0826-4d49-b5ee-1291c3f8b584)


Este proyecto es una aplicación web desarrollada con Python y Flask, diseñada para funcionar como una plataforma educativa para el centro "Autismo +". Permite la gestión de usuarios, cursos, clases, materiales y ofrece funcionalidades tanto para administradores como para estudiantes.

**Características Principales:**

1.  **Autenticación y Roles:**
    *   **Inicio de Sesión y Registro:** Los usuarios pueden iniciar sesión con un nombre de usuario y contraseña. Los administradores tienen una opción de registro separada.
    *   **Roles:** La aplicación distingue entre administradores y estudiantes, otorgando diferentes permisos.
    *   **Gestión de Sesión:** Utiliza sesiones para mantener el estado del usuario logueado.
    *   **Recuperación de Contraseña:** Permite a los usuarios recuperar su contraseña a través de un proceso de restablecimiento por correo electrónico. También permite cambiar el nombre de usuario.
    *    **Vinculación de Correo Electrónico:** Los usuarios pueden vincular un correo electrónico a su cuenta.
2.  **Portal Digital:**
    *   **Panel Personalizado:** Muestra un panel de usuario adaptado a su rol (administrador o estudiante).
    *   **Acceso a Secciones:** Los estudiantes pueden acceder a sus cursos, solicitudes, historial de pagos y asistencia. Los administradores tienen acceso adicional para gestionar estudiantes y clases.
    *   **Enlaces a otras secciones:** Los usuarios pueden navegar a distintas secciones como "Cursos y Notas", "Solicitudes y Reclamos", "Asistencias", "Historial de Pago" y otras opciones de administración.
3.  **Gestión de Estudiantes (Administradores):**
    *   **Añadir Estudiantes:** Los administradores pueden crear nuevas cuentas de estudiantes, incluyendo su grado (primaria o secundaria).
    *   **Listado de Estudiantes:** Los administradores pueden ver un listado de todos los estudiantes, con filtros por clase y grado.
    *   **Crear y Asignar Clases:** Permite crear nuevas clases y asignar estudiantes a esas clases.
4.  **Campus Digital:**
    *   **Listado de Cursos:** Muestra una lista de cursos disponibles, filtrados por grado para estudiantes y todos los cursos para administradores.
    *   **Visualización de Materiales:** Permite a los usuarios acceder a los materiales de cada curso.
    *   **Creación de Cursos (Administradores):** Los administradores pueden crear nuevos cursos, incluyendo su descripción, grado y la clase asociada.
5.  **Gestión de Materiales de Curso:**
    *   **Subida de Archivos (Administradores):** Permite a los administradores subir archivos de apoyo para los cursos.
    *   **Semanas del Curso (Administradores):** Permite a los administradores agregar semanas de contenido, incluyendo archivos.
    *   **Descarga de Archivos:** Los usuarios pueden descargar los archivos de los cursos.
6.  **Transmisión en Vivo:**
    *   **Inicio de Transmisión (Administradores):** Permite iniciar transmisiones en vivo.
    *   **Visualización de la Transmisión:** Los usuarios pueden ver la transmisión en vivo.
7.  **Calendario de Asistencia:**
    *   **Registro de Asistencia:** Se utiliza un calendario para registrar la asistencia, accesible solo para administradores.
8.  **Otras Funcionalidades:**
    *   **Solicitudes y Reclamos:** Los usuarios pueden enviar solicitudes o reclamos a través de un formulario.
    *   **Historial de Pagos:** Se muestra un historial simulado de pagos.
    *   **Cerrar Sesión:** Los usuarios pueden cerrar la sesión actual.
    *   **Vincular Correo:** Los usuarios pueden vincular un correo electrónico a su cuenta para recuperar la contraseña.

**Tecnologías Utilizadas:**

*   **Python:** Lenguaje de programación principal.
*   **Flask:** Framework web para construir la aplicación.
*   **PostgreSQL:** Base de datos para almacenar la información.
*   **HTML, CSS, JavaScript:** Para la interfaz de usuario.
*   **Psycopg2:** Adaptador de PostgreSQL para Python.
*   **FullCalendar:** Para la visualización del calendario de asistencia.
*   **WebRTC** (implementación inicial): Para la transmisión de video en vivo.
*   **Dotenv:** Para la gestión de variables de entorno.

**Propósito:**

La aplicación está diseñada para ser una plataforma integral de gestión y aprendizaje para el centro "Autismo +", proporcionando herramientas para administradores y estudiantes, mejorando la comunicación y la gestión de la información educativa.

**Para un Trabajo:**

Este proyecto es un buen ejemplo de una aplicación web educativa. Cumple con los requerimientos básicos para la gestión de usuarios y contenido. Como fue hecho para un trabajo, se enfoca en la funcionalidad y en demostrar las habilidades en programación web.

![image](https://github.com/user-attachments/assets/a65f1aca-0eb8-4d35-80f2-861aee1f245c)      ![image](https://github.com/user-attachments/assets/d1566707-8162-4d9c-a8bd-d81a303951c4)

