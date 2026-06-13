import os
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point
import sarenv
from sarenv.analytics.evaluator import ComparativeEvaluator
from sarenv.utils import plot
from tqdm.auto import tqdm

log = sarenv.get_logger()

def evaluar_casa_de_campo():
    log.info("--- Iniciando Evaluación (TFM_JC) ---")
    
    # RUTAS ACTUALIZADAS
    data_dir = "TFM_JC/resultados/casa_de_campo"
    base_tfm_dir = Path("TFM_JC/resultados/casa_de_campo")

    if not os.path.exists(data_dir):
        log.error(f"No se encontró la carpeta '{data_dir}'. Ejecuta primero generar_casa_de_campo.py")
        return

    num_drones = 3
    num_lost_persons = 100
    budget_meters = 1500000 
    tamaños_a_evaluar = ["large"] 

    evaluator = ComparativeEvaluator(
        dataset_directory=data_dir,
        evaluation_sizes=tamaños_a_evaluar,
        num_drones=num_drones,
        num_lost_persons=num_lost_persons,
        budget=budget_meters,
    )

    log.info("--- Evaluando Algoritmos ---")
    baseline_results, _ = evaluator.run_baseline_evaluations()

    log.info("--- Guardando Gráficas ---")
    graphs_dir = base_tfm_dir / "graphs"
    graphs_dir.mkdir(parents=True, exist_ok=True)
    evaluator.plot_results(baseline_results, output_dir=str(graphs_dir))

    log.info("--- Generando Visualizaciones de Rutas ---")
    output_plots_dir = base_tfm_dir / "paths_plots"
    output_plots_dir.mkdir(parents=True, exist_ok=True)

    for size, env_data in tqdm(evaluator.environments.items(), desc="Mapas"):
        item = env_data["item"]
        data_crs = env_data["crs"]
        center_proj = gpd.GeoDataFrame(geometry=[Point(item.center_point)], crs="EPSG:4326").to_crs(data_crs).geometry.iloc[0]

        for name, generator in tqdm(evaluator.path_generators.items(), desc=f"Rutas {size}", leave=False):
            generated_paths = generator(center_proj.x, center_proj.y, item.radius_km * 1000, item.heatmap, item.bounds)
            output_file = output_plots_dir / f"{name}_ruta_{size}.pdf"
            
            plot.plot_heatmap(
                item=item, generated_paths=generated_paths,
                name=f"{name} ({size})",
                x_min=item.bounds[0], x_max=item.bounds[2],
                y_min=item.bounds[1], y_max=item.bounds[3],
                output_file=output_file
            )
            
    log.info(f"--- Fin de Evaluación. Resultados en {base_tfm_dir} ---")

if __name__ == "__main__":
    evaluar_casa_de_campo()
