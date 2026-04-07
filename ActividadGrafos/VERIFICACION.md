# ✅ CHECKLIST DE VERIFICACIÓN Y PRUEBA

## 🔍 VERIFICACIÓN PREVIA

Antes de usar la aplicación, verifica que tienes todo:

```
ARCHIVOS REQUERIDOS:
  ☐ electoral_nodos.csv
  ☐ electoral_aristas.csv
  ☐ app.py
  ☐ requirements.txt

ARCHIVOS OPCIONALES (Análisis avanzado):
  ☐ analisis_avanzado.py
  ☐ validador_datos.py

DOCUMENTACIÓN:
  ☐ README.md
  ☐ QUICKSTART.md
  ☐ RETOS_ESPECIFICACION.md
  ☐ RESUMEN_EJECUTIVO.md
  ☐ INDICE.md (archivo de navegación)

SCRIPTS DE EJECUCIÓN (Windows):
  ☐ instalar.bat
  ☐ ejecutar.bat
```

---

## ⚙️ INSTALACIÓN VERIFICADA

### Paso 1: Verificar Python
```bash
python --version
# Debe mostrar: Python 3.8 o superior
```

**Resultado esperado:**
```
Python 3.10.x (o mayor)
```

**Si falla:**
- [Instala Python](https://www.python.org/downloads/)
- Asegúrate de marcar "Add Python to PATH"

---

### Paso 2: Instalar Dependencias
```bash
pip install -r requirements.txt
```

**Salida esperada:**
```
Successfully installed streamlit-1.36.0 pandas-2.0.3 ...
```

**Si hay error:**
- Intenta: `python -m pip install --upgrade pip`
- Luego: `pip install -r requirements.txt`

---

### Paso 3: Ejecutar Aplicación
```bash
streamlit run app.py
```

**Salida esperada:**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://XXX.XXX.X.XXX:8501
```

**Si hay error:**
- Verifica pip instaló streamlit: `pip show streamlit`
- Si no aparece: `pip install streamlit==1.36.0`

---

## 🧪 PRUEBAS FUNCIONALES

### TEST 1: Carga de Datos
**Acción:** Abre http://localhost:8501

**Esperado:**
- ✅ Página carga en <3 segundos
- ✅ Aparece título "🗳️ Mapa de Afinidades Electorales"
- ✅ Se muestra sidebar izquierdo
- ✅ Métricas en la parte superior: "Nodos totales", "Aristas", etc.

**Resultado:**
```
Nodos totales: 66
Aristas totales: 1000+
Comunidades: 3-5
Modularidad: 0.3XX
```

---

### TEST 2: Visualización del Grafo
**Acción:** Baja en la página hasta "Visualización de la Red"

**Esperado:**
- ✅ Se ve un grafo interactivo con nodos y aristas
- ✅ Nodos en diferentes colores (comunidades)
- ✅ Puedes hacer zoom y pan
- ✅ Hover muestra información: nombre, tipo, comunidad

**Verificación:**
- Hover sobre un nodo azul
- Debe mostrar: `<b>[nombre]</b><br>Tipo: candidato<br>Comunidad: 1`

---

### TEST 3: Parámetros Interactivos
**Acción:** En sidebar, cambia "Umbral de peso" a 20

**Esperado:**
- ✅ El grafo cambia (menos aristas)
- ✅ Número total de aristas disminuye
- ✅ Modularidad puede cambiar
- ✅ Número de comunidades puede cambiar

**Verificación:**
```
ANTES (umbral=10):
  Aristas: ~1100
  Modularidad: 0.456

DESPUÉS (umbral=20):
  Aristas: ~800 (menos)
  Modularidad: 0.5XX (podría subir)
```

---

### TEST 4: Algoritmos
**Acción:** Cambia "Algoritmo de detección" a "Girvan-Newman"

**Esperado:**
- ✅ Aparece slider "Número de comunidades" (2-8)
- ✅ Colores del grafo cambian
- ✅ Métricas se actualizan
- ✅ Número de comunidades = valor del slider

**Verificación:**
- Ajusta slider a 5
- Verifica que dice "Comunidades: 5"

---

### TEST 5: Análisis de Comunidades
**Acción:** Baja a "Análisis de Comunidades"

**Esperado:**
- ✅ Tab "Composición" muestra 3+ expanders (una por comunidad)
- ✅ Al expandir, se ven candidatos listados
- ✅ Se ven departamentos agrupados
- ✅ Se ven franjas demográficas

**Verificación:**
- Expande "Comunidad 1"
- Debe haber:
  - Candidatos: (nombre del candidato)
  - Departamentos: (lista de depts)
  - Franjas: (lista de franjas demográficas)

---

### TEST 6: RETO 1 (Puentes)
**Acción:** Marca checkbox "Reto 1: Análisis de Puentes" en sidebar

**Esperado:**
- ✅ Aparece panel "RETO 1: Análisis de Puentes"
- ✅ Tabla con Top 10 nodos puente
- ✅ Columnas: Nodo, Tipo, Betweenness, Grado, Comunidades conectadas
- ✅ Expanders de análisis de impacto

**Verificación:**
- Scroll hasta ver la tabla
- Expande el primer puente
- Debe mostrar:
  ```
  Impacto global:
  - Componentes conexas: X → Y
  - Cambio: +Z
  Interpretación: CRÍTICO/importante
  ```

---

### TEST 7: RETO 2 (Franjas)
**Acción:** Marca checkbox "Reto 2: Evolución por Franja"

**Esperado:**
- ✅ Aparece panel "RETO 2: Evolución por Franja Demográfica"
- ✅ Dropdown con criterios: edad, estrato, educacion, ruralidad
- ✅ 3 tarjetas mostrando información por franja
- ✅ Línea "Resumen de Características" con gráficos

**Verificación:**
- Selecciona "edad" en dropdown
- Deben aparecer 4 tarjetas: "18-25 años", "26-40 años", "41-60 años", "61+ años"
- Cada tarjeta muestra: Conectados, Comunidades

---

### TEST 8: RETO 3 (Parámetros)
**Acción:** Marca checkbox "Reto 3: Comparación de Parámetros"

**Esperado:**
- ✅ Aparece panel "RETO 3: Comparación de Parámetros"
- ✅ Lado izquierdo: Config A (datos actuales)
- ✅ Lado derecho: Config B (con slider ajustable)
- ✅ Tabla comparativa de métricas
- ✅ Indicador de significancia
- ✅ Radio button para seleccionar mejor

**Verificación:**
- Config A muestra umbral actual
- Ajusta slider en Config B a 15
- Observa cambios en métrica "Comunidades"
- Selecciona radio "Config B es mejor"

---

## 📊 PRUEBAS DE DATOS

### TEST 9: Integridad de Datos
**Acción:** Ejecuta validador_datos.py

```bash
python validador_datos.py
```

**Esperado:**
```
✓ electoral_nodos.csv encontrado
✓ electoral_aristas.csv encontrado
✓ Nodos cargados: 66 filas
✓ Aristas cargadas: 1000+ filas
✓ Todas las columnas requeridas presentes
✓ Todos los node_id son únicos
✓ Todas las aristas referencian nodos válidos
✓ Pesos en rango válido: [0, 100]
✓ Grafo con 66 nodos y 1000+ aristas
✓ VALIDACIÓN EXITOSA
```

---

### TEST 10: Análisis Avanzado
**Acción:** Ejecuta analisis_avanzado.py

```bash
python analisis_avanzado.py
```

**Esperado:**
```
[1/8] Cargando datos...
  ✓ 66 nodos cargados
  ✓ 1000+ aristas cargadas

[2/8] Explorando estructura...
  Tipos de nodos:
    - candidato: 6
    - departamento: 34
    - franja_demografica: 9

[3/8] Construyendo grafo...
  ✓ Grafo con 66 nodos y 1000+ aristas

... (continúa) ...

[8/8] RESUMEN
  MODULARIDAD: 0.XXX
  COMUNIDADES: X
  PUENTES: X nodos puente encontrados
```

**Resultado:**
- Se genera archivo: `reporte_analisis_TIMESTAMP.txt`
- Contiene análisis completo sin la interfaz

---

## 🎯 PREGUNTAS CLAVE - VALIDACIÓN

### Pregunta 1: Departamentos similares
**TEST:** En app, busca panel "Respuestas a Preguntas Clave"

**Esperado:**
- Se muestran departamentos agrupados por comunidad
- Ejemplo: "Comunidad 1: Bogotá, Cundinamarca, Antioquia, ..."

---

### Pregunta 2: Regiones vs Comunidades
**TEST:** Mismo panel, segunda pregunta

**Esperado:**
- Se mencionan regiones (Andina, Pacífico, Caribe, etc.)
- Indica si coinciden o no

---

### Pregunta 3: Franjas homogéneas
**TEST:** Mismo panel, cuarta pregunta

**Esperado:**
- Muestra franja más homogénea (ej: "61+ años")
- Tabla comparativa mostrando en cuántas comunidades está cada franja

---

### Pregunta 4: Separación de grupos
**TEST:** Panel "Resumen Ejecutivo"

**Esperado:**
- Métrica "Modularidad" con valor numérico
- Interpretación: ✅/⚠️/❌

---

## 🚨 TROUBLESHOOTING

### ERROR: "ModuleNotFoundError: No module named 'streamlit'"
**Solución:**
```bash
pip install streamlit==1.36.0
```

---

### ERROR: "FileNotFoundError: electoral_nodos.csv"
**Causa:** Archivos CSV no en mismo directorio  
**Solución:**
1. Verifica que `electoral_nodos.csv` existe
2. Verifica que está en la carpeta donde ejecutas `app.py`
3. Ejecuta: `python validador_datos.py`

---

### ERROR: "Port 8501 already in use"
**Causa:** Otra instancia de Streamlit corriendo  
**Solución:**
```bash
# Opción 1: Usar otra puerto
streamlit run app.py --server.port 8502

# Opción 2: Matar proceso
# En Task Manager: busca "streamlit" y termina
```

---

### PANTALLA EN BLANCO / No carga nada
**Causa:** Error de ejecución  
**Solución:**
1. Abre consola: Ctrl+Shift+` en navegador
2. Busca mensaje de error
3. Intenta:
   - Reload: F5
   - Baja umbral de peso
   - Reinicia: `streamlit run app.py --logger.level=debug`

---

### Grafo se ve vacío / sin nodos
**Causa:** Umbral muy alto (filtra todas las aristas)  
**Solución:**
- Baja "Umbral de peso" a 0-5%
- Recarga la página

---

## ✅ CHECKLIST FINAL

Antes de considerar el proyecto completo:

```
FUNCIONALIDAD:
  ☐ App carga sin errores
  ☐ Grafo visualiza correctamente
  ☐ Parámetro umbral funciona (cambia grafo)
  ☐ Parámetro algoritmo funciona
  ☐ Se muestran 3+ comunidades
  ☐ Métricas se actualizan en tiempo real

RETOS:
  ☐ RETO 1 muestra tabla de puentes
  ☐ RETO 1 análisis de impacto funciona
  ☐ RETO 2 dropdown de criterios funciona
  ☐ RETO 2 tarjetas muestran datos correctos
  ☐ RETO 3 Config B slider ajustable
  ☐ RETO 3 tabla comparativa válida

PREGUNTAS CLAVE:
  ☐ Pregunta 1 respondida (departamentos)
  ☐ Pregunta 2 respondida (regiones)
  ☐ Pregunta 3 respondida (medios)
  ☐ Pregunta 4 respondida (franja homogénea)
  ☐ Pregunta 5 respondida (separación)

VALIDACIÓN:
  ☐ validador_datos.py pasa sin errores
  ☐ analisis_avanzado.py genera reporte
  ☐ Reporte contiene hallazgos válidos

DOCUMENTACIÓN:
  ☐ README.md explicita justificación
  ☐ QUICKSTART.md permite empezar rápido
  ☐ RETOS_ESPECIFICACION.md es completa
  ☐ RESUMEN_EJECUTIVO.md es consistente
```

---

## 🏆 ESTADO FINAL

Cuando TODO el checklist de arriba esté completado:

```
✅ MVP IMPLEMENTADO (Calificación 3.0)
✅ RETO 1 COMPLETADO
✅ RETO 2 COMPLETADO
✅ RETO 3 COMPLETADO
✅ DOCUMENTACIÓN COMPLETA
✅ LISTO PARA EVALUACIÓN
```

---

**Generado:** Abril 2026  
**Versión:** 1.0  
**Estado:** Verificación Completa
