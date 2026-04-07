import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
from networkx.algorithms import community
import plotly.graph_objects as go
import plotly.express as px
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')

# Función para aplicar separación mínima entre nodos
def apply_minimum_separation(pos, min_distance=0.1, iterations=5):
    """Aplica separación mínima entre nodos para evitar superposiciones"""
    nodes = list(pos.keys())
    for _ in range(iterations):
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                node1, node2 = nodes[i], nodes[j]
                x1, y1 = pos[node1]
                x2, y2 = pos[node2]
                
                dx = x2 - x1
                dy = y2 - y1
                distance = (dx**2 + dy**2)**0.5
                
                if 0 < distance < min_distance:
                    separation_x = (dx / distance) * (min_distance - distance) * 0.5
                    separation_y = (dy / distance) * (min_distance - distance) * 0.5
                    
                    pos[node1] = (x1 - separation_x, y1 - separation_y)
                    pos[node2] = (x2 + separation_x, y2 + separation_y)
    
    return pos

# Configuración de la página
st.set_page_config(page_title="Mapa de Afinidades Electorales", layout="wide")
st.title("🗳️ Mapa de Afinidades Electorales en Colombia")

# ==================== CARGA DE DATOS ====================
@st.cache_data
def cargar_datos():
    nodos = pd.read_csv('electoral_nodos.csv')
    aristas = pd.read_csv('electoral_aristas.csv')
    return nodos, aristas

nodos, aristas = cargar_datos()

# ==================== CONSTRUCCIÓN DEL GRAFO ====================
@st.cache_resource
def construir_grafo(umbral_peso=0):
    """Construye el grafo bipartito: candidatos + departamentos + franjas"""
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

# ==================== ANÁLISIS DE COMUNIDADES ====================
def detectar_comunidades_louvain(G):
    """Detect communities using Louvain algorithm"""
    return community.greedy_modularity_communities(G)

def detectar_comunidades_girvan_newman(G, num_comunidades=3):
    """Detect communities using Girvan-Newman algorithm"""
    # Copia para no modificar el original
    G_copy = G.copy()
    
    for _ in range(len(list(G_copy.edges())) - num_comunidades):
        # Calcular betweenness de todas las aristas
        betweenness = nx.edge_betweenness_centrality(G_copy)
        # Eliminar la arista con mayor betweenness
        edge = max(betweenness, key=betweenness.get)
        G_copy.remove_edge(*edge)
    
    # Obtener componentes conexas como comunidades
    comunidades = list(nx.connected_components(G_copy))
    return [set(c) for c in comunidades]

def detectar_comunidades_louvain_parametrizado(G, resolution=1.0):
    """Variantes de Louvain con diferentes resoluciones"""
    # Union-Find basado en greedy modularity con resolución
    from networkx.algorithms.community import greedy_modularity_communities
    
    # networkx no soporta resolution en greedy, usamos genérico
    communities_list = list(greedy_modularity_communities(G))
    return communities_list

# ==================== ANÁLISIS DE PUENTES ====================
def identificar_puentes(G, comunidades):
    """Identifica nodos puente (con alta centralidad entre comunidades)"""
    # Mapear nodos a comunidades
    nodo_comunidad = {}
    for i, com in enumerate(comunidades):
        for nodo in com:
            nodo_comunidad[nodo] = i
    
    # Calcular betweenness
    betweenness = nx.betweenness_centrality(G, weight='weight')
    
    # Puentes: nodos que conectan diferentes comunidades
    puentes = {}
    for nodo in G.nodes():
        if nodo in nodo_comunidad:
            # Revisar vecinos
            vecinos_comunidades = set()
            for vecino in G.neighbors(nodo):
                if vecino in nodo_comunidad:
                    vecinos_comunidades.add(nodo_comunidad[vecino])
            
            if len(vecinos_comunidades) > 1:  # Conecta múltiples comunidades
                puentes[nodo] = {
                    'betweenness': betweenness[nodo],
                    'grado': G.degree(nodo),
                    'comunidades_conectadas': len(vecinos_comunidades)
                }
    
    return puentes

