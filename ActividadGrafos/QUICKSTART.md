# 🚀 GUÍA RÁPIDA DE INICIO

## 1️⃣ INSTALACIÓN (5 minutos)

### Opción A: Automática (Windows)
```batch
# Haz doble click en:
instalar.bat

# O en PowerShell:
.\instalar.bat
```

### Opción B: Manual
```bash
# En tu terminal preferida:
pip install -r requirements.txt
```

---

## 2️⃣ INICIAR LA APLICACIÓN

### Opción A: Doble click (Windows)
```batch
ejecutar.bat
```

### Opción B: Manual
```bash
streamlit run app.py
```

**Resultado:** Se abrirá automáticamente en http://localhost:8501

---

## 3️⃣ PRIMEROS PASOS EN LA APP

### 🎮 Panel de Control (Sidebar Izquierdo)

1. **Umbral de peso:** Baja = más conexiones débiles | Sube = solo conexiones fuertes
2. **Algoritmo:** 
   - Louvain → Detección rápida
   - Girvan-Newman → Jerárquico
3. **Retos:** Activa los 3 checkboxes para ver análisis avanzados

### 📊 Secciones principales

| Sección | Qué ves | Acción |
|---------|---------|--------|
| **Metrics** | Nodos, aristas, modularidad | INFO |
| **Grafo** | Visualización en colores | INTERACTÚA (hover) |
| **Comunidades** | Composición de grupos | EXPANDE tabs |
| **Preguntas clave** | Respuestas directas | LEE |
| **Reto 1** | Top puentes | EXPANDE impacto |
| **Reto 2** | Franjas demográficas | SELECCIONA criterio |
| **Reto 3** | Comparación parámetros | AJUSTA y usa radio |

---

## 4️⃣ ANÁLISIS RÁPIDO: ¿QUÉ SIGNIFICA?

### ✅ HIGH Modularidad (>0.5)
```
Significa: Comunidades muy claras
Implicación: Grupos electorales bien definidos
Acción: Confía en los clusters detectados
```

### ⚠️ MEDIUM Modularidad (0.3-0.5)
```
Significa: Comunidades moderadas
Implicación: Algunos solapamientos
Acción: Revisa puentes (Reto 1)
```

### ⛔ LOW Modularidad (<0.3)
```
Significa: Comunidades débiles
Implicación: Red muy interconectada
Acción: Prueba distinto umbral (Reto 3)
```

---

## 5️⃣ EJERCICIOS SUGERIDOS

### Ejercicio 1: Explorar Puentes (Reto 1)
1. Activa Reto 1 en sidebar
2. Observa los Top 10 nodos puente
3. Expande el top 1 (mayor betweenness)
4. ¿Cuántas comunidades conecta?
5. **Pregunta:** ¿Es un candidato o departamento?

### Ejercicio 2: Homogeneidad Demográfica (Reto 2)
1. Activa Reto 2 en sidebar
2. Selecciona criterio: "edad"
3. Observa "Franja más homogénea" en main panel
4. Cambia a criterio "estrato"
5. **Pregunta:** ¿Cambió la franja más homogénea?

### Ejercicio 3: Sensibilidad de Parámetros (Reto 3)
1. Activa Reto 3 en sidebar
2. Deja umbral en 10%, observa modularidad
3. Sube umbral a 25%
4. ¿Aumentó o bajó la modularidad?
5. **Pregunta:** ¿Cambiaron los números de comunidades?

---

## 6️⃣ PREGUNTAS DE DISCUSIÓN

### Para responder con la app:

1. **Geografía Electoral:**
   - ¿Qué departamentos forman una comunidad?
   - ¿Coincide con regiones reales?

2. **Candidatos:**
   - ¿Qué candidatos son "puentes"?
   - ¿Quién es el más central?

3. **Demografía:**
   - ¿Es la edad un factor de división?
   - ¿Y el estrato socioeconómico?

4. **Robustez:**
   - ¿Cambian mucho los resultados con diferente umbral?
   - ¿Qué parámetro es más crítico?

---

## 7️⃣ ARCHIVOS IMPORTANTES

```
ActividadGrafos/
├── app.py                    ← Aplicación principal (Streamlit)
├── analisis_avanzado.py     ← Análisis offline  
├── electoral_nodos.csv      ← Datos (no editar)
├── electoral_aristas.csv    ← Datos (no editar)
├── requirements.txt         ← Dependencias
├── README.md               ← Documentación completa
├── RETOS_ESPECIFICACION.md ← Detalles técnicos
└── validador_datos.py      ← Verificar integridad
```

---

## 8️⃣ TROUBLESHOOTING

### ❌ "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit
```

### ❌ "No se abre el navegador"
Abre manual: http://localhost:8501

### ❌ "Error en la visualización del grafo"
Prueba:
1. Recarga la página (F5)
2. Baja el umbral de peso (menos aristas)
3. Reinicia: Ctrl+C y `streamlit run app.py`

### ❌ "Los datos se ven vacíos"
Verifica:
1. `electoral_nodos.csv` existe
2. `electoral_aristas.csv` existe
3. Ambos en el mismo directorio que `app.py`

Puedes validar con:
```bash
python validador_datos.py
```

---

## 9️⃣ ANÁLISIS AVANZADO (Offline)

Si quieres análisis sin la interfaz web:

```bash
python analisis_avanzado.py
```

Genera:
- Reporte textual con hallazgos
- Top 20 puentes
- Ranking de departamentos
- Archivo: `reporte_analisis_TIMESTAMP.txt`

---

## 🔟 PRÓXIMOS PASOS

1. ✅ Instala y ejecuta la app
2. ✅ Explora los 3 retos (5-10 min cada uno)
3. ✅ Responde las 5 preguntas clave
4. ✅ Escribe conclusiones basadas en hallazgos
5. ✅ (Opcional) Ejecuta `analisis_avanzado.py` para reporte

---

## 📞 AYUDA RÁPIDA

| Pregunta | Respuesta |
|---|---|
| ¿Dónde modifico parámetros? | Sidebar izquierdo |
| ¿Cómo activo los retos? | Checkboxes en sidebar |
| ¿Cómo interpreto modularidad? | Panel "Resumen Ejecutivo" |
| ¿Qué es un puente? | Panel "RETO 1" |
| ¿Cómo exporto resultados? | Captura de pantalla o `analisis_avanzado.py` |

---

**¡Lista para aprender sobre afinidades electorales!** 🗳️
