# Framework SAREnv

---

## 🎯 Guion de Presentación para los Tutores (Respuestas a los 4 Puntos)
*Este es el resumen exacto para contestar punto por punto a las 4 preguntas que formuló el tutor:*

**1. ¿Cómo se genera el espacio de búsqueda inicial?**
"El espacio se define principalmente de dos formas: mediante un **Polígono cerrado** (donde trazamos nosotros unas fronteras estrictas, como el perímetro de la Casa de Campo) o mediante un **Punto central (PLS)**, donde el framework calcula automáticamente un límite de radio expansivo basándose en el comportamiento estadístico de personas perdidas (LPB) según el clima. Para llevarlo a cabo, el sistema hace una llamada a OpenStreetMap y recorta los datos geográficos matemáticamente usando la librería `shapely`."

**2. ¿Cómo sectoriza SAREnv el espacio de búsqueda? (Descripción y Ejemplos)**
"El sistema no trabaja con un terreno continuo, sino que proyecta todo sobre una malla bidimensional (Grid matricial de Numpy). Lo logra mediante un parámetro fundamental llamado `meter_per_bin`. 
* **Ejemplo Numérico:** Si la zona de pruebas de la Casa de Campo mide 2.000 metros de ancho, y configuramos `meter_per_bin = 20`, el sistema divide 2000 entre 20 y crea 100 columnas. El mapa entero se convierte en una enorme matriz cuadriculada.
* **Ejemplo Visual (Los Heatmaps):** La sectorización se ve claramente en las gráficas PDF del mapa de calor que genera el framework. Las imágenes no son fotos de satélite suaves, sino que si hacemos zoom se ven 'pixeladas' (manchas cuadradas de color rojo o azul). Cada uno de esos píxeles o 'cuadraditos color' es la representación gráfica de un sector real de 20x20 metros. El dron no vuela en curvas reales, sino que evalúa el mapa saltando de sector en sector, como si fuera un tablero de ajedrez."

**3. ¿Cuáles son las capas de información que integra y cómo lo hace?**
"Es capaz de integrar capas naturales (bosques, ríos, prados) y artificiales (carreteras, túneles, edificios) extraídas de OpenStreetMap. ¿Cómo lo hace? Primero rasteriza cada geometría (pone un 1 en la matriz donde hay un recurso y un 0 donde no). Luego, asocia a cada capa un peso de probabilidad extraído de manuales de rescate reales. Finalmente, aplasta y fusiona todas las capas en un único 'Mapa de Calor' conservando siempre el elemento de probabilidad máxima en cada cuadrícula (`np.maximum`)."

**4. ¿Cuáles son los parámetros configurables del escenario?**
"Tenemos control total sobre dos niveles. A **nivel de Entorno**, configuramos las coordenadas iniciales, la resolución de la cuadrícula (`meter_per_bin`), el clima y la topografía. Y a **nivel de Simulación de Drones**, configuramos la flota: el número de drones que salen a volar (`num_drones`), el presupuesto máximo de movimientos o batería que tienen asignado (`budget`) y, finalmente, cuántas estadísticas de víctimas independientes debe sembrar el modelo de Montecarlo para comprobar el porcentaje de éxito (`n`=100)."

---

## 1. Definición del Espacio de Búsqueda Inicial
**¿Cómo se genera la región inicial de búsqueda a partir de unas coordenadas?**

