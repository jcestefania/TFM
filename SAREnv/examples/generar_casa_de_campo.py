import os
import shapely
import geopandas as gpd
import numpy as np
from sarenv import (
    CLIMATE_TEMPERATE,
    ENVIRONMENT_TYPE_FLAT,
    DataGenerator,
    get_logger,
)

log = get_logger()

def generar_casa_de_campo():
    """
    Genera el entorno de prueba para la Casa de Campo (Madrid)
    para poder capturar las pantallas del TFM.
    """
    log.info("--- Iniciando Generación de Entorno: Casa de Campo (Madrid) ---")

    data_gen = DataGenerator()

    # Coordenadas aproximadas de la Casa de Campo en Madrid (Longitud, Latitud)
    # Formamos un polígono rectangular más amplio que abarque TODO el parque real
    polygon_coords = [
        [-3.785, 40.395],  # Suroeste (Pegado a la m-40 y Somosaguas)
        [-3.720, 40.395],  # Sureste (Pegado a Madrid Río / Príncipe Pío)
        [-3.720, 40.440],  # Noreste (Ciudad Universitaria / A-6)
        [-3.785, 40.440],  # Noroeste (Aravaca)
        [-3.785, 40.395],  # Cierre
    ]

    casa_de_campo_poly = shapely.geometry.Polygon(polygon_coords)
    output_dir = "resultados_casa_de_campo"

    log.info("1. Definiendo y sectorizando el Espacio de Búsqueda de Madrid")
    
    # Exportamos el mapa de la Casa de Campo
    data_gen.export_dataset_from_polygon(
        polygon=casa_de_campo_poly,
        output_directory=output_dir,
        environment_climate=CLIMATE_TEMPERATE,
        environment_type=ENVIRONMENT_TYPE_FLAT,
        meter_per_bin=20,  # 20 metros por píxel para mayor resolución en el pantallazo
    )

    log.info("--- Generación Completada. Revisa los archivos en la carpeta 'resultados_casa_de_campo' ---")

if __name__ == "__main__":
    generar_casa_de_campo()
