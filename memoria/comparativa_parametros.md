# Comparativa de Parámetros: Iniciales vs. Optimizados (Optuna)

Este documento detalla la comparativa entre la configuración de parámetros que venía por defecto en el framework de MTS (usada en las primeras simulaciones de control) y los nuevos parámetros calibrados que ha encontrado **Optuna** tras 35 trials para cada perfil y algoritmo.

---

## Resumen de Cambios Clave

Antes, los tres perfiles (**Autista, Demencia y Senderista**) utilizaban exactamente la misma configuración genérica. Ahora, cada perfil tiene su propia configuración ajustada a la densidad de su mapa de calor:

* **Perfil de Demencia (Búsqueda concentrada):** Optuna ha incrementado la tasa de evaporación local de feromonas (`local_rho` a `0.129`) e incrementado la iteración de hormigas y abejas. Esto evita que los agentes vuelen en círculos en zonas de altísima probabilidad local y exploren áreas circundantes.
* **Perfil de Senderista (Búsqueda dispersa a lo largo de caminos):** Para ACO, Optuna ha incrementado el peso de la feromona global (`alpha` a `1.475`) en comparación con la heurística local, haciendo que el dron siga de forma más estricta los largos "caminos" probabilísticos trazados por la red topológica del parque.

---

## 1. Algoritmo: ACO (Optimización por Colonia de Hormigas)

| Parámetro | Significado Técnico | Inicial (Default) | Autista (Optimizado) | Demencia (Optimizado) | Senderista (Optimizado) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`alpha`** | Peso del rastro de feromona | **1.00** | 0.813 | 0.729 | 1.475 |
| **`beta`** | Peso de la heurística de visibilidad | **3.00** | 2.075 | 2.221 | 2.093 |
| **`rho`** | Evaporación de feromona global | **0.10** | 0.069 | 0.215 | 0.143 |
| **`local_rho`** | Evaporación de feromona local | **0.05** | 0.095 | 0.129 | 0.024 |
| **`Q`** | Intensidad de la feromona depositada | **1.00** | 0.505 | 2.018 | 0.891 |
| **`n_iterations_aco`** | Iteraciones del algoritmo por paso | **5** | 5 | 6 | 4 |

---

## 2. Algoritmo: ABC (Colonia de Abejas Artificiales)

| Parámetro | Significado Técnico | Inicial (Default) | Autista (Optimizado) | Demencia (Optimizado) | Senderista (Optimizado) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`n_iterations_abc`** | Iteraciones del algoritmo por paso | **10** | 9 | 8 | 13 |
| **`limit`** | Límite de pasos sin mejora antes de abandonar | **10** | 19 | 11 | 16 |
| **`n_employed`** | Número de abejas empleadas (fuentes de comida) | **1** | 1 | 3 | 2 |
| **`n_onlookers`** | Número de abejas espectadoras | **1** | 4 | 4 | 3 |

---

## 3. Algoritmo: BHA (Algoritmo del Agujero Negro)

| Parámetro | Significado Técnico | Inicial (Default) | Autista (Optimizado) | Demencia (Optimizado) | Senderista (Optimizado) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`n_iterations_bha`** | Iteraciones del algoritmo por paso | **10** | 8 | 12 | 9 |
| **`n_stars`** | Número de estrellas (soluciones candidatas) | **5** | 9 | 10 | 8 |