El espacio de búsqueda inicial en SAREnv puede definirse principalmente de dos formas:
1. **Mediante Punto Central y Radio (Radial):** Se define introduciendo unas coordenadas de origen (Longitud, Latitud) que simulan el punto donde la persona fue vista por última vez (PLS o *Last Known Position*). Al recibir solo un punto, el sistema **no realiza una descarga infinita**. Para acotar el tamaño geográfico del mapa, el framework consulta sus tablas internas estadísticas basadas en el comportamiento oficial de personas perdidas (*Lost Person Behavior - LPB*). Cruzando los parámetros del clima y el tipo de entorno (ej. llano y templado), el sistema recupera el radio máximo histórico de recorrido (el tamaño que SAREnv denomina `xlarge`, que en este clima son 9.9 km). Con este límite, el motor traza un perímetro circular alrededor del punto inicial y limita la descarga del terreno a dicho radio máximo.
2. **Mediante Polígono a Medida:** Se le suministra al sistema un arreglo de coordenadas que forman un polígono exacto (usando la librería `shapely.geometry.Polygon`). En lugar de usar la estadística expansiva del LPB para calcular límites, el framework delimitará el escenario ciñéndose estricta y artificialmente al interior de la forma geométrica definida por el usuario.

Una vez definida la región geométrica, el sistema utiliza el submódulo de entrada/salida (`sarenv.io.osm_query`) para conectarse con la API de OpenStreetMap (usando `osmnx`) y descargar exclusivamente los datos geográficos que se solapan con (`intersection()`) nuestro polígono de búsqueda.

**Este código no es parte del código interno del framework, sino de la capa de usuario o scripts de ejecución. Los usuarios definen la geometría usando la librería matemática externa shapely antes de inyectársela a SAREnv.**

**Snippet 1.1: Generación por Polígono a Medida (Frontera Cerrada):**
*Ideal para áreas naturales delimitadas en ciudad o recintos cercados.*
```python
import shapely
from sarenv import DataGenerator, CLIMATE_TEMPERATE, ENVIRONMENT_TYPE_FLAT

data_gen = DataGenerator()

# 1. Definición de las coordenadas objetivo (Casa de Campo, Madrid)
#    Se especifican los puntos [Longitud, Latitud] para cerrar un perímetro exacto.
polygon_coords = [
    [-3.766, 40.407],  # Suroeste
    [-3.738, 40.407],  # Sureste
    [-3.738, 40.432],  # Noreste
    [-3.766, 40.432],  # Noroeste
    [-3.766, 40.407]   # Cierre del polígono
]

# 2. Generación geométrica de la región inicial de búsqueda
#    Convertimos el arreglo en un polígono matemático
casa_de_campo_poly = shapely.geometry.Polygon(polygon_coords)

# 3. Exportación: OSMQuery usará intersect() con este polígono para 
#    bajar solo el terreno estrictamente necesario.
data_gen.export_dataset_from_polygon(
    polygon=casa_de_campo_poly,
    output_directory="resultados_casa_de_campo_poligono",
    environment_climate=CLIMATE_TEMPERATE,
    environment_type=ENVIRONMENT_TYPE_FLAT,
    meter_per_bin=20
)
```

**Snippet 1.2: Generación Radial por Punto Visto por Última Vez (PLS/LKP):**
*Ideal para búsquedas realistas donde la persona huye en cualquier dirección desde un punto origen.*
```python
from sarenv import DataGenerator, CLIMATE_TEMPERATE, ENVIRONMENT_TYPE_FLAT

data_gen = DataGenerator()

# 1. Única coordenada inicial donde constan los últimos pasos (LKP / PLS)
#    Solo se requiere el punto central y el framework bajará el radio 
#    automáticamente según las probabilidades por clima/terreno
punto_visto_por_ultima_vez = (-3.7337, 40.4187) # (Longitud, Latitud)

# 2. Generación radial expansiva basada en estadísticas (Lost Person Behavior)
data_gen.export_dataset(
    center_point=punto_visto_por_ultima_vez,
    output_directory="resultados_casa_de_campo_radial",
    environment_climate=CLIMATE_TEMPERATE,
    environment_type=ENVIRONMENT_TYPE_FLAT,
    meter_per_bin=20
)
```

