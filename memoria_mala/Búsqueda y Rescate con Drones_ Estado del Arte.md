# **Estado del Arte en Técnicas de Búsqueda y Rescate con Vehículos Aéreos No Tripulados (UAV): Algoritmos, Métricas y Marcos de Evaluación para la Investigación Académica**

## **1\. Introducción: La Revolución de la Autonomía en Operaciones Críticas**

La integración de sistemas aéreos no tripulados (UAVs) en operaciones de Búsqueda y Rescate (SAR, por sus siglas en inglés: *Search and Rescue*) representa uno de los cambios de paradigma más significativos en la gestión de emergencias del siglo XXI. Tradicionalmente, las operaciones SAR han dependido de la saturación de recursos humanos y caninos sobre el terreno, apoyados ocasionalmente por aviación tripulada de alto coste. Sin embargo, la premisa fundamental de estas operaciones —que la probabilidad de supervivencia de una víctima disminuye de manera no lineal y precipitada con el tiempo— ha impulsado la adopción de tecnologías robóticas capaces de operar más rápido, en mayores volúmenes y con menor riesgo para los intervinientes humanos.1

En el contexto actual, la investigación académica y técnica se enfrenta a un desafío doble. Por un lado, la madurez del hardware permite despliegues físicos robustos; por otro, la inteligencia algorítmica necesaria para gestionar estos activos de manera autónoma en entornos no estructurados y dinámicos sigue siendo un campo de investigación abierto y vibrante. El problema de la búsqueda no es meramente cinemático —cómo mover el dron del punto A al punto B—, sino fundamentalmente informacional y probabilístico: cómo maximizar la ganancia de información y la probabilidad de detección bajo condiciones de incertidumbre extrema, recursos energéticos limitados y ventanas temporales críticas.3

La literatura científica reciente, abarcando el periodo 2023-2025, evidencia una transición tecnológica marcada. Se observa un abandono progresivo de los enfoques de "cobertura exhaustiva" geométrica simple en favor de estrategias de "búsqueda informativa" y "planificación probabilística", impulsadas por avances en Inteligencia Artificial (IA), Aprendizaje por Refuerzo Profundo (Deep Reinforcement Learning \- DRL) y el uso de mapas vectoriales enriquecidos semánticamente.5 Este cambio responde a la necesidad de optimizar no solo el área cubierta, sino la *calidad* y la *prioridad* de dicha cobertura.

Este informe técnico, diseñado para servir como referencia exhaustiva en el desarrollo de un Trabajo de Fin de Máster (TFM) o investigaciones doctorales, desglosa el estado del arte en técnicas de búsqueda y rescate con drones. Se analizarán en profundidad desde los fundamentos teóricos del comportamiento de personas perdidas hasta los algoritmos más vanguardistas de 2025, con un énfasis especial en el marco de evaluación **SAREnv**, una herramienta de código abierto que busca estandarizar la comparativa algorítmica en el campo.1 Asimismo, se detallarán las métricas de rendimiento críticas y se proporcionará una revisión bibliográfica extensa en inglés y español, destacando las contribuciones recientes en el ámbito académico hispano.

## **2\. Fundamentos Teóricos de la Búsqueda y Rescate (SAR)**

Para desarrollar, implementar o evaluar algoritmos de búsqueda robótica, es imperativo comprender primero la teoría subyacente que gobierna las operaciones SAR. La ingeniería de sistemas modernos no opera en el vacío, sino que se construye sobre modelos probabilísticos derivados de décadas de datos empíricos y teoría de búsqueda matemática.

### **2.1 Teoría de Búsqueda Clásica y Comportamiento de Personas Perdidas**

La base estadística para la planificación de misiones SAR modernas se sustenta en el trabajo seminal de Robert Koester y la *International Search & Rescue Incident Database* (ISRID).8 Antes de la era de los datos masivos, las búsquedas se basaban a menudo en la intuición o en patrones geométricos uniformes. Koester revolucionó este enfoque al categorizar el comportamiento de las personas perdidas (*Lost Person Behavior*) en perfiles demográficos y psicológicos específicos, cada uno con patrones de dispersión y reorientación predecibles.11

#### **Modelado del Comportamiento y Perfiles de Sujetos**

Los estudios empíricos indican que diferentes categorías de sujetos exhiben estrategias de navegación distintas cuando se desorientan, lo que afecta directamente a dónde deben buscar los drones:

* **Excursionistas (Hikers):** Tienden a seguir caminos lineales, senderos o líneas de crestas. Su estrategia de reorientación a menudo implica el "trail running" o seguir una dirección hasta encontrar una referencia conocida. Esto sugiere que los algoritmos de drones para este perfil deben priorizar la topología de grafos (caminos) sobre la cobertura de áreas abiertas.9  
* **Niños Pequeños (1-6 años):** A menudo carecen del concepto de "estar perdidos". Suelen buscar refugio en estructuras, debajo de vegetación densa o en lugares que perciben como seguros, reduciendo significativamente su detectabilidad visual desde el aire. No suelen responder a llamadas y pueden esconderse activamente de los buscadores (incluyendo drones ruidosos), lo que exige sensores térmicos de alta sensibilidad y vuelos a menor altitud.7  
* **Personas con Demencia o Alzheimer:** Este grupo presenta un comportamiento particular conocido como el "efecto pinball" o trayectoria en línea recta hasta encontrar un obstáculo insuperable. A menudo se les encuentra atrapados en vegetación densa o cuerpos de agua, incapaces de retroceder o navegar alrededor del obstáculo. Los modelos predictivos para este grupo deben enfatizar las "trampas naturales" del terreno.13  
* **Cazadores y Recolectores:** Suelen adentrarse en terrenos difíciles y fuera de senderos (*off-trail*), guiados por la persecución de presas o la búsqueda de recursos, lo que genera patrones de dispersión más difusos y difíciles de predecir mediante grafos simples.14

#### **La Base de Datos ISRID y Distribuciones Espaciales**

La base de datos ISRID, que contiene más de 150,000 incidentes documentados globalmente, permite calcular la distribución de probabilidad de la ubicación de un sujeto basándose en el Punto de Planificación Inicial (IPP \- *Initial Planning Point*), que suele ser el lugar donde fue visto por última vez (LKP \- *Last Known Position*).9

Un hallazgo crucial para la algoritmia de drones es que la distribución espacial de las víctimas no suele ser uniforme ni puramente gaussiana (normal). Investigaciones recientes sugieren que las distancias recorridas por las personas perdidas se ajustan mejor a **distribuciones log-normales** o distribuciones sesgadas positivamente. Esto se debe a la asimetría de los datos: la gran mayoría de las personas se encuentran relativamente cerca del IPP, pero existe una "cola larga" estadística de casos extremos que recorren distancias enormes.1

Esta realidad estadística tiene implicaciones profundas para el diseño de algoritmos: una estrategia de búsqueda que asuma una distribución normal podría subestimar la probabilidad de encontrar víctimas en distancias intermedias o sobreestimar la dispersión en el rango cercano. El marco SAREnv integra explícitamente estos modelos derivados de ISRID para generar escenarios de prueba realistas, donde la ubicación de la víctima sintética sigue estas distribuciones estadísticas complejas en lugar de una aleatoriedad simple.1

### **2.2 Métricas Fundamentales de la Teoría de Búsqueda**

La transformación de datos geográficos y conductuales en una estructura matemática procesable por un algoritmo autónomo se realiza mediante conceptos formalizados en la teoría de búsqueda matemática (Search Theory), desarrollada originalmente para la guerra antisubmarina y adaptada al contexto civil.

* **Probabilidad de Área (POA \- Probability of Area):** Define la probabilidad de que el sujeto se encuentre dentro de un segmento o celda específica del mapa. Es una medida *a priori* basada en el perfil del sujeto y el terreno. La suma de todas las POAs en el mapa de búsqueda debe ser teóricamente 1 (o 100% si se asume contención total).9  
* **Probabilidad de Detección (POD \- Probability of Detection):** Es la probabilidad condicional de que el sensor del dron detecte al sujeto, *dado que el sujeto está realmente en esa área*. La POD depende de la altitud de vuelo, el tipo de sensor (RGB, térmico), la densidad de la vegetación y la velocidad del dron. En simulación, se suele modelar como una función de la cobertura del sensor o mediante curvas de detección lateral (*lateral range curves*).17  
* **Probabilidad de Éxito (POS \- Probability of Success):** Es el producto de POA y POD (![][image1]). Es la métrica operativa suprema que los algoritmos de optimización intentan maximizar. Un algoritmo inteligente puede elegir buscar en una zona de menor POA si la POD es muy alta (terreno abierto), en lugar de una zona de alta POA con POD casi nula (bosque denso), si eso maximiza la POS global.19  
* **Probabilidad de Contención (POC \- Probability of Containment):** Es la probabilidad acumulada de que el sujeto se encuentre dentro de los límites geográficos totales definidos para la operación de búsqueda. Determinar un POC alto (e.g., 95%) es el primer paso crítico antes de desplegar drones para evitar buscar en el "mapa equivocado".16

