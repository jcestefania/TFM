# Guía de Estudio TFM: Nuestra Integración y Modificaciones (Parte 2)

Este documento detalla todas las **modificaciones personalizadas, scripts creados y adaptaciones** que hemos implementado sobre el framework de MTS y SAREnv. Está diseñado para que comprendas exactamente qué archivos se han cambiado, qué nos pidieron tus tutores y cómo lo resolvimos.

---

## 📂 Estructura de los Archivos del TFM

Todo nuestro trabajo está organizado para mantener tu workspace limpio y no mezclar tus desarrollos con el código original del framework de MTS:
*   📁 **`TFM_JC/`**: Tu directorio de trabajo.
    *   📁 **`pruebas/`**: Contiene tus escenarios JSON, matrices `.npy` y el panel de control Jupyter Notebook (`Experimentos_MTS_Real.ipynb`).
    *   📁 **`scripts/`**: Tus scripts personalizados (ej. el middleware `generar_json_real.py`).
    *   📁 **`resultados/`**: Carpeta ordenada donde se guardan de forma automática todos los archivos CSV de tus simulaciones.

---

## 🛠️ Resumen de Modificaciones y Peticiones del Tutor

A continuación se detallan las peticiones de tus tutores y las soluciones técnicas que hemos implementado:

### 1. Fusión de Capas por Suma Ponderada (Fase 1)
*   **Petición del tutor:** SAREnv originalmente combinaba las capas de probabilidad (carreteras, vegetación, agua) usando un operador `max` (`np.maximum`), lo que impedía acumular probabilidad en zonas donde se cruzan varias características favorables. Pidieron cambiarlo por una suma ponderada.
*   **Nuestra solución:** Modificamos el método `get_combined_heatmap()` en [generation.py](file:///c:/Users/juanc/Desktop/TFM/TFM-Juan%20Carlos/Software/SAREnv/sarenv/core/generation.py):
    1.  Multiplicamos la matriz binaria de cada capa por su peso correspondiente en la configuración.
    2.  Sumamos todas las capas ponderadas de forma aditiva.
    3.  Normalizamos la matriz final dividiendo cada celda por la suma total de todo el mapa (para que el volumen total siga sumando $1.0$).
    4.  Dejamos el código del `np.maximum` original comentado en el archivo para que el tutor vea el cambio.

### 2. Configuración de 1 Dron (Fase 2)
*   **Petición del tutor:** Configurar las pruebas para un solo UAV/dron (evitando colisiones entre agentes, ya que el código multi-agente de MTS original no incluye esquiva de colisiones en mapas personalizados grandes).
*   **Nuestra solución:** Ajustamos la variable `num_drones = 1` en el panel de control y forzamos a que el JSON inyecte un solo agente.

### 3. Middleware de Conversión y Proyección UTM (Fase 3)
*   **Petición del tutor:** Crear un script que traduzca el mapa real exportado de SAREnv (GeoJSON y `.npy`) al formato JSON que necesita MTS, haciendo que la posición de inicio del dron (LKP) coincida geográficamente.
*   **Nuestra solución:** Creamos el script [generar_json_real.py](file:///c:/Users/juanc/Desktop/TFM/TFM-Juan%20Carlos/Software/framwork-MTS/MTS-UncertainEnvironment-Algoritmos-bioinspirados/TFM_JC/scripts/generar_json_real.py). Este script:
    1.  Lee el punto geográfico del LKP/IPP en Latitud/Longitud (del GeoJSON).
    2.  Calcula el huso UTM correspondiente (ej: Zona 30 Norte, EPSG:32630 para Madrid).
    3.  Proyecta esa coordenada a metros usando la librería `pyproj`.
    4.  Calcula la distancia métrica a la esquina inferior izquierda del mapa (`bounds minx, miny`) y la divide por la resolución del píxel (`meter_per_bin`) para obtener la coordenada discreta exacta `[pixel_x, pixel_y]` en la rejilla de MTS.
    5.  Copia y renombra el archivo `.npy` de probabilidad junto al JSON de salida para que todo esté autocontenido.

### 4. Spawn del Objetivo según el Heatmap (Fase 3)
*   **Problema detectado:** El simulador MTS original colocaba al objetivo al azar cerca de los indicios usando una fórmula gaussiana teórica, lo que ignoraba por completo la geografía del mapa real.
*   **Nuestra solución:** Modificamos [bf-busqueda.py](file:///c:/Users/juanc/Desktop/TFM/TFM-Juan%20Carlos/Software/framwork-MTS/MTS-UncertainEnvironment-Algoritmos-bioinspirados/bf-busqueda.py). Si se carga una simulación con un mapa real y el objetivo está en modo aleatorio (`goal_pos = None`), el script aplana el heatmap real y realiza un muestreo ponderado (`np.random.choice` usando las intensidades del heatmap como pesos de probabilidad). Así, la víctima aparece de forma realista solo en las zonas con alta probabilidad real.

### 5. Estética y Solución de Crashes de la Interfaz 3D (Fase 4)
*   **Petición del tutor:** Cambiar la paleta de colores porque el mapa original se veía "oscuro" (las zonas sin probabilidad se pintaban de negro).
*   **Problemas adicionales detectados:** 
    *   Plotly crasheaba con un `RangeError` de memoria en el navegador en simulaciones largas (1000 pasos) porque intentaba serializar demasiados datos 3D.
    *   El marcador de la víctima (la X roja) se quedaba tapada bajo el relieve de las montañas de probabilidad.
*   **Nuestras soluciones en [interfaz.py](file:///c:/Users/juanc/Desktop/TFM/TFM-Juan%20Carlos/Software/framwork-MTS/MTS-UncertainEnvironment-Algoritmos-bioinspirados/extra/interfaz.py):**
    *   **Estética:** Cambiamos la paleta de colores de `"hot"` a `"YlOrRd"` (Yellow-Orange-Red). Ahora las zonas planas son color crema claro y los picos son rojo intenso.
    *   **Crashes de Memoria:** Si la simulación supera los 100 pasos, el renderizado calcula un salto dinámico (`step_skip`) para dibujar un fotograma cada $N$ pasos, limitando la animación a un máximo de 100 fotogramas y evitando que se llene la memoria.
    *   **Visibilidad de la Víctima:** Calculamos la altura de la X roja dinámicamente sumándole $1.5$ metros al relieve local del mapa de calor, de modo que el marcador flote visiblemente por encima de la montaña de probabilidad.
    *   **Limpieza de temporales:** Eliminamos la exportación opcional que guardaba imágenes PDF en la raíz del proyecto para evitar generar carpetas basura.

### 6. Saneamiento y Redirección de Resultados (Orden del Proyecto)
*   **Petición tuya:** Evitar tener archivos basura dispersos por la raíz del framework de MTS y guardar tus resultados en una carpeta propia.
*   **Nuestras soluciones:**
    *   **Redirección de CSVs:** Modificamos [bf-busqueda.py](file:///c:/Users/juanc/Desktop/TFM/TFM-Juan%20Carlos/Software/framwork-MTS/MTS-UncertainEnvironment-Algoritmos-bioinspirados/bf-busqueda.py) para que, si el JSON de entrada pertenece a `TFM_JC`, guarde automáticamente los CSV de resultados dentro de `TFM_JC/resultados/` en lugar de la raíz `resultados/`.
    *   **Limpieza del repositorio:** Revertimos a su estado original de git todos los archivos modificados del framework original que no necesitábamos (como `generar-json.py`, `bf-expanding.py`, `bf-lawnmower.py`, `ini-pos.py`, `ldfs-heur.py`, `ldfs-miope.py`), manteniendo el repositorio de MTS completamente limpio de rutas de tu ordenador.
