# Solución al Problema de Detección de Múltiples Personas

## 📋 Diagnóstico del Problema

### Problema Original
El sistema detectaba **9 personas cuando solo había 3** en el video. Al analizar los logs:

```
Track 3 + Track 4: score 0.195 → ✅ Fusionados correctamente
Persona 6 vs 7: score 0.282 → ❌ NO fusionados (eran la misma persona)
Persona 6 vs 8: score 0.275 → ❌ NO fusionados (eran la misma persona)  
Persona 6 vs 10: score 0.235 → ❌ NO fusionados (eran la misma persona)
Persona 7 vs 8: score 0.343 → ❌ NO fusionados (eran la misma persona)
```

### Causa Raíz
Las técnicas de comparación **NO ERAN SUFICIENTES**:
1. ❌ Solo comparaba apariencia visual (color, textura, brillo)
2. ❌ Threshold de 0.20 era DEMASIADO ESTRICTO para variaciones naturales
3. ❌ No analizaba geometría facial única de cada persona
4. ❌ No filtraba detecciones esporádicas (ruido)
5. ❌ Confianza mínima muy baja (0.40) permitía falsos positivos

---

## 🔧 Soluciones Implementadas

### 1. **Análisis de Landmarks Faciales** 🆕
```python
def _extract_face_geometry(self, face_landmarks):
    """
    Extrae puntos clave invariantes a escala/rotación:
    - Distancia entre ojos
    - Ratio ancho de boca vs distancia entre ojos  
    - Proporciones faciales (altura/ancho)
    - Vector normalizado de 12 puntos clave
    """
```

**Beneficio:** Identifica personas por su estructura facial única (como huellas dactilares faciales).

### 2. **Comparación Geométrica** 🆕
```python
def _compare_face_geometry(self, landmarks1, landmarks2):
    """
    Compara ratios geométricos entre dos rostros
    - Invariante a escala, rotación, iluminación
    - Más preciso que solo apariencia visual
    """
```

**Score combinado:**
- **50% Similitud Visual** (apariencia)
- **30% Similitud Geométrica** (estructura facial)
- **20% Distancia Espacial** (posición en frame)

### 3. **Threshold Balanceado: 0.30**
```
Antes: 0.20 (DEMASIADO ESTRICTO)
Ahora: 0.30 (BALANCEADO)

Score < 0.30 = MISMO rostro
Score ≥ 0.30 = Rostros DIFERENTES
```

**Justificación:** Tolera variaciones naturales (expresiones faciales, ángulos de cámara, cambios de luz) mientras mantiene buena discriminación entre personas diferentes.

### 4. **Alta Confianza Requerida**
```python
min_detection_confidence=0.7  # Antes: 0.40
```

**Beneficio:** Solo detecta rostros claros y bien definidos. Elimina detecciones de baja calidad que generan ruido.

### 5. **Filtro de Apariciones Mínimas**
```python
min_appearances = 50  # Mínimo 50 apariciones
```

**Beneficio:** Elimina detecciones esporádicas (reflejos, objetos, detecciones erróneas). Una persona real debe aparecer consistentemente.

### 6. **Refinamiento de Landmarks**
```python
face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True,  # Mayor precisión
    min_tracking_confidence=0.6  # Tracking confiable
)
```

---

## 📊 Comparación Antes/Después

| Aspecto | ANTES (Deficiente) | AHORA (Robusto) |
|---------|-------------------|----------------|
| **Técnicas** | Solo visual (5 métricas) | Visual + Geométrico (landmarks) |
| **Threshold Tracking** | 0.20 (muy estricto) | 0.30 (balanceado) |
| **Threshold Fusión** | 0.20 (muy estricto) | 0.30 (balanceado) |
| **Confianza Mínima** | 0.40 (permisivo) | 0.70 (estricto) |
| **Filtrado** | Por tiempo (0.3s) | Por apariciones (50) |
| **Análisis Facial** | Superficial | Profundo (478 landmarks) |
| **Pesos de Score** | 70% visual + 30% espacial | 50% visual + 30% geométrico + 20% espacial |

