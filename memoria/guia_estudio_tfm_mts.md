# Guía de Estudio TFM: Funcionamiento Interno de MTS (Parte 1)

Este documento explica de forma detallada y con rigor académico el funcionamiento teórico y la arquitectura del framework **MTS (Minimum Time Search)**. Está pensado para que puedas estudiarlo y comprender cómo funciona el código original antes de explicarle a tus tutores los cambios que hemos hecho.

---

## 1. ¿Qué es el Framework MTS?

El framework **MTS (Minimum Time Search)** es un simulador desarrollado en Python diseñado para evaluar y comparar algoritmos de búsqueda de vehículos aéreos no tripulados (UAVs / drones) para localizar un objetivo (víctima) en un entorno de incertidumbre.

Su objetivo principal es encontrar una trayectoria de vuelo que **minimice el tiempo esperado (número de pasos)** necesario para que el sensor del dron detecte a la víctima.

---

## 2. El Modelo del Entorno (Mapa de Creencias o *Belief Map*)

El espacio de búsqueda se modela como una cuadrícula o rejilla bidimensional en la que cada celda $(i, j)$ tiene asociada una probabilidad de contener a la víctima. 

Esta matriz de probabilidad se conoce como **Mapa de Creencias (Belief Map)** o $\mathbf{BK}$.
*   La suma de todas las celdas del mapa siempre debe ser exactamente igual a $1.0$ (ya que asumimos que la víctima está en alguna parte del mapa):
    $$\sum_{i} \sum_{j} \mathbf{BK}(i, j) = 1.0$$
*   MTS original genera este mapa de forma sintética colocando "indicios" (clues) y aplicando una distribución Gaussiana alrededor de ellos. (Para tu TFM, hemos cambiado esto para cargar el mapa real de SAREnv).

---

## 3. El Modelo del Sensor (Detección Exponencial)

El dron vuela con un sensor apuntando al suelo. Este sensor no es perfecto: no detecta a la víctima de forma binaria (sí/no) al 100%, sino de forma probabilística. Esto se modela con la **Probabilidad de Detección (POD)**.

La probabilidad de que el sensor detecte a la víctima en una celda $(x_v, y_v)$ cuando el dron está en la posición $(x_d, y_d)$ decae exponencialmente con la distancia euclídea entre ambos:

$$P_D(d) = p_{d\text{max}} \cdot \exp\left( - \left(\frac{d}{\sigma}\right)^2 \right) \quad \text{si } d \le d_{\text{max}}$$

Donde:
*   $d$: Distancia euclídea entre el dron y la celda evaluada.
*   $p_{d\text{max}}$ (`pdmax`): Probabilidad máxima de detección si el dron vuela exactamente encima de la víctima.
*   $d_{\text{max}}$ (`dmax`): Rango máximo de alcance del sensor en celdas.
*   $\sigma$ (`sigma`): Sensibilidad o factor de caída exponencial. A mayor $\sigma$, el sensor es más tolerante a la distancia.

---

## 4. El Bucle de Búsqueda y Filtro Bayesiano (Paso a Paso)

En cada paso de tiempo de la simulación, el motor de MTS realiza de forma consecutiva las siguientes tareas:

### Paso A: Intento de Detección
El dron se encuentra en su coordenada actual $(x_d, y_d)$. El simulador comprueba de forma aleatoria (usando la probabilidad $P_D(d)$ del sensor) si el dron detecta a la víctima en este paso.
*   **Si la detecta:** La simulación finaliza con éxito. Se guarda el número de pasos y se detiene el bucle.
*   **Si NO la detecta:** El dron asume que la víctima no estaba en su rango de visión actual y procede a actualizar su Mapa de Creencias.

### Paso B: Actualización Bayesiana (Filtro de Información Negativa)
Como el sensor **no** ha detectado nada en las celdas barridas, la probabilidad de que la víctima esté en esas celdas **disminuye**. Por consiguiente, dado que la suma de probabilidades debe seguir siendo $1.0$, la probabilidad en las zonas no exploradas **aumenta**.

Matemáticamente, para cada celda $(i, j)$ del mapa, la creencia se actualiza usando el Teorema de Bayes:

$$\mathbf{BK}_{k+1}(i, j) = \frac{\mathbf{BK}_k(i, j) \cdot (1 - P_D(i, j))}{\sum_{u} \sum_{v} \mathbf{BK}_k(u, v) \cdot (1 - P_D(u, v))}$$

Donde $(1 - P_D(i, j))$ es la probabilidad de no detectar a la víctima en la celda $(i, j)$.

### Paso C: Movimiento del Objetivo (Convolución 2D)
Si la víctima se está moviendo (se configura una probabilidad de transición), el mapa de creencia debe "difuminarse" para reflejar la incertidumbre de hacia dónde ha podido caminar la víctima en este paso.

Esto se realiza mediante una **convolución bidimensional** de la matriz de creencia con una matriz de transición de movimiento (como un camino aleatorio o *Random Walk*):

$$\mathbf{BK}_{k+1} = \mathbf{BK}_{k+1} * \mathbf{M}_{\text{transición}}$$

*   *Efecto visual:* Las montañas de probabilidad se van haciendo más bajas y anchas a medida que pasa el tiempo si no se explotan, porque la víctima se mueve y su posición exacta se vuelve más incierta.

---

## 5. Algoritmos de Toma de Decisión (Cómo decide el dron dónde ir)

Una vez actualizado el Mapa de Creencias $\mathbf{BK}$, el dron debe decidir a cuál de sus celdas vecinas moverse en el siguiente paso. MTS implementa dos familias de algoritmos para tomar esta decisión:

### A. Búsqueda Voraz Heurística (`voraz-heur` / `rh_search`)
Es un algoritmo heurístico local que calcula una puntuación para cada uno de los 8 movimientos posibles del dron en el siguiente paso. El dron elige el movimiento con mayor puntuación.

La heurística de puntuación de una celda candidata $c$ combina tres factores:
1.  **Ganancia de Información Directa:** Cuánta probabilidad de creencia barremos por primera vez al mover el sensor a esa posición.
2.  **Atracción al Máximo Global:** Una penalización por distancia al punto del mapa que tiene la máxima probabilidad global, lo que actúa como una "gravedad" que arrastra al dron hacia las zonas más calientes del mapa:
    $$\text{Atracción} = \lambda \cdot \text{Distancia al Máximo}$$
3.  **Corrección de Miopía:** Penaliza volver a pasar por celdas visitadas recientemente para evitar bucles locales infinitos.

### B. Algoritmos de Optimización Global (Bioinspirados)
En lugar de tomar decisiones paso a paso (locales), los algoritmos bioinspirados buscan **optimizar la trayectoria completa** de 1000 pasos a la vez.

*   **ACO (Ant Colony Optimization):** Simula hormigas que recorren el mapa. Las rutas que detectan antes al objetivo se refuerzan con "feromonas". En las siguientes iteraciones, las hormigas siguen las feromonas y refinan la ruta hasta encontrar la trayectoria óptima.
*   **ABC (Artificial Bee Colony):** Simula abejas explorando fuentes de alimento (rutas candidatas). Las abejas obreras evalúan la calidad de la ruta y las observadoras eligen las mejores. Las rutas que no mejoran tras un número de intentos (`limit`) se descartan y se busca una nueva al azar.
*   **BHA (Black Hole Algorithm):** Genera una población de soluciones (estrellas) que son atraídas gravitacionalmente hacia la mejor solución histórica (el agujero negro). Las estrellas se actualizan en cada iteración y, si se acercan demasiado al agujero negro, son "absorbidas" y regeneradas para seguir explorando.
