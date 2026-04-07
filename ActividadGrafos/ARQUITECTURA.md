# 🏗️ ARQUITECTURA DEL PROYECTO

## Diagrama de Flujo Completo

```
┌──────────────────────────────────────────────────────────────────┐
│              MAPA DE AFINIDADES ELECTORALES                      │
│                     (Aplicación Completa)                        │
└──────────────────────────────────────────────────────────────────┘

ENTRADA
├─ electoral_nodos.csv (66 nodos)
└─ electoral_aristas.csv (1000+ aristas)
        ↓
        ↓
┌──────────────────────────────────────────┐
│   MÓDULO 1: CARGA Y CONSTRUCCIÓN         │
├──────────────────────────────────────────┤
│ • Leer CSV                               │
│ • Validar integridad                     │
│ • Construir grafo no dirigido ponderado  │
│ • Aplicar umbral de peso                 │
└──────┬───────────────────────────────────┘
       ↓
┌──────────────────────────────────────────┐
│   MÓDULO 2: DETECCIÓN DE COMUNIDADES     │
├──────────────────────────────────────────┤
│ • Louvain (Greedy Modularity)           │
│   - Optimización directa                 │
│ • Girvan-Newman (Edge Betweenness)      │
│   - Eliminación iterativa                │
└──────┬───────────────────────────────────┘
       ↓
┌──────────────────────────────────────────┐
│   MÓDULO 3: ANÁLISIS DE CENTRALIDAD      │
├──────────────────────────────────────────┤
│ • Degree centrality                      │
│ • Betweenness centrality                 │
│ • Eigenvector centrality                 │
│ • Clustering coefficient                 │
└──────┬───────────────────────────────────┘
       ↓
┌──────────────────────────────────────────────────────────────────┐
│   MÓDULO 4: RETOS INNOVADORES                                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  RETO 1: Análisis de Puentes              RETO 2: Franjas       │ 
│  ├─ Betweenness ranking                   ├─ Edad (4 franjas)   │
│  ├─ Nodos inter-comunidad                 ├─ Estrato (3)        │
│  ├─ Simulación de impacto                 ├─ Educación (2)      │
│  └─ Top 20 puentes                        ├─ Subgrafos          │
│                                           ├─ Homogeneidad       │
│                                           └─ Comparativa        │
│                                                                   │
│  RETO 3: Comparación de Parámetros                              │
│  ├─ Config A (Actual)                                            │
│  ├─ Config B (Alternativa)                                       │
│  ├─ Métricas lado a lado                                         │
│  └─ Selección de validez                                         │
│                                                                   │
└──────┬────────────────────────────────────────────────────────────┘
       ↓
┌──────────────────────────────────────────┐
│   MÓDULO 5: VISUALIZACIÓN                │
├──────────────────────────────────────────┤
│ • Grafo interactivo (Plotly)             │
│ • Colores por comunidad                  │
│ • Tamaño por grado                       │
│ • Hover con información                  │
│ • Controles interactivos                 │
└──────┬───────────────────────────────────┘
       ↓
┌──────────────────────────────────────────┐
│   MÓDULO 6: MÉTRICAS Y REPORTES          │
├──────────────────────────────────────────┤
│ • Modularidad global                     │
│ • Densidad por comunidad                 │
│ • Betweenness por nodo                   │
│ • Tamaño de grupos                       │
│ • Respuestas a preguntas clave           │
└──────┬───────────────────────────────────┘
       ↓
SALIDA
├─ Interfaz web interactiva (Streamlit)
├─ Visualización de grafo (Plotly)
├─ Tabla de métricas
├─ Análisis de retos
└─ Reporte ejecutivo

SALIDA ALTERNATIVA (Análisis Avanzado)
└─ reporte_analisis_TIMESTAMP.txt
```

---