**Snippet 1.3: Tabla Estadística Interna LPB (`sarenv/utils/lost_person_behavior.py`, aprox. línea 18):**
*Aquí el framework almacena en duro las distancias históricas (en kilómetros) recorridas por personas desaparecidas. Los 4 tramos corresponden a los cuartiles estadísticos de la población perdida:*
* *El 25% de los encontrados no recorrieron más de la primera distancia (ej. `0.6 km` para llano).*
* *El 50% de los encontrados estaban antes de la segunda distancia (ej. `1.8 km`).*
* *El 75% estaban antes de la tercera (ej. `3.2 km`).*
* *El 95% (el límite extremo considerado por los rescatistas) se encontraba dentro de la última distancia (ej. `9.9 km`).*

```python
# Tramos de radio (en kilómetros) por cuartiles de LPB: [25%, 50%, 75%, 95%].
# Equivalentes visuales en el framework:       [small, medium, large, xlarge].
# El valor máximo (xlarge) será el tope absoluto que dictará hasta dónde bajará datos OSM.
RADIUS_FLAT_TEMPERATE = [0.6, 1.8, 3.2, 9.9]
RADIUS_FLAT_DRY = [1.3, 2.1, 6.6, 13.1]
RADIUS_MOUNTAINOUS_TEMPERATE = [1.1, 3.1, 5.8, 18.3]
RADIUS_MOUNTAINOUS_DRY = [1.6, 3.2, 6.5, 19.3]
```

**Snippet 1.4: Inyección del Límite de Búsqueda Radial (`sarenv/core/generation.py`, función `export_dataset`, aprox. línea 707):**
*Al recibir el punto inicial (PLS), la función principal restringe automáticamente la petición de territorio usando el nivel probabilístico más grande ("xlarge") para ese clima, asegurando que se descarga el "lienzo completo" de todas las posibles búsquedas futuras.*
```python
log.info("--- Generating master environment for the largest radius ('xlarge') ---")
master_env = self.generate_environment(
    center_point, 
    "xlarge",  # El código inyecta internamente la talla estadística máxima (9.9km)
    environment_climate, 
    environment_type, 
    meter_per_bin
)
```

**Conexión entre Generación Evaluacion (El propósito de los diferentes tamaños):**
Es fundamental entender que SAREnv separa el proceso arquitectónico en dos fases para garantizar la eficiencia computacional simulando rescates reales:

1. **Fase de Generación (El Mapa Maestro):** Como se muestra en el snippet superior, el sistema extrae siempre por defecto el mapa en su tamaño extremo (`xlarge` de 9.9km) para no volver a tener que descargar más datos de OpenStreetMap jamás.
2. **Fase de Evaluación (La Lupa del enjambre):** Cuando los drones despegan, los equipos de rescate jamás iniciarían una búsqueda aleatoria en un radio de 10km (casi 300km²), porque las baterías de los drones se agotarían barriendo fracciones inútiles del mapa. En su lugar, el submódulo de simulación (` DatasetLoader`) funciona como un "molde de galletas" virtual: carga el enorme mapa maestro pre-generado y le recorta dinámicamente un radio pequeño (ej. nivel `small` de 0.6km o `medium` de 1.8km) sobre el centro. Los drones peinan exhaustivamente ese círculo interior y, de no tener éxito, el sistema es capaz de cargar el nivel siguiente sin recurrir de nuevo a internet.

**OSMQuery: (`sarenv/io/osm_query.py`, función `query_features`):**
*De esta manera el framework descarta la información geográfica irrelevante recortando los datos de OpenStreetMap para que encajen estrictamente en nuestro polígono.*
```python
import shapely

# 1. Se consolida toda la geometría en bruto que se bajó desde el satélite/OSM
consolidated_geometry = raw_osm_geometries_gdf.geometry.unary_union

# 2. INTERSECCIÓN: Se recorta matemáticamente la geometría consolidada 
# usando como molde el área/polígono exacto de búsqueda del usuario
final_features_geom = shapely.intersection(
    area_geopolygon.get_geometry(), 
    consolidated_geometry
)
```

