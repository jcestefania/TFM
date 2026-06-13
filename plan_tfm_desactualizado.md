# Plan de Implementación: TFM Juan Carlos (SAREnv + MTS)

## Background & Motivation
El objetivo del Trabajo de Fin de Máster es integrar el generador de entornos reales basados en probabilidad topológica (SAREnv) con el entorno de simulación de algoritmos de búsqueda bioinspirados multiagente (MTS). La arquitectura técnica y el pipeline de datos ya han sido establecidos, permitiendo la generación e inyección de mapas de calor desde SAREnv hacia MTS.

## Scope & Impact
El marco experimental se centrará **exclusivamente en el entorno real de la Casa de Campo (Madrid)**. Las variables independientes del estudio aislarán el comportamiento del enjambre para evaluar su rendimiento táctico, escalabilidad y adaptabilidad frente a la topología urbana/natural.

Variables Independientes:
1.  **Algoritmo de Búsqueda:** Bioinspirados (ACO, ABC, BHA) vs. Clásicos (Lawnmower, Expanding Square, Búsqueda Voraz).
2.  **Tamaño del Enjambre:** Variación en el número de agentes (ej. 2, 5 y 10 drones).
3.  **Condiciones Iniciales:** Variación de las coordenadas de despliegue (`init_pos`) y la posición de la víctima (`obj_pos`).

Variables Dependientes (Métricas):
1.  Tasa de éxito (víctima encontrada vs. batería agotada).
2.  Pasos requeridos / Tiempo de convergencia.
3.  Distancia total recorrida.

## Fases de Implementación

### Fase 1: Validación y Calibración (Sanity Checks)
*   **Orquestación:** Creación de un panel de control interactivo mediante un Jupyter Notebook (`TFM-JuanCarlos/pruebas/experimentos_casacampo.ipynb`) para facilitar el seguimiento con el tutor y aportar una herramienta altamente visual.
*   **Estructura del Notebook de Control:**
    1.  Celdas de Markdown para título y objetivos de las pruebas.
    2.  Celdas de Código para importaciones y configuración del `sys.path`.
    3.  Llamada a `generar_escenario_real.py` para asegurar disponibilidad del JSON y el heatmap `.npy`.
    4.  Lógica programática para cargar el JSON, inyectar dinámicamente variables experimentales (ej. `algoritmo_busqueda`, `num_agents`) y guardar la configuración.
    5.  Ejecución en subproceso de `bf-busqueda.py` con el JSON modificado.
    6.  Visualización interactiva (tablas y/o gráficas) de los resultados extraídos del archivo CSV final.
*   **Acciones Técnicas de Calibración:**
    *   Habilitar la visualización gráfica de trayectorias.
    *   Calibrar la velocidad (`mov_delta`), el alcance del sensor (`dmax`, `pdmax`) y la batería (`num_steps`) para adaptarlos a la matriz generada de 119x139.

### Fase 2: Diseño de Experimentos
*   **Objetivo:** Establecer la batería formal de pruebas.
*   **Acciones:**
    *   Crear los archivos JSON de configuración base para las combinaciones de (Algoritmo) x (Nº Drones).
    *   Fijar un número $N$ de simulaciones de Montecarlo (ej. 50-100 ejecuciones por configuración con distintas semillas y víctimas).

### Fase 3: Ejecución Masiva
*   **Objetivo:** Obtención de datos estadísticos.
*   **Acciones:**
    *   Desarrollar un script automatizado (ej. `lanzar_pruebas_masivas.py`) que itere sobre los JSON creados.
    *   Almacenar todos los logs y resultados CSV organizadamente en el directorio `resultados/`.

### Fase 4: Análisis y Visualización
*   **Objetivo:** Sintetizar la información empírica para la memoria del TFM.
*   **Acciones:**
    *   Desarrollar Jupyter Notebooks de análisis.
    *   Generar gráficas de rendimiento (Boxplots de distancia, curvas de probabilidad de éxito, heatmaps de trayectorias).

## Verification
Cada fase será iterativa. Antes de lanzar la ejecución masiva (Fase 3), se validará con un pequeño lote de pruebas que las métricas extraídas en los CSV tengan sentido físico y algorítmico.