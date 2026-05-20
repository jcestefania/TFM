import os
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point

import sarenv
from sarenv.analytics.evaluator import ComparativeEvaluator
from sarenv.utils import plot
from tqdm.auto import tqdm

log = sarenv.get_logger()

def evaluar_por_punto():
    """
    Evalúa algoritmos sobre el mapa generado a partir del Punto Único.
    Aquí los recortes 'medium' (1.8km) o 'large' (3.2km) recortan un círculo 
    alrededor de ese punto inicial y asumen que puede huir en 360 grados.
    """
    log.info("--- Iniciando Evaluación desde Punto Central (LKP) ---")
    data_dir = "resultados_casa_de_campo_punto"

    if not os.path.exists(data_dir):
        log.error(f"Carpeta '{data_dir}' no encontrada. Ejecuta primero 'generar_casa_de_campo_punto.py'")
        return

    num_drones = 3
    num_lost_persons = 100
    budget_meters = 250000
    
    # Al ser un punto abierto (sin muros perimetrales de polígono), vamos a recortar 
    # los círculos en orden expansivo real (LPB):
    # small (0.6km) -> medium (1.8km) -> large (3.2km) -> xlarge (9.9km)
    tamaños_a_evaluar = ["small", "medium", "large", "xlarge"]

    evaluator = ComparativeEvaluator(
        dataset_directory=data_dir,
        evaluation_sizes=tamaños_a_evaluar,
        num_drones=num_drones,
        num_lost_persons=num_lost_persons,
        budget=budget_meters,
    )

    log.info("--- Evaluando Algoritmos (Espiral, Zonas, etc...) ---")
    baseline_results, time_series_data = evaluator.run_baseline_evaluations()

    log.info("--- Generando Gráfica Visual ---")
    graphs_dir = "resultados_casa_de_campo_punto/graphs"
    os.makedirs(graphs_dir, exist_ok=True)
    evaluator.plot_results(baseline_results, output_dir=graphs_dir)
    log.info(f"-> Gráficas generadas en: {graphs_dir}")

    log.info("--- Generando Visualizaciones de las Rutas sobre el Heatmap ---")
    output_dir = Path("resultados_casa_de_campo_punto/paths_plots")
    output_dir.mkdir(parents=True, exist_ok=True)

    for size, env_data in tqdm(evaluator.environments.items(), desc="Mapas a evaluar por LKP"):
        item = env_data["item"]
        center_proj = (
            gpd.GeoDataFrame(geometry=[Point(item.center_point)], crs="EPSG:4326")
            .to_crs(env_data["crs"])
            .geometry.iloc[0]
        )

        for name, generator in tqdm(evaluator.path_generators.items(), desc=f"Generando rutas LKP ({size})", leave=False):
            generated_paths = generator(
                center_proj.x,
                center_proj.y,
                item.radius_km * 1000,
                item.heatmap,
                item.bounds,
            )

            x_min, y_min, x_max, y_max = item.bounds
            
            output_file = output_dir / f"{name}_punto_{size}_{num_drones}drones_{budget_meters}m.pdf"

            plot.plot_heatmap(
                item=item,
                generated_paths=generated_paths,
                name=f"{name} desde un PLS exacto ({size} - {num_drones} Drones)",
                x_min=x_min,
                x_max=x_max,
                y_min=y_min,
                y_max=y_max,
                output_file=output_file
            )

    log.info("--- Evaluación finalizada. Revisa los PDFs en 'resultados_casa_de_campo_punto/paths_plots' ---")

if __name__ == "__main__":
    evaluar_por_punto()