## Arquitectura de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                        APP.PY                                   │
│                    (Streamlit)                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐     ┌──────────────────┐                │
│  │  SIDEBAR         │     │  MAIN PANEL      │                │
│  │                  │     │                  │                │
│  │ Parámetros:      │────→│ Visualización:   │                │
│  │ • Umbral peso    │     │ • Grafo (Plotly)│                │
│  │ • Algoritmo      │     │ • Métricas      │                │
│  │ • Num comunidades│     │ • Análisis      │                │
│  │ • Retos activos  │     │ • Respuestas    │                │
│  │                  │     │                 │                │
│  └──────────────────┘     └─────────┬────────┘                │
│                                     │                          │
│  ┌──────────────────────────────────▼────────────────────────┐ │
│  │         DATOS PROCESADOS EN TIEMPO REAL                  │ │
│  │                                                          │ │
│  │  • Grafo (NetworkX)                                     │ │
│  │  • Comunidades detectadas                               │ │
│  │  • Centralidad calculada                                │ │
│  │  • Métricas actualizadas                                │ │
│  │                                                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

FUNCIONES PRINCIPALES:
├─ construir_grafo() → Carga datos y crea NetworkX Graph
├─ detectar_comunidades_louvain() → Algoritmo Louvain
├─ detectar_comunidades_girvan_newman() → Algoritmo GN
├─ identificar_puentes() → Nodos inter-comunidad
├─ calcular_metricas_globales() → Métricas de grafo
└─ calcular_metricas_comunidad() → Métricas de grupo
```

---

## Flujo de Interacción del Usuario

```
USUARIO
   ↓
   ├─→ 1. ABRE http://localhost:8501
   │       ↓
   │   Streamlit carga app.py
   │       ↓
   │
   ├─→ 2. SIDEBAR: Ajusta parámetros
   │   ├─ Umbral de peso (slider)
   │   │   ↓ Recalcula grafo
   │   ├─ Algoritmo (selectbox)
   │   │   ↓ Cambia comunidades
   │   ├─ Num comunidades (GN slider)
   │   │   ↓ Ajusta granularidad
   │   └─ Retos (checkboxes)
   │       ↓ Muestra/oculta paneles
   │
   ├─→ 3. MAIN PANEL: Observa resultados
   │   ├─ Métricas globales (widgets)
   │   ├─ Grafo interactivo (Plotly)
   │   │   • Hover → Información nodo
   │   │   • Zoom/Pan → Exploración
   │   ├─ Análisis de comunidades
   │   │   • Tab "Composición" → Lista nodos
   │   │   • Tab "Métricas" → Tabla datos
   │   │   • Tab "Características" → Gráficos
   │   └─ Respuestas a preguntas clave
   │
   ├─→ 4. RETOS: Explora análisis avanzados
   │   ├─ RETO 1: Puentes
   │   │   ├─ Top 10 tabla
   │   │   └─ Expanders con análisis
   │   ├─ RETO 2: Franjas
   │   │   ├─ Dropdown criterio
   │   │   └─ Tarjetas por franja
   │   └─ RETO 3: Parámetros
   │       ├─ Config A vs B lado a lado
   │       └─ Radio para seleccionar
   │
   └─→ 5. RESUMEN: Lee conclusiones
       └─ Panel "Resumen Ejecutivo"
```

---

## Estructura de Datos

```
ENTRADA: DataFrame (Pandas)
┌──────────────────────┬──────────────────────┐
│  electoral_nodos     │  electoral_aristas   │
├──────────────────────┼──────────────────────┤
│ node_id (str)        │ origen (str)         │
│ nombre (str)         │ destino (str)        │
│ tipo (str)           │ peso (float)         │
│ subtipo (str)        │ votos_estimados (int)│
│ región (str)         │ afinidad_bloque (int)│
│ atributos (var)      │                      │
└──────────────────────┴──────────────────────┘
         ↓                      ↓
    PROCESADO
