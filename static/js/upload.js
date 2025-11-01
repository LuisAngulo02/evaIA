/**
 * EvalExpo AI - Upload de Archivos
 * Maneja drag & drop, validación y preview de archivos de video
 */

// Elementos del DOM
let fileInput, uploadZone, filePreview, fileName, fileSize;

/**
 * Inicializa el sistema de upload de archivos
 * @param {string} fileInputId - ID del input de archivo
 */
function initFileUpload(fileInputId) {
    fileInput = document.getElementById(fileInputId);
    uploadZone = document.getElementById('upload-zone');
    filePreview = document.getElementById('file-preview');
    fileName = document.getElementById('file-name');
    fileSize = document.getElementById('file-size');

    if (!fileInput) {
        console.warn('File input not found');
        return;
    }

    setupFileInputListeners();
    setupDragAndDrop();
}

/**
 * Configura los event listeners del input de archivo
 */
function setupFileInputListeners() {
    // Cambio en el input (click o programático)
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            handleFileSelection(file);
        }
    });

    // Click en la zona de upload
    if (uploadZone) {
        uploadZone.addEventListener('click', function() {
            fileInput.click();
        });
    }
}

/**
 * Configura el sistema de drag and drop
 */
function setupDragAndDrop() {
    if (!uploadZone) return;

    // Prevenir comportamiento por defecto
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight cuando se arrastra sobre la zona
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadZone.addEventListener(eventName, highlight, false);
    });

    // Remover highlight al salir
    ['dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, unhighlight, false);
    });

    // Manejar archivo soltado
    uploadZone.addEventListener('drop', handleDrop, false);
}

/**
 * Previene comportamientos por defecto del navegador
 */
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

/**
 * Agrega clase de highlight
 */
function highlight(e) {
    if (uploadZone) {
        uploadZone.classList.add('dragover');
    }
}

/**
 * Remueve clase de highlight
 */
function unhighlight(e) {
    if (uploadZone) {
        uploadZone.classList.remove('dragover');
    }
}

/**
 * Maneja archivos arrastrados y soltados
 */
function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        const file = files[0];
        
        // Validar tipo de archivo
        if (!isValidVideoFile(file)) {
            showCustomAlert('Formato de archivo no válido. Use MP4, AVI, MOV, MKV o WEBM', 'error', 4000);
            return;
        }

        // Asignar archivo al input
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        handleFileSelection(file);
    }
}

/**
 * Valida si el archivo es un video válido
 * @param {File} file - Archivo a validar
 * @returns {boolean}
 */
function isValidVideoFile(file) {
    const validTypes = [
        'video/mp4',
        'video/avi',
        'video/mov',
        'video/quicktime',
        'video/x-msvideo',
        'video/webm',
        'video/x-matroska'
    ];
    return validTypes.includes(file.type);
}

/**
 * Maneja la selección de archivo (drag & drop o click)
 * @param {File} file - Archivo seleccionado
 */
function handleFileSelection(file) {
    // Validar tamaño (500MB máx)
    const MAX_SIZE = 500 * 1024 * 1024;
    if (file.size > MAX_SIZE) {
        showCustomAlert('El archivo es demasiado grande. Máximo 500MB permitido.', 'error', 4000);
        removeFile();
        return;
    }

    // Actualizar UI con info del archivo
    if (fileName && fileSize && filePreview) {
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        filePreview.style.display = 'block';
    }

    // Ocultar zona de upload
    if (uploadZone) {
        uploadZone.style.display = 'none';
    }
}

/**
 * Formatea el tamaño del archivo a una cadena legible
 * @param {number} bytes - Tamaño en bytes
 * @returns {string}
 */
function formatFileSize(bytes) {
    const mb = bytes / 1024 / 1024;
    if (mb >= 1) {
        return mb.toFixed(2) + ' MB';
    }
    const kb = bytes / 1024;
    return kb.toFixed(2) + ' KB';
}

/**
 * Remueve el archivo seleccionado y resetea la UI
 */
function removeFile() {
    if (fileInput) {
        fileInput.value = '';
    }
    
    if (filePreview) {
        filePreview.style.display = 'none';
    }
    
    if (uploadZone) {
        uploadZone.style.display = 'block';
    }
}

// Exportar funciones para uso global
window.initFileUpload = initFileUpload;
window.removeFile = removeFile;
