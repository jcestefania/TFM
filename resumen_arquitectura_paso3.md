# Integración SAREnv + MTS: Arquitectura del TFM

Este documento resume la integración técnica realizada para unir el framework **SAREnv** (generación de entornos reales) con el framework **MTS** (algoritmos de búsqueda bioinspirados).

## 1. Objetivo de la Integración
Sustituir la generación de mapas de probabilidad sintéticos (falsos) de MTS por **mapas de probabilidad reales** basados en topografía de la **Casa de Campo (Madrid)** y el modelo de comportamiento de personas perdidas (**LPB**).

---

## 2. Flujo de Datos (Pipeline)
El sistema funciona en tres etapas desacopladas para mantener la limpieza arquitectónica:
1.  **SAREnv**: Genera la matriz de probabilidad (`Numpy`).
2.  **Script Puente**: Empaqueta el mapa y la configuración en archivos (`.npy` y `.json`).
3.  **MTS**: Carga los archivos y ejecuta los drones (ACO, ABC, etc.).

---

## 3. Archivos Creados y Modificados

### A. `generar_escenario_real.py` (Nuevo - El Puente)
Es el archivo que orquesta a SAREnv para extraer los datos reales.
*   **Función:** Descarga datos de OpenStreetMap, rasteriza capas (caminos, edificios, ríos) y crea un **Heatmap**.
*   **Punto Clave:** Analiza el mapa para encontrar el máximo de probabilidad y colocar ahí a la víctima real.

```python
# Fragmento del script puente:
env = data_gen.generate_environment_from_polygon(polygon=poly, meter_per_bin=20)
heatmap = env.get_combined_heatmap()

# Normalización para el filtro bayesiano de MTS
heatmap = heatmap / np.sum(heatmap)

# Identificar coordenadas de la víctima real (máxima probabilidad)
idx_max = np.unravel_index(np.argmax(heatmap), heatmap.shape)
y_max, x_max = int(idx_max[0]), int(idx_max[1])
```

### B. `bf-busqueda.py` (Modificado - El Motor)
Se ha modificado el motor principal de MTS para que sea capaz de leer mapas externos.
*   **Variable Clave: `bk`**: Es la matriz que los algoritmos (ACO, ABC) usan para "oler" a la víctima.
*   **Lógica de Inyección:** Se ha añadido un condicional que detecta si el JSON pide un mapa real.

```python
# Lógica de carga inteligente en bf-busqueda.py:
ruta_real = params.get("ruta_mapa_real")

if ruta_real:
    # CARGA DESDE SARENV (Archivo binario .npy)
    bk = np.load(path_npy)
else:
    # FALLBACK: Generación sintética original de MTS
    bk = calcular_prob(size, COV, indicios, pesos)
```

### C. `experimentos_casacampo.ipynb` (Nuevo - Panel de Control)
Un Jupyter Notebook para que el usuario controle todo el TFM de forma visual.
*   Permite cambiar el número de drones y el algoritmo (`ACO`, `ABC`, `BHA`, `lawnmower`).
*   Lanza la simulación y muestra los resultados y la animación 3D de Plotly.

---

## 4. Funcionamiento de los Algoritmos Bioinspirados
Todos los algoritmos en este TFM funcionan bajo el concepto de **Distribución de Creencias (Belief Map)**:

1.  **Atracción por Probabilidad:** Los drones leen la variable `bk` (el mapa de SAREnv). Se sienten atraídos por las celdas con valores altos (donde el LPB dice que es más probable encontrar a alguien).
2.  **Descarte Bayesiano:** Cuando un dron pasa por una celda y no encuentra nada, pone ese valor de `bk` a **0**. La "montaña de olor" desaparece y el dron se ve obligado a explorar otras zonas de la Casa de Campo.
3.  **Universalidad:** Al inyectar el mapa en la raíz del script, **todos los algoritmos** (ACO, ABC, BHA, Voraz) entienden y usan el terreno real de la Casa de Campo automáticamente.

---

## 5. Estructura de Carpetas Personalizada
Para este TFM, todo el trabajo se centraliza en:
*   **Configuraciones:** `TFM-JuanCarlos/pruebas/`
*   **Resultados:** `resultados/escenario_real_casacampo/`
*   **Entorno Virtual:** `tfm/` (en la raíz, con todas las dependencias unificadas).