---

## 2. Sectorización del Espacio de Búsqueda
**¿Cómo divide el sistema el espacio?**

SAREnv sectoriza el espacio geográfico continuo convirtiéndolo en una malla o cuadrícula (Grid discretizado) de resolución configurable.
- La división se realiza proyectando el recuadro delimitador del mapa (Bbox) en una matriz bidimensional (un array de `numpy`) donde cada celda o "píxel" representa una porción de terreno real.
- La resolución espacial se controla a través del parámetro fundamental `meter_per_bin` (por defecto 30 metros), que establece los metros cuadrados de terreno real que engloba cada sector/cuadrícula. Si se especifica `meter_per_bin = 20`, cada sector representará un área de 20x20 metros de terreno.
- Estas cuadrículas facilitan las operaciones matriciales de probabilidad y permiten a los agentes (como los drones) evaluar el terreno de forma segmentada (se mueven y escanean de cuadrícula en cuadrícula).

**Snippet 2.1 (Script de usuario, llamando al motor: `examples/generar_casa_de_campo.py`):**
```python
from sarenv import DataGenerator, CLIMATE_TEMPERATE, ENVIRONMENT_TYPE_FLAT

data_gen = DataGenerator()

# Exportación y rasterización del escenario (Proceso de Sectorización)
data_gen.export_dataset_from_polygon(
    polygon=casa_de_campo_poly,
    output_directory="resultados_casa_de_campo",
    environment_climate=CLIMATE_TEMPERATE,  # Clima
    environment_type=ENVIRONMENT_TYPE_FLAT, # Topografía
    
    # -------------------------------------------------------------
    # SECTORIZACIÓN PRINCIPAL DEL MAPA
    meter_per_bin=20,  # Cada unidad de las matrices representará aprox. 20 metros.
    # -------------------------------------------------------------
)
```

**Snippet 2.2 (Código del Framework: `sarenv/core/generation.py`, dentro de `Environment.__init__`, aprox. línea 141):**
*Aquí el framework calcula matemáticamente cuántas "celdas" construirá, basándose en los metros cuadrados físicos del entorno y la resolución seleccionada.*
```python
# Se obtienen los límites físicos máximos y mínimos (Bounds) del mapa importado de OSM
self.minx, self.miny, self.maxx, self.maxy = self.polygon.geometry.bounds

# Se divide la distancia máxima (ancho y alto geográficos + buffer) entre la 
# resolución escogida (los 'meter_per_bin') para obtener el número de celdas del Grid (num_bins_x, num_bins_y)
num_bins_x = int(
    abs(self.maxx - self.minx + 2 * self.buffer_val) / self.meter_per_bin
)
num_bins_y = int(
    abs(self.maxy - self.miny + 2 * self.buffer_val) / self.meter_per_bin
)

log.info("Number of bins x: %i y: %i", num_bins_x, num_bins_y)
```

---

## 3. Capas de Información Integradas
**¿Cuáles son las capas, cómo se integran y cómo describen la probabilidad?**

SAREnv es un entorno multicapa que utiliza etiquetas de OpenStreetMap para clasificar los elementos del mundo real según su tipología:
* **Capas de Infraestructuras**: Edificios (`building`), Carreteras y Caminos (`highway`, local paths, grandes avenidas), Ferrocarriles (`railway`).
* **Capas de Naturaleza e Hidrología**: Ríos, lagos y masas de agua (`water`, `waterway`), Bosques, Matorrales o pastos (`natural`: scrub, wood, grassland).

