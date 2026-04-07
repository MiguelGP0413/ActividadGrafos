# 📁 ÍNDICE DE ARCHIVOS - Mapa de Afinidades Electorales

## 🎯 COMIENZA AQUÍ

```
👤 PRIMER USO
├─ 1️⃣ Lee: QUICKSTART.md (5 min)
├─ 2️⃣ Ejecuta: instalar.bat
├─ 3️⃣ Abre: ejecutar.bat
├─ 4️⃣ Explora: http://localhost:8501
└─ 5️⃣ Lee el "Resumen Ejecutivo" en la app
```

---

## 📋 ESTRUCTURA COMPLETA

### 1️⃣ APLICACIÓN PRINCIPAL

#### `app.py` (1,200+ líneas)
**QUÉ ES:** Aplicación Streamlit interactiva  
**PARA QUÉ:** Ejecutar análisis en tiempo real  
**ESTRUCTURA:**
```python
[1] Importaciones y configuración
[2] Carga de datos (caché)
[3] Construcción de grafo
[4] Algoritmos de detección de comunidades
[5] Análisis de centralidad y puentes
[6] Sidebar con parámetros
[7] Panel principal:
    ├─ Visualización del grafo
    ├─ Análisis de comunidades
    ├─ Respuestas a preguntas clave
    ├─ RETO 1: Análisis de Puentes
    ├─ RETO 2: Evolución por Franja
    ├─ RETO 3: Comparación de Parámetros
    ├─ Resumen ejecutivo
```

**CÓMO UTILIZAR:**
```bash
streamlit run app.py
# O hacer doble click en: ejecutar.bat
```

---

### 2️⃣ HERRAMIENTAS DE ANÁLISIS

#### `analisis_avanzado.py` (400+ líneas)
**QUÉ ES:** Script de análisis offline  
**PARA QUÉ:** Reportes detallados sin interfaz web  
**PRODUCE:**
- Análisis de centralidad (Top 20)
- Ranking de departamentos
- Estadísticas globales
- Reporte en texto: `reporte_analisis_TIMESTAMP.txt`

**CÓMO UTILIZAR:**
```bash
python analisis_avanzado.py
```

**OUTPUT:**
```
reporte_analisis_20260404_153022.txt
  ├─ Resumen de hallazgos
  ├─ Top 20 puentes
  ├─ Rankings de departamentos
  └─ Componentes conexas
```

---

#### `validador_datos.py` (200+ líneas)
**QUÉ ES:** Verificador de integridad  
**PARA QUÉ:** Detectar errores antes de ejecutar  
**VALIDA:**
- Existencia de archivos CSV
- Estructura correcta
- IDs únicos
- Referencias válidas
- Rangos de valores
- Conectividad del grafo

**CÓMO UTILIZAR:**
```bash
python validador_datos.py
```

---

### 3️⃣ DATOS

#### `electoral_nodos.csv`
**QUÉ CONTIENE:** 66 nodos (candidatos, departamentos, franjas demográficas)

**ESTRUCTURA:**
```csv
node_id,nombre,tipo,subtipo,atributo_1,atributo_1_label,...
CAN_01,Paloma Valencia,candidato,derecha,...
DEP_01,Bogotá D.C.,departamento,izquierda,...
FRA_01,18-25 años,franja_demografica,edad,...
```

**TIPOS:**
- **Candidatos (6):** CAN_01 a CAN_06
- **Departamentos (34):** DEP_01 a DEP_34
- **Franjas (9):** FRA_01 a FRA_09

**NO EDITAR:** Los datos son integrales en el análisis

---

#### `electoral_aristas.csv`
**QUÉ CONTIENE:** 1000+ relaciones ponderadas

**ESTRUCTURA:**
```csv
edge_id,origen,destino,tipo_arista,peso,votos_estimados,...
E0001,CAN_01,DEP_01,voto_candidato_departamento,47.98,1798109,...
```