# ==================== MÉTRICAS DEL GRAFO ====================
def calcular_metricas_globales(G, comunidades):
    """Calcula métricas de calidad de la partición"""
    # Modularidad
    if isinstance(comunidades[0], set):
        comunidades = [set(c) for c in comunidades]
    
    modularity = community.modularity(G, comunidades)
    
    # Densidad
    densidad = nx.density(G)
    
    # Diámetro (si es conexo)
    if nx.is_connected(G):
        diametro = nx.diameter(G)
    else:
        # Para grafos desconexos, diámetro de la componente más grande
        largest_cc = max(nx.connected_components(G), key=len)
        diametro = nx.diameter(G.subgraph(largest_cc))
    
    # Coeficiente de clustering
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

def calcular_metricas_comunidad(G, comunidad, nodos_df):
    """Calcula métricas para una comunidad específica"""
    subgrafo = G.subgraph(comunidad)
    
    # Obtener información de integrantes
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

# ==================== SIDEBAR: CONFIGURACIÓN ====================
st.sidebar.markdown("## ⚙️ Configuración")

# Información sobre la construcción del grafo
st.sidebar.markdown("### 📊 Construcción del Grafo")
st.sidebar.info("""
**Nodos:** Candidatos, Departamentos, Franjas demográficas
**Aristas:** Relaciones de voto ponderadas por % de apoyo
**Tipo:** Grafo no dirigido, ponderado
**Justificación:** Las aristas representan afinidad electoral - el peso indica la intensidad del apoyo
""")

# Parámetros interactivos
col1, col2 = st.sidebar.columns(2)

with col1:
    umbral_peso = st.slider("Umbral de peso (afinidad mínima)", 0.0, 50.0, 10.0, step=1.0)

with col2:
    algoritmo = st.selectbox("Algoritmo de detección", 
                            ["Louvain (Greedy)", "Girvan-Newman"])

# Parámetro para Girvan-Newman
if algoritmo == "Girvan-Newman":
    num_comunidades_gn = st.slider("Número de comunidades", 2, 8, 3)
else:
    num_comunidades_gn = 3

# Análisis de retos
st.sidebar.markdown("### 🎯 Retos Innovadores")
mostrar_puentes = st.sidebar.checkbox("Reto 1: Análisis de Puentes", value=True)
mostrar_franjas = st.sidebar.checkbox("Reto 2: Evolución por Franja", value=True)
mostrar_comparacion = st.sidebar.checkbox("Reto 3: Comparación de Parámetros", value=True)

# ==================== CONSTRUCCIÓN DEL GRAFO ====================
G = construir_grafo(umbral_peso)

# Detectar comunidades
if algoritmo == "Louvain (Greedy)":
    comunidades = list(detectar_comunidades_louvain(G))
else:
    comunidades = detectar_comunidades_girvan_newman(G, num_comunidades_gn)

# Convertir a formato consistente
comunidades = [set(c) if not isinstance(c, set) else c for c in comunidades]

# ==================== MAIN PANEL ====================
st.markdown("---")

# SECCIÓN 1: INFORMACIÓN DEL GRAFO
col1, col2, col3, col4 = st.columns(4)
metricas_globales = calcular_metricas_globales(G, comunidades)

with col1:
    st.metric("Nodos totales", metricas_globales['num_nodes'])
with col2:
    st.metric("Aristas totales", metricas_globales['num_edges'])
with col3:
    st.metric("Comunidades", metricas_globales['num_communities'])
with col4:
    st.metric("Modularidad", f"{metricas_globales['modularity']:.3f}")

st.markdown("---")

# SECCIÓN 2: VISUALIZACIÓN DEL GRAFO
st.markdown("## 📈 Visualización de la Red")

# Opciones de visualización
col_layout1, col_layout2, col_layout3, col_layout4 = st.columns(4)
with col_layout1:
    layout_type = st.selectbox("Tipo de layout", 
                              ["Spring (Fuerza)", "Kamada-Kawai", "Circular", "Random", "Shell"],
                              index=0)