┌──────────────────────────────────────────────┐
│        NetworkX.Graph()                      │
├──────────────────────────────────────────────┤
│ Nodos: 66                                   │
│  ├─ atributos: {nombre, tipo, región, ...} │
│  └─ propiedades: grado, centralidad, ...    │
│                                             │
│ Aristas: 1000+                              │
│  ├─ weight: float (0-100)                   │
│  └─ propiedades: betweenness, ...           │
└──────────────────────────────────────────────┘
         ↓
    ANALIZADO
┌──────────────────────────────────────────────┐
│  Comunidades (list of sets)                  │
│  ├─ Comunidad 1: {CAN_01, DEP_01, ...}     │
│  ├─ Comunidad 2: {CAN_02, DEP_05, ...}     │
│  └─ Comunidad 3: {DEP_10, FRA_01, ...}     │
│                                             │
│  Centrality (dict)                          │
│  ├─ Betweenness: {nodo: score, ...}        │
│  ├─ Degree: {nodo: count, ...}             │
│  └─ Eigenvector: {nodo: score, ...}        │
│                                             │
│  Métricas (dict)                            │
│  ├─ Global: {modularity, density, ...}     │
│  └─ Por comunidad: {size, edges, ...}      │
└──────────────────────────────────────────────┘
         ↓
    VISUALIZADO
┌──────────────────────────────────────────────┐
│  Plotly Figure                              │
│  ├─ Nodos: scatter (colors, sizes)          │
│  ├─ Aristas: lines (weights)                │
│  ├─ Hover: información dinámica             │
│  └─ Layout: spring layout 2D                │
└──────────────────────────────────────────────┘
```

---

## Ciclo de Ejecución

```
START (Inicio)
   ↓
┌──────────────────────────────┐
│ app.py ejecutado por Streamlit│
└─────────┬────────────────────┘
          ↓
┌──────────────────────────────┐
│ Datos cargados (caché)       │
│ → electoral_nodos.csv        │
│ → electoral_aristas.csv      │
└─────────┬────────────────────┘
          ↓
┌──────────────────────────────┐
│ Construir Grafo              │
│ • Agregar nodos              │
│ • Agregar aristas            │
│ • Aplicar umbral             │
└─────────┬────────────────────┘
          ↓
         / \
        /   \ ¿Parámetros
       /     \ cambiaron?
      /       \
   NO ↙         ↘ SÍ
     │           ├─ Reconstruir grafo
     │           └─ Volver a analizar
     │
     ↓
┌──────────────────────────────┐
│ Detectar Comunidades         │
│ • Ejecutar Louvain O         │
│ • Ejecutar Girvan-Newman     │
└─────────┬────────────────────┘
          ↓
┌──────────────────────────────┐
│ Calcular Centralidad         │
│ • Betweenness                │
│ • Degree                     │
│ • Eigenvector                │
│ • Clustering                 │
└─────────┬────────────────────┘
          ↓
┌──────────────────────────────┐
│ Calcular Métricas            │
│ • Modularidad                │
│ • Densidad                   │
│ • Diámetro                   │
│ • Por comunidad              │
└─────────┬────────────────────┘
          ↓
┌──────────────────────────────┐
│ Renderizar Interfaz          │
│ • Sidebar con parámetros     │
│ • Visualización grafo        │
│ • Tablas de datos            │
│ • Gráficos de análisis       │
│ • Paneles de retos           │
└─────────┬────────────────────┘
          ↓
┌──────────────────────────────┐
│ Usuario interactúa           │
│ → Cambia parámetro           │
│ → Lee resultados             │
│ → Expande secciones          │
│ → Selecciona retos           │
└─────────┬────────────────────┘
          ↓
         / \
        /   \ ¿Cambios del
       /     \ usuario?
      /       \
    SÍ ↙       ↘ NO
     │         │
     │         ├─→ Espera entrada
     │         │
     └─────────┘
          ↑
          │
LOOP (mientras el usuario interactúe)
```

---

## Stack Tecnológico Simplificado

```
┌─────────────────────────────────────────┐
│           USUARIO (Navegador)           │
└──────────────────┬──────────────────────┘
                   ↓ HTTP
