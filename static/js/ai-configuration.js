// AI Configuration JavaScript - Nivel de Estrictez

let currentLevel = document.getElementById('strictness_level').value;
const saveButton = document.getElementById('saveButton');

function selectLevel(level, event) {
    if (event) {
        event.stopPropagation();
    }
    
    // Actualizar el valor del input oculto
    document.getElementById('strictness_level').value = level;
    
    // Remover clase active de todas las tarjetas y botones
    document.querySelectorAll('.level-card').forEach(card => {
        card.classList.remove('active');
    });
    
    document.querySelectorAll('.btn-select-level').forEach(btn => {
        btn.classList.remove('active');
        const card = btn.closest('.level-card');
        const cardLevel = card.getAttribute('data-level');
        
        if (cardLevel === level) {
            btn.innerHTML = '<i class="fas fa-check-circle me-2"></i>NIVEL SELECCIONADO';
        } else {
            btn.innerHTML = 'SELECCIONAR ESTE NIVEL';
        }
    });
    
    // Agregar clase active a la tarjeta seleccionada
    const selectedCard = document.querySelector(`.level-card[data-level="${level}"]`);
    if (selectedCard) {
        selectedCard.classList.add('active');
        const selectedBtn = selectedCard.querySelector('.btn-select-level');
        if (selectedBtn) {
            selectedBtn.classList.add('active');
        }
    }
    
    // Habilitar el botón de guardar solo si se cambió el nivel
    if (level !== currentLevel) {
        saveButton.disabled = false;
        saveButton.classList.add('btn-pulse');
    } else {
        saveButton.disabled = true;
        saveButton.classList.remove('btn-pulse');
    }
}

// Inicialización al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    // Marcar el nivel actual como seleccionado
    const currentCard = document.querySelector(`.level-card[data-level="${currentLevel}"]`);
    if (currentCard) {
        currentCard.classList.add('active');
        const currentBtn = currentCard.querySelector('.btn-select-level');
        if (currentBtn) {
            currentBtn.classList.add('active');
        }
    }
    
    // Deshabilitar el botón de guardar inicialmente
    saveButton.disabled = true;
});

// Prevenir envío del formulario si no hay cambios
document.getElementById('aiConfigForm').addEventListener('submit', function(e) {
    const selectedLevel = document.getElementById('strictness_level').value;
    if (selectedLevel === currentLevel) {
        e.preventDefault();
        showCustomAlert('No has realizado ningún cambio en la configuración.', 'warning', 3000);
        return false;
    }
});

// Agregar animación de pulso al botón de guardar
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(13, 110, 253, 0.7);
        }
        70% {
            box-shadow: 0 0 0 15px rgba(13, 110, 253, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(13, 110, 253, 0);
        }
    }
    
    .btn-pulse {
        animation: pulse 2s infinite;
    }
`;
document.head.appendChild(style);