**¿Cómo funciona la asignación de probabilidades?**
1. **Extracción y rasterización**: Cada capa se extrae individualmente como un submáster de geometrías. Posteriormente, usa operaciones para rasterizar esas geometrías y transformarlas en cuadrículas marcadas con un `1` donde la geometría existe, y un `0` donde no.
2. **Ponderación**: Mediante la tabla interna `FEATURE_PROBABILITIES`, el sistema multiplica los unos de esa capa en concreto por el peso estadístico o probabilidad de encontrar a una persona perdida ahí.
3. **Fusión Final (Heatmap Combinado)**: En lugar de simplemente sumar todas las capas (lo cual daría valores inflados donde capas se solapan), el sistema integra todas las capas haciendo un cálculo del valor máximo en cada cuadrícula (`np.maximum`), garantizando que la probabilidad térmica no se diluya y refleje siempre la característica geográfica estadísticamente más probable de ese recuadro.

**Snippet 3.1 (Capas u OSM Tags configuradas en `sarenv/core/generation.py`, clase `DataGenerator`):**
*Listado interno de las capas que el módulo pide a OpenStreetMap.*
```python
self.tags_mapping = {
    "structure": {"building": True, "man_made": True, "bridge": True, "tunnel": True},
    "road": {"highway": True, "tracktype": True},
    "linear": {"railway": True, "barrier": True, "fence": True, "wall": True, "pipeline": True},
    "drainage": {"waterway": ["drain", "ditch", "culvert", "canal"]}, 
}
```

**Snippet 3.2 (Rasterización de Geometría en `sarenv/core/generation.py`, final de la función `generate_heatmap_task()`):**
*Aquí las formas de OpenStreetMap (polígonos, líneas) se proyectan como píxeles (1) sobre la cuadrícula matricial de esa capa, convirtiéndose en unos y ceros.*
```python
# Pinta un '1' en las coordenadas de la matriz en las que cae la geometría (ej: donde hay un edificio)
if valid_indices:
    valid_x = np.array(current_geom_img_coords_x)[valid_indices]
    valid_y = np.array(current_geom_img_coords_y)[valid_indices]
    heatmap[valid_y, valid_x] = 1

return heatmap
```

**Snippet 3.3 (Tabla de Estadística de Personas Perdidas en `sarenv/utils/lost_person_behavior.py`):**
*El sistema extrae de manuales de rescate cuánta probabilidad hay de que alguien varado acabe en cada tipo de terreno.*
```python
FEATURE_PROBABILITIES = {
    "building": 0.05,
    "highway": 0.1,
    "water": 0.25,
    "wood": 0.45,
    # ... (Y el resto de probabilidades topológicas)
}
```

**Snippet 3.4 (Fusión Final de Capas en `sarenv/core/generation.py`, método `get_combined_heatmap()`, aprox. línea 431):**
*Y finalmente el código se encarga de ponderar esos "unos" con la tabla de probabilidad y colapsar las matrices.*
```python
# Archivo Interno del Framework: sarenv/core/generation.py (Líneas ~431 a ~442)
import numpy as np

# Fusión de las capas individuales (`water`, `building`, `forest`, etc.)
combined_heatmap = np.zeros((len(yedges) - 1, len(xedges) - 1), dtype=float)

for layer_key, individual_heatmap in heatmaps.items():
    if individual_heatmap is None:
        continue

    # 1. Se aplica la ponderación de la tabla interna FEATURE_PROBABILITIES
    #    (ej: a los edificios les toca un factor, al agua otro)
    alpha = FEATURE_PROBABILITIES.get(layer_key, 0)
    
    # Se multiplica la capa binaria real (1s y 0s) por dicho factor de probabilidad
    filtered_heatmap_part = individual_heatmap.astype(float) * alpha    

    # 2. Integración: Se conservando únicamente la característica con mayor probabilidad (máximo).
    combined_heatmap = np.maximum(combined_heatmap, filtered_heatmap_part)

return combined_heatmap
```

---

## 4. Parámetros Configurables del Sistema y Escenario
A la hora de configurar un escenario de simulación en SAREnv, existen múltiples parámetros que alteran tanto la generación de datos geográficos como el comportamiento de los simuladores métricos.

### Tabla Resumen de Parámetros Configurables

