/* ============================================================
   DASHBOARD ESTUDIANTES JAVASCRIPT
   Funciones para el dashboard de estudiantes
   ============================================================ */

/**
 * Desplaza suavemente a la sección de tareas pendientes
 * @param {Event} event - Evento del click
 */
function scrollToTasks(event) {
    event.preventDefault();
    const tasksSection = document.getElementById('tareas-pendientes');
    if (tasksSection) {
        tasksSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Resaltar brevemente la sección
        tasksSection.style.transition = 'background-color 0.3s ease';
        tasksSection.querySelector('.card').style.boxShadow = '0 0 20px rgba(220, 53, 69, 0.3)';
        setTimeout(() => {
            tasksSection.querySelector('.card').style.boxShadow = '';
        }, 1500);
    }
}
