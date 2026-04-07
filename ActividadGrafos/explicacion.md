# Explicación Detallada del Código: Mapa de Afinidades Electorales

## Por Qué Estos Algoritmos

### Algoritmos de Detección de Comunidades

#### 1. Algoritmo de Louvain (Greedy Modularity)
**Por qué se usa:**
- Es uno de los algoritmos más eficientes y ampliamente utilizados para detectar comunidades en grafos grandes.
- Optimiza la modularidad, una métrica que mide qué tan bien separadas están las comunidades dentro del grafo.
- Es greedy (voraz), lo que significa que toma decisiones locales óptimas en cada paso, resultando en una buena aproximación global.
- En el contexto electoral: Permite identificar grupos de candidatos, departamentos y franjas demográficas que tienen afinidades similares basadas en patrones de votación.

**Ventajas en este proyecto:**
- Maneja grafos ponderados (las aristas tienen pesos basados en porcentaje de votos).
- Es rápido computacionalmente, ideal para análisis interactivo en Streamlit.
- Produce comunidades cohesivas que reflejan afinidades electorales reales.

#### 2. Algoritmo de Girvan-Newman
**Por qué se usa:**
- Se basa en la eliminación de aristas con alta betweenness centrality (centralidad de intermediación).
- Es útil para identificar comunidades jerárquicas y estructuras modulares.
- En análisis electoral: Ayuda a encontrar divisiones naturales en el espectro político, removiendo conexiones "puente" entre grupos ideológicos.

**Complementariedad con Louvain:**
- Louvain es más eficiente para grafos grandes, pero Girvan-Newman puede revelar estructuras más detalladas.
- Se ofrece como alternativa para comparar resultados y validar la robustez del análisis.

### Algoritmos de Análisis de Grafos

#### Betweenness Centrality (para identificar puentes)
**Por qué se usa:**
- Mide qué tan "importante" es un nodo como puente entre diferentes partes del grafo.
- En el contexto electoral: Identifica candidatos o departamentos que conectan diferentes grupos políticos, actuando como "bisagras" ideológicas.

#### Métricas Globales del Grafo
- **Modularidad:** Mide la calidad de la división en comunidades.
- **Densidad:** Indica qué tan conectados están los nodos.
- **Diámetro:** Mide la distancia máxima entre nodos.
- **Coeficiente de Clustering:** Indica la tendencia a formar triángulos (grupos cerrados).

## Cómo se Utilizaron los Datos de los CSV

### Estructura de los Datos

#### `electoral_nodos.csv`
Contiene información sobre los nodos del grafo:
- **node_id:** Identificador único (ej: CAN_01 para candidatos, DEP_01 para departamentos)
- **nombre:** Nombre descriptivo
- **tipo:** Categoría del nodo (candidato, departamento, franja_demografica)
- **subtipo:** Clasificación más específica (ej: derecha, izquierda, centro para candidatos)
- **atributos:** Información adicional como partido político, votos, PIB per cápita, etc.
- **region:** Región geográfica para departamentos

#### `electoral_aristas.csv`
Define las conexiones entre nodos:
- **origen/destino:** IDs de los nodos conectados
- **peso:** Porcentaje de apoyo/votos (valor numérico entre 0-100)
- **votos_estimados:** Número absoluto de votos
- **afinidad_bloque:** Indicador binario de afinidad ideológica
- **tipo_arista:** Descripción del tipo de relación

### Uso en el Código

1. **Carga de Datos:**
   ```python
   nodos = pd.read_csv('electoral_nodos.csv')
   aristas = pd.read_csv('electoral_aristas.csv')
   ```

2. **Construcción del Grafo:**
   - Nodos se agregan con todos sus atributos como propiedades del nodo en NetworkX
   - Aristas se agregan solo si el peso supera el umbral configurado por el usuario
   - El grafo resultante es no-dirigido y ponderado

3. **Filtrado Interactivo:**
   - El umbral de peso permite al usuario filtrar conexiones débiles
   - Esto crea diferentes "vistas" del grafo según el nivel de afinidad deseado

## Explicación Detallada del Código

### Imports y Configuración Inicial

