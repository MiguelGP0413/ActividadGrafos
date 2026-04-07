# 🗳️ Mapa de Afinidades Electorales en Colombia

## Descripción del Proyecto

Aplicación interactiva que analiza las estructuras de afinidad electoral en las elecciones colombianas utilizando teoría de grafos y detección de comunidades. El proyecto responde preguntas sobre cómo se agrupan naturalmente departamentos, candidatos y franjas demográficas basándose en patrones de votación.

---

## 📊 Justificación Formal del Grafo

### Definición de Nodos
Los nodos representan tres tipos de actores electorales heterogéneos:
- **Candidatos (6 nodos):** Actores políticos principales con su base de apoyo
- **Departamentos (34 nodos):** Territorios con estructura electoral propia  
- **Franjas demográficas (9 nodos):** Segmentos poblacionales (edad, estrato, educación, ruralidad)

### Definición de Aristas
Una arista conecta dos nodos si existe una relación de afinidad electoral medible:
- **Peso (w):** Porcentaje de votos (0-100), indica intensidad de la afinidad
- **Dirección:** No dirigido (la afinidad es simétrica)
- **Origen:** Matriz electoral real: candidatos × departamentos con % de apoyo

**Justificación:** Las aristas representan el grado en que dos actores comparten preferencias electorales. Un peso alto (ej: 60%) indica que una región votó fuertemente por un candidato, generando una conexión fuerte.

### Tipo de Grafo
- **Modelo:** Grafo simple no dirigido ponderado
- **Tamaño:** ~770 nodos + ~1,800+ aristas
- **Propiedad:** Heterogéneo (múltiples tipos de nodos)
- **Aplicabilidad:** Permite analysisar multiactor networks

---

## 🎯 Funcionalidades Principales (MVP)

### 1. Carga y Construcción del Grafo
✅ Carga automática desde `electoral_nodos.csv` y `electoral_aristas.csv`  
✅ Construcción con atributos preservados  
✅ Filtrado por umbral de peso

### 2. Identificación de Grupos de Afinidad
✅ **Algoritmo Louvain (greedy modularity):** Optimización de modularidad  
✅ **Algoritmo Girvan-Newman:** Eliminación de aristas puente  
✅ Visualización con diferenciación clara de colores

### 3. Parámetros Modificables
✅ **Umbral de peso:** 0-50% - filtra aristas débiles  
✅ **Algoritmo:** Cambiar entre Louvain y Girvan-Newman  
✅ **Número de comunidades:** Para Girvan-Newman, 2-8 grupos

### 4. Panel de Métricas
✅ **Globales:** Nodos, aristas, modularidad, densidad, diámetro  
✅ **Por comunidad:** Tamaño, densidad interna, grado promedio  
✅ **Interpretación:** Indicadores de calidad de la partición

---

## 📋 Respuestas a Preguntas Clave

### ❓ ¿Qué departamentos tienen perfil de votación similar?
**Respuesta visual:** Se muestran en la misma comunidad (color). La aplicación lista todos los departamentos por grupo.

### ❓ ¿Coinciden con regiones geográficas o bloques ideológicos?
**Respuesta:** Se despliega la región geográfica de cada comunidad y se analiza ideología dominante.

### ❓ ¿Qué medios comparten ecosistema con candidatos?
**Respuesta actual:** El dataset no incluye nodos de medios, pero se visualiza la afinidad ideológica latente.

### ❓ ¿Qué franja es más homogénea?
**Respuesta:** Se calcula la franja que aparece en menos comunidades (más compacta).

### ❓ ¿Qué tan pronunciada es la separación?
**Respuesta:** Se reporta la modularidad (0-1). Valores >0.4 indican separación pronunciada.

---

## 🎯 Retos Innovadores Implementados

### 🌉 RETO 1: Análisis de Puentes
**Descripción:** Identifica nodos que actúan como bisagras entre comunidades distintas.

**Implementación:**
- Cálculo de **betweenness centrality** para cada nodo
- Filtrado de nodos que conectan múltiples comunidades
- **Top 10 nodos puente** con ranking
- **Análisis de impacto:** Simulación de eliminación y cambio en componentes conexas
- **Visualización:** Indicadores de qué pasaría sin estos nodos críticos

**Interpretación:**
- Alto betweenness = nodo importante para cohesión global
- Nodos puente pueden ser "bisagras ideológicas" o territorios swing

### 📊 RETO 2: Evolución por Franja Demográfica
**Descripción:** Compara si los grupos de afinidad cambian según el criterio demográfico.

