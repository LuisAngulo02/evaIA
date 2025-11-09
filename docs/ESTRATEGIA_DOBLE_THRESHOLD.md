# Estrategia de Doble Threshold: Separar Primero, Fusionar Después

## 📋 Problema Identificado

El sistema estaba **fusionando incorrectamente hombre con mujer durante el tracking**:

```
🔬 ANÁLISIS DE SIMILITUD (TRACKING):
   Scores: 0.06 - 0.13 (MUY bajos)
   Resultado: FUSIONADO incorrectamente ❌

🔍 Comparando Persona 1 vs Persona 3 (POST-FUSIÓN):
   GEOMETRÍA: 0.249 (DIFERENTE)
   VISUAL: 0.551 (MUY diferente)
   Score: 0.340 > 0.28
   Resultado: NO FUSIONADO ✓ (pero ya era tarde)
```

### ¿Por Qué Sucedía?

1. **Tracking usa imagen de REFERENCIA** (primera detección guardada)
2. **Post-fusión usa PROMEDIO** de todas las apariciones
3. **Pesos diferentes** entre tracking y fusión
4. **Threshold bajo (0.28)** permitía fusiones incorrectas tempranas

**Resultado**: Una vez fusionados en tracking, la post-fusión no podía separarlos.

## 🎯 Solución: Estrategia de Doble Threshold

### Filosofía

> **"Es mejor crear tracks separados y fusionar después, que fusionar incorrectamente desde el inicio"**

La post-fusión tiene mejor información (todas las apariciones) y más contexto (análisis temporal), por lo que debe ser la responsable de unir personas reales.

## 📊 Configuración de Thresholds

### TRACKING (Fase 1): Moderado

```python
# Threshold: 0.30 (BALANCE - ni muy estricto ni muy permisivo)
# Pesos: 20% visual + 60% geométrico + 20% espacial

if combined_score < 0.30:
    # Continuar track existente
else:
    # Crear NUEVO track (separar)
```

**Objetivo**: Balance entre evitar fusiones incorrectas y no crear demasiados tracks innecesarios.

### POST-FUSIÓN (Fase 2): Permisiva

```python
# Threshold: 0.28 (MÁS BAJO - más fácil fusionar)
# Pesos: 30% visual + 70% geométrico (sin espacial)

if combined_score < 0.28:
    # FUSIONAR tracks (misma persona)
else:
    # Mantener separados (personas diferentes)
```

**Objetivo**: Unir tracks legítimos de la misma persona que fueron separados en tracking por precaución.

### POST-FUSIÓN CON CORTE DE EDICIÓN (Fase 2b): Muy Permisiva

```python
# Threshold: 0.28
# Pesos: 20% visual + 80% geométrico (máximo peso a geometría)

if gap < 3.0s AND geometric_score < 0.20:
    # Aplicar pesos especiales (80% geometría)
    if combined_score < 0.28:
        # FUSIONAR (probable corte de edición)
```

**Objetivo**: Tolerar cambios drásticos de iluminación en cortes de edición.

## � Comparación de Pesos

| Fase | Visual | Geométrico | Espacial | Threshold | Estrategia |
|------|--------|-----------|----------|-----------|------------|
| **Tracking** | 20% | 60% | 20% | **0.30** | MODERADO (balance) |
| **Post-Fusión Normal** | 30% | 70% | 0% | **0.28** | PERMISIVO (unir) |
| **Post-Fusión Corte** | 20% | 80% | 0% | **0.28** | MUY PERMISIVO (unir) |

## 📈 Flujo de Procesamiento

```
FRAME 1-N: TRACKING
├─ Detectar rostro
├─ Comparar con tracks existentes
├─ Score < 0.35? → Añadir a track
└─ Score >= 0.35? → NUEVO TRACK (separar por precaución)

RESULTADO: 5 tracks detectados
├─ Persona 1: 238 apariciones
├─ Persona 2: 3 apariciones (falso positivo)
├─ Persona 3: 502 apariciones
├─ Persona 4: 389 apariciones
└─ Persona 5: 526 apariciones

POST-TRACKING: FUSIÓN
├─ Comparar todos los tracks entre sí
├─ Score < 0.28? → FUSIONAR
├─ Gap < 3s + Geo < 0.20? → FUSIONAR (corte de edición)
└─ Score >= 0.28? → MANTENER SEPARADOS

RESULTADO: 3 tracks finales
├─ Persona 1: 764 apariciones (fusionó con Persona 5)
├─ Persona 2: DESCARTADO (< 30 apariciones)
└─ Persona 3: 891 apariciones (fusionó con Persona 4)
```

