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

window.skipTime = function(seconds) {
    const video = document.getElementById('presentationVideo');
    if (video) {
        const newTime = video.currentTime + seconds;
        // Asegurar que no se pase de los límites
        if (newTime < 0) {
            video.currentTime = 0;
        } else if (newTime > video.duration) {
            video.currentTime = video.duration;
        } else {
            video.currentTime = newTime;
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
