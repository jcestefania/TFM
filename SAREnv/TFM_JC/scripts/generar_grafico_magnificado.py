import os
import matplotlib.pyplot as plt
from sarenv import DatasetLoader, get_logger, visualize_heatmap

log = get_logger()

def generar_grafico_magnificado():
    """
    Genera la visualización profesional con círculos de radio (RoIs)
    y zoom lateral para la Casa de Campo.
    """
    # RUTA ACTUALIZADA A TFM_JC
    dataset_dir = "TFM_JC/resultados/casa_de_campo"
    output_dir = "TFM_JC/resultados/casa_de_campo"
    
    if not os.path.exists(dataset_dir):
        log.error(f"No se encuentra la carpeta {dataset_dir}. Ejecuta primero generar_casa_de_campo.py")
        return

    # 1. Cargar el dataset (usamos large para el zoom, pero xlarge para ver todos los radios si existen)
    log.info(f"Cargando datos desde {dataset_dir}...")
    loader = DatasetLoader(dataset_directory=dataset_dir)
    
    # Intentamos cargar 'xlarge' para que el gráfico muestre todos los círculos posibles
    item = loader.load_environment("xlarge")
    
    if not item:
        log.warning("No se pudo cargar 'xlarge', intentando con 'large'...")
        item = loader.load_environment("large")

    if not item:
        log.error("No se pudo cargar ningún entorno válido.")
        return

    # 2. Generar la visualización "Magnified Heatmap" oficial
    log.info("Generando visualización profesional con zoom lateral...")
    
    # Esta función de SAREnv genera un PDF llamado 'heatmap_{size}_magnified.pdf'
    visualize_heatmap(item, plot_basemap=True, plot_inset=True)
    
    # 3. Mover el archivo generado a la carpeta de resultados del TFM
    filename = f"heatmap_{item.size}_magnified.pdf"
    if os.path.exists(filename):
        dest_path = os.path.join(output_dir, filename)
        if os.path.exists(dest_path):
            os.remove(dest_path)
        os.rename(filename, dest_path)
        log.info(f"--- ¡LISTO! ---")
        log.info(f"Gráfico guardado en: {dest_path}")
    else:
        log.error(f"No se encontró el archivo '{filename}'. Revisa la carpeta raíz.")

if __name__ == "__main__":
    generar_grafico_magnificado()