```python
import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
from networkx.algorithms import community
import plotly.graph_objects as go
import plotly.express as px
from itertools import combinations
# Función para aplicar separación mínima entre nodos
def apply_minimum_separation(pos, min_distance=0.1):
    """Aplica separación mínima entre nodos para evitar superposiciones"""
    nodes = list(pos.keys())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node1, node2 = nodes[i], nodes[j]
            x1, y1 = pos[node1]
            x2, y2 = pos[node2]
            
            # Calcular distancia
            dx = x2 - x1
            dy = y2 - y1
            distance = (dx**2 + dy**2)**0.5
            
            if distance < min_distance and distance > 0:
                # Calcular vector de separación
                separation_x = (dx / distance) * (min_distance - distance) * 0.5
                separation_y = (dy / distance) * (min_distance - distance) * 0.5
                
                # Aplicar separación
                pos[node1] = (x1 - separation_x, y1 - separation_y)
                pos[node2] = (x2 + separation_x, y2 + separation_y)
    
    return pos
```

**Lógica:** Se importan todas las bibliotecas necesarias. NetworkX para teoría de grafos, Plotly para visualizaciones, Streamlit para la interfaz web.

```python
st.set_page_config(page_title="Mapa de Afinidades Electorales", layout="wide")
st.title("🗳️ Mapa de Afinidades Electorales en Colombia")
```

**Lógica:** Configura la página de Streamlit con título descriptivo.

### Carga de Datos

```python
@st.cache_data
def cargar_datos():
    nodos = pd.read_csv('electoral_nodos.csv')
    aristas = pd.read_csv('electoral_aristas.csv')
    return nodos, aristas

nodos, aristas = cargar_datos()
```

**Lógica:** 
- `@st.cache_data` cachea los datos para evitar recargas innecesarias
- Carga los CSV en DataFrames de pandas para procesamiento posterior

### Construcción del Grafo

```python
@st.cache_resource
def construir_grafo(umbral_peso=0):
    G = nx.Graph()
    
    # Agregar nodos con atributos
    for idx, row in nodos.iterrows():
        G.add_node(row['node_id'], 
                  nombre=row['nombre'],
                  tipo=row['tipo'],
                  subtipo=row.get('subtipo', ''),
                  region=row.get('region', ''),
                  atributo_1=row.get('atributo_1', ''),
                  atributo_2_label=row.get('atributo_2_label', ''))
    
    # Agregar aristas ponderadas
    for idx, row in aristas.iterrows():
        peso = row['peso']
        if peso >= umbral_peso:
            G.add_edge(row['origen'], row['destino'], 
                      weight=peso,
                      votos=row.get('votos_estimados', 0),
                      afinidad_bloque=row.get('afinidad_bloque', 0))
    
    return G
```

**Lógica:**
- Crea un grafo vacío usando NetworkX
- Itera sobre el DataFrame de nodos para agregarlos con todos sus atributos
- Itera sobre aristas, pero solo agrega aquellas cuyo peso supera el umbral
- Las aristas incluyen peso (para algoritmos) y metadatos adicionales

### Algoritmos de Detección de Comunidades

#### Louvain
```python
def detectar_comunidades_louvain(G):
    return community.greedy_modularity_communities(G)
```

**Lógica:** Aplica el algoritmo greedy de Louvain que maximiza la modularidad.

#### Girvan-Newman
```python
def detectar_comunidades_girvan_newman(G, num_comunidades=3):
    G_copy = G.copy()
    
    for _ in range(len(list(G_copy.edges())) - num_comunidades):
        betweenness = nx.edge_betweenness_centrality(G_copy)
        edge = max(betweenness, key=betweenness.get)
        G_copy.remove_edge(*edge)
    
    comunidades = list(nx.connected_components(G_copy))
    return [set(c) for c in comunidades]
```

**Lógica:**
- Crea una copia del grafo para no modificar el original
- Calcula repetidamente la betweenness de aristas
- Elimina la arista con mayor betweenness (la más "importante" para conectar comunidades)
- Continúa hasta tener el número deseado de comunidades
- Las componentes conexas resultantes son las comunidades

