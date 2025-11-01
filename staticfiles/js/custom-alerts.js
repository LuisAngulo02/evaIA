/* ============================================================
   CUSTOM ALERTS SYSTEM
   Sistema de alertas personalizadas animadas
   ============================================================ */

/**
 * Muestra una alerta personalizada animada
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - Tipo de alerta: 'success', 'error', 'warning', 'info'
 * @param {number} duration - Duración en milisegundos (default: 4000)
 */
function showCustomAlert(message, type = 'info', duration = 4000) {
    // Crear contenedor de alertas si no existe
    let container = document.getElementById('custom-alerts-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'custom-alerts-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
        `;
        document.body.appendChild(container);
    }

    // Configuración de colores e iconos según el tipo
    const configs = {
        success: {
            gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            icon: 'fa-check-circle',
            bgColor: '#f0f8ff'
        },
        error: {
            gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            icon: 'fa-exclamation-circle',
            bgColor: '#fff0f0'
        },
        warning: {
            gradient: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
            icon: 'fa-exclamation-triangle',
            bgColor: '#fff9e6'
        },
        info: {
            gradient: 'linear-gradient(135deg, #06beb6 0%, #48b1bf 100%)',
            icon: 'fa-info-circle',
            bgColor: '#e6f7ff'
        }
    };

    const config = configs[type] || configs.info;

    // Crear el elemento de alerta
    const alert = document.createElement('div');
    alert.className = 'custom-alert';
    alert.style.cssText = `
        background: white;
        border-radius: 16px;
        padding: 18px 24px;
        margin-bottom: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        display: flex;
        align-items: center;
        gap: 16px;
        animation: slideInRight 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        border-left: 4px solid transparent;
        border-image: ${config.gradient} 1;
        position: relative;
        overflow: hidden;
    `;

    // Barra de progreso
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: absolute;
        bottom: 0;
        left: 0;
        height: 3px;
        background: ${config.gradient};
        width: 100%;
        animation: progressShrink ${duration}ms linear;
    `;

    // Icono
    const iconContainer = document.createElement('div');
    iconContainer.style.cssText = `
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: ${config.gradient};
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    `;
    iconContainer.innerHTML = `<i class="fas ${config.icon}" style="color: white; font-size: 18px;"></i>`;

    // Contenido
    const content = document.createElement('div');
    content.style.cssText = `
        flex-grow: 1;
        font-size: 14px;
        color: #333;
        font-weight: 500;
        line-height: 1.5;
    `;
    content.innerHTML = message; // Cambiado de textContent a innerHTML para soportar HTML

    // Botón de cerrar
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '<i class="fas fa-times"></i>';
    closeBtn.style.cssText = `
        background: transparent;
        border: none;
        color: #999;
        cursor: pointer;
        font-size: 16px;
        padding: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 8px;
        transition: all 0.2s;
        flex-shrink: 0;
    `;
    closeBtn.onmouseover = () => {
        closeBtn.style.background = '#f0f0f0';
        closeBtn.style.color = '#333';
    };
    closeBtn.onmouseout = () => {
        closeBtn.style.background = 'transparent';
        closeBtn.style.color = '#999';
    };
    closeBtn.onclick = () => removeAlert(alert);

    // Ensamblar alerta
    alert.appendChild(progressBar);
    alert.appendChild(iconContainer);
    alert.appendChild(content);
    alert.appendChild(closeBtn);
    container.appendChild(alert);

    // Auto-remover después de la duración
    setTimeout(() => removeAlert(alert), duration);
}

/**
 * Remueve una alerta con animación
 */
function removeAlert(alert) {
    alert.style.animation = 'slideOutRight 0.3s ease-out';
    setTimeout(() => {
        if (alert.parentNode) {
            alert.parentNode.removeChild(alert);
        }
    }, 300);
}

// Agregar estilos de animación
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(120%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(120%);
            opacity: 0;
        }
    }

    @keyframes progressShrink {
        from {
            width: 100%;
        }
        to {
            width: 0%;
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes fadeOut {
        from {
            opacity: 1;
        }
        to {
            opacity: 0;
        }
    }

    @keyframes scaleIn {
        from {
            transform: scale(0.7);
            opacity: 0;
        }
        to {
            transform: scale(1);
            opacity: 1;
        }
    }

    @keyframes scaleOut {
        from {
            transform: scale(1);
            opacity: 1;
        }
        to {
            transform: scale(0.7);
            opacity: 0;
        }
    }

    .custom-alert:hover {
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.18);
        transform: translateY(-2px);
        transition: all 0.2s ease;
    }
`;
document.head.appendChild(style);

// Sobrescribir alert() global (opcional)
window.customAlert = showCustomAlert;

/**
 * Muestra un diálogo de confirmación personalizado
 * @param {string} message - Mensaje a mostrar
 * @param {string} confirmText - Texto del botón confirmar (default: 'Aceptar')
 * @param {string} cancelText - Texto del botón cancelar (default: 'Cancelar')
 * @returns {Promise<boolean>} - true si confirma, false si cancela
 */
function showCustomConfirm(message, confirmText = 'Aceptar', cancelText = 'Cancelar') {
    return new Promise((resolve) => {
        // Crear overlay
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.2s ease;
            backdrop-filter: blur(4px);
        `;

        // Crear modal
        const modal = document.createElement('div');
        modal.style.cssText = `
            background: white;
            border-radius: 20px;
            padding: 32px;
            max-width: 450px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: scaleIn 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
        `;

        // Icono
        const icon = document.createElement('div');
        icon.style.cssText = `
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 24px;
        `;
        icon.innerHTML = '<i class="fas fa-question" style="color: white; font-size: 28px;"></i>';

        // Mensaje
        const messageEl = document.createElement('div');
        messageEl.style.cssText = `
            font-size: 18px;
            color: #333;
            text-align: center;
            margin-bottom: 32px;
            line-height: 1.6;
            font-weight: 500;
        `;
        messageEl.innerHTML = message; // Cambiado de textContent a innerHTML para soportar HTML

        // Contenedor de botones
        const buttonsContainer = document.createElement('div');
        buttonsContainer.style.cssText = `
            display: flex;
            gap: 12px;
            justify-content: center;
        `;

        // Botón cancelar
        const cancelBtn = document.createElement('button');
        cancelBtn.textContent = cancelText;
        cancelBtn.style.cssText = `
            padding: 12px 32px;
            border-radius: 12px;
            border: 2px solid #e0e0e0;
            background: white;
            color: #666;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            min-width: 120px;
        `;
        cancelBtn.onmouseover = () => {
            cancelBtn.style.background = '#f5f5f5';
            cancelBtn.style.borderColor = '#ccc';
        };
        cancelBtn.onmouseout = () => {
            cancelBtn.style.background = 'white';
            cancelBtn.style.borderColor = '#e0e0e0';
        };
        cancelBtn.onclick = () => {
            closeModal(false);
        };

        // Botón confirmar
        const confirmBtn = document.createElement('button');
        confirmBtn.textContent = confirmText;
        confirmBtn.style.cssText = `
            padding: 12px 32px;
            border-radius: 12px;
            border: none;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            min-width: 120px;
        `;
        confirmBtn.onmouseover = () => {
            confirmBtn.style.transform = 'translateY(-2px)';
            confirmBtn.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.5)';
        };
        confirmBtn.onmouseout = () => {
            confirmBtn.style.transform = 'translateY(0)';
            confirmBtn.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.4)';
        };
        confirmBtn.onclick = () => {
            closeModal(true);
        };

        // Función para cerrar el modal
        function closeModal(result) {
            overlay.style.animation = 'fadeOut 0.2s ease';
            modal.style.animation = 'scaleOut 0.2s ease';
            setTimeout(() => {
                if (overlay.parentNode) {
                    overlay.parentNode.removeChild(overlay);
                }
                resolve(result);
            }, 200);
        }

        // Cerrar con ESC
        const escHandler = (e) => {
            if (e.key === 'Escape') {
                closeModal(false);
                document.removeEventListener('keydown', escHandler);
            }
        };
        document.addEventListener('keydown', escHandler);

        // Ensamblar
        buttonsContainer.appendChild(cancelBtn);
        buttonsContainer.appendChild(confirmBtn);
        modal.appendChild(icon);
        modal.appendChild(messageEl);
        modal.appendChild(buttonsContainer);
        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        // Focus en botón confirmar
        confirmBtn.focus();
    });
}

// Exportar función de confirmación
window.customConfirm = showCustomConfirm;