| Parámetro | Módulo/Nivel | Descripción |
| :--- | :--- | :--- |
| `center_point` / `polygon` | Entorno | Punto de inicio u origen (Longitud, Latitud) de la persona perdida o polígono a medida de la zona de búsqueda. |
| `meter_per_bin` | Entorno/Rejilla | Metros de lado que representa cada celda de la cuadrícula o sector. Controla la resolución del grid (ej: 30m). |
| `environment_climate` | Entorno (Físico) | Factor del clima en la zona de búsqueda que influye (ej: `CLIMATE_TEMPERATE`, `CLIMATE_DRY`). |
| `environment_type` | Entorno (Físico) | Tipo de relieve y estructura general (ej: `ENVIRONMENT_TYPE_FLAT`, `ENVIRONMENT_TYPE_MOUNTAINOUS`). |
| `n` (generación de víctimas) | Simulación | Número de ubicaciones de personas perdidas reales/ficticias que el generador inyectará (ej: generar 100 víctimas para las pruebas). |
| `n_agents` / Algoritmo | Drones / Evaluación | Cantidad de agentes de búsqueda o drones simultáneos desplegados en la evaluación de caminos. |
| `budget` (Presupuesto) | Drones / Batería | Limitación de celdas/movimientos/batería para las simulaciones de los drones (ej: prespuesto de 100000 pasos). |

**Snippet 4.1 (Script de evaluación simulada: `examples/04_evaluate_coverage_paths.py`):**
```python
from sarenv.analytics.evaluator import Evaluator

# Configuración de los parámetros del escenario métrico y simuladores
evaluator = Evaluator(
    base_dir="resultados_casa_de_campo/50", # Datos geográficos calculados
    test_types=['random', 'lawnmower'],     # Algoritmos de enjambre (drones)
    
    # PARAMETRIZACIÓN DEL ESCENARIO DE RESCATE
    n=100,             # Número de simulaciones o "clones" probabilísticos de la víctima
    n_agents=3,        # Número de drones / efectivos de rescate simulados
    budget=100000,     # Límite de batería / capacidad (movimientos por agente)
)

# Ejecuta el análisis de cobertura y evalúa estadísticamente el rendimiento
evaluator.evaluate()
```

---

## 5. Simulación de Víctimas y Evaluación Estadística (El Método de Montecarlo)
**¿Qué significan las $N$ personas desaparecidas y cómo se esconden en el simulador?**

En SAREnv, cuando se configura el parámetro `n=100` (número de personas desaparecidas), el marco **no simula una catástrofe con 100 víctimas reales** dispersas por el mapa a la vez. En su lugar, el sistema emplea un enfoque estadístico similar a métodos de Montecarlo para calcular la **Probabilidad de Éxito**:

1. **Siembra Probabilística (Esconder a las víctimas):** El evaluador extrae el Mapa de Calor (Heatmap) generado en pasos anteriores, el cual contiene las probabilidades topológicas. A continuación, el generador esparce en el mapa **100 víctimas diferentes e independientes (100 simulaciones matemáticas simultáneas)** de una persona perdida. Estas 100 víctimas no caen al azar: se esconden en el mapa obedeciendo escrupulosamente a la densidad de calor. Por ejemplo, en terrenos de alto interés estadístico (caminos o ríos) caerán en un gran porcentaje, y las zonas "frías" se llevarán un número menor de estas víctimas. *(Ver Snippet 5.1)*
2. **Evaluación de Algoritmos:** Cada vez que el sensor del algoritmo de drones barre una celda y detecta a una de estas "víctimas", suma `+1` a su contador de aciertos.
3. **Generación de Curvas (Gráficas de Éxito):** Al agotarse la batería (`budget`), el simulador divide las víctimas encontradas entre las 100 totales que había escondido en ese entorno. Si un patrón de búsqueda localizó a 70 de esas 100 víctimas repartidas por la topografía, los gráficos generados dictaminarán que, ante un rescate real en ese terreno con ese algoritmo, **se tiene un 70% estadístico de Probabilidad Localizada (Probability of Success).**