with col_layout2:
    show_labels = st.checkbox("Mostrar etiquetas", value=False)
with col_layout3:
    min_degree = st.slider("Grado mínimo para mostrar", 0, 20, 0)
with col_layout4:
    avoid_overlaps = st.checkbox("Evitar superposiciones", value=True)

# Filtrar nodos por grado mínimo
nodos_filtrados = [n for n in G.nodes() if G.degree(n) >= min_degree]
G_filtrado = G.subgraph(nodos_filtrados)

# Preparar datos para visualización
if layout_type == "Spring (Fuerza)":
    k_base = 4 if avoid_overlaps else 3
    k = k_base * (1 + len(G_filtrado) / 40)
    pos = nx.spring_layout(G_filtrado, k=k, iterations=250, seed=42, weight='weight')
elif layout_type == "Kamada-Kawai":
    pos = nx.kamada_kawai_layout(G_filtrado, weight='weight')
elif layout_type == "Circular":
    pos = nx.circular_layout(G_filtrado)
elif layout_type == "Random":
    pos = nx.random_layout(G_filtrado, seed=42)
else:  # Shell
    pos = nx.shell_layout(G_filtrado)

# Aplicar separación adicional si está activado
if avoid_overlaps and layout_type in ["Spring (Fuerza)", "Kamada-Kawai"]:
    min_dist = 0.18 if len(G_filtrado) < 40 else 0.22
    pos = apply_minimum_separation(pos, min_distance=min_dist, iterations=8)

# Asignar comunidades a nodos
nodo_comunidad_map = {}
colores_comunidad = px.colors.qualitative.Set3 + px.colors.qualitative.Dark24  # Más colores
for i, com in enumerate(comunidades):
    for nodo in com:
        if nodo in nodos_filtrados:  # Solo nodos filtrados
            nodo_comunidad_map[nodo] = i

# Crear figura Plotly
fig = go.Figure()

# Agregar aristas (solo para nodos filtrados)
for origen, destino in G_filtrado.edges():
    if origen in pos and destino in pos:  # Verificar que existan posiciones
        x0, y0 = pos[origen]
        x1, y1 = pos[destino]
        peso = G_filtrado[origen][destino]['weight']
        fig.add_trace(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            mode='lines',
            line=dict(width=max(0.5, peso/10), color='rgba(200, 200, 200, 0.6)'),
            hoverinfo='none',
            showlegend=False
        ))

# Agregar nodos
for nodo in G_filtrado.nodes():
    if nodo in pos:  # Verificar posición
        x, y = pos[nodo]
        com_id = nodo_comunidad_map.get(nodo, 0)
        color = colores_comunidad[com_id % len(colores_comunidad)]
        
        tipo = G_filtrado.nodes[nodo]['tipo']
        nombre = G_filtrado.nodes[nodo]['nombre']
        
        # Tamaño mejorado según tipo y grado
        grado = G_filtrado.degree(nodo)
        base_size = 15 if tipo == 'candidato' else 12 if tipo == 'departamento' else 10
        tamaño = base_size + (grado * 1.5)
        
        # Modo según opción de etiquetas
        mode = 'markers+text' if show_labels else 'markers'
        text = [nombre[:15]] if show_labels else ['']
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode=mode,
            text=text,
            textposition="top center",
            textfont=dict(size=7, color='black'),
            marker=dict(size=tamaño, color=color, 
                       line=dict(width=2, color='white'),
                       symbol='circle' if tipo == 'candidato' else 'square' if tipo == 'departamento' else 'diamond'),
            hovertext=f"<b>{nombre}</b><br>Tipo: {tipo}<br>Comunidad: {com_id+1}<br>Grado: {grado}",
            hoverinfo='text',
            showlegend=False,
            name=f'Comunidad {com_id+1}'
        ))

