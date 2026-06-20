# Plan de Trabajo TFM: Optimización SAR con Drones (SAREnv + MTS)

Este archivo centraliza la estrategia, el estado de los componentes y los próximos pasos del proyecto para mantener el contexto entre sesiones.

## 📂 Estructura Organizada (TFM_JC)
- `TFM_JC/scripts/`: Generación, Evaluación, Mapas Interactivos (HTML) y Visualización Pro.
- `TFM_JC/resultados/`: Datos (.npy, .geojson), Gráficas (.png), Rutas (.pdf) y `path_plots_html/`.
- `TFM_JC/memoria/`: Borradores LaTeX, Guía de Montecarlo y documentos de trabajo.
- `TFM_JC/notebooks/`: Cuadernos académicos.

## 🚀 Hoja de Roadmap
1. **Fase 1: Remates Finales en SAREnv (Cuaderno 1)** - *Optimizaciones pedidas por los tutores.* **[COMPLETA]**
2. **Fase 2: Preparación del Entorno de Pruebas (MTS)** - *Búsqueda voraz con 1 dron y familiarización.* **[COMPLETA]**
3. **Fase 3: El Middleware (Integración SAREnv y MTS)** - *Conversión a JSON y transformación de coordenadas.* **[COMPLETA]**
4. **Fase 4: Hito Visual (Paso 1)** - *Carga del mapa real en la web app de MTS y validación.* **[COMPLETA]**
5. **Fase 5: Escenarios Canónicos por Capas y Benchmarking** - *Modelar perfiles del manual (Autista, Demencia, Senderista) y comparar la búsqueda informada frente a la aleatoria.* **[COMPLETA]**
6. **Fase 6: Trayectoria de Bomberos y Trabajo Futuro** - *Simular el rendimiento de la ruta real de los bomberos y documentar objetivos móviles.* **[PLANIFICADA]**

## 📑 Estado de la Memoria
1. **Capítulo 1 (Introducción):** Estructurado y redactado con objetivos y contexto. **[COMPLETO]**
2. **Capítulo 2 (Estado del Arte):** Detallado y fusionado con fundamentos bayesianos. **[COMPLETO]**
3. **Capítulo 3 (Modelado):** Ampliado con las formulaciones de SAREnv, sensor, RBF y Montecarlo. **[COMPLETO]**
4. **Capítulo 4 (Desarrollo e Integración):** Modificaciones de la fusión y el middleware UTM explicados. **[BORRADOR LISTO]**
5. **Capítulo 5 (Experimentación):** Justificación LPB por perfiles del manual, variables y métricas redactadas. **[BORRADOR REDACTADO]**
6. **Capítulo 6 (Análisis de Resultados):** Tablas definitivas de 6 algoritmos e interpretación de resultados redactada. **[COMPLETO]**

## 📝 Tareas Pendientes ( Roadmap )

### FASE 1: Remates Finales en SAREnv (Cuaderno 1)
- [x] **Modificar la fusión de capas:** Cambiar `np.maximum` por una suma ponderada y posterior normalización en `sarenv/core/generation.py` y actualizar la documentación/notebook correspondientes.
- [x] **Opciones de hiperparámetros para futura GUI:** Añadir comentarios con corchetes en las definiciones del Notebook (clima, tipo de entorno, resoluciones, tamaños) para documentar todas las opciones admitidas.
- [x] **Justificación visual del Heatmap:** Añadir celda Markdown detallando la lógica de probabilidad en Casa de Campo (Lago, Zoo, Parque de Atracciones) con sus pesos específicos.

### FASE 2: Preparación del entorno de pruebas
- [x] **Reducir a 1 Agente:** Configurar todas las simulaciones y pruebas para un solo dron (evitando colisiones en MTS).
- [x] **Familiarización con MTS:** Ejecutar pruebas básicas en MTS (Greedy con 1 dron) para analizar la estructura de entrada de datos.

### FASE 3: El Middleware (Integración de SAREnv y MTS)
- [x] **Conversión de Matriz (.npy) a JSON:** Desarrollar el script de traducción basándose en `generar-json.py` de MTS para generar los JSON que necesita MTS.
- [x] **Transformación de Coordenadas:** Implementar la conversión de coordenadas globales (Lat/Lon) de SAREnv a coordenadas locales (X, Y) para MTS tomando como origen el margen inferior izquierdo de la búsqueda, basándose en `generar_plan.py` / `plan.py`.

### FASE 4: Hito Visual (Paso 1)
- [x] **Carga y Verificación Visual:** Cargar el mapa real exportado en el entorno MTS y contrastar visualmente en la aplicación web que el mapa renderizado se corresponde fielmente con el mapa de SAREnv.
- [x] **Punto de Control:** Detener la ejecución para avisar a los tutores una vez logrado este hito.

### FASE 5: Escenarios Canónicos por Capas y Benchmarking
- [x] **Definir perfiles de víctimas (LPB):** Redactar en LaTeX la justificación de los perfiles del manual (Autista, Demencia, Senderista) y las 5 métricas en el Capítulo 5.
- [x] **Generar mapas de calor por capas:** Crear los mapas en SAREnv con restricciones de transitabilidad física para Autista (capa estructuras/agua), Demencia (bosques) y Senderista (caminos).
- [x] **Ejecutar simulaciones masivas (1000 iteraciones):** Correr por detrás las simulaciones en MTS (semillas 0-49) de Voraz, ACO, ABC y BHA y guardar las trayectorias.
- [x] **Evaluar rendimiento y tasa de acierto:** Evaluar en Python con `PathEvaluator` de SAREnv el rendimiento de la búsqueda informada (con heatmap) frente a la ciega (totalmente aleatoria).

### FASE 6: Trayectoria de Bomberos y Trabajo Futuro
- [ ] **Simular ruta de Bomberos:** Simular la detección en la trayectoria real de los bomberos en el simulacro de la Casa de Campo y compararla en la tabla de resultados.
- [ ] **Documentar objetivos móviles:** Redactar en el capítulo de Conclusiones el modelo teórico markoviano de objetivos móviles como Trabajo Futuro utilizando el manual y el notebook de referencia.
