/**
 * EvalExpo AI - JavaScript Base Global
 * Funcionalidades compartidas en toda la aplicación
 */

(function() {
    'use strict';

    // ========== INICIALIZACIÓN DE TOOLTIPS ==========
    function initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // ========== INICIALIZACIÓN DE TOASTS ==========
    function initToasts() {
        $('.toast').each(function() {
            const toast = new bootstrap.Toast(this, {
                delay: 6000,
                autohide: true
            });
            toast.show();
        });
    }

    // ========== ANIMACIONES Y EFECTOS ==========
    function initAnimations() {
        // Add fade-in animation to cards
        $('.card').addClass('fade-in');
        
        // Add smooth scroll behavior
        $('html').css('scroll-behavior', 'smooth');
    }

    // ========== MOSTRAR TOAST DINÁMICO ==========
    function showToast(message, type = 'info') {
        const iconMap = {
            'success': 'check-circle',
            'error': 'exclamation-triangle',
            'danger': 'exclamation-triangle',
            'warning': 'exclamation-circle',
            'info': 'info-circle',
            'primary': 'info-circle'
        };

        const icon = iconMap[type] || 'info-circle';

        const toastHtml = `
            <div class="toast show align-items-center border-0 shadow-lg mb-3 toast-${type}" role="alert">
                <div class="d-flex w-100">
                    <div class="toast-body d-flex align-items-center">
                        <div class="me-3">
                            <i class="fas fa-${icon} fa-lg"></i>
                        </div>
                        <div class="flex-grow-1">
                            <span>${message}</span>
                        </div>
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        let toastContainer = $('.position-fixed.top-0.end-0');
        if (toastContainer.length === 0) {
            $('body').append('<div class="position-fixed top-0 end-0 p-3" style="z-index: 1055; margin-top: 90px;"></div>');
            toastContainer = $('.position-fixed.top-0.end-0');
        }
        
        toastContainer.append(toastHtml);
        
        const newToast = $('.toast').last();
        const toast = new bootstrap.Toast(newToast[0], {delay: 6000});
        toast.show();
    }

    // ========== SISTEMA DE NOTIFICACIONES ==========
    function loadNotifications() {
        fetch('/notifications/dropdown-simple/')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const dropdownContent = document.getElementById('notificationDropdownContent');
                    if (dropdownContent) {
                        dropdownContent.innerHTML = data.html;
                    }
                    updateNotificationBadge(data.unread_count);
                }
            })
            .catch(error => {
                console.error('Error cargando notificaciones:', error);
                const dropdownContent = document.getElementById('notificationDropdownContent');
                if (dropdownContent) {
                    dropdownContent.innerHTML = '<div class="dropdown-item text-center text-danger">Error al cargar</div>';
                }
            });
    }

    function updateNotificationBadge(count) {
        const badge = document.getElementById('notificationCount');
        if (badge) {
            if (count > 0) {
                badge.textContent = count > 99 ? '99+' : count;
                badge.style.display = 'inline-block';
            } else {
                badge.style.display = 'none';
            }
        }
    }

    // ========== MANEJAR CLICK EN NOTIFICACIÓN ==========
    function handleNotificationClick(event, notificationId) {
        event.preventDefault();
        event.stopPropagation();
        
        // Obtener CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value 
                       || document.querySelector('meta[name="csrf-token"]')?.content;
        
        // Obtener el elemento de la notificación
        const notificationElement = event.currentTarget;
        const actionUrl = notificationElement.getAttribute('href');
        
        // Cerrar el dropdown
        const dropdown = bootstrap.Dropdown.getInstance(document.getElementById('notificationDropdown'));
        if (dropdown) {
            dropdown.hide();
        }
        
        // Marcar como leída y redirigir
        fetch(`/notifications/mark-read/${notificationId}/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Actualizar el badge
                updateNotificationBadge(data.unread_count);
            }
            // Redirigir a la URL de acción
            window.location.href = actionUrl || data.action_url;
        })
        .catch(error => {
            console.error('Error al marcar como leída:', error);
            // Aun así, redirigir
            window.location.href = actionUrl;
        });
        
        return false;
    }

    // ========== INICIALIZACIÓN DEL SISTEMA DE NOTIFICACIONES ==========
    function initNotifications() {
        // Cargar inicialmente
        loadNotifications();
        
        // Cargar cuando se haga click en el botón
        const notifBtn = document.getElementById('notificationDropdown');
        if (notifBtn) {
            notifBtn.addEventListener('shown.bs.dropdown', function() {
                loadNotifications();
            });
        }
        
        // Auto-refresh cada 30 segundos
        setInterval(loadNotifications, 30000);
    }

    // ========== INICIALIZACIÓN GENERAL ==========
    $(document).ready(function() {
        initTooltips();
        initToasts();
        initAnimations();
        
        // Inicializar notificaciones solo si el usuario está autenticado
        if (document.getElementById('notificationDropdown')) {
            initNotifications();
        }
    });

    // ========== EXPORTAR FUNCIONES GLOBALMENTE ==========
    window.showToast = showToast;
    window.updateNotificationBadge = updateNotificationBadge;
    window.loadNotifications = loadNotifications;
    window.handleNotificationClick = handleNotificationClick;

})();
