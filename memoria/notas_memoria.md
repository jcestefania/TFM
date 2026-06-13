# Notas de Redacción para la Memoria del TFM

Este documento centraliza las explicaciones técnicas, justificaciones teóricas y análisis visuales desarrollados durante el refinamiento de SAREnv. Se incluye la indicación exacta de en qué archivo `.tex` y sección de la memoria debe integrarse cada bloque.

---

## 📝 Bloque 1: Modificación de la Fusión de Capas (Suma vs. Máximo)

### 📍 Dónde colocarlo en la Memoria:
*   **Archivo:** `memoria/chapters/3-ModeladoDelProblema.tex`
*   **Sección:** `\subsection{Proyección y Fusión a Nivel de Rejilla (Rasterización)}`
*   **Punto exacto:** Sustituir la explicación del paso 3 (Fusión por Operador de Máxima Probabilidad) y la Ecuación (3.8) que definía la matriz mediante `max`.

### ✍️ Texto a integrar:

A diferencia del diseño original de SAREnv, que utiliza un operador de máximo en cada celda para evitar acumulaciones artificiales de probabilidad, en este trabajo se ha modificado la lógica de fusión para implementar una **suma ponderada y posterior normalización**. 

El paper original de SAREnv (*"SAREnv: An Open-Source Dataset and Benchmark Tool for Informed Wilderness Search and Rescue Using UAVs"*, página 14) señala como una limitación del operador de máximo el hecho de no considerar el efecto acumulativo cuando convergen múltiples características favorables en un mismo punto, lo que puede llevar a infravalorar zonas ricas en características (*feature-rich zones*).

Para resolver esta limitación, el proceso de fusión se ha reformulado en dos pasos:
1. **Suma Ponderada:**
   $$\mathbf{POA}_{\text{unnorm}}(i, j) = \sum_{k} \mathbf{M}_k(i, j) \cdot \alpha_k$$
   donde $\mathbf{M}_k(i, j) \in \{0, 1\}$ es la presencia binaria de la capa $k$, y $\alpha_k$ es su peso de probabilidad en la tabla `FEATURE_PROBABILITIES`.
2. **Normalización Global:**
   $$\mathbf{POA}_{\text{norm}}(i, j) = \frac{\mathbf{POA}_{\text{unnorm}}(i, j)}{\sum_{u=1}^{N_y} \sum_{v=1}^{N_x} \mathbf{POA}_{\text{unnorm}}(u, v)}$$

Debido a la topología de los datos de OpenStreetMap, los polígonos de cobertura de suelo (bosque, agua, prados) son geográficamente disjuntos y no se solapan entre sí. Los únicos solapamientos se producen por elementos lineales (caminos, ríos) e infraestructuras cruzando dichos fondos. Por tanto, la suma no genera un mapa diluido, sino que preserva los picos de los caminos y el agua, al tiempo que eleva la importancia de sus intersecciones.

---

## 📝 Bloque 2: Justificación del Mapa de Calor y Análisis Visual (Casa de Campo)

### 📍 Dónde colocarlo en la Memoria:
*   **Archivo:** `memoria/chapters/3-ModeladoDelProblema.tex` (al final del capítulo, como caso de estudio práctico) o en `memoria/chapters/4-DesarrolloEIntegracion.tex` (bajo una sección de "Validación del Entorno Real").
*   **Sección:** Crear una nueva subsección llamada `\subsection{Validación Visual y Análisis del Mapa de Calor de la Casa de Campo}`.
*   **Punto exacto:** Insertar el texto justo debajo de la figura donde se muestre la captura del mapa interactivo de verificación geográfica (`verificacion_TFM_JC.png`).

### ✍️ Texto a integrar:

La distribución de la densidad de probabilidad de área (POA) obtenida en el mapa interactivo de la Casa de Campo muestra una topografía probabilística que se ajusta a los modelos de comportamiento de personas perdidas (LPB) y a la geografía real del parque:

1. **Pico Absoluto (Área Centro-Este):** La zona de color rojo más intenso y oscuro del mapa de calor se sitúa en la región centro-este del parque. Este pico coincide con la proximidad al IPP (Punto de Planificación Inicial), reflejando la distribución radial log-normal. Debido a que la probabilidad de distancia decae a medida que el sujeto se aleja de su última posición conocida, el modelo prioriza de forma natural la zona central.
2. **Pico Secundario del Zoo (Zona Sur):** En el sur del mapa, se aprecia un pico de calor secundario de tonalidad naranja-roja localizado directamente sobre las instalaciones del *Zoo Aquarium de Madrid*. Este incremento se justifica por la alta densidad de edificaciones y recintos (capa `structure`, con un peso base de $0.13$) y la confluencia de senderos peatonales de acceso.
3. **Pico Secundario del Lago (Zona Este):** En el margen derecho del mapa, la probabilidad asciende hacia la zona del *Lago*. Este pico secundario está motivado por el peso específico de las masas de agua (capa `water`, de $0.08$) en combinación con la red de caminos limítrofes (capa `road`, de $0.13$).
4. **Efecto de la Fusión por Suma:** Al aplicar la suma ponderada de capas, las intersecciones del terreno (como un sendero que bordea el lago o una estructura de acceso al zoo rodeada de vegetación) acumulan aditivamente sus pesos, permitiendo que estos puntos de alto interés destaquen de manera realista sobre el fondo y guíen de manera óptima las trayectorias de búsqueda del enjambre de drones.