### Análisis de Puentes

```python
def identificar_puentes(G, comunidades):
    nodo_comunidad = {}
    for i, com in enumerate(comunidades):
        for nodo in com:
            nodo_comunidad[nodo] = i
    
    betweenness = nx.betweenness_centrality(G, weight='weight')
    
    puentes = {}
    for nodo in G.nodes():
        if nodo in nodo_comunidad:
            vecinos_comunidades = set()
            for vecino in G.neighbors(nodo):
                if vecino in nodo_comunidad:
                    vecinos_comunidades.add(nodo_comunidad[vecino])
            
            if len(vecinos_comunidades) > 1:
                puentes[nodo] = {
                    'betweenness': betweenness[nodo],
                    'grado': G.degree(nodo),
                    'comunidades_conectadas': len(vecinos_comunidades)
                }
    
    return puentes
```

**Lógica:**
- Mapea cada nodo a su comunidad
- Calcula betweenness centrality para todos los nodos
- Para cada nodo, identifica las comunidades de sus vecinos
- Si un nodo conecta múltiples comunidades, se considera un "puente"
- Registra métricas de importancia del puente

### Métricas del Grafo

#### Métricas Globales
```python
def calcular_metricas_globales(G, comunidades):
    modularity = community.modularity(G, comunidades)
    densidad = nx.density(G)
    
    if nx.is_connected(G):
        diametro = nx.diameter(G)
    else:
        largest_cc = max(nx.connected_components(G), key=len)
        diametro = nx.diameter(G.subgraph(largest_cc))
    
    coef_clustering = nx.average_clustering(G)
    
    return {
        'modularity': modularity,
        'density': densidad,
        'diameter': diametro,
        'avg_clustering': coef_clustering,
        'num_nodes': G.number_of_nodes(),
        'num_edges': G.number_of_edges(),
        'num_communities': len(comunidades)
    }
```

**Lógica:**
- **Modularidad:** Mide qué tan bien definidas están las comunidades
- **Densidad:** Proporción de aristas existentes vs posibles
- **Diámetro:** Distancia máxima entre nodos (en componente más grande si no conexo)
- **Clustering:** Tendencia promedio a formar triángulos

#### Métricas por Comunidad
```python
def calcular_metricas_comunidad(G, comunidad, nodos_df):
    subgrafo = G.subgraph(comunidad)
    
    integrantes = [(nodo, G.nodes[nodo]['nombre'], G.nodes[nodo]['tipo']) 
                   for nodo in comunidad]
    
    metricas = {
        'size': len(comunidad),
        'density': nx.density(subgrafo),
        'edges': subgrafo.number_of_edges(),
        'avg_degree': sum(dict(subgrafo.degree()).values()) / len(comunidad) if len(comunidad) > 0 else 0,
        'integrantes': integrantes
    }
    
    return metricas
```

**Lógica:** Calcula métricas específicas para cada comunidad individual.

### Interfaz de Usuario (Sidebar)

```python
umbral_peso = st.slider("Umbral de peso (afinidad mínima)", 0.0, 50.0, 10.0, step=1.0)
algoritmo = st.selectbox("Algoritmo de detección", ["Louvain (Greedy)", "Girvan-Newman"])
```

**Lógica:** Permite configuración interactiva de parámetros clave.

### Construcción y Análisis Principal

```python
G = construir_grafo(umbral_peso)

if algoritmo == "Louvain (Greedy)":
    comunidades = list(detectar_comunidades_louvain(G))
else:
    comunidades = detectar_comunidades_girvan_newman(G, num_comunidades_gn)

comunidades = [set(c) if not isinstance(c, set) else c for c in comunidades]
```

**Lógica:** Aplica el algoritmo seleccionado al grafo filtrado.

### Visualización

```python
pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

nodo_comunidad_map = {}
colores_comunidad = px.colors.qualitative.Set3
for i, com in enumerate(comunidades):
    for nodo in com:
        nodo_comunidad_map[nodo] = i
```

**Lógica:**
- `spring_layout` posiciona nodos usando algoritmo de resortes
- Asigna colores únicos a cada comunidad para visualización

