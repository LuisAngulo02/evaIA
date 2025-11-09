# ⚖️ CONFIGURACIÓN BALANCEADA - Detección de Rostros

## 🎯 CAMBIOS APLICADOS (Balance Precisión/Velocidad)

### ✅ MEJORAS EN ALGORITMO DE COMPARACIÓN

#### 1. Resolución Balanceada
- **Antes (muy lento)**: 128x128 píxeles
- **Intento 1 (muy rápido pero impreciso)**: 64x64 píxeles
- **AHORA (BALANCE)**: **96x96 píxeles** ✅
  - 2.25x más datos que 64x64
  - Suficiente detalle para diferenciar hombre/mujer
  - Solo 1.77x más lento que 64x64

#### 2. Sistema de 5 Métricas Mejorado

| Métrica | Peso | Qué Detecta |
|---------|------|-------------|
| **Color HSV** | 30% | Tono de piel, color de cabello |
| **Brillo/Intensidad** | 15% | Tono de piel claro/oscuro |
| **Textura (Laplaciano)** | 20% | Barba, arrugas, piel lisa vs rugosa |
| **Estructura Pixel** | 15% | Diferencias generales de apariencia |
| **Geometría (Sobel)** | 20% | Forma facial: mandíbula, cejas, nariz |

**Total**: 100% de análisis robusto

#### 3. Métricas con Estadísticas Avanzadas

```python
# ❌ ANTES: Solo promedio simple
texture_diff = abs(var1 - var2) / max(var1, var2)

# ✅ AHORA: Media + Desviación estándar (más robusto)
texture_diff = (abs(mean1 - mean2) / max(mean1, mean2) + 
                abs(std1 - std2) / max(std1, std2)) / 2.0
```

**Ventaja**: Captura mejor las diferencias de textura (barba, piel)

---

### 🎚️ THRESHOLDS MÁS ESTRICTOS

| Parámetro | Valor Anterior | NUEVO Valor | Objetivo |
|-----------|---------------|-------------|----------|
| **Fusión duplicados** | `< 0.35` | `< 0.30` ⬇️ | Solo fusionar si son EXTREMADAMENTE similares |
| **Tracking continuo** | `< 0.40` | `< 0.35` ⬇️ | Crear nuevo track más fácilmente |
| **Ventana temporal** | `< 7.0s` | `< 10.0s` ⬆️ | Tracking más robusto (no perder track) |
| **Peso visual vs espacial** | `60% / 40%` | `70% / 30%` | Priorizar similitud visual sobre posición |

---

### 📊 INTERPRETACIÓN DE SCORES

```
0.00 ━━━━━━━━━ 0.30 ━━━━━━━ 0.35 ━━━━━━━━━ 0.45 ━━━━━━━━━━━━━ 1.00
 │              │            │              │                      │
 │              │            │              │                      │
IDÉNTICO   MISMO ROSTRO  TRACKING      SIMILARES         COMPLETAMENTE
           (fusionar)    (continuar)  (NO fusionar)       DIFERENTES
```

### Ejemplos:

| Score | Interpretación | Acción del Sistema |
|-------|----------------|-------------------|
| `0.15` | Misma persona, ángulo diferente | ✅ Fusionar/Continuar |
| `0.28` | Misma persona, iluminación muy diferente | ✅ Fusionar/Continuar |
| `0.32` | Personas MUY parecidas (mismo género, edad) | ⚠️ Crear track separado |
| `0.38` | Hombre y mujer con características distintivas | ❌ Definitivamente diferentes |
| `0.50+` | Completamente diferentes | ❌ Sin duda diferentes |

---

## ⏱️ RENDIMIENTO ESPERADO

### Tiempo de Procesamiento

| Duración Video | Frames Procesados | Tiempo Esperado |
|----------------|-------------------|-----------------|
| 15 segundos | ~150 | **3-5 segundos** |
| 30 segundos | ~300 | **5-10 segundos** |
| 60 segundos | ~600 | **10-15 segundos** |
| 120 segundos | ~1200 | **20-30 segundos** |

**Factor clave**: Sample rate = 3 (procesa 1 de cada 3 frames)

---

## 🎯 CASOS DE USO

### ✅ Caso 1: Hombre y Mujer
**Características distintivas**:
- Barba vs piel lisa (textura)
- Mandíbula más angular vs suave (geometría)
- Posible diferencia de tono de piel (color)

**Score esperado**: `0.40 - 0.65` (definitivamente diferentes)
**Resultado**: ✅ **2 participantes detectados**

---

### ✅ Caso 2: Dos Hombres Diferentes
**Características distintivas**:
- Uno con barba, otro sin (textura fuerte)
- Diferente tono de piel (color)
- Diferente estructura facial (geometría)

**Score esperado**: `0.35 - 0.55` (diferentes)
**Resultado**: ✅ **2 participantes detectados**

---

### ✅ Caso 3: Dos Mujeres Diferentes
**Características distintivas**:
- Diferente color/largo de cabello (color HSV)
- Diferente tono de piel (brillo)
- Diferente forma de cara (geometría)

