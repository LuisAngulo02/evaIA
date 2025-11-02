/**
 * EvalExpo AI - JavaScript para Calificación de Presentaciones
 * Funciones para la vista de calificación y revisión de presentaciones
 */

// Video controls - Declaradas globalmente
window.togglePlayPause = function() {
    const video = document.getElementById('presentationVideo');
    const icon = document.getElementById('playPauseIcon');
    
    if (video) {
        if (video.paused) {
            video.play();
            if (icon) icon.className = 'fas fa-pause';
        } else {
            video.pause();
            if (icon) icon.className = 'fas fa-play';
        }
    }
};

window.skipTime = function(seconds, retryCount = 0) {
    const video = document.getElementById('presentationVideo');
    if (!video) {
        console.warn('Video element not found');
        return;
    }
    
    // Verificar que el video tenga duración válida
    if (!video.duration || isNaN(video.duration) || video.duration === 0 || video.duration === Infinity) {
        // Solo mostrar advertencia en el primer intento
        if (retryCount === 0) {
            console.warn('Video duration not available, waiting...');
        }
        // Intentar cargar el video primero
        if (video.readyState < 1) {
            video.load();
        }
        // Reintentar hasta 10 veces (5 segundos)
        if (retryCount < 10) {
            setTimeout(() => window.skipTime(seconds, retryCount + 1), 500);
        }
        return;
    }
    
    // Calcular el nuevo tiempo
    let newTime = video.currentTime + seconds;
    
    // Asegurar que no se pase de los límites
    newTime = Math.max(0, Math.min(newTime, video.duration));
    
    // Verificar que la posición sea seekable
    let isSeekable = false;
    let maxSeekable = 0;
    
    if (video.seekable && video.seekable.length > 0) {
        for (let i = 0; i < video.seekable.length; i++) {
            const start = video.seekable.start(i);
            const end = video.seekable.end(i);
            maxSeekable = Math.max(maxSeekable, end);
            
            if (newTime >= start && newTime <= end) {
                isSeekable = true;
                break;
            }
        }
    } else {
        // Si no hay información de seekable, asumir que es seekable
        isSeekable = true;
    }
    
    if (!isSeekable) {
        // Si la posición no es seekable, intentar con la posición máxima cargada
        if (maxSeekable > 0 && newTime > maxSeekable) {
            // Solo mostrar advertencia cada 3 reintentos
            if (retryCount % 3 === 0) {
                console.log(`Esperando buffer: ${maxSeekable.toFixed(1)}s / ${newTime.toFixed(1)}s`);
            }
            // Reintentar hasta 20 veces (10 segundos)
            if (retryCount < 20) {
                setTimeout(() => window.skipTime(seconds, retryCount + 1), 500);
            } else {
                // Después de 10 segundos, ir a la posición máxima disponible
                console.log('Moviéndose a la posición máxima cargada:', maxSeekable);
                newTime = maxSeekable - 0.5; // Un poco antes del final del buffer
                isSeekable = true;
            }
        }
        
        if (!isSeekable) {
            return;
        }
    }
    
    // Solo log en el primer intento o cuando finalmente funciona
    if (retryCount === 0 || (retryCount > 0 && isSeekable)) {
        console.log(`Seek: ${video.currentTime.toFixed(1)}s → ${newTime.toFixed(1)}s`);
    }
    
    // Guardar el estado de reproducción
    const wasPlaying = !video.paused;
    
    // Pausar si está reproduciendo (ayuda con el seek)
    if (wasPlaying) {
        video.pause();
    }
    
    // Realizar el seek
    try {
        video.currentTime = newTime;
        
        // Reanudar reproducción si estaba reproduciéndose
        if (wasPlaying) {
            // Esperar a que el seek termine
            video.addEventListener('seeked', function onSeeked() {
                video.play().catch(err => {
                    if (retryCount === 0) {
                        console.warn('No se pudo reanudar:', err);
                    }
                });
            }, { once: true });
        }
    } catch (error) {
        if (retryCount === 0) {
            console.error('Error al hacer seek:', error);
        }
    }
};