```python
fig = go.Figure()

# Agregar aristas
for origen, destino in G.edges():
    x0, y0 = pos[origen]
    x1, y1 = pos[destino]
    fig.add_trace(go.Scatter(
        x=[x0, x1, None], y=[y0, y1, None],
        mode='lines',
        line=dict(width=0.5, color='rgba(200, 200, 200, 0.5)'),
        hoverinfo='none',
        showlegend=False
    ))

# Agregar nodos
for nodo in G.nodes():
    x, y = pos[nodo]
    com_id = nodo_comunidad_map.get(nodo, 0)
    color = colores_comunidad[com_id % len(colores_comunidad)]
    
    tipo = G.nodes[nodo]['tipo']
    nombre = G.nodes[nodo]['nombre']
    
    grado = G.degree(nodo)
    tamaño = 10 + (grado * 2)
    
    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        mode='markers+text',
        text=[nombre[:20]],
        textposition="middle center",
        textfont=dict(size=8),
        marker=dict(size=tamaño, color=color, 
                   line=dict(width=2, color='white'),
                   symbol='circle' if tipo == 'candidato' else 'square' if tipo == 'departamento' else 'diamond'),
        hovertext=f"<b>{nombre}</b><br>Tipo: {tipo}<br>Comunidad: {com_id+1}<br>Grado: {grado}",
        hoverinfo='text',
        showlegend=False
    ))
```

**Lógica:**
- Dibuja aristas como líneas transparentes
- Dibuja nodos como puntos coloreados por comunidad
- Tamaño de nodos proporcional al grado (número de conexiones)
- Tooltips muestran información detallada al pasar el mouse

### Análisis de Comunidades

```python
tabs = st.tabs(["Composición", "Métricas", "Características"])

with tabs[0]:
    for i, comunidad in enumerate(comunidades):
        with st.expander(f"**Comunidad {i+1}** ({len(comunidad)} nodos)", expanded=(i==0)):
            candidatos = [n for n in comunidad if G.nodes[n]['tipo'] == 'candidato']
            departamentos = [n for n in comunidad if G.nodes[n]['tipo'] == 'departamento']
            franjas = [n for n in comunidad if G.nodes[n]['tipo'] == 'franja_demografica']
            
            # Mostrar cada tipo...
```

**Lógica:** Organiza la información de comunidades en pestañas para fácil navegación.

### Respuestas a Preguntas Clave

Esta sección analiza preguntas específicas del dominio electoral:

1. **Departamentos con perfil similar:** Agrupa departamentos por comunidad
2. **Coincidencia con regiones geográficas:** Verifica si comunidades corresponden a regiones
3. **Medios de comunicación:** Nota que no hay datos de medios
4. **Franja más homogénea:** Encuentra la franja presente en menos comunidades
5. **Separación entre grupos:** Evalúa la modularidad

### Retos Innovadores

#### Reto 1: Análisis de Puentes
```python
puentes = identificar_puentes(G, comunidades)
puentes_ranking = sorted(puentes.items(), 
                        key=lambda x: x[1]['betweenness'], 
                        reverse=True)[:10]
```

**Lógica:** Identifica y rankea los nodos más importantes para conectar comunidades.

#### Reto 2: Evolución por Franja Demográfica
```python
franjas_del_tipo = nodos[(nodos['tipo'] == 'franja_demografica') & 
                         (nodos['subtipo'] == franja_seleccionada)]['node_id'].tolist()

franjas_validas = [f for f in franjas_del_tipo if f in G.nodes()]

for franja_id in franjas_validas[:3]:
    vecinos = list(G.neighbors(franja_id))
    subgrafo = G.subgraph(vecinos)
    
    if len(subgrafo) > 1:
        sub_comunidades = list(detectar_comunidades_louvain(subgrafo))
```

**Lógica:** Para cada franja demográfica, analiza el subgrafo de nodos conectados a ella.

#### Reto 3: Comparación de Parámetros
```python
umbral_b = st.slider("Umbral alternativo", 0.0, 50.0, 5.0, key="umbral_b")

G_b = construir_grafo(umbral_b)
comunidades_b = list(detectar_comunidades_louvain(G_b))
metricas_b = calcular_metricas_globales(G_b, comunidades_b)
```

