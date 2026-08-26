# Plan Maestro TFM: Optimización SAR con Drones (SAREnv + MTS)

Este archivo centraliza la estrategia, el estado de los componentes y la hoja de ruta definitiva del proyecto.

## 📂 Estructura Limpia Consolidada (`sarenv-mts`)
- `MTS-UncertainEnvironment-Algoritmos-bioinspirados/`:
  - `sarenv/`: Paquete integrado de SAREnv (probabilidad topológica LPB de Robert Koester).
  - `metrics/`: Módulo de evaluación centralizado (`PathEvaluatorTFM`).
  - `middleware/`: Herramientas de unión SAREnv <-> MTS (`utils_pipeline.py` y `generar_json_real.py`).
  - `busquedas/`: Algoritmos bioinspirados (ACO, ABC, BHA y Voraz).
  - `extra/`: Sensor footprint (50 m) y mapa de creencias residual $b(v^k)$.
  - `experiments/`: Scripts para optimización y simulaciones en lote.
  - `TFM_JC/notebooks/`: Cuadernos interactivos oficiales (`Notebook_Demo_Rapida_Interactiva.ipynb`, `Analisis_Resultados.ipynb`, `Benchmark_Perfiles_Real_Interactivo.ipynb`).
  - `TFM_JC/resultados/`: Base de datos de 900 simulaciones, CSV maestro y figuras 300 DPI en inglés.

## 🚀 Hoja de Ruta Restante (Hacia la Entrega y Defensa)
1. **Fase 1: Verificación de Cuadernos en VS Code** - **[EN CURSO POR EL USUARIO]**
2. **Fase 2: Redacción Integral y Compilación de la Memoria LaTeX** - **[SIGUIENTE PASO]**
   - Integrar documentos de modelado de sensor (50 m), restricciones físicas, RBF y Montecarlo.
   - Insertar tablas de 900 simulaciones y figuras vectoriales en inglés.
   - Redactar Conclusiones y Trabajo Futuro (Ruta Bomberos + Víctimas Dinámicas).
   - Compilación limpia del PDF final.
3. **Fase 3: Preparación de Diapositivas y Defensa del TFM** - **[PLANIFICADA]**

## 📑 Estado de los Capítulos de la Memoria (`Software/memoria/`)
1. **Capítulo 1 (Introducción y Motivación):** Redactado con objetivos del proyecto.
2. **Capítulo 2 (Estado del Arte):** Detallado con fundamentos bayesianos y algoritmos SAR.
3. **Capítulo 3 (Modelado del Entorno y Sensor):** Formulación de SAREnv, sensor de 50 m y filtros OSM.
4. **Capítulo 4 (Arquitectura e Integración):** Arquitectura modular `sarenv-mts` y middleware UTM.
5. **Capítulo 5 (Marco Experimental):** Justificación LPB de perfiles de Koester, Optuna y métricas.
6. **Capítulo 6 (Análisis de Resultados):** Tablas de 900 simulaciones, boxplots y discusión.
7. **Capítulo 7 (Conclusiones y Trabajo Futuro):** Resumen de aportaciones, rutas reales de bomberos y objetivos móviles.