window.toggleFullscreen = function() {
    const video = document.getElementById('presentationVideo');
    if (video) {
        if (video.requestFullscreen) {
            video.requestFullscreen();
        } else if (video.webkitRequestFullscreen) {
            video.webkitRequestFullscreen();
        } else if (video.msRequestFullscreen) {
            video.msRequestFullscreen();
        }
    }
};

// Score input handling
window.initScorePreview = function(maxScore) {
    const scoreInput = document.getElementById('final_score');
    const scoreFill = document.getElementById('scoreFill');
    const scorePercentage = document.getElementById('scorePercentage');
    
    if (!scoreInput || !scoreFill || !scorePercentage) return;
    
    function updateScorePreview() {
        const value = parseFloat(scoreInput.value) || 0;
        const percentage = Math.min((value / maxScore) * 100, 100);
        
        scoreFill.style.width = percentage + '%';
        scorePercentage.textContent = percentage.toFixed(1) + '%';
        
        // Change color based on score
        if (percentage >= 90) {
            scoreFill.style.background = '#28a745';
        } else if (percentage >= 70) {
            scoreFill.style.background = '#28a745';
        } else if (percentage >= 50) {
            scoreFill.style.background = '#ffc107';
        } else {
            scoreFill.style.background = '#dc3545';
        }
    }
    
    scoreInput.addEventListener('input', updateScorePreview);
    updateScorePreview(); // Initial update
};

// Toggle participant feedback
window.toggleParticipantFeedback = function(header) {
    const content = header.nextElementSibling;
    const icon = header.querySelector('.fa-chevron-down, .fa-chevron-up');
    
    const isHidden = content.style.display === 'none' || 
                     window.getComputedStyle(content).display === 'none';
    
    if (isHidden) {
        content.style.display = 'block';
        if (icon) {
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
        }
    } else {
        content.style.display = 'none';
        if (icon) {
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
        }
    }
};

// Initialize video event listeners
window.initVideoControls = function() {
    const video = document.getElementById('presentationVideo');
    const icon = document.getElementById('playPauseIcon');
    
    if (video && icon) {
        video.addEventListener('play', () => {
            icon.className = 'fas fa-pause';
        });
        
        video.addEventListener('pause', () => {
            icon.className = 'fas fa-play';
        });
        
        video.addEventListener('ended', () => {
            icon.className = 'fas fa-play';
        });
    }
};

// Participants comparison chart
window.initParticipantsChart = function(participantsData) {
    const canvas = document.getElementById('participantsChart');
    if (!canvas || !participantsData || participantsData.length === 0) return;
    
    const ctx = canvas.getContext('2d');
    
    // Simple bar chart
    const barWidth = canvas.width / participantsData.length - 20;
    const maxValue = 100;
    const chartHeight = canvas.height - 80;
    
    participantsData.forEach((participant, index) => {
        const x = index * (barWidth + 20) + 20;
        const barHeight = (participant.coherence / maxValue) * chartHeight;
        const y = canvas.height - barHeight - 30;
        
        // Draw bar
        const gradient = ctx.createLinearGradient(0, y, 0, y + barHeight);
        gradient.addColorStop(0, '#667eea');
        gradient.addColorStop(1, '#764ba2');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(x, y, barWidth, barHeight);
        
        // Draw value on top
        ctx.fillStyle = '#2c3e50';
        ctx.font = 'bold 14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(participant.coherence.toFixed(1) + '%', x + barWidth/2, y - 5);
        
        // Draw label
        ctx.fillStyle = '#6c757d';
        ctx.font = '12px Arial';
        ctx.fillText(participant.name, x + barWidth/2, canvas.height - 10);
    });
    
    // Draw axis
    ctx.strokeStyle = '#dee2e6';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(10, canvas.height - 30);
    ctx.lineTo(canvas.width - 10, canvas.height - 30);
    ctx.stroke();
};

// Las funciones ya están exportadas a window arriba directamente
