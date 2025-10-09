# Guía de Usuario - EvalExpo AI

## **¿Qué es EvalExpo AI?**

EvalExpo AI es una plataforma educativa inteligente que utiliza **Inteligencia Artificial** para evaluar presentaciones de video de estudiantes. El sistema analiza automáticamente aspectos como contenido, fluidez, lenguaje corporal y calidad de voz, proporcionando retroalimentación detallada tanto para estudiantes como docentes.

---

## **Tipos de Usuarios**

### **Estudiantes**
- Suben videos de sus presentaciones
- Reciben análisis automático por IA
- Consultan sus calificaciones y retroalimentación
- Descargan reportes de su progreso

### 👨‍🏫 **Docentes**
- Gestionan cursos y asignaciones
- Califican presentaciones con apoyo de IA
- Generan reportes de rendimiento
- Exportan calificaciones en PDF


---

## **Primeros Pasos**

###  **1. Registro e Inicio de Sesión**

#### **Acceder al Sistema:**
1. Abrir navegador web
2. Ir a: `http://127.0.0.1:8000` (desarrollo local)
3. Hacer clic en **"Iniciar Sesión"**

#### **Credenciales de Prueba:**
- **Docente:** `docente1` / `123456`
- **Estudiantes:** `estudiante1`, `estudiante2`, `estudiante3`, `estudiante4`, `estudiante5` / `123456`

###  **2. Perfiles de Usuario**
Cada usuario tiene un perfil con:
- Información personal
- Avatar personalizable
- Configuraciones de cuenta
- Historial de actividad

---

## **Guía Para Estudiantes**

###  **1. Subir una Presentación**

#### **Pasos para Subir:**
1. **Acceder** → Ir al Dashboard de Estudiante
2. **Navegar** → Clic en "Subir Presentación"
3. **Completar Formulario:**
   - Título de la presentación
   - Descripción o notas
   - Seleccionar asignación
   - Cargar archivo de video (.mp4, .avi, .mov)
4. **Enviar** → Clic en "Subir Presentación"

#### **Formatos Soportados:**
- **Video:** MP4, AVI, MOV
- **Tamaño máximo:** 100 MB
- **Duración:** Según límites de la asignación

###  **2. Ver Mis Presentaciones**

#### **Información Disponible:**
- **Estado:** Subida, Procesando, Analizada, Calificada
- **Análisis IA:** Puntajes automáticos
- **Calificación Final:** Nota del docente
- **Retroalimentación:** Comentarios del profesor

#### **Estados de Presentación:**
- 🔵 **Subida:** Video cargado exitosamente
- 🟡 **Procesando:** IA analizando el contenido
- 🟢 **Analizada:** Análisis IA completado
- ⭐ **Calificada:** Evaluación final del docente
- 🔴 **Error:** Problema en el procesamiento

###  **3. Consultar Calificaciones**

#### **Ver Reportes:**
1. **Acceder** → Dashboard → "Mis Calificaciones"
2. **Explorar:**
   - Promedio general
   - Mejor calificación
   - Número total de presentaciones
   - Cursos participados

#### **Exportar Reportes:**
1. **Ir a** → "Mis Calificaciones"
2. **Clic en** → "Descargar Reporte PDF"
3. **Obtener:** Archivo PDF con historial completo

###  **4. Entender el Análisis IA**

#### **Métricas Evaluadas:**
- **📋 Contenido (0-100%):** Relevancia y estructura del tema
- **🗣️ Fluidez (0-100%):** Tiempo de participación


#### **Cómo Interpretar:**
- **85-100%:** Excelente
- **70-84%:** Bueno
- **60-69%:** Regular
- **Menos de 60%:** Necesita mejora

---

##  **Guía Para Docentes**

###  **1. Gestionar Cursos**

#### **Crear un Curso:**
1. **Dashboard** → "Gestionar Cursos"
2. **Clic** → "Crear Nuevo Curso"
3. **Completar:**
   - Código del curso (ej: PROG101)
   - Nombre del curso
   - Descripción
   - Estado (Activo/Inactivo)
4. **Guardar** → Clic en "Crear Curso"

#### **Editar/Eliminar Cursos:**
- **Editar:** Clic en ícono de lápiz
- **Eliminar:** Clic en ícono de basura
- **Desactivar:** Cambiar estado a inactivo

###  **2. Crear Asignaciones**

