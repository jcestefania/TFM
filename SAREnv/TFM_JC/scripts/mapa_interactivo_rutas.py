import os
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyproj import Transformer
from shapely.geometry import Point
import geopandas as gpd
from sarenv import DatasetLoader, get_logger
from sarenv.utils.geo import get_utm_epsg
from sarenv.analytics.evaluator import ComparativeEvaluator

log = get_logger()

def generar_mapas_por_algoritmo_final_pro():
    output_dir = "TFM_JC/resultados/casa_de_campo"
    # Carpeta específica para los mapas interactivos
    html_plots_dir = os.path.join(output_dir, "path_plots_html")
    os.makedirs(html_plots_dir, exist_ok=True)
    
    loader = DatasetLoader(dataset_directory=output_dir)
    item = loader.load_environment("large")
    if not item: return

    # 1. Configuración de Coordenadas
    data_crs = get_utm_epsg(item.center_point[0], item.center_point[1])
    transformer = Transformer.from_crs(data_crs, "EPSG:4326", always_xy=True)
    
    # 2. Datos del Heatmap
    rows, cols = item.heatmap.shape
    x_coords = np.linspace(item.bounds[0], item.bounds[2], cols)
    y_coords = np.linspace(item.bounds[1], item.bounds[3], rows)
    lons, lats, probs = [], [], []
    for r in range(0, rows, 2): 
        for c in range(0, cols, 2):
            p = item.heatmap[r, c]
            if p > 1e-7:
                lon, lat = transformer.transform(x_coords[c], y_coords[r])
                lons.append(lon); lats.append(lat); probs.append(p)
    
    df_heatmap = pd.DataFrame({'lat': lats, 'lon': lons, 'prob': probs})

    # 3. Evaluador y Colores "Aviation Pro"
    evaluator = ComparativeEvaluator(dataset_directory=output_dir, num_drones=3, budget=450000)
    center_proj = gpd.GeoDataFrame(geometry=[Point(item.center_point)], crs="EPSG:4326").to_crs(data_crs).geometry.iloc[0]
    
    # Paleta técnica: Azul Zafiro, Verde Bosque, Índigo
    colores_drones = ['#0F52BA', '#228B22', '#4B0082'] 
    nombres_colores = ['Azul Zafiro', 'Verde Bosque', 'Índigo']

    # 4. Generación de mapas
    for name, generator in evaluator.path_generators.items():
        print(f"Generando mapa Pro para: {name}...")
        
        fig = px.density_map(
            df_heatmap, lat='lat', lon='lon', z='prob', radius=10,
            center=dict(lat=item.center_point[1], lon=item.center_point[0]),
            zoom=13, map_style="open-street-map", opacity=0.4,
            color_continuous_scale="YlOrRd", title=f"SAR MISSION PLANNING: {name.upper()} STRATEGY"
        )

        fig.update_layout(
            # Colorbar a la izquierda para no estorbar a la leyenda de drones
            coloraxis_colorbar=dict(
                title='Probabilidad',
                thickness=15,
                len=0.5,
                x=-0.12, 
                xanchor='right',
                y=0.5,
                yanchor='middle'
            ),
            legend=dict(
                title="Swarm Fleet (3 Agents)",
                yanchor="top", y=0.99,
                xanchor="right", x=0.99,
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor="DarkSlateGray",
                borderwidth=2
            ),
            margin=dict(l=100, r=20, t=60, b=20)
        )

        path_meters = generator(center_proj.x, center_proj.y, item.radius_km * 1000, item.heatmap, item.bounds)
        
        for i, drone_path in enumerate(path_meters):
            path_coords = list(drone_path.coords)
            p_lons, p_lats = [], []
            for cx, cy in path_coords:
                plon, plat = transformer.transform(cx, cy)
                p_lons.append(plon); p_lats.append(plat)
            
            fig.add_trace(go.Scattermap(
                lon=p_lons, lat=p_lats, mode='lines',
                line=dict(width=4, color=colores_drones[i]),
                name=f"Drone {i+1} ({nombres_colores[i]})",
            ))

        # Guardado organizado
        filename = f"mission_{name}_pro.html"
        path_html = os.path.join(html_plots_dir, filename)
        fig.write_html(path_html)
        print(f"-> Mapa guardado en: {path_html}")
        fig.show()

generar_mapas_por_algoritmo_final_pro()
