/**
 * Register Form - User Registration Functionality
 * Handles password visibility, username validation, password strength, and form submission
 */

$(document).ready(function() {
    initializePasswordToggles();
    initializeUsernameChecker();
    initializePasswordStrength();
    initializePasswordMatch();
    initializeFormSubmission();
    initializeRoleHelper();
});

/**
 * Initialize password visibility toggles
 */
function initializePasswordToggles() {
    $('#togglePassword1, #togglePassword2').click(function() {
        const targetId = $(this).attr('id') === 'togglePassword1' ? '#id_password1' : '#id_password2';
        const passwordField = $(targetId);
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
 * Check username availability via AJAX
 */
function initializeUsernameChecker() {
    const checkUsernameUrl = $('#id_username').data('check-url');
    
    $('#id_username').on('blur', function() {
        const username = $(this).val();
        if (username.length >= 3) {
            $.get(checkUsernameUrl, {username: username}, function(data) {
                if (data.exists) {
                    $('#usernameCheck i').removeClass('fa-question-circle fa-check-circle text-success').addClass('fa-times-circle text-danger');
                    $('#id_username').addClass('is-invalid');
                } else {
                    $('#usernameCheck i').removeClass('fa-question-circle fa-times-circle text-danger').addClass('fa-check-circle text-success');
                    $('#id_username').removeClass('is-invalid').addClass('is-valid');
                }
            });
        }
    });
}

/**
 * Initialize password strength checker
 */
function initializePasswordStrength() {
    $('#id_password1').on('input', function() {
        const password = $(this).val();
        const strength = checkPasswordStrength(password);
        $('#passwordStrength').html(strength.html).removeClass().addClass('password-strength ' + strength.class);
    });
}

/**
 * Initialize password match verification
 */
function initializePasswordMatch() {
    $('#id_password2').on('input', function() {
        const password1 = $('#id_password1').val();
        const password2 = $(this).val();
        
        if (password2.length > 0) {
            if (password1 === password2) {
                $('#passwordMatch').html('<small class="text-success"><i class="fas fa-check me-1"></i>Las contraseñas coinciden</small>');
                $(this).removeClass('is-invalid').addClass('is-valid');
            } else {
                $('#passwordMatch').html('<small class="text-danger"><i class="fas fa-times me-1"></i>Las contraseñas no coinciden</small>');
                $(this).removeClass('is-valid').addClass('is-invalid');
            }
        } else {
            $('#passwordMatch').html('');
            $(this).removeClass('is-valid is-invalid');
        }
    });
}

/**
 * Check password strength
 * @param {string} password - The password to check
 * @returns {Object} Strength object with class and HTML
 */
function checkPasswordStrength(password) {
    let score = 0;
    let feedback = [];

    if (password.length >= 8) score++;
    else feedback.push('al menos 8 caracteres');

    if (/[a-z]/.test(password)) score++;
    else feedback.push('letras minúsculas');

    if (/[A-Z]/.test(password)) score++;
    else feedback.push('letras mayúsculas');

    if (/[0-9]/.test(password)) score++;
    else feedback.push('números');

    if (/[^a-zA-Z0-9]/.test(password)) score++;
    else feedback.push('símbolos especiales');

    const strength = {
        0: {class: 'weak', html: '<small><i class="fas fa-times me-1"></i>Muy débil</small>'},
        1: {class: 'weak', html: '<small><i class="fas fa-exclamation me-1"></i>Débil</small>'},
        2: {class: 'fair', html: '<small><i class="fas fa-minus me-1"></i>Regular</small>'},
        3: {class: 'good', html: '<small><i class="fas fa-check me-1"></i>Buena</small>'},
        4: {class: 'strong', html: '<small><i class="fas fa-check-circle me-1"></i>Fuerte</small>'},
        5: {class: 'strong', html: '<small><i class="fas fa-shield-alt me-1"></i>Muy fuerte</small>'}
    };

    return strength[score] || strength[0];
}

/**
 * Initialize form submission handler
 */
function initializeFormSubmission() {
    $('#registerForm').on('submit', function(e) {
        console.log('Formulario enviado');
        $('#submitBtn').html('<i class="fas fa-spinner fa-spin me-2"></i>Creando cuenta...');
        $('#submitBtn').prop('disabled', true);
    });
}

/**
 * Initialize role selection helper
 */
function initializeRoleHelper() {
    $('#id_role').change(function() {
        const role = $(this).val();
        const institutionField = $('#id_institution');
        
        if (role === 'ESTUDIANTE') {
            institutionField.attr('placeholder', 'Universidad, Instituto, Colegio...');
        } else if (role === 'DOCENTE') {
            institutionField.attr('placeholder', 'Institución donde enseña...');
        } else {
            institutionField.attr('placeholder', 'Institución...');
        }
    });
}
