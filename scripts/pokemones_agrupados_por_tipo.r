# 1. Cargar librerías necesarias
library(ggplot2)
library(dplyr)

# 2. CARGAR LOS DATOS DESDE TUS ARCHIVOS CSV (Paso faltante)
# Usamos read.csv para leer los archivos que ya tienes en tu carpeta
pokemon <- read.csv("scripts/pokemon_limpio.csv")
estadisticas <- read.csv("scripts/estadisticas_limpias.csv")
pokemon_tipo <- read.csv("scripts/pokemon_tipo_relacion.csv")
tipos <- read.csv("scripts/tipos_limpios.csv")

# 3. Unir las tablas (Inner Join)
df_completo <- pokemon %>%
  inner_join(estadisticas, by = "id_pokemon") %>%
  inner_join(pokemon_tipo, by = "id_pokemon") %>%
  inner_join(tipos, by = "id_tipo")

# 4. Obtener el Top 10 basado en el Total Base
top_10_pokemon <- df_completo %>%
  arrange(desc(total_base)) %>%
  head(10)

# 5. Crear la gráfica con ggplot2
grafica_final <- ggplot(top_10_pokemon, aes(x = reorder(nombre, total_base), y = total_base, fill = nombre_tipo)) +
  geom_bar(stat = "identity", color = "black") +
  coord_flip() +  
  scale_fill_viridis_d(option = "plasma") + 
  labs(
    title = "Top 10 Pokémon con Mayor Poder Base",
    subtitle = "Análisis de DataDex Consulting",
    x = "Nombre del Pokémon",
    y = "Poder Total Base",
    fill = "Elemento"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 16, color = "darkblue"),
    axis.text = element_text(size = 12)
  )

# 6. MOSTRAR Y GUARDAR LA GRÁFICA
print(grafica_final)
ggsave("docs/assets/top_10_poder_base.png", grafica_final, width = 10, height = 7)