┌─────────────────────────────────────────┐
│        STREAMLIT (Frontend Web)         │
│  ├─ Widgets interactivos                │
│  ├─ Renderizado HTML/CSS                │
│  └─ Comunicación WebSocket              │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│      PYTHON BACKEND (app.py)            │
│  ├─ NetworkX (Análisis de grafos)      │
│  ├─ Pandas (Procesamiento de datos)    │
│  ├─ Plotly (Visualización)             │
│  ├─ NumPy/SciPy (Matemática)           │
│  └─ scikit-learn (ML utilities)        │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│      DATOS (CSV en filesystem)          │
│  ├─ electoral_nodos.csv                │
│  └─ electoral_aristas.csv              │
└─────────────────────────────────────────┘
```

---

## Mapa Mental del Proyecto

```
                    PROYECTO
                        │
        ┌───────────────┼───────────────┐
        │               │               │
      DATA          ANÁLISIS        INTERFACE
        │               │               │
        ├─ Nodos        ├─ Grafo        ├─ Streamlit
        ├─ Aristas      ├─ Comunidades  ├─ Plotly
        └─ CSV          ├─ Centralidad  ├─ Widgets
                        ├─ Métricas     └─ Tabs/Expanders
                        └─ Retos

                      RETOS
        ┌───────────────┼───────────────┐
        │               │               │
       RETO 1         RETO 2          RETO 3
      Puentes        Franjas        Parámetros
        │               │               │
        ├─ Betweenness  ├─ Edad        ├─ Config A
        ├─ Ranking      ├─ Estrato     ├─ Config B
        └─ Impacto      ├─ Educación   └─ Comparativa
                        └─ Subgrafos
```

---

## Decisiones de Diseño

```
DECISIÓN 1: Grafo No Dirigido
├─ Motivo: Afinidad es simétrica
├─ Beneficio: Simplifica análisis
└─ Impacto: Válido para votación

DECISIÓN 2: Pesos (% de apoyo)
├─ Motivo: Intensidad de relación
├─ Beneficio: Grafo realista
└─ Impacto: Comunidades más claras

DECISIÓN 3: Louvain + Girvan-Newman
├─ Motivo: Dos perspectivas
├─ Beneficio: Validación cruzada
└─ Impacto: Reto 3 comparación

DECISIÓN 4: Streamlit (tipo de interfaz)
├─ Motivo: Rápido de desarrollar
├─ Beneficio: Interactividad completa
└─ Impacto: No requiere HTML/CSS/JS

DECISIÓN 5: 3 Retos integrados
├─ Motivo: Requiere el proyecto
├─ Beneficio: Análisis profundo
└─ Impacto: Mayor valor educativo
```

---

## Requisitos No Funcionales

```
PERFORMANCE:
└─ Carga inicial: <3 segundos
└─ Cambio de parámetro: <1 segundo
└─ Visualización: 60 FPS

ESCALABILIDAD:
└─ Puede manejar 1000+ nodos
└─ Puede manejar 10,000+ aristas
└─ Memoria: <500MB

USABILIDAD:
└─ Interfaz intuitiva
└─ Documentación completa
└─ Mensajes de error claros
└─ Tooltips informativos

CONFIABILIDAD:
└─ Validación de datos
└─ Manejo de errores
└─ Caché de resultados
└─ Recovery de fallos
```

---

## Versionado

```
app.py v1.0
├─ Algoritmos estables
├─ UI finalizada
├─ Retos implementados
└─ Pronto para producción

analisis_avanzado.py v1.0
├─ Scripts de análisis
├─ Reportes automáticos
└─ Completo

validador_datos.py v1.0
├─ Validación integral
└─ Tests incluidos

Documentación v1.0
├─ 6 archivos Markdown
├─ +5000 palabras
├─ Ejemplos incluidos
└─ Referencias completas
```

---

*Arquitectura diseñada para ser robusta, escalable y educativa.*