**Lógica:** Construye una segunda configuración con parámetros diferentes y compara métricas.

### Leyenda de Símbolos
- **🔵 Círculos:** Candidatos presidenciales (nodos principales del análisis)
- **🔶 Cuadrados:** Departamentos (unidades territoriales)
- **🔷 Diamantes:** Franjas demográficas (categorías poblacionales)

**Por qué diferentes símbolos:** Facilita la identificación rápida del tipo de nodo sin necesidad de leer etiquetas, especialmente útil en grafos densos donde las etiquetas causarían superposiciones.

### Corrección de Orden de Variables
**Problema resuelto:** `G_filtrado` se estaba usando antes de ser definido, causando `NameError`.

**Solución:** Reordenar el código para definir `G_filtrado` antes de usarlo en los layouts:

```python
# Filtrar nodos por grado mínimo (antes de layouts)
nodos_filtrados = [n for n in G.nodes() if G.degree(n) >= min_degree]
G_filtrado = G.subgraph(nodos_filtrados)

# Ahora usar G_filtrado en los layouts
if layout_type == "Spring (Fuerza)":
    k = k_base * (1 + len(G_filtrado) / 50)
    pos = nx.spring_layout(G_filtrado, k=k, iterations=200, seed=42)
```

### Grosor de Aristas Proporcional al Peso
Las aristas tienen diferentes grosores para representar visualmente la intensidad de las conexiones:

```python
peso = G_filtrado[origen][destino]['weight']
ancho = max(0.5, peso/10)  # Mínimo 0.5, máximo ~9.16
```

**Estadísticas de pesos:**
- **Mínimo:** 0.5% (aristas muy delgadas)
- **Promedio:** 34.8% (aristas medianas)
- **Máximo:** 91.6% (aristas muy gruesas)
- **Fórmula:** ancho = peso ÷ 10 (con mínimo de 0.5)

**Interpretación visual:**
- 🔸 **Aristas delgadas:** Conexiones débiles (bajo porcentaje de votos)
- 🔹 **Aristas gruesas:** Conexiones fuertes (alto porcentaje de votos)

### Grosor de Aristas Proporcional al Peso
Las aristas tienen diferentes grosores para representar visualmente la intensidad de las conexiones:

```python
peso = G_filtrado[origen][destino]['weight']
ancho = max(0.5, peso/10)  # Mínimo 0.5, máximo ~9.16
```

**Estadísticas de pesos:**
- **Mínimo:** 0.5% (aristas muy delgadas)
- **Promedio:** 34.8% (aristas medianas)  
- **Máximo:** 91.6% (aristas muy gruesas)
- **Fórmula:** ancho = peso ÷ 10 (con mínimo de 0.5)

**Interpretación visual:**
- 🔸 **Aristas delgadas:** Conexiones débiles (bajo porcentaje de votos)
- 🔹 **Aristas gruesas:** Conexiones fuertes (alto porcentaje de votos)

Esto permite identificar rápidamente las conexiones más importantes en el grafo electoral.

### Corrección de Error NameError
**Problema identificado:** `NameError: name 'G_filtrado' is not defined`

**Causa:** `G_filtrado` se estaba usando antes de ser definido en el código.

**Solución aplicada:** Reordenar la lógica para definir `G_filtrado` antes de los cálculos de layout.

## Conclusión

Este código implementa un análisis completo de afinidades electorales usando teoría de grafos:

- **Modelado:** Representa candidatos, departamentos y franjas como nodos conectados por afinidad electoral
- **Análisis:** Detecta comunidades usando algoritmos robustos
- **Interactividad:** Permite exploración dinámica de parámetros
- **Interpretación:** Proporciona insights sobre el panorama político colombiano

Los algoritmos elegidos (Louvain, Girvan-Newman, betweenness centrality) son apropiados para el dominio y permiten análisis tanto eficiente como detallado de las estructuras comunitarias en los datos electorales.</content>
<parameter name="filePath">c:\Users\Migue\OneDrive\Desktop\ActividadGrafos\explicacion.md