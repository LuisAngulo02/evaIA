/**
 * Login Form - Authentication Functionality
 * Handles password visibility, form submission, and UI enhancements
 */

$(document).ready(function() {
    initializePasswordToggle();
    initializeFormSubmission();
    initializeFocusEffects();
    initializeFeatureAnimations();
});

/**
 * Initialize password visibility toggle
 */
function initializePasswordToggle() {
    $('#togglePassword').click(function() {
        const passwordField = $('#id_password');
        const passwordFieldType = passwordField.attr('type');
        const toggleIcon = $(this).find('i');
        
        if (passwordFieldType === 'password') {
            passwordField.attr('type', 'text');
            toggleIcon.removeClass('fa-eye').addClass('fa-eye-slash');
        } else {
            passwordField.attr('type', 'password');
            toggleIcon.removeClass('fa-eye-slash').addClass('fa-eye');
        }
    });
}

/**
 * Initialize form submission with loading state
 */
function initializeFormSubmission() {
    $('#loginForm').on('submit', function() {
        const submitBtn = $(this).find('button[type="submit"]');
        const originalText = submitBtn.html();
        
        submitBtn.addClass('btn-loading');
        submitBtn.html('<i class="fas fa-spinner fa-spin me-2"></i>Iniciando sesión...');
        submitBtn.prop('disabled', true);
        
        // Restore button if validation error occurs
        setTimeout(function() {
            if (submitBtn.hasClass('btn-loading')) {
                submitBtn.removeClass('btn-loading');
                submitBtn.html(originalText);
                submitBtn.prop('disabled', false);
            }
        }, 5000);
    });
}

/**
 * Initialize focus effects for form controls
 */
function initializeFocusEffects() {
    $('.form-control').on('focus', function() {
        $(this).parent().addClass('focused');
    }).on('blur', function() {
        $(this).parent().removeClass('focused');
    });
}

/**
 * Initialize entrance animations for feature items
 */
function initializeFeatureAnimations() {
    $('.feature-item').each(function(index) {
        $(this).css('animation-delay', (index * 0.1) + 's');
        $(this).addClass('fadeInUp');
    });
}

/**
 * Show custom toast notification
 * @param {string} message - The message to display
 * @param {string} type - The type of notification (success, error, warning, info)
 */
function showToast(message, type = 'info') {
    const toastId = 'toast-' + Date.now();
    const iconMap = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    };
    
    const toast = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0 show" role="alert" style="position: fixed; top: 100px; right: 20px; z-index: 9999;">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas ${iconMap[type]} me-2"></i>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" onclick="$('#${toastId}').remove()"></button>
            </div>
        </div>
    `;
    
    $('body').append(toast);
    
    setTimeout(() => {
        $('#' + toastId).fadeOut(() => {
            $('#' + toastId).remove();
        });
    }, 5000);
}
