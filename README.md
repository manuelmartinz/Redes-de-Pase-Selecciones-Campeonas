# Análisis de redes en selecciones campeonas del mundo
Este proyecto analiza las redes de pase de selecciones campeonas (Argentina 2022, Francia 2018 y España 2024) desde la perspectiva de las redes complejas.

## Metodología

1. **Construcción de la red**
   - A partir de los eventos de pase, se construye una red dirigida y ponderada por partido.
   - Se genera también una red agregada por selección (todos los partidos considerados).

2. **Versión para análisis global**
   - Para comparar con las redes aleatorias se obtiene una versión **no ponderada**:
     - Existe enlace si hay al menos un pase entre dos jugadores.
   - En esta red se calculan N, E, D, ⟨k⟩, ⟨d⟩ y ⟨C⟩.

3. **Redes aleatorias equivalentes**
   - Se generan redes aleatorias G(N, p) con:
     - Mismo número de nodos N.
     - Mismo número esperado de enlaces E (o mismo grado medio ⟨k⟩).
   - Para ello se usa la probabilidad:
     - Red no dirigida: p ≈ 2E / [N(N−1)]
     - Red dirigida: p ≈ E / [N(N−1)]
   - Las redes se generan con herramientas tipo **RandomNets** / `genera_red_ponderada_aleatoria` y se exportan a formato compatible con Gephi.

4. **Análisis estructural**
   - Cálculo de medidas globales para cada red real y su red aleatoria equivalente.
   - Estudio de:
     - Distribución de grados P(k).
     - Coeficientes de clustering locales.
     - Número de componentes y componente gigante.

5. **Centralidad y comunidades**
   - Cálculo de centralidades (grado, intermediación, cercanía, vector propio).
   - Detección de comunidades:
     - Método de Louvain.
     - Método de Girvan–Newman.
   - Interpretación en términos de roles tácticos y zonas del campo.

6. **Visualización**
   - Visualización de la red en Gephi:
     - Layouts de tipo force-directed.
     - Tamaño y color de los nodos según centralidad.
     - Grosor de los enlaces según peso (nº de pases).
   - Visualización del esqueleto de la red.
   - Visualización de los pases de tipo ofensivo.