# Mejorar layout de la figura
fig.update_layout(
    title="Red de Afinidades Electorales",
    showlegend=False,
    hovermode='closest',
    height=800 if avoid_overlaps else 700,  # Más altura si evitamos overlaps
    width=1000 if avoid_overlaps else None,  # Más ancho si evitamos overlaps
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, autorange=True),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, autorange=True),
    plot_bgcolor='rgba(0,0,0,0)',  # Fondo transparente para coincidir con Streamlit
    paper_bgcolor='rgba(0,0,0,0)'  # Fondo del papel también transparente
)

st.plotly_chart(fig, use_container_width=True)

# Leyenda de símbolos
st.markdown("### 📋 Leyenda de Símbolos")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🔵 **Círculos:** Candidatos presidenciales")
with col2:
    st.markdown("🔶 **Cuadrados:** Departamentos")
with col3:
    st.markdown("🔷 **Diamantes:** Franjas demográficas")

# Leyenda de aristas
st.markdown("### 🔗 Leyenda de Aristas")
st.markdown("""
- **Delgadas (0.5px):** Conexiones débiles (< 5% afinidad)
- **Medianas (3-5px):** Conexiones moderadas (30-50% afinidad)  
- **Gruesas (5-9px):** Conexiones fuertes (> 50% afinidad)
""")

# Información sobre la visualización
st.info("""
💡 **Consejos para mejor visualización:**
- **Spring Layout:** Mejor para ver clusters naturales, pero puede ser caótico
- **Circular:** Organiza nodos en círculos concéntricos
- **Etiquetas:** Actívalas solo para grafos pequeños para evitar desorden
- **Grado mínimo:** Filtra nodos poco conectados para simplificar
- **Evitar superposiciones:** Aumenta el espacio entre nodos para mejor claridad
- **Grosor de aristas:** Representa la intensidad de afinidad (más grueso = más fuerte)
""")

st.markdown("---")

# SECCIÓN 3: ANÁLISIS DE COMUNIDADES
st.markdown("## 🔍 Análisis de Comunidades")

tabs = st.tabs(["Composición", "Métricas", "Características"])

with tabs[0]:
    st.markdown("### Integrantes por Comunidad")
    for i, comunidad in enumerate(comunidades):
        with st.expander(f"**Comunidad {i+1}** ({len(comunidad)} nodos)", expanded=(i==0)):
            # Clasificar por tipo
            candidatos = [n for n in comunidad if G.nodes[n]['tipo'] == 'candidato']
            departamentos = [n for n in comunidad if G.nodes[n]['tipo'] == 'departamento']
            franjas = [n for n in comunidad if G.nodes[n]['tipo'] == 'franja_demografica']
            
            if candidatos:
                st.markdown("**Candidatos:**")
                for nodo in candidatos:
                    st.write(f"  - {G.nodes[nodo]['nombre']}")
            
            if departamentos:
                st.markdown("**Departamentos:**")
                cols = st.columns(3)
                for j, nodo in enumerate(departamentos):
                    cols[j % 3].write(f"  - {G.nodes[nodo]['nombre']}")
            
            if franjas:
                st.markdown("**Franjas demográficas:**")
                for nodo in franjas:
                    st.write(f"  - {G.nodes[nodo]['nombre']}")

with tabs[1]:
    st.markdown("### Métricas de Comunidades")
    metricas_df = []
    for i, comunidad in enumerate(comunidades):
        metricas = calcular_metricas_comunidad(G, comunidad, nodos)
        metricas_df.append({
            'Comunidad': f'Com {i+1}',
            'Tamaño': metricas['size'],
            'Aristas internas': metricas['edges'],
            'Densidad': f"{metricas['density']:.3f}",
            'Grado promedio': f"{metricas['avg_degree']:.2f}"
        })
    
    df_metricas = pd.DataFrame(metricas_df)
    st.dataframe(df_metricas, use_container_width=True)

