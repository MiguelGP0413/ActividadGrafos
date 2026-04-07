"""
Validador de Integridad de Datos
Verifica que los archivos CSV estén correctos antes de ejecutar la aplicación
"""

import pandas as pd
import sys
import os

def validar_integridad():
    print("\n" + "="*70)
    print("VALIDADOR DE INTEGRIDAD - Mapa de Afinidades Electorales")
    print("="*70 + "\n")
    
    errores = []
    advertencias = []
    
    # ==================== VALIDAR EXISTENCIA ====================
    print("[1/6] Verificando existencia de archivos...")
    
    if not os.path.exists('electoral_nodos.csv'):
        errores.append("❌ electoral_nodos.csv no encontrado")
    else:
        print("  ✓ electoral_nodos.csv encontrado")
    
    if not os.path.exists('electoral_aristas.csv'):
        errores.append("❌ electoral_aristas.csv no encontrado")
    else:
        print("  ✓ electoral_aristas.csv encontrado")
    
    if errores:
        print("\n⛔ ERRORES CRÍTICOS - No se puede continuar")
        for error in errores:
            print(f"  {error}")
        return False
    
    # ==================== CARGAR DATOS ====================
    print("\n[2/6] Cargando datos...")
    
    try:
        nodos = pd.read_csv('electoral_nodos.csv')
        print(f"  ✓ Nodos cargados: {len(nodos)} filas")
    except Exception as e:
        errores.append(f"❌ Error al cargar electoral_nodos.csv: {e}")
    
    try:
        aristas = pd.read_csv('electoral_aristas.csv')
        print(f"  ✓ Aristas cargadas: {len(aristas)} filas")
    except Exception as e:
        errores.append(f"❌ Error al cargar electoral_aristas.csv: {e}")
    
    if errores:
        print("\n⛔ ERRORES CRÍTICOS")
        for error in errores:
            print(f"  {error}")
        return False
    
    # ==================== VALIDAR ESTRUCTURA ====================
    print("\n[3/6] Validando estructura...")
    
    # Columnas esperadas en nodos
    cols_nodos_requeridas = ['node_id', 'nombre', 'tipo']
    for col in cols_nodos_requeridas:
        if col not in nodos.columns:
            errores.append(f"❌ Columna faltante en nodos: {col}")
        else:
            print(f"  ✓ Nodos tiene columna: {col}")
    
    # Columnas esperadas en aristas
    cols_aristas_requeridas = ['origen', 'destino', 'peso']
    for col in cols_aristas_requeridas:
        if col not in aristas.columns:
            errores.append(f"❌ Columna faltante en aristas: {col}")
        else:
            print(f"  ✓ Aristas tiene columna: {col}")
    
    if errores:
        print("\n⛔ ERRORES EN ESTRUCTURA")
        for error in errores:
            print(f"  {error}")
        return False
    
    # ==================== VALIDAR CONTENIDO ====================
    print("\n[4/6] Validando contenido...")
    
    # Verificar IDs únicos
    if nodos['node_id'].nunique() != len(nodos):
        advertencias.append("⚠️ Hay node_id duplicados")
    else:
        print("  ✓ Todos los node_id son únicos")
    
    # Verificar tipos válidos
    tipos_validos = nodos['tipo'].unique()
    print(f"  ✓ Tipos de nodos encontrados: {', '.join(tipos_validos)}")
    
    # Verificar aristas referencias
    nodos_set = set(nodos['node_id'])
    aristas_invalidas = 0
    
    for idx, row in aristas.iterrows():
        if row['origen'] not in nodos_set:
            aristas_invalidas += 1
        if row['destino'] not in nodos_set:
            aristas_invalidas += 1
    
    if aristas_invalidas > 0:
        advertencias.append(f"⚠️ {aristas_invalidas} references a nodos no existentes")
    else:
        print("  ✓ Todas las aristas referencian nodos válidos")
    
    # Verificar rangos de peso
    peso_min = aristas['peso'].min()
    peso_max = aristas['peso'].max()
    
    if peso_min < 0 or peso_max > 100:
        advertencias.append(f"⚠️ Pesos fuera del rango [0, 100]: min={peso_min}, max={peso_max}")
    else:
        print(f"  ✓ Pesos en rango válido: [{peso_min:.1f}, {peso_max:.1f}]")
    
    # ==================== ESTADÍSTICAS ====================
    print("\n[5/6] Estadísticas de datos...")
    
    print(f"\n  Nodos por tipo:")
    print(nodos['tipo'].value_counts().to_string().replace('\n', '\n    '))
    
    print(f"\n  Franjas demográficas por subtipo:")
    franjas = nodos[nodos['tipo'] == 'franja_demografica']
    if len(franjas) > 0:
        print(franjas['subtipo'].value_counts().to_string().replace('\n', '\n    '))
    
    print(f"\n  Distribución de pesos (aristas):")
    print(f"    Media: {aristas['peso'].mean():.2f}%")
    print(f"    Mediana: {aristas['peso'].median():.2f}%")
    print(f"    Desv. Est: {aristas['peso'].std():.2f}%")
    
    # ==================== VERIFICACIÓN DE GRAFO ====================
    print("\n[6/6] Verificación de grafo...")
    
    try:
        import networkx as nx
        
        G = nx.Graph()
        
        # Agregar nodos
        for idx, row in nodos.iterrows():
            G.add_node(row['node_id'])
        
        # Agregar aristas
        for idx, row in aristas.iterrows():
            if row['origen'] in G and row['destino'] in G:
                G.add_edge(row['origen'], row['destino'], weight=row['peso'])
        
        print(f"  ✓ Grafo construido: {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas")
        print(f"  ✓ Componentes conexas: {nx.number_connected_components(G)}")
        print(f"  ✓ Densidad: {nx.density(G):.4f}")
        
        if nx.is_connected(G):
            print(f"  ✓ Diámetro: {nx.diameter(G)}")
        else:
            largest_cc = max(nx.connected_components(G), key=len)
            print(f"  ⚠️ Grafo no conexo. Componente más grande: {len(largest_cc)} nodos")
        
    except ImportError:
        advertencias.append("⚠️ NetworkX no instalado - no se puede validar grafo")
    except Exception as e:
        advertencias.append(f"⚠️ Error al construir grafo: {e}")
    
    # ==================== RESUMEN ====================
    print("\n" + "="*70)
    print("RESUMEN DE VALIDACIÓN")
    print("="*70)
    
    if errores:
        print(f"\n❌ ERRORES ({len(errores)}):")
        for error in errores:
            print(f"  {error}")
    
    if advertencias:
        print(f"\n⚠️ ADVERTENCIAS ({len(advertencias)}):")
        for adv in advertencias:
            print(f"  {adv}")
    
    if not errores:
        print(f"\n✅ VALIDACIÓN EXITOSA")
        print(f"Puedes ejecutar: streamlit run app.py")
        return True
    else:
        print(f"\n❌ VALIDACIÓN FALLIDA")
        print(f"Verifica los errores antes de ejecutar la aplicación")
        return False

if __name__ == "__main__":
    success = validar_integridad()
    print("\n")
    sys.exit(0 if success else 1)