## 🎭 Casos de Uso

### Caso 1: Misma Persona con Diferentes Iluminaciones

```
Tracking:
├─ Frame 100: Persona con luz normal → Track 1
├─ Frame 500: Misma persona con sombra → Score 0.36
└─ Resultado: NUEVO TRACK 2 (separado por precaución)

Post-Fusión:
├─ Comparar Track 1 vs Track 2
├─ Geometría: 0.15 (MUY similar - misma estructura facial)
├─ Visual: 0.40 (diferente por luz)
├─ Score: 0.227 < 0.28
└─ Resultado: FUSIONADOS ✅ (misma persona)
```

### Caso 2: Hombre vs Mujer

```
Tracking (threshold 0.30):
├─ Frame 100: Mujer → Track 1
├─ Frame 200: Hombre → Score esperado: 0.25-0.35
├─ Si score < 0.30 → FUSIONADO ⚠️ (error posible)
└─ Si score >= 0.30 → SEPARADO ✓ (correcto)

Post-Fusión (detección):
├─ Comparar Track 1 vs Track 2
├─ Geometría: 0.24-0.30 (diferentes estructuras faciales)
├─ Visual: 0.40-0.55 (muy diferentes)
├─ Score: 0.30-0.40 > 0.28
└─ NO FUSIONADO ✓ (personas diferentes)
```

**Balance**: Threshold 0.30 en tracking reduce riesgo pero no lo elimina. Post-fusión actúa como red de seguridad.

## 🔧 Configuración Final

### ~~Mejora Adicional Necesaria~~ **REMOVIDA**

~~**Actualizar imagen de referencia periódicamente**~~ ❌ CAUSÓ PROBLEMAS

**Problema detectado**: Sistema de actualización de referencia causaba:
1. **Fotos azules**: Conversión de color BGR/RGB incorrecta
2. **Scores inflados**: color_hsv: 1.000 (máximo) hacía todos los scores altos (0.46-0.67)
3. **Fusión incorrecta**: 3 personas fusionadas en 1 solo track

**Solución**: Eliminado sistema de actualización automática. Se usa la primera imagen capturada durante todo el tracking.

### Configuración Estable Final

**Tracking**:
- Threshold: **0.30** (balance moderado)
- Pesos: 20% visual + 60% geométrico + 20% espacial
- Sin actualización de referencia automática

**Post-Fusión**:
- Threshold: **0.28** (permisivo)
- Pesos normal: 30% visual + 70% geométrico
- Pesos cortes: 20% visual + 80% geométrico

## 📊 Resultados Esperados

### Sin Estrategia de Doble Threshold (ANTES)

```
Tracking con threshold 0.28:
├─ 3 tracks detectados
├─ Hombre + Mujer fusionados ❌
└─ Post-fusión no puede arreglar

Resultado: 2 personas detectadas (INCORRECTO)
```

### Con Estrategia de Doble Threshold (AHORA)

```
Tracking con threshold 0.35:
├─ 5 tracks detectados (más conservador)
├─ Algunos tracks legítimos separados ✓
└─ Algunos tracks ilegítimos aún fusionados ⚠️

Post-Fusión con threshold 0.28:
├─ Fusiona tracks legítimos (misma persona)
├─ Detecta cortes de edición
└─ Mantiene separados personas diferentes

Resultado: 3 personas detectadas (CORRECTO)
```

## ⚠️ Limitación Actual

**Si el tracking fusiona incorrectamente**, la post-fusión NO puede separarlos porque:
- Ya se perdió la información individual de cada track
- Solo tiene promedios de rostros mezclados
- Geometría promedio no discrimina bien entre hombre/mujer fusionados

**Próxima mejora necesaria**: Actualizar imagen de referencia durante tracking para evitar fusiones incorrectas desde el inicio.

---

**Versión**: V7  
**Fecha**: 2025-11-07  
**Cambios**: 
- Tracking threshold: 0.35 → 0.30 (balance moderado)
- Tracking pesos: 20%+60%+20% (sin cambios)
- Eliminado: Sistema de actualización automática de referencia (causaba fotos azules)
- Estado: Configuración estable y funcional