#### **Nueva Asignación:**
1. **Dashboard** → "Gestionar Asignaciones"
2. **Crear Nueva** → Completar formulario:
   - Título de la asignación
   - Descripción detallada
   - Curso asignado
   - Tipo de presentación
   - Duración máxima (minutos)
   - Fecha límite
   - Puntaje máximo
   - Instrucciones específicas

#### **Tipos de Presentación:**
- **Presentación Individual**
- **Presentación Grupal**
- **Debate**
- **Conferencia**
- **Pitch de Negocio**
- **Seminario**

###  **3. Calificar Presentaciones**

#### **Proceso de Calificación:**
1. **Acceder** → "Calificar Presentaciones"
2. **Seleccionar** → Presentación a evaluar
3. **Revisar:**
   - Video de la presentación
   - Análisis automático de IA
   - Métricas individuales
4. **Calificar:**
   - Asignar puntaje final (0-100)
   - Escribir retroalimentación
   - Considerar análisis IA como referencia
5. **Guardar** → Confirmar calificación

#### **Herramientas de Calificación:**
- ** Reproductor de video** integrado
- ** Sugerencias de IA** automáticas
- ** Editor de retroalimentación** con plantillas
- ** Métricas detalladas** por categoría

###  **4. Reportes y Analytics**

#### **Ver Estadísticas:**
1. **Dashboard** → "Reportes y Analytics"
2. **Analizar:**
   - Total de presentaciones
   - Promedio general de calificaciones
   - Rendimiento por curso
   - Progreso de estudiantes

#### **Exportar Datos:**
- **PDF General:** Todas las calificaciones
- **PDF por Curso:** Datos específicos de un curso
- **Reportes Detallados:** Análisis completo

---

##  **Navegación del Sistema**

###  **Menú Principal**

#### **Para Estudiantes:**
- ** Dashboard:** Resumen personal
- ** Subir Presentación:** Nueva presentación
- ** Mis Presentaciones:** Historial personal
- ** Mis Calificaciones:** Notas y reportes

#### **Para Docentes:**
- ** Dashboard:** Panel de control
- ** Cursos:** Gestión de materias
- ** Asignaciones:** Tareas y proyectos
- ** Calificar:** Evaluar presentaciones
- ** Reportes:** Analytics y exportación

###  **Interfaz de Usuario**

#### **Características del Diseño:**
- ** Responsive:** Funciona en móvil y desktop
- ** Moderno:** Diseño limpio y profesional
- ** Rápido:** Navegación fluida
- ** Intuitivo:** Iconos y colores significativos

---

##  **Características Técnicas**

###  **Análisis de IA**

#### **Tecnologías Utilizadas:**
- **Procesamiento de Video:** Análisis automático
- **Reconocimiento de Voz:** Transcripción automática

#### **Proceso Automático:**
1. **Subida** → Video cargado al servidor
2. **Extracción** → Audio y frames del video
3. **Análisis** → IA procesa múltiples aspectos
4. **Puntuación** → Generación de métricas
5. **Feedback** → Sugerencias automáticas

### **Gestión de Archivos**

#### **Almacenamiento:**
- Videos guardados de forma segura
- Respaldos automáticos
- Compresión optimizada
- Acceso controlado por permisos

#### **Formatos y Límites:**
- **Formatos:** MP4, AVI, MOV, WMV
- **Tamaño máximo:** 100 MB por archivo
- **Duración:** Configurable por asignación
- **Resolución:** Hasta 1080p recomendado

---

##  **Exportación de Datos**

###  **Reportes en PDF**

#### **Para Docentes:**
- **Reporte General:** Todas las calificaciones
- **Por Curso:** Datos específicos de materia
- **Contenido incluido:**
  - Lista de estudiantes
  - Calificaciones finales
  - Puntajes de IA
  - Estadísticas generales
  - Fechas de evaluación

#### **Para Estudiantes:**
- **Mi Reporte Personal:** Historial completo
- **Contenido incluido:**
  - Todas mis presentaciones
  - Calificaciones recibidas
  - Retroalimentación docente
  - Progreso académico
  - Estadísticas personales

###  **Proceso de Exportación**
1. **Seleccionar** → Tipo de reporte deseado
2. **Clic** → "Exportar Reporte PDF"
3. **Esperar** → Generación automática
4. **Descargar** → Archivo listo para usar

---

##  **Preguntas Frecuentes (FAQ)**

###  **Para Estudiantes**

**Q: ¿Qué formatos de video puedo subir?**
A: MP4, AVI, MOV y WMV hasta 100 MB.

**Q: ¿Cuánto tarda el análisis de IA?**
A: Entre 5-15 minutos dependiendo de la duración del video.