with tabs[2]:
    st.markdown("### Resumen de Características")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Densidad (conexión interna):**")
        densidades = [nx.density(G.subgraph(c)) for c in comunidades]
        fig_dens = px.bar(x=range(len(densidades)), y=densidades, 
                         labels={'x': 'Comunidad', 'y': 'Densidad'},
                         title="Densidad interna por comunidad")
        st.plotly_chart(fig_dens, use_container_width=True)
    
    with col2:
        st.markdown("**Tamaño de comunidades:**")
        tamaños = [len(c) for c in comunidades]
        fig_tamaños = px.pie(values=tamaños, names=[f'Com {i+1}' for i in range(len(tamaños))],
                             title="Distribución de nodos")
        st.plotly_chart(fig_tamaños, use_container_width=True)

st.markdown("---")

# SECCIÓN 4: RESPUESTAS A PREGUNTAS CLAVE
st.markdown("## 📋 Respuestas a Preguntas Clave")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ❓ ¿Qué departamentos tienen perfil similar?")
    
    # Departamentos por comunidad
    for i, comunidad in enumerate(comunidades):
        depts = [n for n in comunidad if G.nodes[n]['tipo'] == 'departamento']
        if depts:
            st.info(f"""
            **Comunidad {i+1}:**
            {', '.join([G.nodes[d]['nombre'] for d in depts])}
            """)

with col2:
    st.markdown("### ❓ ¿Coinciden con regiones geográficas?")
    
    # Analizar regiones
    for i, comunidad in enumerate(comunidades):
        depts = [n for n in comunidad if G.nodes[n]['tipo'] == 'departamento']
        if depts:
            regiones = set([G.nodes[d]['region'] for d in depts if 'region' in G.nodes[d]])
            if regiones:
                st.info(f"**Comunidad {i+1}:** Regiones: {', '.join(regiones)}")

# Pregunta 3: Medios y candidatos
st.markdown("### ❓ ¿Qué medios de comunicación comparten ecosistema?")
st.info("*Nota: El dataset no contiene nodos de medios, pero el análisis muestra afiliaciones ideológicas en las comunidades*")

# Pregunta 4: Franja más homogénea
st.markdown("### ❓ ¿Qué franja demográfica es más homogénea?")

franjas_en_comunidades = {}
for i, comunidad in enumerate(comunidades):
    franjas = [n for n in comunidad if G.nodes[n]['tipo'] == 'franja_demografica']
    for f in franjas:
        if G.nodes[f]['nombre'] not in franjas_en_comunidades:
            franjas_en_comunidades[G.nodes[f]['nombre']] = []
        franjas_en_comunidades[G.nodes[f]['nombre']].append(i)

if franjas_en_comunidades:
    homogeneidad = {franja: len(set(coms)) for franja, coms in franjas_en_comunidades.items()}
    franja_mas_homogenea = min(homogeneidad.keys(), key=lambda x: homogeneidad[x])
    
    st.success(f"**Franja más homogénea:** {franja_mas_homogenea} (presente en {homogeneidad[franja_mas_homogenea]} comunidad/s)")
    
    df_homogeneidad = pd.DataFrame({
        'Franja demográfica': list(homogeneidad.keys()),
        'Número de comunidades': list(homogeneidad.values())
    }).sort_values('Número de comunidades')
    
    st.dataframe(df_homogeneidad, use_container_width=True)

# Pregunta 5: Separación entre grupos
st.markdown("### ❓ ¿Qué tan pronunciada es la separación entre grupos?")

col1, col2 = st.columns(2)

with col1:
    st.metric("Modularidad", f"{metricas_globales['modularity']:.4f}", 
              "↑ Mejor separación")

with col2:
    if metricas_globales['modularity'] >= 0.4:
        st.success("✅ Separación muy pronunciada (modularidad > 0.4)")
    elif metricas_globales['modularity'] >= 0.3:
        st.info("⚠️ Separación moderada (modularidad 0.3-0.4)")
    else:
        st.warning("⚠️ Separación débil (modularidad < 0.3)")

st.markdown("---")

