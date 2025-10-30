/* ============================================================
   EDIT PRESENTATION JAVASCRIPT
   Funciones para la interfaz de edición de presentaciones
   ============================================================ */

// Handle file selection
const videoInput = document.getElementById('id_video_file');
if (videoInput) {
    videoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            handleNewVideo(file);
        }
    });
}

// ===== DRAG AND DROP FUNCTIONALITY =====

const uploadArea = document.getElementById('upload-area');

/**
 * Previene el comportamiento por defecto del navegador
 */
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

/**
 * Resalta el área de carga cuando se arrastra un archivo
 */
function highlight(e) {
    if (uploadArea) {
        uploadArea.classList.add('dragover');
    }
}

/**
 * Quita el resaltado del área de carga
 */
function unhighlight(e) {
    if (uploadArea) {
        uploadArea.classList.remove('dragover');
    }
}

/**
 * Maneja el evento de soltar archivo
 */
function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        const file = files[0];
        const videoInput = document.getElementById('id_video_file');
        if (videoInput) {
            videoInput.files = files;
            handleNewVideo(file);
        }
    }
}

if (uploadArea) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });

    uploadArea.addEventListener('drop', handleDrop, false);

    // Click upload area to select file
    uploadArea.addEventListener('click', function() {
        const videoInput = document.getElementById('id_video_file');
        if (videoInput) {
            videoInput.click();
        }
    });
}

// ===== VIDEO HANDLING =====

/**
 * Maneja la selección de un nuevo video
 * @param {File} file - Archivo de video seleccionado
 */
function handleNewVideo(file) {
    // Validate file type
    const validTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/quicktime', 'video/x-msvideo', 'video/webm', 'video/x-matroska'];
    if (!validTypes.includes(file.type)) {
        showCustomAlert('Formato de archivo no válido. Use MP4, AVI, MOV, MKV o WEBM', 'error', 4000);
        return;
    }

    // Validate file size (500MB)
    if (file.size > 500 * 1024 * 1024) {
        showCustomAlert('El archivo es demasiado grande. Máximo 500MB', 'error', 4000);
        return;
    }

    // Show new video preview
    const preview = document.getElementById('newVideoPreview');
    const videoElement = document.getElementById('newVideoElement');
    const videoSource = document.getElementById('newVideoSource');
    const videoInfo = document.getElementById('newVideoInfo');

    const url = URL.createObjectURL(file);
    videoSource.src = url;
    videoElement.load();

    videoInfo.textContent = `${file.name} - ${(file.size / 1024 / 1024).toFixed(2)} MB`;
    preview.style.display = 'block';

    // Scroll to preview
    preview.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Elimina el nuevo video seleccionado
 */
function removeNewVideo() {
    document.getElementById('id_video_file').value = '';
    document.getElementById('newVideoPreview').style.display = 'none';
    
    // Revoke object URL to free memory
    const videoSource = document.getElementById('newVideoSource');
    if (videoSource.src) {
        URL.revokeObjectURL(videoSource.src);
        videoSource.src = '';
    }
}

/**
 * Alterna la vista previa del video actual
 */
function toggleVideoPreview() {
    const preview = document.getElementById('currentVideoPreview');
    if (preview.style.display === 'none') {
        preview.style.display = 'block';
    } else {
        preview.style.display = 'none';
    }
}

/**
 * Confirma y elimina el video actual de la presentación
 */
function confirmDeleteVideo() {
    if (confirm('¿Estás seguro de que deseas eliminar el video actual? Esta acción no se puede deshacer.')) {
        // Get presentation ID from URL
        const pathParts = window.location.pathname.split('/');
        const presentationId = pathParts[pathParts.indexOf('presentation') + 1];
        
        // Call delete endpoint
        fetch(`/presentations/presentation/${presentationId}/delete-video/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Hide current video display
                const currentVideoDisplay = document.querySelector('.current-video-display');
                if (currentVideoDisplay) {
                    currentVideoDisplay.remove();
                }
                
                // Show new video section
                const newVideoSection = document.getElementById('newVideoSection');
                if (newVideoSection) {
                    newVideoSection.style.display = 'block';
                }
                
                // Show success message
                showCustomAlert('Video eliminado exitosamente. Ahora puedes subir un nuevo video o grabar en vivo.', 'success', 4000);
            } else {
                showCustomAlert('Error al eliminar el video: ' + (data.message || 'Error desconocido'), 'error', 4000);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showCustomAlert('Error al eliminar el video. Por favor, intenta de nuevo.', 'error', 4000);
        });
    }
}

/**
 * Get CSRF token from cookies
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ===== ASSIGNMENT SELECTION HANDLER =====

const assignmentSelect = document.getElementById('id_assignment');
if (assignmentSelect) {
    assignmentSelect.addEventListener('change', function() {
        const assignmentId = this.value;
        
        if (assignmentId) {
            fetch(`/presentations/api/assignment-details/?assignment_id=${assignmentId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error('Error:', data.error);
                        return;
                    }
                    
                    // Update assignment info in sidebar
                    document.getElementById('assignment-info').innerHTML = `
                        <p><strong>Curso:</strong> ${data.course}</p>
                        <p><strong>Tipo:</strong> ${data.type}</p>
                        <p><strong>Duración máxima:</strong> ${data.max_duration} min</p>
                        <p><strong>Fecha límite:</strong> ${data.due_date}</p>
                        <p><strong>Puntaje máximo:</strong> ${data.max_score} puntos</p>
                        <div class="mt-3">
                            <strong>Instrucciones:</strong>
                            <div class="bg-light p-2 rounded mt-2 small">
                                ${data.instructions || 'No hay instrucciones específicas.'}
                            </div>
                        </div>
                    `;
                })
                .catch(error => {
                    console.error('Error fetching assignment details:', error);
                });
        }
    });
}
