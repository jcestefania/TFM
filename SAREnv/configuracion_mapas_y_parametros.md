# Configuración de Mapas y Parámetros en SAREnv

### 1. Cómo se generan los mapas de probabilidades (Heatmaps)

**Dónde:** [sarenv/core/generation.py](sarenv/core/generation.py) (dentro de `get_combined_heatmap()`) y [sarenv/utils/lost_person_behavior.py](sarenv/utils/lost_person_behavior.py).

**Explicación:** Se generan pequeñas matrices (grids) por cada tipo de elemento del mapa (ríos, carreteras, etc.), se multiplican por su probabilidad de encontrar a una persona en ellos (según `FEATURE_PROBABILITIES`) y luego se hace un "máximo" de todos estos mapas superpuestos para tener el mapa de calor final. Las descargas del mapa, en la clase `Environment`, usan los métodos como `generate_heatmap_task()` para convertir las geometrías en píxeles.

**Código (`generation.py` en la línea ~431):**
```python
        combined_heatmap = np.zeros(
            (len(self.yedges) - 1, len(self.xedges) - 1), dtype=float
        )

        for key, individual_heatmap in self.heatmaps.items():
            if individual_heatmap is None:
                continue

            # Se coge el peso de probabilidad estadístico del diccionario
            alpha = FEATURE_PROBABILITIES.get(key, 0)
            
            # Se multiplica la probabilidad por las zonas donde está el objeto (río, calle...)
            filtered_heatmap_part = individual_heatmap.astype(float) * alpha    

            # Se fusionan usando np.maximum para no diluir probabilidades si un objeto pisa a otro
            combined_heatmap = np.maximum(combined_heatmap, filtered_heatmap_part)

        return combined_heatmap
```

---

### 2. Número y Generación de Víctimas

**Dónde:** [sarenv/core/lost_person.py](sarenv/core/lost_person.py) (clase `LostPersonLocationGenerator`). Puedes ver cómo instanciarlo en [examples/03_generate_survivors.py](examples/03_generate_survivors.py).

**Explicación:** El número de víctimas es tan simple como pasarle el parámetro `n` al llamar a `.generate_locations(n=100)`. La generación busca un punto al azar dentro de las zonas probables, aplicando el método tipo "ruleta" con `random.choices()`. Internamente, una función _calculate_weights()` hace un sumatorio de probabilidades por polígonos del mapa.

**Código (`lost_person.py` desde la línea ~58):**
```python
        while len(locations) < n: # El bucle funciona hasta alcanzar el nº de víctimas 'n'
            # 1. Se selecciona un tipo de terreno dándole ventaja a los terrenos calientes mediante "weights"
            chosen_type = random.choices(
                list(self.type_probabilities.keys()),
                weights=list(self.type_probabilities.values()),
                k=1
            )[0]
            
            # 2. Nos quedamos solo con las geografías de ese tipo (ej: Ríos) 
            type_gdf = self.features[self.features['feature_type'] == chosen_type] 
            
            # 3. Y finalmente cogemos una zona aleatoria específica de ese tipo
            chosen_feature = type_gdf.sample(n=1, weights='area_probability').iloc[0]                                                                                       
            feature_buffer = chosen_feature.geometry.buffer(15) # Damos 15 metros de margen (buffer)

            final_search_area = feature_buffer.intersection(main_search_circle)                                                                             

            # 4. Inyectamos las coordenadas XY (Point) dentro del polígono resultante
            point = self._generate_random_point_in_polygon(final_search_area)   
            if point:
                locations.append(point)
```

---

### 3. Las llamadas a OpenStreetMap

**Dónde:** [sarenv/io/osm_query.py](sarenv/io/osm_query.py) (función `query_features`).

**Explicación:** El framework usa la librería especializada OSMnx (`ox`) para descargar datos de OpenStreetMap. Una vez se descarga ese recuadro de mapa en bruto (en formato lat/lon estándar u `EPSG:4326` basado en etiquetas semánticas configuradas en `generation.py` como `{"building": True}`), el código lo recorta físicamente aplicando `shapely.intersection()` para quitar basura extra.

**Código (`osm_query.py` sobre la línea ~37):**
```python
    try:
        # Se solicita la información al API de OSM usando el polígono y las etiquetas (ej. 'building': True)
        raw_osm_geometries_gdf = ox.features_from_polygon(
            area_geopolygon.get_geometry(), 
            tags=tags_to_query
        )
    except Exception as e:
        log.warning("An error occurred while querying features from OSM: %s", str(e))
        return None

    # [...] Múltiples comprobaciones de nulos [...]
    
    # Convierte todo a una masa gigante de polígonos
    consolidated_geometry = raw_osm_geometries_gdf.geometry.unary_union
    
    # Recorta (intersection) la geometría descargada para que encaje EXACTAMENTE 
    # dentro del escenario del simulador y no tengamos información fuera de la pantalla
    final_features_geom = shapely.intersection(
        area_geopolygon.get_geometry(), 
        consolidated_geometry
    )