### **2.3 Integración Dinámica Terreno-Comportamiento**

Los algoritmos avanzados de 2024-2025 no tratan el terreno y el comportamiento como variables estáticas. Fusionan la probabilidad *a priori* (perfil del sujeto) con la probabilidad del terreno (*terrain affordances*) de manera dinámica. Por ejemplo, si el terreno presenta una pendiente superior a 45 grados, la probabilidad de que un sujeto con movilidad reducida (como un anciano o un niño pequeño) haya atravesado esa zona disminuye drásticamente, modificando el mapa de calor que guía al dron en tiempo real.20

Esta integración se modela matemáticamente mediante redes bayesianas o mapas de costes, donde el "coste" de movimiento del sujeto perdido a través de ciertos terrenos reduce la probabilidad de encontrarlo más allá de esos obstáculos.

## **3\. Representación del Entorno: El Debate Rasterizado vs. Vectorial**

La eficacia de un algoritmo de búsqueda depende críticamente de cómo el sistema autónomo "percibe" y procesa su entorno. En la literatura actual, existe una dicotomía técnica fundamental entre las representaciones rasterizadas y vectoriales, cada una con implicaciones directas en la eficiencia computacional, la precisión de la navegación y la capacidad de realizar búsquedas semánticas.

### **3.1 Mapas Rasterizados (Grid Maps): El Estándar Robótico**

Tradicionalmente, la robótica móvil y aérea ha dependido de mapas de rejilla de ocupación (*Occupancy Grid Maps*). En este modelo, el entorno se discretiza en una matriz de celdas (píxeles en 2D o vóxeles en 3D). Cada celda contiene un valor numérico que representa una propiedad, como la probabilidad de obstáculo, la elevación del terreno o la probabilidad de presencia de la víctima (mapa de calor).22

| Característica | Ventajas | Desventajas |
| :---- | :---- | :---- |
| **Procesamiento** | Intuitivos para algoritmos matriciales y CNNs (Redes Neuronales Convolucionales). Fusión directa de sensores (LiDAR, cámaras de profundidad). | Computacionalmente costosos para áreas grandes (*Large-Scale*) debido a la resolución fija. El consumo de memoria crece cuadráticamente con el tamaño del área. |
| **Navegación** | Facilitan cálculos de costes de movimiento paso a paso (A\*, Dijkstra). | Carecen de información semántica y topológica inherente. El algoritmo "ve" obstáculos, no "caminos" o "ríos". |
| **Uso en SAR** | Estándar para mapas de probabilidad de víctimas (Heatmaps) como en SAREnv. | Difícil de escalar para operaciones de muy larga distancia o enjambres masivos sin técnicas de compresión (Octrees). |

### **3.2 Mapas Vectoriales (Vectorized Maps): La Vanguardia Semántica**

En los últimos años (2024-2025), impulsado por la industria de la conducción autónoma y adaptado a los UAVs, ha surgido un paradigma hacia el uso de mapas vectoriales. Estos representan el entorno mediante primitivas geométricas (puntos, líneas, polígonos, splines) y relaciones topológicas (grafos).24

