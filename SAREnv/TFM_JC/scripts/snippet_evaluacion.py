import os
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point
import sarenv
from sarenv.analytics.evaluator import ComparativeEvaluator
from sarenv.utils import plot
from tqdm.auto import tqdm

# 1. Configuración de parámetros REALISTAS (Optimizado para Casa de Campo)
data_dir = "TFM_JC/resultados/casa_de_campo"
base_tfm_dir = Path("TFM_JC/resultados/casa_de_campo")

num_drones = 3
num_lost_persons = 20   # 20 víctimas para un Montecarlo rápido y representativo
budget_meters = 450000  # 450 km: Presupuesto coherente con el área de 12.7 km²
tamaños_a_evaluar = ["large"] 

print("--- Iniciando Evaluación con Parámetros Reales (TFM_JC) ---")

# 2. Inicialización del Evaluador
evaluator = ComparativeEvaluator(
    dataset_directory=data_dir,
    evaluation_sizes=tamaños_a_evaluar,
    num_drones=num_drones,
    num_lost_persons=num_lost_persons,
    budget=budget_meters,
)

# 3. Ejecución de algoritmos base
print("Ejecutando trayectorias (Spiral, Concentric, Pizza)...")
baseline_results, _ = evaluator.run_baseline_evaluations()

# 4. Guardado de gráficas de rendimiento actualizadas
graphs_dir = base_tfm_dir / "graphs"
graphs_dir.mkdir(parents=True, exist_ok=True)
print(f"Exportando gráficas de rendimiento a {graphs_dir}...")
evaluator.plot_results(baseline_results, output_dir=str(graphs_dir))

# 5. Generación de las nuevas rutas (PDF) con el budget ajustado
print("Generando visualizaciones de rutas actualizadas en PDF...")
output_plots_dir = base_tfm_dir / "paths_plots"
output_plots_dir.mkdir(parents=True, exist_ok=True)

for size, env_data in tqdm(evaluator.environments.items(), desc="Mapas"):
    item = env_data["item"]
    data_crs = env_data["crs"]
    center_proj = gpd.GeoDataFrame(geometry=[Point(item.center_point)], crs="EPSG:4326").to_crs(data_crs).geometry.iloc[0]

    for name, generator in tqdm(evaluator.path_generators.items(), desc=f"Rutas {size}", leave=False):
        # El generador ahora usará los 450km de budget total
        generated_paths = generator(center_proj.x, center_proj.y, item.radius_km * 1000, item.heatmap, item.bounds)
        output_file = output_plots_dir / f"{name}_ruta_{size}.pdf"
        
        plot.plot_heatmap(
            item=item, generated_paths=generated_paths,
            name=f"{name} ({size})",
            x_min=item.bounds[0], x_max=item.bounds[2],
            y_min=item.bounds[1], y_max=item.bounds[3],
            output_file=output_file
        )

print(f"--- Proceso Completado. Resultados y PDFs actualizados en {base_tfm_dir} ---")
