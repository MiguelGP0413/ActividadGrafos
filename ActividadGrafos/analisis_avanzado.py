"""
Script de Análisis Avanzado - Mapa de Afinidades Electorales
Genera reportes detallados, validaciones y visualizaciones adicionales
"""

import pandas as pd
import numpy as np
import networkx as nx
from networkx.algorithms import community
from itertools import combinations
import json
from datetime import datetime

print("\n" + "="*70)
print("ANÁLISIS AVANZADO: Mapa de Afinidades Electorales en Colombia")
print("="*70 + "\n")

# ==================== CARGA DE DATOS ====================
print("[1/8] Cargando datos...")
nodos = pd.read_csv('electoral_nodos.csv')
aristas = pd.read_csv('electoral_aristas.csv')
print(f"  ✓ {len(nodos)} nodos cargados")
print(f"  ✓ {len(aristas)} aristas cargadas\n")

# ==================== EXPLORACIÓN DE DATOS ====================
print("[2/8] Explorando estructura de datos...")

print("\n  Tipos de nodos:")
tipos_nodos = nodos['tipo'].value_counts()
for tipo, count in tipos_nodos.items():
    print(f"    - {tipo}: {count}")

print("\n  Subtipos demográficos:")
subtipo_counts = nodos[nodos['tipo'] == 'franja_demografica']['subtipo'].value_counts()
for subtipo, count in subtipo_counts.items():
    print(f"    - {subtipo}: {count}")

print("\n  Regiones representadas:")
regions = nodos[nodos['tipo'] == 'departamento']['region'].unique()
for region in sorted(regions):
    count = len(nodos[(nodos['tipo'] == 'departamento') & (nodos['region'] == region)])
    print(f"    - {region}: {count} departamentos")

# ==================== CONSTRUCCIÓN DEL GRAFO ====================
print("\n[3/8] Construyendo grafo...")

G = nx.Graph()

# Agregar nodos
for idx, row in nodos.iterrows():
    G.add_node(row['node_id'], 
               nombre=row['nombre'],
               tipo=row['tipo'],
               subtipo=row.get('subtipo', ''),
               region=row.get('region', ''),
               atributo_1=row.get('atributo_1', ''))

# Agregar aristas
for idx, row in aristas.iterrows():
    peso = row['peso']
    G.add_edge(row['origen'], row['destino'], 
               weight=peso,
               votos=row.get('votos_estimados', 0))

print(f"  ✓ Grafo con {G.number_of_nodes()} nodos y {G.number_of_edges()} aristas")
print(f"  ✓ Densidad: {nx.density(G):.4f}")
print(f"  ✓ Componentes conexas: {nx.number_connected_components(G)}")

# ==================== ANÁLISIS DE CENTRALIDAD ====================
print("\n[4/8] Análisis de Centralidad...")

# Betweenness centrality
betweenness = nx.betweenness_centrality(G, weight='weight')
top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]

print("\n  Top 10 nodos por Betweenness Centrality:")
for nodo, valor in top_betweenness:
    print(f"    {G.nodes[nodo]['nombre']:<30} {valor:.4f}")

# Degree centrality
degree_cent = nx.degree_centrality(G)
top_degree = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:10]

print("\n  Top 10 nodos por Grado (Degree Centrality):")
for nodo, valor in top_degree:
    grado = G.degree(nodo)
    print(f"    {G.nodes[nodo]['nombre']:<30} Grado: {grado}")