# SECCIÓN 5: RETO 1 - ANÁLISIS DE PUENTES
if mostrar_puentes:
    st.markdown("## 🌉 RETO 1: Análisis de Puentes")
    st.markdown("*Identifica nodos que conectan grupos distintos — candidatos o departamentos que actúan como bisagras*")
    
    puentes = identificar_puentes(G, comunidades)
    
    if puentes:
        # Ranking de puentes
        puentes_ranking = sorted(puentes.items(), 
                                key=lambda x: x[1]['betweenness'], 
                                reverse=True)[:10]
        
        st.markdown("### Top 10 Nodos Puente")
        puentes_data = []
        for nodo, metricas in puentes_ranking:
            puentes_data.append({
                'Nodo': G.nodes[nodo]['nombre'],
                'Tipo': G.nodes[nodo]['tipo'],
                'Betweenness': f"{metricas['betweenness']:.4f}",
                'Grado': metricas['grado'],
                'Comunidades conectadas': metricas['comunidades_conectadas']
            })
        
        df_puentes = pd.DataFrame(puentes_data)
        st.dataframe(df_puentes, use_container_width=True)
        
        # Análisis de impacto
        st.markdown("### 🔴 Análisis de Impacto: ¿Qué pasaría si se eliminaran?")
        
        for nodo, metricas in puentes_ranking[:3]:
            with st.expander(f"{G.nodes[nodo]['nombre']} (Betweenness: {metricas['betweenness']:.4f})"):
                G_temp = G.copy()
                G_temp.remove_node(nodo)
                
                # Calcular cambio en componentes conexas
                componentes_antes = nx.number_connected_components(G)
                componentes_despues = nx.number_connected_components(G_temp)
                
                st.warning(f"""
                **Impacto global:**
                - Componentes conexas: {componentes_antes} → {componentes_despues}
                - Cambio: {componentes_despues - componentes_antes:+d}
                
                **Interpretación:** 
                Este nodo es {'CRÍTICO' if componentes_despues > componentes_antes else 'importante'} 
                para la cohesión de la red.
                """)
    else:
        st.info("No se encontraron puentes significativos en esta configuración.")

st.markdown("---")

# SECCIÓN 6: RETO 2 - EVOLUCIÓN POR FRANJA DEMOGRÁFICA
if mostrar_franjas:
    st.markdown("## 📊 RETO 2: Evolución por Franja Demográfica")
    st.markdown("*¿Cambian los grupos de afinidad según el criterio demográfico considerado?*")
    
    # Filtrar franjas por tipo
    franjas_tipos = nodos[nodos['tipo'] == 'franja_demografica']['subtipo'].unique()
    
    franja_seleccionada = st.selectbox("Selecciona criterio demográfico:", franjas_tipos)
    
    # Crear subgrafos por franja
    franjas_del_tipo = nodos[(nodos['tipo'] == 'franja_demografica') & 
                             (nodos['subtipo'] == franja_seleccionada)]['node_id'].tolist()
    
    # Nodos validados
    franjas_validas = [f for f in franjas_del_tipo if f in G.nodes()]
    
    if franjas_validas:
        col1, col2, col3 = st.columns(3)
        
        for idx, franja_id in enumerate(franjas_validas[:3]):
            col = [col1, col2, col3][idx]
            
            with col:
                franja_nombre = G.nodes[franja_id]['nombre']
                
                # Vecinos de esta franja
                vecinos = list(G.neighbors(franja_id))
                subgrafo = G.subgraph(vecinos)
                
                if len(vecinos) > 0:
                    # Detectar comunidades en el subgrafo
                    if len(subgrafo) > 1:
                        sub_comunidades = list(detectar_comunidades_louvain(subgrafo))
                    else:
                        sub_comunidades = [[vecinos[0]]] if vecinos else []
                    
                    st.markdown(f"### {franja_nombre}")
                    st.metric("Nodos conectados", len(vecinos))
                    st.metric("Comunidades", len(sub_comunidades))
                    
                    # Listado
                    if sub_comunidades:
                        for com_idx, com in enumerate(sub_comunidades[:2]):
                            nombres = [G.nodes[n]['nombre'] for n in com if n in G.nodes()]
                            if nombres:
                                st.write(f"**Grupo {com_idx+1}:** {', '.join(nombres[:3])}")
    else:
        st.info("No hay franjas de este tipo conectadas en el grafo actual.")

