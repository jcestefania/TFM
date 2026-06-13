import os
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyproj import Transformer
from sarenv import DatasetLoader, get_logger
from sarenv.utils.geo import get_utm_epsg

log = get_logger()

def verificar_geografia_interactiva():
    # RUTA ACTUALIZADA
    output_dir = "TFM_JC/resultados/casa_de_campo"
    
    if not os.path.exists(output_dir):
        log.error(f"No se encuentra la carpeta {output_dir}")
        return

    loader = DatasetLoader(dataset_directory=output_dir)
    item = loader.load_environment("large") 
    
    if not item: return

    features_path = os.path.join(output_dir, "features.geojson")
    boundary_geom = None
    if os.path.exists(features_path):
        with open(features_path, 'r') as f:
            geojson_data = json.load(f)
        for feat in geojson_data['features']:
            if feat['id'] == 'boundary':
                boundary_geom = feat['geometry']
                break

    epsg_code = get_utm_epsg(item.center_point[0], item.center_point[1])
    transformer = Transformer.from_crs(epsg_code, "EPSG:4326", always_xy=True)
    
    heatmap = item.heatmap
    step = 2
    rows, cols = heatmap.shape
    x_coords = np.linspace(item.bounds[0], item.bounds[2], cols)
    y_coords = np.linspace(item.bounds[1], item.bounds[3], rows)
    
    lons, lats, probs = [], [], []
    for r in range(0, rows, step):
        for c in range(0, cols, step):
            p = heatmap[r, c]
            if p > 1e-8:
                lon, lat = transformer.transform(x_coords[c], y_coords[r])
                lons.append(lon)
                lats.append(lat)
                probs.append(p)

    df = pd.DataFrame({'lon': lons, 'lat': lats, 'prob': probs})

    fig = px.density_mapbox(
        df, lat='lat', lon='lon', z='prob', radius=12,
        center=dict(lat=item.center_point[1], lon=item.center_point[0]), 
        zoom=13, mapbox_style="open-street-map", opacity=0.5,
        color_continuous_scale="YlOrRd", # Forzamos escala Amarillo-Naranja-Rojo
        range_color=[df['prob'].min(), df['prob'].max()], # Ajustamos el rango
        title="VERIFICACIÓN TFM_JC (TAMAÑO LARGE)"
    )

    if boundary_geom:
        coords = boundary_geom['coordinates'][0]
        fig.add_trace(go.Scattermapbox(
            lon=[c[0] for c in coords], lat=[c[1] for c in coords],
            mode='lines', line=dict(width=2, color='black'), # Borde negro más discreto
            name='Límite Casa de Campo'
        ))

    path_html = os.path.join(output_dir, "verificacion_TFM_JC.html")
    fig.write_html(path_html)
    log.info(f"Mapa generado: {path_html}")
    fig.show()

if __name__ == "__main__":
    verificar_geografia_interactiva()