**ATRIBUTOS:**
- `peso`: Porcentaje 0-100 (intensidad de apoyo)
- `votos_estimados`: Número estimado de votos
- `afinidad_bloque`: 0 o 1 (ideología)

**NO EDITAR:** Los datos son integrales en el análisis

---

### 4️⃣ DOCUMENTACIÓN

#### `README.md` (PRINCIPAL)
**QUÉ CONTIENE:**
- Descripción del proyecto
- Justificación formal del grafo
- MVP (Calificación 3.0) - Detallado
- Respuestas a 5 preguntas clave
- 3 Retos explicados
- Cómo ejecutar
- Metodología técnica
- Interpretación de resultados
- Referencias bibliográficas

**CUÁNDO LEER:**
- Primero para entender el proyecto
- Para fundamentación teórica
- Para interpretar resultados

---

#### `QUICKSTART.md` (GUÍA RÁPIDA)
**QUÉ CONTIENE:**
- Instalación en 5 minutos
- Primeros pasos
- Significado de métricas
- 3 Ejercicios prácticos
- Troubleshooting

**CUÁNDO LEER:**
- Si acabas de descargar
- Para empezar rápido
- Si hay problemas

---

#### `RETOS_ESPECIFICACION.md` (TÉCNICO)
**QUÉ CONTIENE:**
- Especificación completa de cada reto
- Algoritmos matemáticos
- Implementación détaille
- Casos de uso electoral
- Matrices de validación
- Mockups visuales

**CUÁNDO LEER:**
- Para entender retos profundamente
- Para modificar código
- Para validación técnica

---

#### `RESUMEN_EJECUTIVO.md`
**QUÉ CONTIENE:**
- Resumen de todo el proyecto
- Archivos entregados
- MVP checklist
- Instrucciones completas
- Flujo recomendado
- Métricas de éxito
- Extensiones posibles

**CUÁNDO LEER:**
- Para ver estado general
- Para evaluación
- Para próximos pasos

---

#### `INDICE.md` (ESTE ARCHIVO)
**QUÉ CONTIENE:**
- Guía de navegación
- Propósito de cada archivo
- Dónde encontrar qué
- Quicklinks

---

### 5️⃣ INSTALACIÓN Y EJECUCIÓN

#### `requirements.txt`
**QUÉ CONTIENE:**
```
streamlit==1.36.0
pandas==2.0.3
numpy==1.24.3
networkx==3.2
plotly==5.18.0
scipy==1.11.1
scikit-learn==1.3.1
```

**CÓMO USAR:**
```bash
pip install -r requirements.txt
```

---

#### `instalar.bat` (Windows)
**QUÉ HACE:**
1. Verifica Python instalado
2. Instala dependencias
3. Confirma éxito

**CÓMO USAR:**
```batch
# Doble click en instalar.bat
O
.\instalar.bat
```

---

#### `ejecutar.bat` (Windows)
**QUÉ HACE:**
1. Verifica Streamlit instalado
2. Inicia la aplicación
3. Abre navegador en localhost:8501

**CÓMO USAR:**
```batch
# Doble click en ejecutar.bat
O
.\ejecutar.bat
```

---

## 🔍 BÚSQUEDA RÁPIDA

### Por Pregunta
```
¿Qué departamentos juntos?
  → app.py → Panel "Análisis de Comunidades" → Tab "Composición"

¿Coincide con regiones?
  → app.py → Panel "Respuestas a Preguntas Clave" → Pregunta 2

¿Franja más homogénea?
  → app.py → Panel "Respuestas a Preguntas Clave" → Pregunta 4

¿Separación entre grupos?
  → app.py → Panel "Resumen Ejecutivo" → Métrica "Modularidad"
```

### Por Reto
```
RETO 1: Puentes
  → app.py → Panel "RETO 1: Análisis de Puentes"
  → RETOS_ESPECIFICACION.md → Sección "RETO 1"

RETO 2: Franjas
  → app.py → Panel "RETO 2: Evolución por Franja"
  → RETOS_ESPECIFICACION.md → Sección "RETO 2"

RETO 3: Parámetros
  → app.py → Panel "RETO 3: Comparación de Parámetros"
  → RETOS_ESPECIFICACION.md → Sección "RETO 3"
```

