// AI Configuration JavaScript - SOLO MODO VISUAL (Sin funcionalidad de guardado)

// Esta página es solo informativa, no permite cambiar la configuración
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔒 Modo solo lectura activado - Esta página es informativa únicamente');
    
    // Deshabilitar cualquier intento de interacción con formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            console.warn('Formulario deshabilitado - Página de solo lectura');
            return false;
        });
    });
    
    // Agregar tooltip informativo a las tarjetas
    const levelCards = document.querySelectorAll('.level-card');
    levelCards.forEach(card => {
        card.style.cursor = 'default';
        card.title = 'Información sobre este nivel de evaluación';
    });
    
    // Mensaje informativo en consola
    console.log('%c📖 PÁGINA INFORMATIVA', 'color: #0d6efd; font-size: 16px; font-weight: bold;');
    console.log('Esta página muestra información sobre los niveles de evaluación de IA.');
    console.log('No permite modificar la configuración del sistema.');
});

// Prevenir clicks en elementos deshabilitados
function preventClick(event) {
    event.preventDefault();
    event.stopPropagation();
    return false;
}

// Animación suave para mejorar la experiencia visual
const style = document.createElement('style');
style.textContent = `
    .level-card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .level-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
    }
    
    .level-card.active {
        border: 2px solid #0d6efd !important;
        box-shadow: 0 8px 30px rgba(13, 110, 253, 0.3) !important;
    }
    
    .info-banner {
        animation: slideInDown 0.5s ease;
    }
    
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);
