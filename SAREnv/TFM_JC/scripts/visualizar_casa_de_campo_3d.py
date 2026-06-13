import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sarenv import DatasetLoader, get_logger

log = get_logger()

def create_3d_heatmap_matplotlib(heatmap, bounds, title="Casa de Campo 3D"):
    """Crea una vista 3D usando matplotlib."""
    minx, miny, maxx, maxy = bounds
    x = np.linspace(minx, maxx, heatmap.shape[1])
    y = np.linspace(miny, maxy, heatmap.shape[0])
    X, Y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # Superficie con la escala de colores correcta
    surf = ax.plot_surface(X, Y, heatmap, cmap='YlOrRd', alpha=0.9,
                          linewidth=0, antialiased=True)
    
    ax.set_title(title)
    ax.view_init(elev=30, azim=45)
    plt.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Densidad de Probabilidad')
    return fig

def create_3d_heatmap_plotly(heatmap, bounds):
    """Crea un mapa 3D interactivo usando Plotly."""
    minx, miny, maxx, maxy = bounds
    x = np.linspace(minx, maxx, heatmap.shape[1])
    y = np.linspace(miny, maxy, heatmap.shape[0])

    fig = go.Figure(data=[go.Surface(
        x=x, y=y, z=heatmap,
        colorscale='YlOrRd',
        colorbar=dict(title='Probabilidad')
    )])

    fig.update_layout(
        title='Casa de Campo - Probabilidad 3D Interactiva',
        scene=dict(
            xaxis_title='Easting (m)',
            yaxis_title='Northing (m)',
            zaxis_title='Probabilidad'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    return fig

def visualizar_3d_resultados():
    # RUTA ACTUALIZADA A TFM_JC
    output_dir = "TFM_JC/resultados/casa_de_campo"
    
    if not os.path.exists(output_dir):
        log.error(f"No se encuentra la carpeta {output_dir}. Ejecuta primero generar_casa_de_campo.py")
        return

    # 1. Cargar el dataset (usamos large para que sea más ligero el 3D)
    log.info(f"Cargando datos desde {output_dir}...")
    loader = DatasetLoader(dataset_directory=output_dir)
    item = loader.load_environment("large")
    
    if not item:
        log.error("No se pudo cargar el entorno 'large'.")
        return

    log.info(f"Visualizando heatmap 3D de tamaño: {item.heatmap.shape}")

    # 2. Visualización Matplotlib (Estática)
    log.info("Generando vista 3D estática...")
    fig_mpl = create_3d_heatmap_matplotlib(item.heatmap, item.bounds)
    path_static = os.path.join(output_dir, "casa_de_campo_3d_static.png")
    plt.savefig(path_static)
    log.info(f"Imagen guardada en: {path_static}")

    # 3. Visualización Plotly (Interactiva)
    log.info("Generando vista 3D interactiva (HTML)...")
    fig_plotly = create_3d_heatmap_plotly(item.heatmap, item.bounds)
    path_html = os.path.join(output_dir, "casa_de_campo_3d_interactivo.html")
    fig_plotly.write_html(path_html)
    log.info(f"Mapa interactivo guardado en: {path_html}")
    
    # Intentar mostrarlo
    fig_plotly.show()

if __name__ == "__main__":
    visualizar_3d_resultados()
