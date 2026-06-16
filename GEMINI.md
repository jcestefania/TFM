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
5. **Fase 5: Escenarios Canónicos y Comparativa (LPB)** - *Modelar perfiles de víctimas (Demencia, Senderista) y enfrentar ACO vs ABC vs BHA.* **[EN PROCESO]**
6. **Fase 6: Simulación de Objetivos Dinámicos** - *Implementar búsqueda de víctimas móviles en MTS.* **[PLANIFICADA]**

## 📑 Estado de la Memoria
1. **Capítulo 1 (Introducción):** Estructurado y redactado con objetivos y contexto. **[COMPLETO]**
2. **Capítulo 2 (Estado del Arte):** Detallado y fusionado con fundamentos bayesianos. **[COMPLETO]**
3. **Capítulo 3 (Modelado):** Ampliado con las formulaciones de SAREnv, sensor, RBF y Montecarlo. **[COMPLETO]**
4. **Capítulo 4 (Desarrollo e Integración):** Modificaciones de la fusión y el middleware UTM explicados. **[BORRADOR LISTO]**
5. **Capítulo 5 (Experimentación):** Justificación LPB, variables y métricas formales redactadas. **[BORRADOR REDACTADO]**

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

### FASE 5: Escenarios Canónicos y Comparativa (LPB)
- [x] **Definir perfiles de víctimas (LPB):** Redactar en LaTeX la justificación de los perfiles de Demencia (Alzheimer) y Senderista basados en las estadísticas reales de SAREnv.
- [ ] **Generar mapas de calor específicos:** Crear los mapas con radio `"small"` ($0.6\text{ km}$) para Demencia y `"large"` ($3.2\text{ km}$) para Senderistas.
- [ ] **Simulaciones de Benchmark:** Correr comparativas completas de Voraz, ACO, ABC y BHA en ambos escenarios y almacenar métricas de rendimiento.

### FASE 6: Simulación de Objetivos Dinámicos
- [ ] **Configurar movimiento en JSON:** Inyectar la matriz de transición de movimiento `"p_transicion"` en la configuración real.
- [ ] **Evaluar persecución móvil:** Ejecutar los algoritmos sobre el objetivo en movimiento y registrar la evolución de la búsqueda en la Casa de Campo.