# Eigenvector centrality
try:
    eigen_cent = nx.eigenvector_centrality(G, max_iter=1000, weight='weight')
    top_eigen = sorted(eigen_cent.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print("\n  Top 10 nodos por Eigenvector Centrality (influencia):")
    for nodo, valor in top_eigen:
        print(f"    {G.nodes[nodo]['nombre']:<30} {valor:.4f}")
except:
    print("\n  ✗ Eigenvector centrality no converge en este grafo")

# ==================== DETECCIÓN DE COMUNIDADES ====================
print("\n[5/8] Detección de Comunidades (Louvain)...")

comunidades_louvain = list(community.greedy_modularity_communities(G))
modularidad_louvain = community.modularity(G, comunidades_louvain)

print(f"  ✓ {len(comunidades_louvain)} comunidades detectadas")
print(f"  ✓ Modularidad: {modularidad_louvain:.4f}")

# Análisis por comunidad
print("\n  Composición de comunidades:")
for i, com in enumerate(comunidades_louvain, 1):
    candidatos = [n for n in com if G.nodes[n]['tipo'] == 'candidato']
    depts = [n for n in com if G.nodes[n]['tipo'] == 'departamento']
    franjas = [n for n in com if G.nodes[n]['tipo'] == 'franja_demografica']
    
    print(f"\n    Comunidad {i} ({len(com)} nodos):")
    
    if candidatos:
        print(f"      Candidatos ({len(candidatos)}):")
        for c in candidatos:
            print(f"        - {G.nodes[c]['nombre']}")
    
    if depts:
        print(f"      Departamentos ({len(depts)}):")
        regions = set([G.nodes[d]['region'] for d in depts if 'region' in G.nodes[d]])
        print(f"        Regiones: {', '.join(regions)}")
    
    if franjas:
        print(f"      Franjas demográficas ({len(franjas)}):")
        for f in franjas:
            print(f"        - {G.nodes[f]['nombre']}")
    
    # Densidad
    subg = G.subgraph(com)
    densidad = nx.density(subg)
    print(f"      Densidad interna: {densidad:.4f}")

# ==================== ANÁLISIS DE PUENTES ====================
print("\n[6/8] Análisis de Puentes (Nodos Críticos)...")

# Mapear nodos a comunidades
nodo_comunidad = {}
for i, com in enumerate(comunidades_louvain):
    for nodo in com:
        nodo_comunidad[nodo] = i

# Identificar puentes
puentes = {}
for nodo in G.nodes():
    if nodo in nodo_comunidad:
        vecinos_comunidades = set()
        for vecino in G.neighbors(nodo):
            if vecino in nodo_comunidad:
                comm_id = nodo_comunidad[vecino]
                vecinos_comunidades.add(comm_id)
        
        if len(vecinos_comunidades) > 1:
            puentes[nodo] = {
                'betweenness': betweenness[nodo],
                'grado': G.degree(nodo),
                'comunidades_conectadas': len(vecinos_comunidades)
            }

if puentes:
    print(f"  ✓ {len(puentes)} nodos puente encontrados\n")
    
    puentes_ranking = sorted(puentes.items(), 
                            key=lambda x: x[1]['betweenness'], 
                            reverse=True)[:15]
    
    print("  Top 15 Puentes:")
    for nodo, metricas in puentes_ranking:
        print(f"    {G.nodes[nodo]['nombre']:<30} | " + 
              f"Betweenness: {metricas['betweenness']:.4f} | " +
              f"Grado: {metricas['grado']} | " +
              f"Comunidades: {metricas['comunidades_conectadas']}")
else:
    print("  ✗ No se encontraron puentes en esta configuración")

# ==================== ANÁLISIS POR FRANJA DEMOGRÁFICA ====================
print("\n[7/8] Análisis de Homogeneidad por Franja Demográfica...")

franjas_tipos = nodos[nodos['tipo'] == 'franja_demografica']['subtipo'].unique()

for franja_tipo in franjas_tipos:
    franjas_del_tipo = nodos[(nodos['tipo'] == 'franja_demografica') & 
                             (nodos['subtipo'] == franja_tipo)]['node_id'].tolist()
    
    comunidades_por_franja = []
    for franja_id in franjas_del_tipo:
        if franja_id in nodo_comunidad:
            comunidades_por_franja.append(nodo_comunidad[franja_id])
    
    # Calcular homogeneidad
    if comunidades_por_franja:
        num_comunidades_unicas = len(set(comunidades_por_franja))
        homogeneidad = (1 - num_comunidades_unicas / len(comunidades_por_franja)) * 100
        
        print(f"\n  {franja_tipo.upper()}:")
        print(f"    - Franjas en esta categoría: {len(franjas_del_tipo)}")
        print(f"    - Comunidades ocupadas: {num_comunidades_unicas}")
        print(f"    - Homogeneidad: {homogeneidad:.1f}%")

# ==================== ESTADÍSTICAS DE DEPARTAMENTOS ====================
print("\n[8/8] Ranking de Departamentos por Conectividad...")

depts = [n for n in G.nodes() if G.nodes[n]['tipo'] == 'departamento']
dept_grados = [(G.nodes[n]['nombre'], G.degree(n), betweenness[n]) for n in depts]
dept_grados_sorted = sorted(dept_grados, key=lambda x: x[1], reverse=True)

print("\n  Top 10 Departamentos más conectados:")
for nombre, grado, central in dept_grados_sorted[:10]:
    print(f"    {nombre:<25} Grado: {grado:2d} | Betweenness: {central:.4f}")

# ==================== RESUMEN FINAL ====================
print("\n" + "="*70)
print("RESUMEN DE HALLAZGOS")
print("="*70)

resumen = f"""
ESTRUCTURA DEL GRAFO:
  • Nodos: {G.number_of_nodes()}
  • Aristas: {G.number_of_edges()}
  • Densidad global: {nx.density(G):.4f}
  • Diámetro: {nx.diameter(G) if nx.is_connected(G) else "N/A (grafo desconexo)"}

COMUNIDADES DETECTADAS (Louvain):
  • Número: {len(comunidades_louvain)}
  • Modularidad: {modularidad_louvain:.4f}
  • Interpretación: {'Comunidades bien definidas' if modularidad_louvain > 0.4 else 'Separación moderada' if modularidad_louvain > 0.3 else 'Comunidades débiles'}

NODOS CRÍTICOS:
  • Puentes identificados: {len(puentes)}
  • Nodo más central: {max(degree_cent.items(), key=lambda x: x[1])[0]} 
    ({G.nodes[max(degree_cent.items(), key=lambda x: x[1])[0]]['nombre']})

REGIONES ELECTORALES:
  • Regiones representadas: {len(regions)}
  • Departamentos más conectados: {dept_grados_sorted[0][0] if dept_grados_sorted else 'N/A'}
  
CONCLUSIONES:
  ✓ Se detectan {len(comunidades_louvain)} grupos naturales de afinidad electoral
  ✓ Modularidad de {modularidad_louvain:.4f} indica estructura {'clara' if modularidad_louvain > 0.4 else 'moderada' if modularidad_louvain > 0.3 else 'compleja'}
  ✓ Existen {len(puentes)} nodos puente que conectan diferentes ecosistemas electorales
  ✓ La homogeneidad varía según criterio demográfico (edad, estrato, educación)
"""

print(resumen)

# ==================== GUARDAR REPORTE ====================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
reporte_path = f"reporte_analisis_{timestamp}.txt"

with open(reporte_path, 'w', encoding='utf-8') as f:
    f.write("="*70 + "\n")
    f.write("REPORTE DE ANÁLISIS - Mapa de Afinidades Electorales\n")
    f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("="*70 + "\n\n")
    
    f.write(resumen)
    
    f.write("\n\nTOP 20 PUENTES:\n")
    f.write("-"*70 + "\n")
    if puentes:
        puentes_ranking = sorted(puentes.items(), 
                                key=lambda x: x[1]['betweenness'], 
                                reverse=True)[:20]
        for nodo, metricas in puentes_ranking:
            f.write(f"{G.nodes[nodo]['nombre']:<30} | " +
                   f"Betweenness: {metricas['betweenness']:.4f}\n")
    else:
        f.write("No se encontraron puentes\n")

print(f"\n✓ Reporte guardado en: {reporte_path}\n")