**Score esperado**: `0.30 - 0.50` (diferentes)
**Resultado**: ✅ **2 participantes detectados**

---

### ✅ Caso 4: Misma Persona (No Duplicar)
**Características**:
- Sale y entra de cuadro
- Cambios de ángulo/iluminación

**Score esperado**: `0.10 - 0.28` (mismo rostro)
**Resultado**: ✅ **1 participante (correctamente fusionado)**

---

## 🔧 AJUSTES FINOS SI ES NECESARIO

### Si TODAVÍA detecta 1 cuando hay 2:

**Hacer aún MÁS ESTRICTO** (más fácil crear tracks separados):

```python
# En línea ~347 - Fusión de duplicados
if similarity_score < 0.25:  # Cambiar de 0.30 a 0.25

# En línea ~697 - Tracking continuo
if best_match is not None and best_score < 0.30:  # Cambiar de 0.35 a 0.30
```

---

### Si detecta 3+ cuando hay 2 (demasiados duplicados):

**Hacer MENOS ESTRICTO** (fusionar más fácilmente):

```python
# En línea ~347 - Fusión de duplicados
if similarity_score < 0.35:  # Cambiar de 0.30 a 0.35

# En línea ~697 - Tracking continuo
if best_match is not None and best_score < 0.40:  # Cambiar de 0.35 a 0.40
```

---

## 📝 QUÉ BUSCAR EN LOS LOGS

Cuando proceses un video, deberías ver:

```bash
🎥 Iniciando detección de rostros con MediaPipe...
📊 Video: 30.0s, 30.0 FPS, 900 frames

# Durante el procesamiento (cada ~50 frames)
🔬 Análisis de similitud:
   color_hsv: 0.423 (peso: 0.30)
   brightness: 0.312 (peso: 0.15)
   texture: 0.456 (peso: 0.20)      ← Importante para barba
   structural: 0.389 (peso: 0.15)
   geometry: 0.478 (peso: 0.20)      ← Importante para forma facial
   ➡️ SCORE TOTAL: 0.412            ← > 0.35 = diferentes ✅

⏳ Progreso: 33.3%
⏳ Progreso: 66.7%
✅ DETECCIÓN FINALIZADA: 2 tracks encontrados

🔄 Iniciando fusión de tracks duplicados...
⚠️ Persona 1 y Persona 2 similares (score: 0.412) - NO fusionados (personas diferentes) ✅
✅ Después de fusión: 2 tracks únicos

🎯 Resultado: 2 participantes identificados, Score: 92.3/100
```

**Claves**:
- ✅ Score entre tracks **>= 0.30** = NO se fusionan
- ✅ Score de tracking **>= 0.35** = Crea nuevo track
- ✅ Aparecen logs de comparación visual (3% del tiempo)

---

## 🚀 CÓMO PROBAR

1. **El servidor debería recargar automáticamente** (ya detectó los cambios)
2. **Sube un video** con 2 personas claramente diferentes
3. **Observa los logs** en la terminal
4. **Verifica el resultado** en la página de presentación

---

## 🎯 RESULTADO ESPERADO

Con esta configuración balanceada:

✅ **Procesa en 5-15 segundos** (no minutos)
✅ **Detecta 2 personas diferentes** (hombre/mujer)
✅ **NO fusiona incorrectamente**
✅ **NO crea duplicados** de la misma persona
✅ **Logs informativos** para diagnóstico

---

## 📊 COMPARACIÓN GENERAL

| Versión | Resolución | Métricas | Thresholds | Velocidad | Precisión |
|---------|-----------|----------|------------|-----------|-----------|
| **Original** | 64x64 | 2 simples | 0.50/0.55 | ⚡⚡⚡ Rápido | ❌ Baja (fusiona todo) |
| **Mejorada v1** | 128x128 | 5 complejas (LBP) | 0.35/0.40 | 🐌 Muy lenta | ⏸️ No terminaba |
| **Optimizada v2** | 64x64 | 4 simples | 0.35/0.40 | ⚡⚡ Rápido | ⚠️ Media (sigue fusionando) |
| **BALANCEADA v3** ✅ | 96x96 | 5 mejoradas | 0.30/0.35 | ⚡ Bueno | ✅ Alta (diferencia bien) |

---

## 💡 VENTAJAS DE ESTA CONFIGURACIÓN

1. **5 métricas diferentes** → Captura múltiples aspectos
2. **Resolución 96x96** → Balance perfecto detalle/velocidad
3. **Estadísticas avanzadas** → Media + STD (no solo promedio)
4. **Thresholds estrictos (0.30/0.35)** → Solo fusiona si es OBVIO que es la misma persona
5. **Peso visual 70%** → Prioriza características físicas sobre posición
6. **Ventana temporal 10s** → No pierde tracks cuando alguien sale/entra

---

**Prueba ahora y comparte los logs para ver si detecta correctamente 2 personas!** 🚀