st.markdown("---")

# SECCIÓN 7: RETO 3 - COMPARACIÓN DE PARÁMETROS
if mostrar_comparacion:
    st.markdown("## ⚖️ RETO 3: Comparación de Parámetros")
    st.markdown("*Compara dos configuraciones del mismo análisis lado a lado*")
    
    st.info("Configuración A: Parámetros actuales (arriba)")
    
    # Configuración B: con umbral diferente
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Configuración A (Actual)")
        st.metric("Umbral peso", umbral_peso)
        st.metric("Algoritmo", algoritmo)
        st.metric("Comunidades", metricas_globales['num_communities'])
        st.metric("Modularidad", f"{metricas_globales['modularity']:.3f}")
    
    with col2:
        st.markdown("### Configuración B (Alternativa)")
        
        # Cambio en parámetros para B
        umbral_b = st.slider("Umbral alternativo", 0.0, 50.0, 5.0, key="umbral_b")
        
        # Construir grafo alternativo
        G_b = construir_grafo(umbral_b)
        comunidades_b = list(detectar_comunidades_louvain(G_b))
        comunidades_b = [set(c) if not isinstance(c, set) else c for c in comunidades_b]
        metricas_b = calcular_metricas_globales(G_b, comunidades_b)
        
        st.metric("Umbral peso", umbral_b)
        st.metric("Algoritmo", "Louvain (Greedy)")
        st.metric("Comunidades", metricas_b['num_communities'])
        st.metric("Modularidad", f"{metricas_b['modularity']:.3f}")
    
    st.markdown("---")
    
    # Comparativa visual
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Cambios detectados:**")
        
        cambio_comunidades = metricas_b['num_communities'] - metricas_globales['num_communities']
        cambio_modularidad = metricas_b['modularity'] - metricas_globales['modularity']
        
        if cambio_comunidades != 0:
            st.write(f"💠 Comunidades: {cambio_comunidades:+d}")
        if cambio_modularidad != 0:
            st.write(f"📈 Modularidad: {cambio_modularidad:+.3f}")
    
    with col2:
        st.markdown("**Recomendación:**")
        if abs(cambio_modularidad) > 0.05:
            st.success("Diferencia significativa - ambas configuraciones son válidas")
        else:
            st.info("Configuraciones similares - parámetros robustos")
    
    # Permitir selección
    mejor = st.radio("¿Cuál configuración consideras más válida?", 
                     ["Configuración A (Actual)", "Configuración B (Alternativa)"])
    
    if mejor == "Configuración B (Alternativa)":
        st.warning("✅ Seleccionaste Config B. En producción, se usaría umbral=" + str(int(umbral_b)))

st.markdown("---")

# SECCIÓN 8: RESUMEN EJECUTIVO
st.markdown("## 📊 Resumen Ejecutivo")

resumen_col1, resumen_col2 = st.columns(2)

with resumen_col1:
    st.markdown("### Hallazgos Principales")
    st.markdown(f"""
    1. **Red:** {metricas_globales['num_nodes']} nodos, {metricas_globales['num_edges']} aristas
    2. **Fragmentación:** {metricas_globales['num_communities']} grupos naturales detectados
    3. **Cohesión:** Modularidad = {metricas_globales['modularity']:.3f}
    4. **Densidad:** {metricas_globales['density']:.3f} (conexión global)
    5. **Complejidad:** Diámetro = {metricas_globales['diameter']}
    """)

with resumen_col2:
    st.markdown("### Interpretación")
    if metricas_globales['modularity'] > 0.5:
        st.success("✅ **Comunidades muy bien definidas** - hay grupos claros de afinidad")
    elif metricas_globales['modularity'] > 0.3:
        st.info("⚠️ **Comunidades moderadamente definidas** - algunos solapamientos")
    else:
        st.warning("⚠️ **Comunidades débiles** - red muy interconectada")

st.markdown("---")
st.markdown("*Aplicación desarrollada para análisis de afinidades electorales en Colombia.*")
