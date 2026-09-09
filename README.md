# Optimizacion Inteligente de Rutas de Busqueda y Rescate con Drones mediante la Integracion de SAREnv y MTS en Entornos de Incertidumbre

**Trabajo de Fin de Master (TFM)**  
**Master Universitario en Robotica y Automatizacion**  
**Universidad Carlos III de Madrid (UC3M)**  
*Septiembre 2026*

**Autor:** Juan Carlos Estefania  
**Tutores:** Prof. Jesus Garcia Herrero & Prof. Juan Pedro Llerena Cana  
**Grupo de Investigacion:** Inteligencia Artificial Aplicada (GIAA) - UC3M  

---

## Enlaces del Proyecto

- **Rama oficial del software integrado en el laboratorio (GIAA):**  
  https://github.com/Jompy-GitHub/MTS-UncertainEnvironment/tree/sarenv-mts
- **Repositorio personal del proyecto completo:**  
  https://github.com/jcestefania/TFM/tree/sarenv-mts

---

## Resumen Ejecutivo

En las operaciones de Busqueda y Salvamento (SAR) en entornos boscosos y semiurbanos (WiSAR), el tiempo de respuesta es decisivo para la supervivencia de la persona extraviada. Los patrones de barrido geometrico ciego clasicos (Lawnmower o espirales) son ineficientes al ignorar las restricciones del terreno y la distribucion asimetrica de presencia.

Este proyecto desarrolla e integra **`sarenv-mts`**, una arquitectura de software desacoplada que unifica:
1. **Cartografia Abierta y Modelado Topologico:** Descarga vectorial de OpenStreetMap (OSM) y mapas de probabilidad espacial basados en el comportamiento empirico de personas desaparecidas (*Lost Person Behavior* - LPB de Robert Koester).
2. **Filtrado de Restricciones Duras:** Mascaras espaciales R-Tree (`sindex`) que anulan la probabilidad ($P=0.0$) en zonas no transitables (lagos y edificaciones).
3. **Middleware Espacial:** Conversion analitica de coordenadas metricas globales UTM (EPSG:32630) a rejillas discretas ($\delta = 10\text{ m/celda}$).
4. **Planificadores Bioinspirados:** Optimizacion de trayectorias mediante Colonia de Abejas Artificiales (ABC), Algoritmo de Agujeros Negros (BHA) y Colonia de Hormigas (ACO), calibrados mediante optimizacion bayesiana con Optuna.
5. **Validacion Experimental Masiva:** Benchmark de 900 simulaciones de Montecarlo sobre el escenario real de la Casa de Campo de Madrid ($17.22\text{ km}^2$), demostrando que la busqueda bayesiana informada multiplica entre 3x y 6x la tasa de exito frente a las lineas de base convencionales.

---

## Estructura del Repositorio

```text
.
├── framwork-MTS/
│   └── MTS-UncertainEnvironment-Algoritmos-bioinspirados/  # Nucleo del framework sarenv-mts
│       ├── sarenv/            # Paquete generador de probabilidad y conector OSM
│       ├── busquedas/         # Planificadores bioinspirados (ACO, ABC, BHA, Voraz, Lawnmower)
│       ├── metrics/           # Modulo PathEvaluatorTFM (5 metricas oficiales SAR)
│       ├── middleware/        # Conversores UTM <-> Rejilla y exportador JSON
│       ├── extra/             # Utilidades de footprint de sensor y scripts
│       └── TFM_JC/            # Cuadernos interactivos y base de datos de 900 simulaciones
├── memoria/                   # Codigo fuente LaTeX completo de la memoria del TFM
│   ├── chapters/              # Capitulos 1 al 7
│   ├── imagenes/              # Figuras vectoriales, diagramas TikZ y graficos
│   ├── memoria.tex            # Documento principal LaTeX (plantilla oficial UC3M)
│   └── referencias.bib        # 55 referencias bibliograficas con DOI verificado
├── objetivos_dinamicos/       # Material de victimas dinamicas y datos del simulacro de bomberos
├── sync_lab.py                # Script de sincronizacion limpia con el repositorio del laboratorio
└── requirements.txt           # Dependencias de Python para reproducibilidad
```

---

## Instalacion y Reproducibilidad

### 1. Clonar el repositorio
```bash
git clone -b sarenv-mts https://github.com/jcestefania/TFM.git
cd TFM
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Ejecutar los Cuadernos Interactivos
Navega a la carpeta de cuadernos y abre Jupyter:
```bash
jupyter notebook framwork-MTS/MTS-UncertainEnvironment-Algoritmos-bioinspirados/TFM_JC/notebooks/Notebook_Demo_Rapida_Interactiva.ipynb
```
En el cuaderno podras seleccionar el perfil (Demencia, Autista, Senderista), el algoritmo de vuelo, y visualizar en tiempo real la evolucion de la trayectoria y la absorcion del mapa de creencias.

---

## Compilacion de la Memoria LaTeX

El directorio `memoria/` contiene la monografia completa configurada segun la normativa de la Biblioteca de la UC3M.
Para compilar localmente:
```bash
cd memoria
pdflatex memoria.tex
biber memoria
pdflatex memoria.tex
pdflatex memoria.tex
```
O bien cargar la carpeta `memoria/` directamente en Overleaf para compilar con XeLaTeX/pdfLaTeX.

---

## Agradecimientos

Agradecimiento especial al **Departamento de Informatica** y al grupo **GIAA** de la Universidad Carlos III de Madrid por los recursos computacionales y la tutela cientifica proporcionada durante el desarrollo de este trabajo.