**Q: ¿Puedo subir la misma presentación varias veces?**
A: Sí, pero solo la última versión será evaluada.

**Q: ¿Cómo mejoro mi puntaje de IA?**
A: Practica la fluidez, mantén contacto visual, organiza bien el contenido.

###  **Para Docentes**

**Q: ¿Puedo modificar las calificaciones después?**
A: Sí, puedes editar calificaciones en cualquier momento.

**Q: ¿Cómo uso el análisis de IA para calificar?**
A: Úsalo como referencia, pero tu criterio profesional es definitivo.

**Q: ¿Puedo crear múltiples cursos?**
A: Sí, no hay límite en el número de cursos.

**Q: ¿Los estudiantes ven las métricas de IA?**
A: Sí, pueden ver todos los puntajes automáticos.

---

##  **Solución de Problemas**

###  **Problemas Comunes**

#### **Error al Subir Video:**
- ✅ Verificar formato del archivo
- ✅ Confirmar tamaño menor a 100 MB  
- ✅ Revisar conexión a internet
- ✅ Intentar con otro navegador

#### **Video No se Procesa:**
- ✅ Esperar 15 minutos máximo
- ✅ Verificar que el video tenga audio
- ✅ Confirmar que no esté corrupto
- ✅ Contactar soporte técnico

#### **No Puedo Ver Calificaciones:**
- ✅ Verificar que la presentación esté calificada
- ✅ Refrescar la página
- ✅ Verificar permisos de acceso
- ✅ Revisar filtros aplicados

#### **Exportación No Funciona:**
- ✅ Confirmar que hay datos para exportar
- ✅ Verificar permisos del navegador
- ✅ Permitir descargas automáticas
- ✅ Intentar desde otro dispositivo

---

##  **Seguridad y Privacidad**

###  **Protección de Datos**



#### **Privacidad:**
- Videos solo visibles para docente y estudiante propietario
- Calificaciones confidenciales
- Datos personales protegidos
- Cumplimiento de normativas educativas

---


##  **Requisitos del Sistema**

###  **Requisitos Mínimos**

#### **Navegador Web:**
- Chrome 90+ (Recomendado)
- Firefox 88+
- Safari 14+
- Edge 90+

#### **Conexión a Internet:**
- Mínimo: 5 Mbps para subida
- Recomendado: 10 Mbps o superior
- Estable para videos largos

#### **Hardware:**
- **RAM:** 4 GB mínimo
- **Procesador:** Dual-core 2.0 GHz
- **Almacenamiento:** 100 MB libres
- **Cámara/Micrófono:** Para grabación de videos

---

##  **Consejos y Mejores Prácticas**

###  **Para Mejores Presentaciones**

#### **Preparación del Video:**
- ** Calidad:** Grabar en HD (1080p)
- ** Audio:** Usar micrófono externo si es posible
- ** Iluminación:** Luz frontal clara y uniforme
- ** Encuadre:** Mostrar desde cintura hacia arriba

#### **Durante la Presentación:**
- ** Contacto visual:** Mirar directamente a la cámara
- ** Claridad:** Hablar despacio y articular bien
- ** Estructura:** Introducción, desarrollo, conclusión clara

###  **Para Docentes**

#### **Estrategias de Evaluación:**
- ** Usar IA como apoyo:** No como reemplazo del criterio profesional
- ** Retroalimentación constructiva:** Comentarios específicos y útiles
- ** Evaluar prontamente:** Responder en máximo 5 días hábiles
- ** Analizar tendencias:** Usar reportes para mejorar la enseñanza

#### **Gestión Eficiente:**
- ** Organizar cursos:** Usar códigos claros y descriptivos
- ** Asignaciones detalladas:** Instrucciones específicas y criterios claros
- ** Fechas límite realistas:** Dar tiempo suficiente para preparación
- ** Monitoreo regular:** Revisar progreso semanalmente

---

##  **Glosario de Términos**

** Asignación:** Tarea específica que requiere una presentación
** IA (Inteligencia Artificial):** Sistema automatizado de análisis
** Dashboard:** Panel principal de control del usuario
** Presentación:** Video subido por el estudiante para evaluación
** Calificación:** Nota final asignada por el docente
** Retroalimentación:** Comentarios del profesor sobre la presentación
** Reporte:** Documento PDF con datos de rendimiento
** Procesamiento:** Análisis automático del video por IA
** Perfil:** Información personal y configuración del usuario
** Curso:** Materia o asignatura académica

---

**© 2025 EvalExpo AI - Todos los derechos reservados**

