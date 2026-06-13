# Conceptos Clave para la Defensa del TFM: SAREnv y Montecarlo

Este documento resume la lógica matemática y de simulación detrás de la evaluación de rutas en el proyecto SAREnv. Es fundamental para explicar y defender cómo se obtienen las métricas de éxito de los algoritmos.

---

## 1. ¿Qué significa "100 víctimas" (o 20 víctimas) en el código?

En misiones SAR reales, el dron busca a **una sola persona** (ej. un senderista perdido). El parámetro `num_lost_persons = 100` **NO** significa que haya un accidente masivo con 100 personas a la vez.

Significa que el ordenador va a ejecutar **100 simulaciones independientes** (100 "universos paralelos").

### El Método de Montecarlo (Paso a Paso)
Para evitar que los resultados sean fruto de la "buena o mala suerte" de una sola ejecución, usamos este método estadístico:

1.  **Universo 1:** El sistema "esconde" a la persona virtual en un punto del mapa. Este punto no es totalmente aleatorio; se elige utilizando el **Mapa de Calor (MAP)** (es más probable que caiga cerca de un camino o río).
2.  **Barrido:** El sistema comprueba si la ruta trazada por los drones pasa por encima del sensor visual de ese punto. Si pasa -> **Éxito**.
3.  **Universo 2:** El sistema borra a la persona anterior y genera un **nuevo escenario** escondiendo a una nueva persona en otro punto basado en el Heatmap. Se vuelve a comprobar el éxito.
4.  **Agregación:** Tras repetir esto 100 veces, el sistema cuenta los éxitos. Si de 100 universos independientes, la ruta pasó por encima de la persona en 72 ocasiones, la métrica **Victims Found %** será del **72%**.

Esta métrica representa la **robustez estadística** de la ruta.

---

## 2. Si hay 20 simulaciones, ¿por qué solo hay 1 ruta dibujada en los mapas?

La clave operativa de la simulación es que **el dron no es reactivo ni busca en tiempo real**. El dron ejecuta un plan de vuelo *offline* (planificado de antemano).

### La Lógica de Generación vs Evaluación:

1.  **Fase de Planificación (1 sola vez):**
    El algoritmo (ej. la Espiral) recibe el Mapa de Calor y el presupuesto de batería (ej. 450 km). Con esos datos matemáticos, el algoritmo dibuja el patrón de búsqueda óptimo. **Se genera un único dibujo (ruta)**. Ese es el dibujo que vemos en los PDFs y HTMLs interactivos.
2.  **Fase de Validación (Las 20/100 simulaciones):**
    Para comprobar si el dibujo que hemos generado es realmente bueno, dejamos esa ruta "congelada" sobre el mapa. Luego, lanzamos la simulación de Montecarlo. 
    *Tiramos a la persona 1... ¿La ruta congelada la pisa? Sí.*
    *Tiramos a la persona 2... ¿La ruta congelada la pisa? No.*

**Conclusión para la defensa:**
*"El mapa muestra la trayectoria pre-planificada óptima generada por el algoritmo. Para validar empíricamente su calidad, sometimos esa única ruta a 100 simulaciones de Montecarlo. El resultado demostró que esta trayectoria estática es capaz de interceptar al X% de las víctimas posibles según la distribución probabilística del entorno."*