**Snippet 5.1: Siembra probabilística de Víctimas (`sarenv/core/lost_person.py`, función `generate_locations`, aprox. línea 58):**
*Aquí se ve cómo el simulador usa `random.choices` apoyándose en los pesos de probabilidad (`type_probabilities`) para esconder a cada "clon" (`n`). Se elige un tipo de característica topográfica (ej: un edificio, un río), y luego se planta un punto aleatorio muy cerca usando un buffer geométrico.*
```python
while len(locations) < n:
    # Seleccionan una capa geográfica aleatoria pesada por su probabilidad teórica
    chosen_type = random.choices(
        list(self.type_probabilities.keys()),
        weights=list(self.type_probabilities.values()),
        k=1
    )[0]
    
    # Filtran la base de datos geográfica para sacar solo los caminos, o los bosques, etc.
    type_gdf = self.features[self.features['feature_type'] == chosen_type]
    
    # Extraen una sola geometría aleatoria pesada por su 'area_probability' (el calor)
    chosen_feature = type_gdf.sample(n=1, weights='area_probability').iloc[0]
    
    # Generan el punto de escondite (clon/víctima) pegadito a esa característica topográfica (buffer 15m)
    feature_buffer = chosen_feature.geometry.buffer(15)
    final_search_area = feature_buffer.intersection(main_search_circle)

    point = self._generate_random_point_in_polygon(final_search_area)
    locations.append(point)
```

---

## Tabla Resumen de Conceptos Clave de SAREnv (Puntos 1 al 5)

A continuación se condensan y resumen los 4 pilares fundamentales de cómo SAREnv procesa e integra la información del entorno:

| Punto | Concepto Principal | Resumen de Funcionamiento en SAREnv | Módulos Principales |
| :---: | :--- | :--- | :--- |
| **1. Definición del Espacio** | Polígonos de Borde (Bbox) y Recorte | Se traza un polígono geométrico base (mediante radio desde un punto o coordenadas a medida). El sistema asegura descartar toda la basura geográfica fuera del límite mediante `shapely.intersection()`. | Scripts de usuario (ej: `examples/X`), `shapely`, `osm_query.py` |
| **2. Sectorización** | Grid 2D y `meter_per_bin` | El espacio vectorizado se convierte en una malla discreta. Se usa el parámetro de resolución `meter_per_bin` para decidir el tamaño físico real (en metros) que representa cada celda/píxel de la matriz. | `core/generation.py` (Clase `DataGenerator`) |
| **3. Capas e Integración** | Capas de OSM y Mapa de Calor (Heatmap) | Diferencia terrenos urbanos (`building`, `highway`) o naturales (`water`, `wood`). Crea mapas superpuestos y los pondera por su estadística (`FEATURE_PROBABILITIES`). Luego los fusiona aplicando el valor máximo (`np.maximum`). | `core/generation.py`, `utils/lost_person_behavior.py` |
| **4. Parámetros** | Configuración de Clima, Variables y Drones | Controlan desde el terreno (`climate`, `environment_type`) hasta las variables simuladas como el límite de batería del dron (`budget`), el nº de drones (`n_agents`) y el nº de simulaciones a plantar (`n`). | `analytics.evaluator`, `core.lost_person` |
| **5. Simulación (Montecarlo)** | `n` víctimas (Clones estadísticos) y Puntos/Éxito | SAREnv extrae el Mapa de Calor (Probabilidades) y en lugar de buscar a 1 víctima, simula perderla 100 veces en 100 sitios diferentes proporcionalmente al calor. Las "víctimas encontradas" (hasta la rotura de batería) entre las 100 totales forman el % real que salva de los algoritmos simulados. | `analytics.evaluator`, Generador Gráficas |

---