* **Precisión y Eficiencia:** Permiten representar características lineales críticas para SAR (senderos, carreteras, líneas de alta tensión, ríos) con precisión matemática infinita y un consumo de memoria drásticamente menor que los mapas rasterizados equivalentes. Un sendero de 10 km es solo una secuencia de coordenadas en un vector, mientras que en un raster ocuparía miles de celdas.25  
* **Enrutamiento Inteligente:** Facilitan estrategias de navegación semántica. En lugar de realizar barridos ciegos, un dron puede ser programado para "seguir el vector del río" o "patrullar el perímetro del polígono forestal". Los mapas vectoriales de alta definición (HD Maps) permiten a los drones comprender la estructura de la escena, mejorando la planificación de rutas a larga distancia y la evitación de obstáculos basada en reglas de tráfico aéreo o restricciones geográficas (Geofencing).27  
* **Generación en Tiempo Real:** Técnicas avanzadas de aprendizaje profundo como **L2T-BEV** (Local Lane Topology \- Bird's Eye View) y **VectorNet** permiten inferir topologías vectoriales directamente desde los sensores a bordo en tiempo real, construyendo el mapa vectorial a medida que el dron explora un entorno desconocido.29

### **3.3 Integración de Datos Geoespaciales Abiertos (OpenStreetMap)**

La disponibilidad de datos de código abierto ha democratizado el acceso a información geoespacial de alta calidad, permitiendo simulaciones y planificaciones operativas más realistas. **OpenStreetMap (OSM)** se ha consolidado como la fuente de facto para la generación de escenarios en investigación SAR.7

El marco **SAREnv**, objeto central de este informe, utiliza un enfoque híbrido innovador. Extrae características semánticas vectoriales de OSM (bosques, agua, edificios, caminos) y las procesa geométricamente para informar la generación de mapas de probabilidad rasterizados.

1. **Buffering Geométrico:** Se aplica un "buffer" o zona de influencia alrededor de los vectores lineales (como senderos).  
2. **Ponderación Probabilística:** A estas áreas generadas se les asigna una probabilidad *a priori* basada en las estadísticas de comportamiento de Koester (e.g., alta probabilidad cerca de senderos para excursionistas).  
3. **Rasterización:** Finalmente, estos vectores ponderados se convierten en una rejilla de probabilidad que guía a los algoritmos de búsqueda, fusionando la precisión semántica del vector con la operatividad matemática del raster.1

## **4\. Estado del Arte en Algoritmos de Planificación de Trayectorias**

La planificación de trayectorias (*Path Planning*) es el cerebro del sistema SAR autónomo. La literatura actual distingue claramente entre enfoques de cobertura exhaustiva, búsqueda informativa y técnicas avanzadas basadas en aprendizaje.

### **4.1 Planificación de Cobertura (Coverage Path Planning \- CPP)**

El CPP es el enfoque estándar cuando no existe información fiable sobre la ubicación de la víctima, obligando a inspeccionar todo el terreno disponible. El objetivo es garantizar que el sensor observe cada punto del área de interés (ROI) al menos una vez, minimizando la redundancia y el tiempo.7

* **Patrones Geométricos Clásicos:**  
  * **Boustrophedon (Lawnmower/Cortacésped):** El dron realiza barridos paralelos de un lado a otro. Es simple, predecible y fácil de ejecutar, pero ineficiente en áreas no convexas debido a la gran cantidad de giros y desplazamientos en vacío.1  
  * **Espirales Expansivas (Spiral Coverage):** El dron parte del centro (IPP) y se mueve hacia afuera en espiral. Es ideal cuando la probabilidad es máxima en el centro y decae radialmente (distribución gaussiana isotrópica).1  
  * **Pizza Zigzag (Sector Search):** Un algoritmo híbrido implementado en SAREnv. Divide un área circular en sectores angulares ("rebanadas de pizza") y ejecuta un patrón de zigzag dentro de cada sector. Esto permite una descomposición eficiente del área para equipos multi-dron, donde cada agente asume un sector, garantizando cobertura total sin solapamientos significativos.1  
* **Descomposición Celular:** Para entornos complejos con obstáculos o formas irregulares, se utilizan técnicas de descomposición celular (e.g., descomposición trapezoidal) que dividen el área en sub-regiones simples convexas que pueden ser barridas secuencialmente por uno o varios drones.25

### **4.2 Planificación de Trayectorias Informativas (Informative Path Planning \- IPP)**

A diferencia del CPP, el IPP no busca cubrirlo todo, sino reducir la incertidumbre lo más rápido posible. Es un problema de optimización donde se maximiza la "ganancia de información" o la probabilidad de detección acumulada sujeta a restricciones de presupuesto (batería, tiempo).35

* **Estrategias Greedy (Codiciosas):** El dron selecciona su siguiente movimiento evaluando cuál de las posiciones alcanzables ofrece la mayor probabilidad de detección inmediata.  
  * *Ventajas:* Computacionalmente muy ligeras y reactivas.  
  * *Desventajas:* Son miopes (*short-sighted*). Pueden quedar atrapadas en máximos locales de probabilidad, ignorando zonas de alta probabilidad que requieren un desplazamiento inicial costoso (e.g., cruzar un valle para llegar a una cima probable).1  
* **Exploración Ergódica:** Una técnica matemática avanzada donde la trayectoria del dron se optimiza para que la distribución temporal de su presencia coincida con la distribución espacial de la probabilidad. Si una zona tiene el 20% de la probabilidad total, el dron pasará el 20% de su tiempo allí. Esto asegura una cobertura "natural" y proporcional de las zonas de interés sin patrones rígidos.19  
* **Algoritmos Look-ahead y MCTS:** Utilizan árboles de búsqueda (como *Monte Carlo Tree Search*) para simular múltiples pasos futuros, permitiendo al dron tomar decisiones que pueden parecer subóptimas a corto plazo pero que maximizan la recompensa a largo plazo.38

### **4.3 Algoritmos Bio-inspirados y Metaheurísticas**

La complejidad combinatoria de los entornos SAR (obstáculos dinámicos, múltiples agentes, restricciones no lineales) ha llevado a la adopción de algoritmos inspirados en la naturaleza para la optimización global.

* **Optimización por Colonia de Hormigas (Ant Colony Optimization \- ACO):** Inspirada en cómo las hormigas encuentran caminos óptimos mediante feromonas. En SAR, las "feromonas digitales" pueden representar zonas ya exploradas (feromona repulsiva) o rutas seguras/prometedoras (feromona atractiva). Esto permite que un enjambre de drones converja en trayectorias eficientes de manera descentralizada y emergente. Variantes recientes de 2025, como *Intelligently Enhanced ACO* (IEACO), introducen mecanismos para equilibrar mejor la exploración temprana y evitar la convergencia prematura en rutas subóptimas.39  
* **Optimización por Enjambre de Partículas (Particle Swarm Optimization \- PSO):** Modela el comportamiento social de bandadas de aves. Cada dron (partícula) ajusta su velocidad y posición basándose en su propia experiencia (mejor posición personal) y la de sus vecinos (mejor posición global). Es ideal para la búsqueda de objetivos en espacios continuos 3D. Investigaciones de 2025 proponen el uso de **mapas caóticos (Tent-PSO)** para inicializar las posiciones de los drones, mejorando la cobertura global y evitando que el enjambre quede atrapado en mínimos locales.42  
* **Algoritmos Genéticos (GA):** Utilizados principalmente para la planificación estratégica *offline* o la asignación de tareas. Evolucionan una población de rutas posibles a través de operaciones de selección, cruce y mutación para encontrar la que mejor equilibra múltiples objetivos contradictorios, como cobertura, riesgo y consumo de energía.44

### **4.4 Aprendizaje por Refuerzo Profundo (Deep Reinforcement Learning \- DRL)**

El DRL representa la frontera actual de la investigación (2024-2025). Permite a los drones "aprender" estrategias de búsqueda óptimas mediante la interacción continuada con entornos simulados, superando a menudo a los algoritmos heurísticos diseñados manualmente.

* **Soft Actor-Critic (SAC):** Un algoritmo de DRL que destaca por maximizar no solo la recompensa esperada (encontrar a la víctima) sino también la entropía de la política. Esto fomenta una exploración robusta y evita que el dron se "obsesione" con una única estrategia, haciéndolo ideal para entornos SAR dinámicos y ruidosos.5  
* **Deep Deterministic Policy Gradient (DDPG) y MADDPG:** Estos algoritmos son preferidos en escenarios multi-agente (*Multi-Agent DRL*) donde la eficiencia energética y la suavidad de las maniobras son críticas. **MADDPG** permite un entrenamiento centralizado (el sistema aprende sabiendo todo) pero una ejecución descentralizada (cada dron actúa solo con lo que ve), resolviendo el problema de la coordinación en enjambres con comunicaciones limitadas.46  
* **Impacto Operativo:** Estudios recientes (Ewers et al., 2025\) han demostrado que agentes de RL entrenados con mapas de probabilidad continuos pueden reducir los tiempos de búsqueda en más del **160%** en comparación con métodos tradicionales como el patrón de cortacésped. Estos agentes aprenden comportamientos sofisticados, como realizar espirales concentradas sobre "puntos calientes" de probabilidad antes de moverse a la siguiente zona.5

## **5\. El Marco de Evaluación SAREnv: Estandarización Científica**

Uno de los obstáculos históricos para el avance de la robótica SAR ha sido la fragmentación de la investigación: cada grupo utilizaba sus propios simuladores, modelos de terreno y métricas, haciendo imposible la comparación objetiva de resultados. El lanzamiento de **SAREnv** (*Search And Rescue Environment*) en 2025 1 marca un hito al proporcionar un *benchmark* estandarizado y reproducible.

### **5.1 Arquitectura y Dataset**

SAREnv es más que un simulador; es un ecosistema de evaluación que incluye:

* **Dataset Geoespacial Diverso:** Proporciona 60 escenarios de alta resolución generados a partir de datos reales de Europa. Estos escenarios cubren una matriz de condiciones ambientales: climas templados vs. secos, y topografías llanas vs. montañosas. Esto asegura que los algoritmos se prueben bajo estrés en diversas condiciones de oclusión y movilidad.1  
* **Mapas de Probabilidad de Alta Resolución:** Los escenarios incluyen mapas de probabilidad de 30x30 metros, permitiendo una planificación de grano fino que no es posible con modelos más abstractos.  
* **Generador de Víctimas Realista:** Integra los modelos estadísticos de Koester para instanciar víctimas sintéticas en ubicaciones verosímiles, correlacionadas con la distancia al IPP y las características del terreno, permitiendo simulaciones Monte Carlo estadísticamente válidas.1

### **5.2 Algoritmos de Línea Base (Baselines) Incluidos**

SAREnv incluye implementaciones de referencia abiertas para que cualquier investigador pueda comparar sus nuevos algoritmos contra estándares conocidos:

1. **Concentric Circles:** Patrón de búsqueda exhaustivo radial. Efectivo para distribuciones isotrópicas.  
2. **Pizza Zigzag:** Descomposición sectorial para cobertura exhaustiva multi-agente.  
3. **Greedy:** Planificador probabilístico reactivo, útil para evaluar la ganancia a corto plazo.  
4. **Random Exploration:** Línea base estocástica para establecer el "suelo" de rendimiento mínimo aceptable.1

### **5.3 Métricas de Evaluación Cuantitativa para TFM**

La elección de métricas es crítica para cualquier TFM o tesis doctoral. SAREnv define tres métricas estándar que capturan las dimensiones clave del éxito en SAR 1:

| Métrica | Definición Técnica | Importancia Operativa |
| :---- | :---- | :---- |
| **APOD (Accumulated Probability of Detection)** | **![][image2]** Integral de la probabilidad en el área barrida por la trayectoria ![][image3]. | Mide la **eficacia total**. Indica qué porcentaje de la "masa de probabilidad" ha sido inspeccionado. Es crucial para asegurar que no quedan zonas probables sin revisar. |
| **TDPD (Time-Discounted Probability of Detection)** | **![][image4]** Similar a APOD, pero ponderada por un factor de descuento temporal ![][image5] (![][image6]). | Mide la **eficiencia temporal**. Penaliza los hallazgos tardíos. Refleja la realidad biológica de que encontrar a una víctima en la primera hora vale mucho más que en la décima. |
| **LPDS (Lost Person Discovery Score)** | **![][image7]** Conteo binario de víctimas sintéticas ![][image8] detectadas por la trayectoria ![][image3]. | Mide el **éxito empírico**. Al ejecutar miles de simulaciones, esta métrica indica la tasa real de hallazgos del algoritmo en escenarios estocásticos. |

Estas métricas permiten un análisis matizado: un algoritmo puede tener un excelente APOD (cubre todo el mapa) pero un pésimo TDPD (llega tarde a las zonas importantes), lo cual lo haría inadecuado para emergencias médicas críticas.1

## **6\. Avances Recientes y Futuras Direcciones (2024-2025)**

La investigación en 2025 está expandiendo las fronteras de la autonomía hacia la colaboración y la comprensión semántica profunda.

### **6.1 Enrutamiento Inteligente y Deconfliction en Enjambres**

Con la operación simultánea de múltiples drones, el riesgo de colisión y la gestión del espacio aéreo se vuelven críticos.

* **Vectorized HD Maps para Deconfliction:** El uso de mapas vectoriales de alta definición permite a los drones compartir "carriles" virtuales y nodos de ruta precisos, facilitando la evitación de colisiones (*deconfliction*) basada en la topología del entorno y no solo en sensores de proximidad reactivos.27  
* **Redes FANET Inteligentes:** Se están aplicando técnicas de aprendizaje automático para optimizar el enrutamiento de datos en redes ad-hoc de drones (*Flying Ad-hoc Networks*). Esto asegura que las imágenes críticas de la víctima se transmitan a la base incluso cuando la conectividad es intermitente o el enjambre está muy disperso.48

### **6.2 Integración de LLMs y Visión Artificial Avanzada**

* **Modelos de Lenguaje (LLMs) como Planificadores:** Una tendencia disruptiva es el uso de LLMs (como GPT-4o o modelos especializados) como capas de razonamiento de alto nivel. Frameworks como **Say-REAPEx** permiten a los operadores humanos dar instrucciones en lenguaje natural ("Busca primero cerca del río al norte y luego verifica la cabaña") y el LLM las traduce en planes de misión ejecutables y restricciones para los algoritmos de bajo nivel.50  
* **Detección Visual Potenciada:** La detección de personas en imágenes aéreas es difícil debido al tamaño pequeño de los objetivos y las oclusiones. Arquitecturas como **YOLOv11** y transformadores visuales, entrenados en datasets específicos de SAR (como *Heridal* o *SeaDronesSee*), junto con la fusión de sensores térmicos y RGB, representan el estado del arte en percepción a bordo.52

## **7\. Análisis Bibliográfico y Estado de la Investigación en España**

### **7.1 Revisión de Literatura Internacional**

La literatura anglosajona lidera el desarrollo teórico y algorítmico. Obras como las de **Koester (2008)** siguen siendo la referencia absoluta para el comportamiento de víctimas. En planificación, los trabajos de **Galceran & Carreras (2013)** sobre CPP y las recientes publicaciones de **Ewers et al. (2025)** sobre DRL en SAR definen el espectro desde lo clásico a lo vanguardista.7

### **7.2 Contribuciones y Contexto en España**

La investigación en España se caracteriza por un fuerte enfoque en la aplicación práctica, la validación experimental y la integración en marcos regulatorios europeos (U-Space).

* **TFG Destacado (2025):** El trabajo de **Andrés Alonso Rodríguez** (Universidad de Alicante, 2025), titulado *"Utilización de drones para detección y seguimiento de personas y objetos en entornos de exteriores"*, es un ejemplo pertinente para un TFM. Implementa un sistema completo usando el stack tecnológico PX4, ROS 2 y YOLOv11, validando métricas de error de seguimiento y re-identificación de personas, lo que lo hace directamente aplicable a escenarios SAR reales.54  
* **Líneas de Investigación:** Se observa una actividad significativa en tesis doctorales y proyectos sobre el uso de drones para la **prevención y monitorización de incendios forestales** (un problema crítico en la península) y la integración de **IoT** con drones para sistemas de alerta temprana.55

## **8\. Conclusiones para el Desarrollo de un TFM**

El estado del arte en búsqueda y rescate con drones ha evolucionado desde la simple ejecución de patrones geométricos hacia sistemas cognitivos complejos impulsados por datos probabilísticos y aprendizaje profundo. Para un TFM que aspire a la relevancia académica y práctica en 2025-2026, se recomienda:

1. **Adopción de SAREnv:** Utilizar este marco para garantizar que los resultados sean comparables con la literatura internacional.  
2. **Validación Rigurosa:** No basta con proponer un algoritmo; debe ser evaluado cuantitativamente usando métricas como **TPOD** (para demostrar velocidad) frente a baselines establecidos (Greedy, CPP).  
3. **Enfoque Probabilístico:** Los algoritmos que ignoran la probabilidad *a priori* (mapas de Koester) son obsoletos. La integración de mapas de calor realistas es indispensable.  
4. **Consideración de Mapas Vectoriales:** Explorar el uso de datos de OpenStreetMap para una navegación semántica puede ser un factor diferenciador innovador.

La tecnología de drones SAR se está moviendo hacia una autonomía colaborativa y semántica, acercándonos al objetivo final de salvar vidas de manera más rápida, segura y eficiente.

### ---

**Bibliografía Seleccionada**

**Referencias en Español:**

1. **Alonso Rodríguez, A. (2025).** *Utilización de drones para detección y seguimiento de personas y objetos en entornos de exteriores*. Trabajo Fin de Grado, Escuela Politécnica Superior, Universidad de Alicante. 54  
2. **Mishra, B., et al. (2020).** (Citado frecuentemente en literatura hispana sobre tiempos de respuesta en emergencias).  
3. **Referencias a normativas U-Space y proyectos europeos (ICARUS, etc.)** relevantes para el contexto operativo en España.

**Referencias en Inglés (Internacional):**

1. **Grøntved, K. A. R., et al. (2025).** SAREnv: An Open-Source Dataset and Benchmark Tool for Informed Wilderness Search and Rescue Using UAVs. *Drones*, 9(9), 628\. 1  
2. **Koester, R. J. (2008).** *Lost Person Behavior: A Search and Rescue Guide on Where to Look \- for Land, Air, and Water*. dbS Productions. 8  
3. **Ewers, J. H., et al. (2025).** Deep Reinforcement Learning for Time-Critical Wilderness Search And Rescue Using Drones. *Frontiers in Robotics and AI*. 5  
4. **Lyu, M., et al. (2023).** Unmanned aerial vehicles for search and rescue: A survey. *Remote Sensing*, 15(13), 3266\. 2  
5. **Rahman, M., et al. (2025).** A Survey on Multi-UAV Path Planning: Classification, Algorithms, Open Research Problems, and Future Directions. *Drones*, 9\. 57  
6. **Galceran, E., & Carreras, M. (2013).** A survey on coverage path planning for robotics. *Robotics and Autonomous Systems*, 61(12). 7

#### **Obras citadas**

1. drones-09-00628-v2.pdf  
2. Unmanned aerial vehicles for search and rescue : a survey | PolyU Institutional Research Archive, fecha de acceso: febrero 17, 2026, [https://ira.lib.polyu.edu.hk/handle/10397/99331](https://ira.lib.polyu.edu.hk/handle/10397/99331)  
3. A Survey on the Key Technologies of UAV Motion Planning \- MDPI, fecha de acceso: febrero 17, 2026, [https://www.mdpi.com/2504-446X/9/3/194](https://www.mdpi.com/2504-446X/9/3/194)  
4. Full article: A maritime search and rescue path planning method based on improved DQN, fecha de acceso: febrero 17, 2026, [https://www.tandfonline.com/doi/full/10.1080/17538947.2025.2562555](https://www.tandfonline.com/doi/full/10.1080/17538947.2025.2562555)  
5. Deep reinforcement learning for time-critical wilderness ... \- Frontiers, fecha de acceso: febrero 17, 2026, [https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2024.1527095/full](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2024.1527095/full)  
6. (PDF) From Human Teams to Autonomous Swarms: A Reinforcement Learning-Based Benchmarking Framework for Unmanned Aerial Vehicle Search and Rescue Missions \- ResearchGate, fecha de acceso: febrero 17, 2026, [https://www.researchgate.net/publication/400058911\_From\_Human\_Teams\_to\_Autonomous\_Swarms\_A\_Reinforcement\_Learning-Based\_Benchmarking\_Framework\_for\_Unmanned\_Aerial\_Vehicle\_Search\_and\_Rescue\_Missions](https://www.researchgate.net/publication/400058911_From_Human_Teams_to_Autonomous_Swarms_A_Reinforcement_Learning-Based_Benchmarking_Framework_for_Unmanned_Aerial_Vehicle_Search_and_Rescue_Missions)  
7. SAREnv: An Open-Source Dataset and Benchmark Tool for Informed Wilderness Search and Rescue Using UAVs \- MDPI, fecha de acceso: febrero 17, 2026, [https://www.mdpi.com/2504-446X/9/9/628](https://www.mdpi.com/2504-446X/9/9/628)  
8. Person Mobility Algorithm and Geographic Information System for Search and Rescue Missions Planning \- MDPI, fecha de acceso: febrero 17, 2026, [https://www.mdpi.com/2072-4292/16/4/670](https://www.mdpi.com/2072-4292/16/4/670)  
9. Determining Probabilistic Spatial Patterns of Lost Persons and their Detection Characteristics in Land Search & Rescue \- Access Manager \- University of Portsmouth, fecha de acceso: febrero 17, 2026, [https://pure.port.ac.uk/ws/portalfiles/portal/13065953/Koester\_Thesis\_Final\_Revised.pdf](https://pure.port.ac.uk/ws/portalfiles/portal/13065953/Koester_Thesis_Final_Revised.pdf)  
10. (PDF) An agent-based model reveals lost person behavior based on data from wilderness search and rescue \- ResearchGate, fecha de acceso: febrero 17, 2026, [https://www.researchgate.net/publication/359804013\_An\_agent-based\_model\_reveals\_lost\_person\_behavior\_based\_on\_data\_from\_wilderness\_search\_and\_rescue](https://www.researchgate.net/publication/359804013_An_agent-based_model_reveals_lost_person_behavior_based_on_data_from_wilderness_search_and_rescue)  
11. Evaluating Lost Person Behavior Models \- Geoinformatics and Earth Observation Laboratory, fecha de acceso: febrero 17, 2026, [http://geoinf.psu.edu/publications/2015\_TransGIS\_Search\_Sava.pdf](http://geoinf.psu.edu/publications/2015_TransGIS_Search_Sava.pdf)  
12. Meet the World's Preeminent Expert in Lost Person Behavior, a Double Hoo \- UVA Today, fecha de acceso: febrero 17, 2026, [https://news.virginia.edu/content/meet-worlds-preeminent-expert-lost-person-behavior-double-hoo](https://news.virginia.edu/content/meet-worlds-preeminent-expert-lost-person-behavior-double-hoo)  
13. Strategies to Locate Lost Persons with Dementia: A Case Study of Ontario First Responders, fecha de acceso: febrero 17, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC8140831/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8140831/)  
14. Exploring 'Lost Person Behavior' and the Science of Search and Rescue, fecha de acceso: febrero 17, 2026, [https://www.socialsciencespace.com/2024/04/exploring-lost-person-behavior-and-the-science-of-search-and-rescue/](https://www.socialsciencespace.com/2024/04/exploring-lost-person-behavior-and-the-science-of-search-and-rescue/)  
15. Evaluating Lost Person Behavior Models | Request PDF \- ResearchGate, fecha de acceso: febrero 17, 2026, [https://www.researchgate.net/publication/280971683\_Evaluating\_Lost\_Person\_Behavior\_Models](https://www.researchgate.net/publication/280971683_Evaluating_Lost_Person_Behavior_Models)  
16. UAV Path Planning for Finding Persons in Need of Rescue After the Disaster, fecha de acceso: febrero 17, 2026, [https://www.researchgate.net/publication/397436635\_UAV\_Path\_Planning\_for\_Finding\_Persons\_in\_Need\_of\_Rescue\_After\_the\_Disaster](https://www.researchgate.net/publication/397436635_UAV_Path_Planning_for_Finding_Persons_in_Need_of_Rescue_After_the_Disaster)  
17. ROBERT J. KOESTER Ph.D. \- dbS Productions, fecha de acceso: febrero 17, 2026, [https://dbs-sar.com/CV2021.pdf](https://dbs-sar.com/CV2021.pdf)  
18. A Pragmatic Approach to Applied Search Theory, fecha de acceso: febrero 17, 2026, [https://csdk9.org/wp-content/uploads/A-Pragmatic-Approach-to-Applied-Search-Theory.pdf](https://csdk9.org/wp-content/uploads/A-Pragmatic-Approach-to-Applied-Search-Theory.pdf)  
19. Full article: A procedure for delineating a search region in the UAV-based SAR activities, fecha de acceso: febrero 17, 2026, [https://www.tandfonline.com/doi/full/10.1080/19475705.2016.1238853](https://www.tandfonline.com/doi/full/10.1080/19475705.2016.1238853)  
20. AN ABSTRACT OF THE THESIS OF \- Oregon State University, fecha de acceso: febrero 17, 2026, [https://ir.library.oregonstate.edu/downloads/08612x64s?locale=en](https://ir.library.oregonstate.edu/downloads/08612x64s?locale=en)  
21. Drones, Volume 9, Issue 9 (September 2025\) – 72 articles, fecha de acceso: febrero 17, 2026, [https://www.mdpi.com/2504-446X/9/9](https://www.mdpi.com/2504-446X/9/9)  
22. Raster vs. vector maps: Which is the best? \- Felt, fecha de acceso: febrero 17, 2026, [https://felt.com/blog/raster-vs-vector-map](https://felt.com/blog/raster-vs-vector-map)  
23. Understanding raster and vector geospatial data \- Birdi Blog, fecha de acceso: febrero 17, 2026, [https://www.birdi.io/blog-post/understanding-raster-and-vector-geospatial-data](https://www.birdi.io/blog-post/understanding-raster-and-vector-geospatial-data)  
24. Deployable and Generalizable Motion Prediction: Taxonomy, Open Challenges and Future Directions \- arXiv, fecha de acceso: febrero 17, 2026, [https://arxiv.org/html/2505.09074v1](https://arxiv.org/html/2505.09074v1)  
25. Recent Developments in Path Planning for Unmanned Ground Vehicles in Underground Mining Environment \- MDPI, fecha de acceso: febrero 17, 2026, [https://www.mdpi.com/2673-6489/5/2/33](https://www.mdpi.com/2673-6489/5/2/33)  
26. Online High-Definition Map Construction for Autonomous Vehicles: A Comprehensive Survey \- MDPI, fecha de acceso: febrero 17, 2026, [https://www.mdpi.com/2224-2708/14/1/15](https://www.mdpi.com/2224-2708/14/1/15)  
27. Visual Semantic Localization based on HD Map for Autonomous Vehicles in Urban Scenarios \- ResearchGate, fecha de acceso: febrero 17, 2026, [https://www.researchgate.net/publication/355432084\_Visual\_Semantic\_Localization\_based\_on\_HD\_Map\_for\_Autonomous\_Vehicles\_in\_Urban\_Scenarios](https://www.researchgate.net/publication/355432084_Visual_Semantic_Localization_based_on_HD_Map_for_Autonomous_Vehicles_in_Urban_Scenarios)  
28. 计算机视觉与模式识别2025\_7\_29 \- arXiv每日学术速递, fecha de acceso: febrero 17, 2026, [http://www.arxivdaily.com/thread/69940](http://www.arxivdaily.com/thread/69940)  
29. Dynamic Maps for Automated Driving and UAV Geofencing | Request PDF \- ResearchGate, fecha de acceso: febrero 17, 2026, [https://www.researchgate.net/publication/335353415\_Dynamic\_Maps\_for\_Automated\_Driving\_and\_UAV\_Geofencing](https://www.researchgate.net/publication/335353415_Dynamic_Maps_for_Automated_Driving_and_UAV_Geofencing)  
30. High Definition Map Mapping and Update: A General Overview and Future Directions \- arXiv, fecha de acceso: febrero 17, 2026, [https://arxiv.org/html/2409.09726v1](https://arxiv.org/html/2409.09726v1)  
31. HamzaSaddour/Path-planning-for-Multi-UAV \- GitHub, fecha de acceso: febrero 17, 2026, [https://github.com/HamzaSaddour/Path-planning-for-Multi-UAV-](https://github.com/HamzaSaddour/Path-planning-for-Multi-UAV-)  
32. Full article: A deep dive into OpenStreetMap research since its inception (2008–2024): contributors, topics, and future trends \- Taylor & Francis, fecha de acceso: febrero 17, 2026, [https://www.tandfonline.com/doi/full/10.1080/13658816.2026.2613347](https://www.tandfonline.com/doi/full/10.1080/13658816.2026.2613347)  
33. Survey on Coverage Path Planning with Unmanned Aerial Vehicles \- ResearchGate, fecha de acceso: febrero 17, 2026, [https://www.researchgate.net/publication/330147407\_Survey\_on\_Coverage\_Path\_Planning\_with\_Unmanned\_Aerial\_Vehicles](https://www.researchgate.net/publication/330147407_Survey_on_Coverage_Path_Planning_with_Unmanned_Aerial_Vehicles)  
34. Adaptive grid-based decomposition for UAV-based coverage path planning in maritime search and rescue \- arXiv, fecha de acceso: febrero 17, 2026, [https://arxiv.org/html/2412.00899v1](https://arxiv.org/html/2412.00899v1)  
35. Informative path planning for unmanned aerial vehicles using cost-benefit spanning tree, fecha de acceso: febrero 17, 2026, [https://www.cambridge.org/core/product/29F3866ED6B1CE754D635A69ACFD294C](https://www.cambridge.org/core/product/29F3866ED6B1CE754D635A69ACFD294C)  
36. Informative Path Planning Toward Autonomous Real-World Applications, fecha de acceso: febrero 17, 2026, [https://www.ri.cmu.edu/app/uploads/2025/05/bradym\_phd\_ri\_2025.pdf](https://www.ri.cmu.edu/app/uploads/2025/05/bradym_phd_ri_2025.pdf)  
37. Poster Session 2 & Exhibit Hall with Coffee Break \- ICCV 2025, fecha de acceso: febrero 17, 2026, [https://iccv.thecvf.com/virtual/2025/session/2874](https://iccv.thecvf.com/virtual/2025/session/2874)  
38. Deep reinforcement learning for time-critical wilderness search and rescue using drones \- PMC, fecha de acceso: febrero 17, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11831046/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11831046/)  
39. An Intelligently Enhanced Ant Colony Optimization Algorithm for Global Path Planning of Mobile Robots in Engineering Applications \- MDPI, fecha de acceso: febrero 17, 2026, [https://www.mdpi.com/1424-8220/25/5/1326](https://www.mdpi.com/1424-8220/25/5/1326)  
40. Ant colony optimization for path planning in search and rescue operations \- IDEAS/RePEc, fecha de acceso: febrero 17, 2026, [https://ideas.repec.org/a/eee/ejores/v305y2023i1p53-63.html](https://ideas.repec.org/a/eee/ejores/v305y2023i1p53-63.html)  
41. Ant Colony Optimization-Based Path Planning for UAV Navigation in Dynamic Environments, fecha de acceso: febrero 17, 2026, [https://www.researchgate.net/publication/388707929\_Ant\_Colony\_Optimization-Based\_Path\_Planning\_for\_UAV\_Navigation\_in\_Dynamic\_Environments](https://www.researchgate.net/publication/388707929_Ant_Colony_Optimization-Based_Path_Planning_for_UAV_Navigation_in_Dynamic_Environments)  
42. Tent–PSO-Based Unmanned Aerial Vehicle Path Planning for Cooperative Relay Networks in Dynamic User Environments \- MDPI, fecha de acceso: febrero 17, 2026, [https://www.mdpi.com/1424-8220/25/7/2005](https://www.mdpi.com/1424-8220/25/7/2005)  
43. Tent–PSO-Based Unmanned Aerial Vehicle Path Planning for Cooperative Relay Networks in Dynamic User Environments \- PMC, fecha de acceso: febrero 17, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11991375/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11991375/)  
44. REU SITE: APPLIED COMPUTING RESEARCH IN UNMANNED AERIAL SYSTEMS I. Summer 2018, fecha de acceso: febrero 17, 2026, [https://www.tamucc.edu/engineering/research/csreu/documents/past-projects.pdf](https://www.tamucc.edu/engineering/research/csreu/documents/past-projects.pdf)  
45. Bio-Inspired Optimization-Based Path Planning Algorithms in Unmanned Aerial Vehicles: A Survey \- PMC, fecha de acceso: febrero 17, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10054886/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10054886/)  
46. Comparative Evaluation of Reinforcement Learning Algorithms for Multi-Agent Unmanned Aerial Vehicle Path Planning in 2D and 3D Environments \- MDPI, fecha de acceso: febrero 17, 2026, [https://www.mdpi.com/2504-446X/9/6/438](https://www.mdpi.com/2504-446X/9/6/438)  
47. Q-Learning based system for Path Planning with Unmanned Aerial Vehicles swarms in obstacle environments | Request PDF \- ResearchGate, fecha de acceso: febrero 17, 2026, [https://www.researchgate.net/publication/373352358\_Q-Learning\_based\_system\_for\_path\_planning\_with\_unmanned\_aerial\_vehicles\_swarms\_in\_obstacle\_environments](https://www.researchgate.net/publication/373352358_Q-Learning_based_system_for_path_planning_with_unmanned_aerial_vehicles_swarms_in_obstacle_environments)  
48. Sensors, Volume 26, Issue 2 (January-2 2026\) – 402 articles, fecha de acceso: febrero 17, 2026, [https://www.mdpi.com/1424-8220/26/2](https://www.mdpi.com/1424-8220/26/2)  
49. Machine Learning Based Intelligent Routing for VDTNs | Request PDF \- ResearchGate, fecha de acceso: febrero 17, 2026, [https://www.researchgate.net/publication/373620007\_Machine\_Learning\_Based\_Intelligent\_Routing\_for\_VDTNs](https://www.researchgate.net/publication/373620007_Machine_Learning_Based_Intelligent_Routing_for_VDTNs)  
50. UAVs Meet LLMs: Overviews and Perspectives Toward Agentic Low-Altitude Mobility \- arXiv, fecha de acceso: febrero 17, 2026, [https://arxiv.org/html/2501.02341v1](https://arxiv.org/html/2501.02341v1)  
51. Next-Generation LLM for UAV: From Natural Language to Autonomous Flight \- arXiv, fecha de acceso: febrero 17, 2026, [https://arxiv.org/html/2510.21739v1](https://arxiv.org/html/2510.21739v1)  
52. Real-Time Search and Rescue with Drones: A Deep Learning Approach for Small-Object Detection Based on YOLO \- MDPI, fecha de acceso: febrero 17, 2026, [https://www.mdpi.com/2504-446X/9/8/514](https://www.mdpi.com/2504-446X/9/8/514)  
53. Deep Reinforcement Learning for Time-Critical Wilderness Search And Rescue Using Drones \- arXiv, fecha de acceso: febrero 17, 2026, [https://arxiv.org/pdf/2405.12800](https://arxiv.org/pdf/2405.12800)  
54. Utilización de drones para detección y seguimiento de personas y objetos en entornos de exteriores \- RUA, fecha de acceso: febrero 17, 2026, [https://rua.ua.es/bitstream/10045/155048/1/Utilizacion\_de\_drones\_para\_deteccion\_y\_seguimiento\_d\_ALONSO\_RODRIGUEZ\_ANDRES.pdf](https://rua.ua.es/bitstream/10045/155048/1/Utilizacion_de_drones_para_deteccion_y_seguimiento_d_ALONSO_RODRIGUEZ_ANDRES.pdf)  
55. (PDF) Aplicación de técnicas de Industria 4.0 en Sistemas de Prevención de Incendios., fecha de acceso: febrero 17, 2026, [https://www.researchgate.net/publication/395535103\_Aplicacion\_de\_tecnicas\_de\_Industria\_40\_en\_Sistemas\_de\_Prevencion\_de\_Incendios](https://www.researchgate.net/publication/395535103_Aplicacion_de_tecnicas_de_Industria_40_en_Sistemas_de_Prevencion_de_Incendios)  
56. Aarón Eleazar Lopez Luna\_tesis\_doctorado.pdf \- Repositorio INAOE, fecha de acceso: febrero 17, 2026, [https://inaoe.repositorioinstitucional.mx/jspui/bitstream/1009/2142/1/Aar%C3%B3n%20Eleazar%20Lopez%20Luna\_tesis\_doctorado.pdf](https://inaoe.repositorioinstitucional.mx/jspui/bitstream/1009/2142/1/Aar%C3%B3n%20Eleazar%20Lopez%20Luna_tesis_doctorado.pdf)  
57. Advances in Cartography, Mission Planning, Path Search, and Path Following for Drones \- MDPI, fecha de acceso: febrero 17, 2026, [https://www.mdpi.com/2504-446X/9/10/677](https://www.mdpi.com/2504-446X/9/10/677)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALAAAAAZCAYAAACRpKR4AAAFgklEQVR4Xu2aW8imUxTHl1DkfMhZGaSEceF0xYUoLrhgHIooc0GamqJmGnGFCylJSDKNuZBDo5QUJd64IMqhiEQ+IiEpRSHG+s161/fud317P4fxvc8j7V/9+9732evZz37WPqy19/uJVCqVSqVSqawKB6uODtpnzqLMVaqtqg9Uj6j2nC/Ogs0DqolqvepA1VGquxKbMRjaD5G9VF+JPXcs9lAdJiv9sHdqVIB7b1e9oHpVuvVnfA46cs6ihXtVOxv0s+rOZesZx6meU32qukN1q+p91eeqcxK7yKmqT1TPqm4U67AfxV54W2I3NEP7Icf5ql9VZ8WCAdkhK9891beqm5atZ1wo1q+viC1K96l+EPPNoYldyomysv6oG1T7+g1N/CZ2Q+R0sc57QmyFoLLHVK9JvmF3i9VzRCxQTlC9IzbDU9aIPb9vhy+CIfyQ43qZddploWwMvC2RS1R/qzZPv5+s+ki1RfJRh/6mHlbnHFx/SvWN2GIQ+Uzs/tYIgBENi7Cks0p+Iba0Py5me1BqlOAdvSFcp6EPqq4L14EB8bHq8FgwAov2Qwk66nWxOq8IZWNAO36KF8WiA1GCiLmfzAZYaYDy/pTjjxz0OX3/kuTTNZ8w/C1yiNhDqCRykVgFb4tVgh0DscT+Yrmtd7TjL55rCA2/OV4cgSH8kAPfnDf9S72kIl1YJ+WBA6yOtKMvHtofigVi/UTZ02Jp11+qi+cs5vF+J3LlYEGjPvybw/34puqA+aIZZ0rZcQ+LlW0Uq4hVpTSbwB8YNyP+Im+IbdhS6ITWEDEAQ/ghQiryopgP/Pnb5yzKsJ9g05QbxJSRh+fK2rhUrB25SPCyWBm5Pv3J96Yc1fu99E4MbOo7NhZM6eRHKsnlIGvFKn9GbMbxOZcCpJDHkkfGlABHbhKrIxUhJpc7RVil4261SeSeXepNGcIPkQ9Vt0w/027qniyXtnO22GYpHagMXny9O4OXtID0IK541MVKS/vYoOEnPrNaN8FigF1uNYdfxMpLMKmxie1ZhrD5rthJwDax3A4tiVV8tdhAIBTynQqb8BCzQyy3TWGV/UNWDmKc3cblqq976D3VKbvu7MaQfkiZyCzM85d7aEcfGMQ+YP/NygsMyO9UX8rMB+h7sbZdIFa39x0DvgnSMexKE56y3J7D8RSDPsm+kxvkwkWKN7gtp+LlsVsTCzKw0nm9YzO0H5jMdMrxMosax4jdw7198ZV4i/SPPCl+nEgEaaJrv7ldbhI37Tkcjuaa/LjLiRgwc5tglvRpcDpbmKWlHLdrvYtmCD+kEI7ZALldKnLGvqzWAJ6ItaEp7QFvaxMeUX6PBVO6bFpb/U24wiCbXyTgVOxyM8lhNcGGc8EUdpjMthzU+2e8OAJD+CFlIrYBi3BfU0gtweAljSB96JKSlfDIUZp4TpcBTDTDpnRaQ9TjXUsnEGwO2/zYqSHgu/DSzvtKsRXlGpl/eTZfhIjcAPZcio1cG4vexC3aDykcb5HT5+jaDme1N3E8u0sE8NBeOoEgb6acd83BCs8Gl7GRO//Ff/ixMaXzAZQ7sI6cJrbBYTZFx/CdzRmKZRyPLIk1KHKu2I639GPAUAzhB4cOf3L6N0ffAbwk+RV3d1ZiD/kMrDY4OcE2dwbsKyeDvIQfr+XSB1JO7sfPWVih3FGpbkuNCuAYbLeLzTJmCStAqUP4yZGz3/vF7uOfXZ6ffuZIakyG9MMZYmfH6XOuTco5TovtaNvMrZPyRIGuP2R4LhrFeXAT6akSPtgqlhK8JeV2MR7ic1Itqe5x40VAWCZE+fHKSdNrJegkP1flF6lHxe5r+3Xqv05fP/xfIfyTw+IDznrj/7lUKpVKpVKpVCqVSqVSqVQqleH5B8pU5afIhB+5AAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGsAAAAXCAYAAAAMX7G2AAAE1ElEQVR4Xu2ZXahVVRDHRyooTMsUKiy1iCRKJMygsPQhIyl76Dt67MEQBSkoDJIggqCCCLVSKXqIQuuxtx4uGRQqEdEHlGGB2ENkICShaM6v2XPP2uPa++zzsc+52P3BH8/ea929PmatmVlLkWnOGWaorlc9o7oylE0zxXhN9Y9qj+rPUDbNFOJq1Y+qy1Xvq/6V9ncX34+6sFRjanGr6sH4siHPis1vU/BylTym+lh1vmq12M66oFRjuLwstiCq9Jdq9mTt8bNQ9ZN0mcQamMv3VJfEggpuiC+ci1UTqufC+7ZZrjquej4WKDeJGW1XLBgTp1Qb4ssewdB/q5bFgl7A/fymeiIWtMw6MYPcFQvE+kTZL7FgDOBtDquuiQV9gLG2xpe9wGSdVq2IBS2zX8wguThFnyj7KhaMATzOsBayu/++oSN8YKDt2QfHJN9x3AWrj7KnQtmoYSF9KuayqyAerVXNTZ7vVs2crNFhjeTH7JDg8a3KfGFU2V+ENnEvEbImypoG4zZZKraoZsWCgh/EkgEWGAnE76rHVR9J3igecuJc3yvmIq8onkn2snwm9uF5saBF5oi1+YdqRyEWza9ig3lksuZ48RCR2yVXqe5InnFxE2IJG2PLGYtx4/5ZBClkv8yFk4vj/7FX7MM0MiroLG0ekI6xEElHv+lxG+CScpMO9JXkA9xdYjDAY3xe/E7xzDsNObhP2kgTj0pjcaaq6lAbuMug3crzxIAwHiZzUOqMleI78NpYEIjGciN/L2XPxrss+MomHRoW7grY0VWxYFBWSU2Q7oGmxiJjpF4us02JxvIY9oGUPQqxL0uVf83BRe+S+LJH/Hx1fywIcINB9gTEDAZ4XvHMIHEfDJA++W0H5Wk9h3qLVHdKx4j8DddscJ+cHfSBb7GYcyGCcXyiukhsctM5vE31bfLsxATDn1kUKZX2oIAOdYOA+o0MnuLjAmmzmwvcJna78YpYdoSIa/TjXbED83axOMEuJXt8Q/WC6nUp86Vqp+pV1ddik/+OWGx5U2xnkNlFSKVpJxoSl4XrcvcV55AxvpQ8O55duvF9p6XGulG6GItGu7FPdUj6NxYryHdxqiq4OGX3ebDl0H5SzBhMHquZGMFOuaWow2SwqrnrBJ8MPwP58yaxunyP77Kz7inqRHKHYnYq/5WEscnkFohl1TxjjMs6VUvkDsV4gROqo6qfVStV35VqJPDHNFQHndsotrr7NVY/MLj5xW93n+CBORcjXpTO1ZAHfsd3hK/sGNhzYPwPpZP5pbBoLi1+M+m3J885JsSOJxHGwbfcfWfjLZ1mAuoucfHJ+GbgLLQ8KWsTdk0aaFm1bxW/MUIuvWV3sEoXixntaSm7J9ykn2dww00zxmFd5NI2bq4vsCYrLzdw51EpGysGw7bABfpOYqC4hoXFM7Eslya/LZZpYqTVYl4A9+Jg/AeK3/zb9D50t9S4poZgpM3S4zkyjRVMCIexqg+wHTHUw6qHxFJMJmIUTIi5OuJNzMbic0qujEUZ3+dcaB2j/M/HSdjS3F1hCFZM3bZkVx2RckJQ5zKHCbtgVG01hUzy5viyAez26+LLJhDEcHv465iSwhdiF4sHxTKeFOIVDXOwXS+2y7aIpdC4HeLbMHhSOldQ/0vOAL2CAo9dhaoZAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAXCAYAAAAyet74AAAAh0lEQVR4XmNgGAWDG+wB4v8EMAMrEJ8HYj0g5gTiHSBBIOABYl8oGwyCgFgIytYE4ttQthIQG0PZGABk2hwouwiIJZHkUMBPII6GskEasCpUBOIDDBC3gTCI7YIkDwcNQNwKZTMC8VIkPhzYAPFvIBZGEvMA4otoYgzMQKyGLAAV40ATG9QAALktF00+GSlEAAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIoAAAAXCAYAAADUf9f5AAAGGElEQVR4Xu2aaYi9YxTAj1D2PUuWQSJRki1CPiCyZgnxQfayfPAnpWhKkqwhZPvnE1miRJIyoQj5IFv6C2VJQimyZDm//3nPvWfOPM+979y5y5iZX53mPsu97/s+z3nO9o7I0mHz3FGAOevnzhUWzjoqe6qsUtkhjS0mXlPZNndWOE9WlGXo3K7yu8rTKj+msUmA4t6sskHo21Dl7NDuB/NPy50rDM7OKp+obKfyuMq/Mjqrso3KqdLffRyk8ltoozirQ7sta1QOz50BfndrseeNspgt0cEqp+fOlvDd73JnWzilz6isp3KMmEUZ1ULtrfKCmDLi5kpsoXKtyi9ibmZdMQX7KE5qQMlPbD77hkdeVbk+9UV4bu6lJt+oXNCZPXmmVD4TU/BBOUtMYebFJiozKtel/lHzh9hG1EAp7gntk2TuSUCpfcG+FlPCX1UO6Myw55oJ7RquGJnjVP6R8a9Pjb9VrsidA8DvzOuZOIFfqZybB0bM22IbE2OQCG4n3hOKwn1Grmr+bixdi3iKmAVyWIx3Q7sG91KKzVA6lA/LxHUmCc/HgdgtDwzAjFi40ZqjxU5MLz8+CvZV+VnKpwMrweZuGfpKiuKcLPX7b2NRdhdTlGjBnEvFxp4Q26hJwrMM60CzXn/JPJ6JC7MQ0VyPAzKSl8U2EfcXIR55pPl8p9g4D/ZtZ4YpE7EDY2zwjk3/XSob+SSxzAlr0IvjxdaglCFxj4zh5iYJlvdFsSC/BnElB4pYzdvHStkSkrh83vxtxaiznF5gQrk2mxlBid4Tcyceg3gs5bAI3DsbeaXY3Geb/sg7YhanBouIIr2hsmno57ooB/d3a+ifFPuJBffxHiMfi8Vonh0Sz52j8qSUYy9g/VCsyE6p3YFF4oc4xeMGs8e1S9kMpyJbmmmZbSqJRTzGITsqxTv44V4+HbfDon6h8lCQ78Xu7UhZWIYxLDxEKFkHNveI0ObgzYitH89QUxTmXZ36qtaXk8QP5U0ZB5wArs0CtGEPsdimLWzwTc3fGu52XpHZikJVt7VZHgOc/NqGE0f5AXIX5Vaa4Pf15nOGmCdmPqxT7RprI/3q4Aj5QUx77xO7vscY/bhX2hWbcEGY4H7MyGgtKr/NRi6UXooSccuDpexHVhTus3poSf3a3MAwOUysaDQl3TpF29I8phcr0Y+LxX67H7gdnr+X1VkIR8ncuGkQ2ioKG8+8khvOZEUhZsECFeFH29wAbC+msQuBlBiJTIttWJtTMGx4dg5LP3BRVIFRVDIJr9WQBDCGovFSdbOmn3EyyVjTAebtKhb7uALFufw2gWvG6zmlEAFLQCBPEuCK7xyq8kFoR3IwSxsp0naheDfzvMyNkufDCWIVwew6WATuo1RTGSUe7JWC6QgbwGsA0nOyK0oKxDFs9GMqd6jcLxYXEPOxVner3NCMRd5SeVjlNpX3mz6yNrKWR8UsYWljPZ3N2am/2kD4nPdztZQtsGd7uYrdU1H6LRS8pPKpDK4o3ADXqplhxijrjwNXzCxYhhLni6XYKLlDseoasY1DibCGPNuBzThWgdPsLtXTe69xeBvLcpGYyUfRsEqXNHMypYIbFmqV2Pex1LuIKQBt0umtulNn4QW37HLXpHYHFqiaEgUofN0igysKC9TrRRQLe0buXESwiV+GNutGgc6zjFJMMC3d1NyDTMctgbuSP6W/W0fxahViFJaXqYALIw70dgmPZTLZVa7FTW8MaDJoHGaUv8wrVS+XA/h+Xyc2/wGxDWNz2eQMgTT9e4kpDPWK6BJYUzI/6KVsmWG9FMSaXJY7a6CFaHkvTT5EzO9CjpKXExyoaenWZqaaftwOSpR5UOx9FQpChRd391MY5zt+6CiYed2jH0+pfJg75wkxF7WVnv8T5P4Y8LvUMbKfcuh/U6wUjFuglO3vYJYTWF5OPAucsw7aNUuQ5wKHM/dj7mt7UGIs/7iE6aL+T+CFdu4ze3gWWBOCIr7jClaNipcwBKqLzZKSMe2fO1vAu68zc2cJtBdXQ+6dUy14Tsx3YZrwwxFMpNc7LhczqzeKpYaYV07cUuNC6Zb12xYF/9f8B/nGQWr9Ipj3AAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAXCAYAAADUUxW8AAABCElEQVR4XuWTsWoCQRRFb9CAnQSCEFJIShG0CYKBdCEINkKaiD9gYeefBEGwFz9ABJEU6VMHbAQLwVIQrPW+vF1ZL9loKx44xb47b2d2ZhY4N3L0WYuncEX79EaDGn3VYoRrmqdTeicZhnRL2/AZlAKdwMf0JPulDA8bGgTYkr+1GJKGN49oSjLjh35oMcoK/oKWBmRNi7SuQcgY3vwldcOWbDvd1SDkgS7gL1DsUzJajJKkA3jzrWRHsRs0gzdXJPuXR/oJ/64OndP76IA4nuA7nQ2ebVab/X0/IoYXeGNJ6ta8lNoBVbqhbxrA63/t+h4L486tCc9jf0FbakKLAfaD2I2yE7h4du2VK7VlD3eBAAAAAElFTkSuQmCC>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEgAAAAWCAYAAABjadrAAAABKUlEQVR4Xu2Xv0tCURTHT1iBIAjmErTk4uYi5N7QIrT1Fzg09ndIs06Ck6uLCBENgYNjDYGTg+DkEg5BBf74Xu5t8IuXlxbCfZ4PfHi879kO975znoiiKIoSBGX4AivwDU5Xy/vNBXyHafdunk8uV8AXHFOWgx+wSPk2JMSe0BY8pFoQLOCQslOX31K+KUk4gQN4RLUgSIltxLMn71L+G07gPezDEtWCI6pBnEdhTt43bMMDqgWJrxG+fB0F+AhrYhsUK3yN8OWM+Zh/ir1SscU0okdZ1uUNyteRF3ulYnmCDKYRI8q2mWJNOIPnXAidBzin7Bp2xI7pTTFTrCoxmWKGn006497P4KvL/8Kd2F+WS7HLYvDcwDq8kv9d6oLfpHfFMQeKouw1S17QOEGu/kJ6AAAAAElFTkSuQmCC>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFwAAAAXCAYAAACGcCj3AAADiElEQVR4Xu2ZTahNURTH/0KRl+9Ikd4LJS+SkI/BI6TExISYI0oZPBmoV0ZGPkdSMhADGQuDVwyEKcoI+SiSUhTysf6tvc/Zd7179jn33s07cn/175yzzr7nY52911p7X+DPsUH0y2mis00W3Qrsk5y9SyIuiw6LzovGBPY9wX6XhJwSzRG9EvU62zjRsqxFl6SscNuPovtuf73bdknMNNFMt39V9NPt73Pb/5pn0CR2EBoCYlooOiN67X5D9WMkYZyeAu3hG6FxPQXMCfbZvCy8/x3ReHtitNgs+gEd+svNuRg3oA4/aux0xjlj2yt6Ijpp7O0yV/QGev+XTt/c1nJB9MAaRxv2At9jw4qiCp/QGJvZk/kxLB9Ei62xQ/zH7kGeM0JmiW4iL01rhe8xO+2JEi5CSz+yCfmH25a1UPjijO0pKXP4LqdawhjH4UdncYLyLxBzOI8/Q0vR2jID7YeW0SDmcFZEfI+/xQAaQ+ZY6DOV+pHJkw+62p6oId7hszHS4Qx1RQ6nE94h71zNtDVrXQ7z1l1o4mY+JPuh11njGxXB0HIJ2pghps54h7MctA5/DE3oFuYoJnBfJl6Hhh1eq52ylfnrhKhP9Baax4gvR7e74yjzkX/pOhNz+AsnC0vEdW5/AvJr0PG2xK3CPei9OfegvzjaPDtEK4PjKMegF+Bkp67EYniRw0MOIXcQR0Ol3lgAR813Y2MeqZy014qeW2PN6MThfgbsHcLO1YnD+XuGMQ+vy1FTCYaUQVTIsAVwrXuRNVaEs90t1lhAzOHD0LKwCK7xhOfpsLPBccg86Hp+Ebw/fx+GpCHR6eDYPl9GirWHI2h9oYpVET+yffAYMYfHqhTyVfQwOGbb8NizRPQeOhp8BWJhLrDPzfYL3D59eTw4l8Ee/RTaw6vCi/mVwRSw15U5nD3OJ3UrT2ziwxkv148GAhvfmzYLnXwNei4WcrhOxPtz/Z/5IIwOB1BQHrJkWmWNJTDxhLGKL9rJuncVh1fBx+hee8LBBbDQKVOdiriCuMMJR1o/tMdbhqyBX5hDuhWmQ2tP1qCEK4+MdcPQmRZ5hHxFr5l2u3aeVA4nKRevbqM4pFSBk6IMXoiTnFbi9lLoR/ITB+KHzhffqA1SOpywVGNH6AT6h0vMnZDlB5+obM9rpmbT4T40wtLIrx4S9jL7J0EoDsOQ1A5PUQSkmIv0/AZwys8UlFS8vAAAAABJRU5ErkJggg==>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAXCAYAAADQpsWBAAAA2UlEQVR4XmNgGAUjAohDMTLgBmJJNDE42A3E/ED8FYivQsVEoOyHDFg0gky3hbL/MyA0gYAZAw5NLkDMA8QsDBBNU5DkGIH4MBDzIoklIrEZ0oH4NBALIolxAHE0Eh9kiDyMA5LcCsST4NIQoATFWIExAyQQQDQMgALmABJ/PRA3AbE6TEATiN8yoGqKAeKVUDYnEKsAsR8QW8JVAIEMAyQgngHxNQaIQchAEYifoImBgTAQWwExM7oEAySg3qMLEgI7GCCBVYUugQ/sgmJ4kBMDQE4GJS3yAAAJVh5UkFMtnAAAAABJRU5ErkJggg==>