```

---

### 4. Configuración de drones, algoritmos exhaustivos y control de presupuestos
**Dónde:** Principalmente en la librería de algoritmos de drones [sarenv/analytics/paths.py](sarenv/analytics/paths.py). Para ver cómo configurarlos, revisa [examples/04_evaluate_coverage_paths.py](examples/04_evaluate_coverage_paths.py).

**Explicación:** Se configura muy fácilmente el número de drones a través de una clase "Evaluator" global (`num_drones=3, num_lost_persons=100, budget=350000`). En cuanto a implementaciones, se usan algoritmos exhaustivos como `generate_spiral_path`, `generate_concentric_circles_path` o `generate_pizza_zigzag_path`. Estos algoritmos generan una trayectoria de vuelo gigante para 1 solo dron y luego `split_path_for_drones()` lo parte en trozos perfectamente proporcionales según la batería/autonomía de configuración (`budget`).

**Código (`paths.py`):**
```python
# Ejemplo de cómo la ruta se corta por drone (~ línea 9)
def split_path_for_drones(path: LineString, num_drones: int) -> list[LineString]:                                                                                   
    if num_drones <= 1 or path.is_empty or path.length == 0:
        return [path]
    segments = []
    # Divide equitativamente los metros totales entre los drones solicitados
    segment_length = path.length / num_drones
    for i in range(num_drones):
        segments.append(substring(path, i * segment_length, (i + 1) * segment_length))                                                                              
    return segments

# Dentro de cualquier algoritmo (Ej. 'generate_spiral_path' línea ~32)
# Apply budget constraint if specified - trim excess points
if budget is not None and budget > 0:
    # Se impone que ningún dron vuele por encima de la autonomía max (presupuesto)
    paths = restrict_path_length(paths, budget / num_drones)
```

---

### 5. Tamaño y Resolución del Mapa

**Dónde:** [sarenv/core/generation.py](sarenv/core/generation.py), [sarenv/utils/lost_person_behavior.py](sarenv/utils/lost_person_behavior.py) y [examples/01_generate_sar_data.py](examples/01_generate_sar_data.py).

**Explicación:** Los tamaños se pasan como etiquetas tipo `"small"`, `"medium"`, `"large"` o `"xlarge"`. Estas etiquetas se transforman en radios en Km reales mediante la función `get_environment_radius_by_size()` basándose en listas estadísticas de distancias en función del clima y del terreno. La resolución (discretización) se define usando el parámetro `meter_per_bin` (por defecto a `30`), lo cual define cuántos metros cuadrados representan cada píxel de las matrices NumPy del heatmap.

---

### 6. Origen y "Spawn" de los Drones

**Dónde:** [sarenv/analytics/evaluator.py](sarenv/analytics/evaluator.py) y [sarenv/analytics/paths.py](sarenv/analytics/paths.py).

**Explicación:** Los drones no despegan de un "punto base" lejano (Home base). Spawnean directamente en el inicio del segmento de búsqueda que les ha tocado.
* El punto inicial siempre arranca calculando el origen del mapa geográfico `center_proj` para pasarlo a la función generadora `(center_x, center_y)`.
* Cuando termina de dibujarse el patrón maestro completo, la función `split_path_for_drones()` "corta la cuerda", y entrega los segmentos resultantes.
* Cada dron invocado comienza a operar donde indica el primer punto topológico de su propio trozo (Es decir, el Dron 2 spawnea donde finaliza el trayecto del Dron 1).

**Código (evaluator.py y paths.py combinados):**
```python
# Saca el centro desde el cargador de mapas
center_proj = gpd.GeoDataFrame(geometry=[Point(item.center_point)], crs="EPSG:4326").to_crs(env_data["crs"]).geometry.iloc[0]

# La ruta completa se origina basándose en center_proj.x y center_proj.y
full_path = LineString(zip(
    center_x + radius * np.cos(theta), 
    center_y + radius * np.sin(theta), 
    strict=True
))                                                  

# Al realizar el corte de la ruta gigante, se define implícitamente dónde aparece cada drone!
def split_path_for_drones(path: LineString, num_drones: int) -> list[LineString]:                                                                                   
    segments = []
    segment_length = path.length / num_drones

    for i in range(num_drones):
        # El 1er punto de cada "substring" calculado aquí, es el punto físico de Spawn del dron
        segments.append(substring(path, i * segment_length, (i + 1) * segment_length))                                                                              
    return segments
```