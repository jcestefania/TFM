import os
from sarenv import (
    CLIMATE_TEMPERATE,
    ENVIRONMENT_TYPE_FLAT,
    DataGenerator,
    get_logger,
)

log = get_logger()

def generar_por_punto():
    """
    Genera el entorno a partir de un único punto central (PLS - Point Last Seen).
    El framework descargará un área circular alrededor de este punto.
    """
    log.info("--- Generación de Entorno por Punto LKP: Casa de Campo ---")
    data_gen = DataGenerator()
    
    # Coordenada exacta del punto donde se vio a la persona por última vez (PLS)
    # Por ejemplo: cerca del Lago de la Casa de Campo
    punto_inicial = (-3.7337, 40.4187) # (Longitud, Latitud)

    # Carpeta distinta para no mezclar con la prueba del polígono
    output_dir = "resultados_casa_de_campo_punto"

    log.info(f"1. Descargando el entorno asumiendo el punto central en {punto_inicial}")
    
    # Exportamos el mapa basado únicamente en el punto central.
    # El framework calculará la zona necesaria según las probabilidades.
    data_gen.export_dataset(
        center_point=punto_inicial,
        output_directory=output_dir,
        environment_climate=CLIMATE_TEMPERATE,
        environment_type=ENVIRONMENT_TYPE_FLAT,
        meter_per_bin=20,
    )

    log.info(f"--- Generación Completada. Resultados extraídos en la carpeta '{output_dir}' ---")

if __name__ == "__main__":
    generar_por_punto()