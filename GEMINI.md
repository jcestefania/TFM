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

## 🚀 Hoja de Ruta del Proyecto
1. **Fase 1: Remates Finales en SAREnv** - **[COMPLETA]**
2. **Fase 2: Preparación del Entorno de Pruebas (MTS)** - **[COMPLETA]**
3. **Fase 3: Middleware e Integración de Coordenadas UTM** - **[COMPLETA]**
4. **Fase 4: Hito Visual y Cuaderno Demostración Rápida** - **[COMPLETA]**
5. **Fase 5: Verificación de Rutas Relativas y Portabilidad Total** - **[COMPLETA]**
6. **Fase 6: Framework Modular y Publicación en GitHub (`sarenv-mts`)** - **[COMPLETA]**
7. **Fase 7: Simulación Trayectoria Bomberos vs Drones** - **[SIGUIENTE PASO]**
8. **Fase 8: Redacción de Trabajo Futuro (Objetivos Móviles)** - **[PLANIFICADA]**
9. **Fase 9: Cierre y Compilación Final de la Memoria LaTeX** - **[PLANIFICADA]**
10. **Fase 10: Diapositivas y Preparación de la Defensa** - **[PLANIFICADA]**

## 📑 Estado de la Memoria
1. **Capítulo 1 (Introducción):** Estructurado y redactado con objetivos y contexto. **[COMPLETO]**
2. **Capítulo 2 (Estado del Arte):** Detallado y fusionado con fundamentos bayesianos. **[COMPLETO]**
3. **Capítulo 3 (Modelado):** Ampliado con las formulaciones de SAREnv, sensor (50 m), RBF y Montecarlo. **[COMPLETO]**
4. **Capítulo 4 (Desarrollo e Integración):** Middleware UTM, arquitectura de paquetes y filtros OSM. **[BORRADOR LISTO]**
5. **Capítulo 5 (Experimentación):** Justificación LPB por perfiles de Koester, Optuna y métricas. **[BORRADOR REDACTADO]**
6. **Capítulo 6 (Análisis de Resultados):** Tablas definitivas de 900 simulaciones e interpretación. **[COMPLETO]**
7. **Capítulo 7 (Conclusiones y Trabajo Futuro):** En redacción (incluye extensión de víctimas dinámicas). **[BORRADOR]**
