# Mejora en Filtrado de Falsos Positivos

## 📋 Problema Identificado

Durante el procesamiento se detectó **Persona 2 con solo 3 apariciones** que fue descartada automáticamente. El análisis mostró:

```
Persona 2 vs Persona 1:
- Score geométrico: 0.409 (MUY diferente)
- Score visual: 0.324
- Score final: 0.384 → NO fusionado ✓ CORRECTO

Persona 2: 3 apariciones
→ DESCARTADO (< 50 frames mínimo)
```

### Posibles Causas

1. **Falso positivo**: Sombra, reflejo, objeto confundido como rostro
2. **Detección débil**: Rostro parcial o mal iluminado con baja confianza
3. **Participación brevísima**: Persona real que aparece < 1 segundo

## 🎯 Solución Implementada

### 1. Aumentar Confianza Mínima de Detección

**Antes**:
```python
min_detection_confidence=0.70  # ALTA
min_tracking_confidence=0.60
```

**Después**:
```python
min_detection_confidence=0.75  # MUY ALTA - evita falsos positivos
min_tracking_confidence=0.65   # Mayor confianza en tracking
```

**Efecto**: MediaPipe solo detecta rostros con **75%+ de confianza**, eliminando detecciones débiles (sombras, reflejos, rostros borrosos) ANTES de crear tracks.

### 2. Reducir Umbral Mínimo de Apariciones

**Antes**:
```python
min_appearances = 50  # ~5 segundos @ 30fps con sample_rate=3
```

**Después**:
```python
min_appearances = 30  # ~3 segundos @ 30fps con sample_rate=3
```

**Cálculo**:
- Sample rate: 3 (procesa 1 de cada 3 frames)
- Video @ 30fps
- 30 apariciones × 3 frames/aparición ÷ 30 fps = **3 segundos**
- 50 apariciones × 3 frames/aparición ÷ 30 fps = **5 segundos**

**Efecto**: Captura participaciones breves válidas (3+ segundos) sin permitir falsos positivos (< 1 segundo).

## 📊 Balance Alcanzado

### Prevención de Falsos Positivos

| Mecanismo | Umbral | Efecto |
|-----------|--------|---------|
| **Confianza inicial** | 0.75 | Elimina detecciones débiles ANTES de tracking |
| **Validación landmarks** | Requerida | Descarta rostros sin estructura facial clara |
| **Tamaño mínimo** | 30×30 píxeles | Ignora rostros muy pequeños o lejanos |
| **Apariciones mínimas** | 30 frames | Elimina detecciones esporádicas post-fusión |

### Detección de Participaciones Válidas

| Duración | Frames Detectados | ¿Se Detecta? | Motivo |
|----------|-------------------|--------------|---------|
| < 1 seg | < 10 frames | ❌ NO | Falso positivo probable |
| 1-3 seg | 10-30 frames | ⚠️ DUDOSO | Depende de confianza |
| 3+ seg | 30+ frames | ✅ SÍ | Participación válida |
| 5+ seg | 50+ frames | ✅ SÍ (antes) | Participación clara |

## 🔬 Proceso de Filtrado por Capas

```
CAPA 1: Detección MediaPipe
├─ Confianza < 0.75? → DESCARTADO
├─ Sin landmarks? → DESCARTADO  
├─ Tamaño < 30px? → DESCARTADO
└─ ✅ PASA A TRACKING

CAPA 2: Tracking y Comparación
├─ Score < 0.28 con track existente? → AÑADIR A TRACK
└─ Score >= 0.28 con todos? → NUEVO TRACK

CAPA 3: Fusión Temporal
├─ Gap < 3s Y geometría < 0.20? → FUSIONAR (corte de edición)
└─ Score < 0.28? → FUSIONAR (misma persona)

CAPA 4: Filtrado Final
├─ Apariciones < 30? → DESCARTADO (ruido/brevísimo)
└─ Apariciones >= 30? → ✅ PARTICIPANTE VÁLIDO
```

## 📈 Resultados Esperados

### Caso: Persona 2 (3 apariciones, score 0.409)

```
1. ✅ Pasó confianza 0.75 (detección inicial fuerte)
2. ✅ Pasó validación de landmarks
3. ✅ Creó track separado (score 0.409 >> 0.28)
4. ❌ DESCARTADO en filtrado final (3 << 30 apariciones)
```

**Diagnóstico**: Probablemente falso positivo fuerte (sombra con forma de rostro) o persona que apareció brevemente (< 1 segundo) y desapareció.

**Resultado**: ✅ Sistema funcionó correctamente - descartó detección con muy pocas apariciones.

### Caso: Persona Real con 3 Segundos de Aparición

```
Frames esperados: 30 apariciones
├─ 1. ✅ Confianza 0.75+ en múltiples frames
├─ 2. ✅ Landmarks consistentes
├─ 3. ✅ Tracking exitoso (30+ apariciones)
└─ 4. ✅ DETECTADO como participante
```

**Resultado**: ✅ Sistema detecta participaciones válidas de 3+ segundos.

## 🎬 Casos Especiales

### Editing Cuts con Pocas Apariciones

Si una persona aparece 2 segundos, luego hay un corte, luego aparece 2 segundos más:

```
Aparición 1: 20 frames → Track temporal
Gap: < 3s
Aparición 2: 20 frames → Track temporal

Fusión temporal:
├─ Gap < 3s? ✅ SÍ
├─ Geometría similar? ✅ SÍ (< 0.20)
└─ FUSIONAR → 40 frames totales → ✅ DETECTADO
```

### Falsos Positivos Recurrentes

Si una sombra/reflejo aparece múltiples veces:

```
Apariciones: 5 frames + 3 frames + 4 frames + ... = 25 frames total
├─ Confianza variable (algunas < 0.75)
├─ Geometría inconsistente
└─ Total < 30 frames → ❌ DESCARTADO
```

## ✅ Conclusión

**Balance óptimo alcanzado**:
- **Confianza 0.75**: Elimina falsos positivos débiles temprano
- **Umbral 30 frames**: Capta participaciones válidas (3+ seg) sin ruido
- **Resultado**: Sistema robusto que detecta personas reales y descarta detecciones esporádicas

**Comportamiento con Persona 2**:
- ✅ Correctamente identificada como diferente (score 0.409)
- ✅ Correctamente descartada por pocas apariciones (3 frames)
- ✅ No afectó detección de las 3 personas principales

---

**Versión**: V5  
**Fecha**: 2025-11-07  
**Cambios**: Confianza 0.70→0.75, Umbral 50→30 frames