**Implementación:**
- Filtrado de subgrafos por franja (edad, estrato, educación, ruralidad)
- Detección de comunidades en cada subgrafo
- Comparación de modularidad entre criterios
- **Resumen:** Identifica cuál criterio produce partición más clara

**Resultado esperado:**
- Si la modularidad por edad es alta → edad es factor diferenciador
- Si por estrato es baja → menos diferenciación por clase económica

### ⚖️ RETO 3: Comparación de Parámetros
**Descripción:** Compara dos configuraciones del análisis lado a lado.

**Implementación:**
- **Config A:** Parámetros actuales del usuario
- **Config B:** Parámetros alternativos (usuario ajusta umbral)
- **Métricas comparadas:** 
  - Número de comunidades
  - Modularidad
  - Cambios en composición
- **Selección de validez:** Usuario vota cuál configuración es mejor
- **Visualización:** Diferencias resaltadas

---

## 🚀 Cómo Ejecutar

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar la Aplicación
```bash
streamlit run app.py
```

Luego abre en tu navegador: `http://localhost:8501`

---

## 📊 Estructura de Archivos

```
ActividadGrafos/
├── app.py                           # Aplicación principal (Streamlit)
├── electoral_nodos.csv              # Datos de nodos
├── electoral_aristas.csv            # Datos de aristas/relaciones
├── requirements.txt                 # Dependencias Python
└── README.md                        # Este archivo
```

---

## 🔬 Metodología Técnica

### Algoritmos de Detección de Comunidades

#### 1. **Louvain (Greedy Modularity Optimization)**
- **Ventaja:** Rápido, escala bien a grafos grandes
- **Objetivo:** Maximizar modularidad global
- **Fórmula:** Q = (1/2m) Σ [A_ij - (k_i × k_j)/(2m)] × δ(c_i, c_j)
- **Cuándo usar:** Para particiones de máxima calidad general

#### 2. **Girvan-Newman (Edge Betweenness)**
- **Ventaja:** Intuición clara: elimina puentes entre grupos
- **Proceso:** Iteralmente elimina aristas con mayor betweenness
- **Resultado:** Produce hierarchical clustering
- **Cuándo usar:** Para análisis de estructura jerárquica

### Métricas Clave

| Métrica | Rango | Interpretación |
|---------|-------|-----------------|
| **Modularidad** | [0, 1] | >0.4: comunidades bien separadas |
| **Densidad** | [0, 1] | Proporción de aristas posibles realizadas |
| **Betweenness** | [0, 1] | Importancia de nodo como puente |
| **Coef. Clustering** | [0, 1] | Transitividad: si A-B y B-C, ¿A-C? |

---

## 📈 Interpretación de Resultados

### Escenarios Típicos

**Caso 1: Modularidad Alta (>0.5)**
- ✅ Comunidades muy claras
- ✅ Grupos con identidad electoral distinta
- ✅ Pocos nodos puente

**Caso 2: Modularidad Moderada (0.3-0.5)**
- ⚠️ Estructura emergente pero difusa
- ⚠️ Algunos outliers ideológicos
- ⚠️ Puntos de contacto entre bloques

**Caso 3: Modularidad Baja (<0.3)**
- ⚠️ Red muy interconectada
- ⚠️ Afinidades fragmentadas
- ⚠️ Dificultad para polarización clara

---

## 💡 Posibles Usos

1. **Análisis Político:** Identificar coaliciones naturales
2. **Geografía Electoral:** Regiones que votan igual
3. **Segmentación Demográfica:** Perfiles electorales por edad/estrato
4. **Influyentes:** Nodos puente como bisagras de cambio
5. **Predicción:** Inferir voto de nuevos municipios

---

## ⚠️ Limitaciones y Trabajo Futuro

### Actuales
- Dataset sintético/simplificado (real tiene + de 30M votantes)
- No incluye series temporales
- No modela campañas de influencia

### Mejoras Posibles
1. Integrar datos de medios de comunicación
2. Análisis temporal (elecciones 2018, 2022)
3. Modelo de difusión de preferencias
4. Validación con votación real por mesa
5. Análisis de sentimiento en redes sociales

---

## 📚 Referencias

- **NetworkX:** https://networkx.org/
- **Louvain Algorithm:** Blondel et al. (2008)
- **Girvan-Newman:** Girvan & Newman (2002)
- **Graph Clustering:** Schaeffer (2007)

---

## 👤 Autor
Actividad de Análisis de Grafos - Semestre 2026

---

**Última actualización:** Abril 2026