### Por Concepto Técnico
```
Construcción del grafo
  → app.py → Función "construir_grafo"
  → README.md → Sección "Justificación Formal del Grafo"

Algoritmos de clustering
  → app.py → Funciones "detectar_comunidades_*"
  → README.md → Sección "Metodología Técnica"
  → RETOS_ESPECIFICACION.md → Sección correspondiente

Betweenness centrality
  → app.py → Función "identificar_puentes"
  → RETOS_ESPECIFICACION.md → RETO 1 → "Implementación Técnica"

Métricas
  → app.py → Función "calcular_metricas_*"
  → README.md → Tabla "Métricas Clave"
```

---

## 📊 FLUJO RECOMENDADO

```
INSTALACIÓN:
  1. Lee QUICKSTART.md (5 min)
  2. Ejecuta instalar.bat (2 min)
  ✓ Listo para usar

PRIMER ANÁLISIS:
  3. Ejecuta ejecutar.bat
  4. Lee el "Resumen Ejecutivo" en la app (3 min)
  5. Activa los 3 retos en sidebar
  6. Explora cada sección (15 min)
  ✓ Entiendes la herramienta

ANÁLISIS PROFUNDO:
  7. Lee README.md (20 min)
  8. Lee RETOS_ESPECIFICACION.md (20 min)
  9. Ejecuta analisis_avanzado.py
  10. Compara resultados
  ✓ Análisis completo

DOCUMENTACIÓN:
  11. Usa INDICE.md como guía
  12. Consulta RESUMEN_EJECUTIVO.md para próximos pasos
  ✓ Proyecto documentado
```

---

## 🎯 CHECKLIST DE FUNCIONALIDAD

### MVP (Calificación 3.0)
- ✅ Cargar dataset y construir grafo
- ✅ Identificar grupos con visualización clara
- ✅ Modificar parámetros en tiempo real
- ✅ Panel con métricas de calidad

### Preguntas Clave
- ✅ ¿Qué departamentos juntos?
- ✅ ¿Coincide con regiones?
- ✅ ¿Medios de comunicación?
- ✅ ¿Franja más homogénea?
- ✅ ¿Separación entre grupos?

### Retos Innovadores
- ✅ RETO 1: Análisis de Puentes
- ✅ RETO 2: Evolución por Franja
- ✅ RETO 3: Comparación de Parámetros

### Documentación
- ✅ README con fundamentos
- ✅ QUICKSTART para inicio rápido
- ✅ RETOS_ESPECIFICACION técnico
- ✅ RESUMEN_EJECUTIVO evaluación
- ✅ INDICE para navegación

### Herramientas
- ✅ app.py interactiva
- ✅ analisis_avanzado.py reportes
- ✅ validador_datos.py verificación
- ✅ Scripts de instalación

---

## 🔗 SIGUIENTES PASOS

1. **Instala:** `instalar.bat`
2. **Ejecuta:** `ejecutar.bat`
3. **Lee:** RESUMEN_EJECUTIVO.md en la app
4. **Explora:** Los 3 retos activados
5. **Analiza:** Según flujo recomendado arriba

---

## 📞 REFERENCIAS RÁPIDAS

| Necesitas | Archivo |
|---|---|
| Empezar ahora | QUICKSTART.md |
| Entender teoría | README.md |
| Detalles técnicos | RETOS_ESPECIFICACION.md |
| Ver estado | RESUMEN_EJECUTIVO.md |
| Navegar | INDICE.md (aquí) |
| Reportes | analisis_avanzado.py |
| Verificar datos | validador_datos.py |

---

**Proyecto Completo y Listo para Usar** ✅  
**Versión:** 1.0  
**Fecha:** Abril 2026
