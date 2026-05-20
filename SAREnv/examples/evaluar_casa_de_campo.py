import os
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point

import sarenv
from sarenv.analytics.evaluator import ComparativeEvaluator
from sarenv.analytics import metrics
from sarenv.utils import plot
from tqdm.auto import tqdm

log = sarenv.get_logger()

def evaluar_casa_de_campo():
    """
    Ejecuta una evaluación de rutas sobre el entorno generado de la Casa de Campo.
    Aquí puedes experimentar con los parámetros de la simulación.
    """
    log.info("--- Iniciando Evaluación en la Casa de Campo ---")
    data_dir = "resultados_casa_de_campo"  # Carpeta donde están el geojson y el npy

    # Verificar que existen los datos
    if not os.path.exists(data_dir):
        log.error(f"No se encontró la carpeta '{data_dir}'. Ejecuta primero 'generar_casa_de_campo.py'")
        return

    # 1. Configuración de Parámetros (¡AQUÍ PUEDES JUGAR!)
    num_drones = 3              # Número de agentes/drones simultáneos
    num_lost_persons = 100      # Número de supervivientes simulados a repartir según probabilidad
    budget_meters = 1500000     # ¡Subimos aún MÁS la batería! Al haber agrandado el mapa 5 veces, necesitan más alcance. 
    
    # En un polígono cerrado queremos evaluar TODO el recinto.
    # Usamos 'xlarge' y 'large' dado que el tamaño del polígono ahora es masivo
    tamaños_a_evaluar = ["large", "xlarge"] 

    # Inicializar el evaluador
    evaluator = ComparativeEvaluator(
        dataset_directory=data_dir,
        evaluation_sizes=tamaños_a_evaluar,
        num_drones=num_drones,
        num_lost_persons=num_lost_persons,
        budget=budget_meters,
    )

    # 2. Correr la Simulación (Evalúa algoritmos como Creeping Line, Spiral, etc.)
    log.info("--- Evaluando Algoritmos de Cobertura ---")
    baseline_results, time_series_data = evaluator.run_baseline_evaluations()

    # 3. Mostrar Gráficas de Resultados (Éxito vs Distancia/Tiempo)
    log.info("--- Generando y Guardando Gráficas Estadísticas ---")
    graphs_dir = "resultados_casa_de_campo/graphs"
    os.makedirs(graphs_dir, exist_ok=True)
    evaluator.plot_results(baseline_results, output_dir=graphs_dir)
    log.info(f"-> Gráficas generadas en: {graphs_dir}")

    # 4. Generar PDFs con el trazado de la ruta sobre el Mapa (Heatmap + Rutas)
    log.info("--- Generando Visualizaciones de las Rutas ---")
    output_dir = Path("resultados_casa_de_campo/paths_plots")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Iterar sobre los mapas generados y los algoritmos evaluados para pintarlos
    for size, env_data in tqdm(evaluator.environments.items(), desc="Mapas a evaluar"):
        item = env_data["item"]
        
        # Obtenemos el punto central en coordenadas proyectadas
        center_proj = (
            gpd.GeoDataFrame(geometry=[Point(item.center_point)], crs="EPSG:4326")
            .to_crs(env_data["crs"])
            .geometry.iloc[0]
        )

        for name, generator in tqdm(evaluator.path_generators.items(), desc=f"Generando rutas ({size})", leave=False):
            log.info(f"Pintando la ruta del algoritmo '{name}' para tamaño '{size}'...")

            # Generamos de nuevo la ruta para poder dibujarla encima del mapa
            generated_paths = generator(
                center_proj.x,
                center_proj.y,
                item.radius_km * 1000,
                item.heatmap,
                item.bounds,
            )

            x_min, y_min, x_max, y_max = item.bounds
            output_file = output_dir / f"{name}_casa_de_campo_ruta_{size}.pdf"

            plot.plot_heatmap(
                item=item,
                generated_paths=generated_paths,
                name=f"{name} en Casa de Campo ({size})",
                x_min=x_min,
                x_max=x_max,
                y_min=y_min,
                y_max=y_max,
                output_file=output_file
            )

            log.info(f"Guardado mapa con ruta: {output_file}")
            
    log.info("--- ¡Evaluación Finalizada con Éxito! ---")

if __name__ == "__main__":
    evaluar_casa_de_campo()