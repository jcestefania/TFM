import os
import shapely
import numpy as np
import osmnx as ox
from sarenv import (
    CLIMATE_TEMPERATE,
    ENVIRONMENT_TYPE_FLAT,
    DataGenerator,
    get_logger,
)
from sarenv.core.loading import DatasetLoader
from sarenv.utils.geo import get_utm_epsg
from pyproj import Transformer

log = get_logger()

# Configuración OSMnx
ox.settings.timeout = 300  
ox.settings.request_retries = 5  

def generar_casa_de_campo():
    """
    Genera el entorno de la Casa de Campo usando el polígono exacto de Google Earth.
    """
    log.info("--- Iniciando Generación de Entorno (TFM_JC) ---")

    data_gen = DataGenerator()

    polygon_coords = [
        [-3.753046089833776, 40.44343778644211],
        [-3.771067897299357, 40.43808936530237],
        [-3.780967823387276, 40.41887000168707],
        [-3.773618938561301, 40.40203996553611],
        [-3.724145972222016, 40.41588490845162],
        [-3.753046089833776, 40.44343778644211]
    ]

    casa_de_campo_poly = shapely.geometry.Polygon(polygon_coords)
    
    # NUEVA RUTA ORGANIZADA
    output_dir = "TFM_JC/resultados/casa_de_campo"
    os.makedirs(output_dir, exist_ok=True)

    log.info(f"Exportando dataset a {output_dir}...")
    data_gen.export_dataset_from_polygon(
        polygon=casa_de_campo_poly,
        output_directory=output_dir,
        environment_climate=CLIMATE_TEMPERATE,
        environment_type=ENVIRONMENT_TYPE_FLAT,
        meter_per_bin=20,
    )

    log.info("--- Generación Completada en TFM_JC ---")

if __name__ == "__main__":
    generar_casa_de_campo()