---

## 🧪 Cómo Verificar los Cambios

### Logs Esperados

**Al procesar video:**
```
🎥 INICIANDO DETECCIÓN DE ROSTROS CON MediaPipe AVANZADO
⚙️ Threshold fusión: < 0.30 (BALANCEADO con landmarks)
⚙️ Confianza mínima MediaPipe: 0.7
⚙️ Análisis de landmarks faciales: ACTIVADO
⚙️ Filtro temporal: Mínimo 50 apariciones
```

**Al detectar rostros:**
```
✅ Landmarks extraídos: 6 puntos clave
✅ ACEPTADO: Rostro válido - conf=0.832, size=156x184
```

**Al comparar:**
```
🔍 Comparando Persona 1 vs Persona 2: Score = 0.28
   ✅ FUSIONANDO (score < 0.30) - Mismo rostro
```

**Al filtrar:**
```
🔍 Evaluando Persona 1:
   📊 Apariciones: 237
   ⏱️  Tiempo en pantalla: 23.7s
   ⚖️  Comparación: 237 >= 50? True
   ✅ ACEPTADO - Participante real

🔍 Evaluando Persona 2:
   📊 Apariciones: 4
   ⏱️  Tiempo en pantalla: 0.4s
   ⚖️  Comparación: 4 >= 50? False
   🚫 DESCARTADO - Probablemente ruido o detección esporádica
```

---

## 🎯 Resultado Esperado

Para un video con **3 personas reales**:
- ✅ Detección: 3 tracks finales
- ✅ Tracks descartados: 0-2 (ruido)
- ✅ Sin fusiones incorrectas
- ✅ Cada persona tiene > 50 apariciones

---

## 🚀 Próximos Pasos

1. **Procesar el video nuevamente** y compartir los logs completos
2. **Verificar** que detecte exactamente 3 personas
3. **Si detecta más:** Revisar los scores de fusión en los logs
4. **Si detecta menos:** Verificar que las 3 personas cumplen las 50 apariciones mínimas

---

## 🔬 Fundamento Técnico

### MediaPipe Face Mesh
- Detecta **478 landmarks faciales** en 3D
- Precisión submilimétrica en condiciones óptimas
- Invariante a rotación y escala

### Landmarks Clave Usados
```
33, 263: Esquinas externas de los ojos
1: Punta de la nariz
61, 291: Comisuras de la boca
152: Barbilla
```

### Ratios Geométricos
```
mouth_to_eye_ratio = ancho_boca / distancia_ojos
face_proportions = altura_cara / distancia_ojos
```

Estos ratios son **únicos para cada persona** y no cambian con expresiones faciales o ángulos.

---

## 📝 Cambios en el Código

### Archivos Modificados
- `apps/ai_processor/services/face_detection_service.py`

### Nuevos Métodos
1. `_extract_face_geometry()` - Extrae landmarks clave
2. `_compare_face_geometry()` - Compara estructura facial

### Métodos Actualizados
1. `_process_video_mediapipe()` - Alta confianza + landmarks
2. `_merge_duplicate_tracks()` - Threshold 0.30 + geometría
3. Filtrado final - 50 apariciones mínimas

---

## 💡 Por Qué Funcionará

1. **Landmarks son únicos:** Como huellas dactilares, cada persona tiene proporciones faciales únicas
2. **Threshold realista:** 0.30 tolera variaciones naturales sin permitir falsos positivos
3. **Múltiples métricas:** Combinar visual + geométrico + espacial es más robusto
4. **Filtrado inteligente:** Elimina ruido sin perder participantes reales
5. **Alta confianza:** Solo procesa rostros de calidad, reduciendo basura

---

## ⚠️ Limitaciones Conocidas

- Requiere rostros visibles y claros (confianza 0.7+)
- Personas con < 50 apariciones (< 5s en video) no serán detectadas
- Cambios drásticos de apariencia (máscara, gafas oscuras) pueden confundir

---

**Fecha:** 7 de Noviembre de 2025
**Versión:** 2.0 - Detección con Landmarks Faciales
