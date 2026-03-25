# DataDex Consulting - Área de Análisis de Datos
# Proyecto: Enciclopedia Pokémon
# Gráfica: Comparativa de Fortalezas (Ataque) vs Debilidades (Defensa) de los Mejores Pokémon por Tipo

# 1. INSTALACIÓN Y CARGA DE LIBRERÍAS
install.packages("ggplot2")
install.packages("tidyr") 
install.packages("dplyr") 

library(ggplot2)
library(tidyr)
library(dplyr)

# ==============================================================================
# 2. SIMULACIÓN DE DATOS (REMPLAZAR ESTO CON LA CONEXIÓN A TU BD MYSQL)
# En producción, usarías: df_pokemon_combat <- dbGetQuery(con, "SELECT ...")
# ==============================================================================

# Simulamos el Top 1 de algunos tipos clave (representando al "mejor")
df_pokemon_combat <- data.frame(
  tipo_principal = c("Fuego", "Agua", "Planta", "Eléctrico", "Lucha", "Psíquico", "Dragón", "Acero"),
  best_pokemon_name = c("Mega Charizard Y", "Mega Blastoise", "Mega Venusaur", "Zapdos", "Lucario", "Mewtwo", "Rayquaza", "Metagross"),
  ataque_base = c(104, 103, 100, 90, 110, 110, 150, 135),
  defensa_base = c(78, 120, 123, 85, 70, 90, 90, 130)
)

# ==============================================================================
# 3. PREPARACIÓN DE DATOS PARA GGPLOT (Normalización)
# ==============================================================================

df_long <- df_pokemon_combat %>%
  select(tipo_principal, best_pokemon_name, ataque_base, defensa_base) %>%
  pivot_longer(cols = c(ataque_base, defensa_base), 
               names_to = "stat_type", 
               values_to = "stat_value")

# Mejoramos los nombres para la leyenda
df_long$stat_type <- ifelse(df_long$stat_type == "ataque_base", "Puntos de Ataque (Fortaleza)", "Puntos de Defensa (Debilidad)")

# Creamos una etiqueta combinada para el eje X
df_long$ejex_label <- paste0(df_long$tipo_principal, "\n(", df_long$best_pokemon_name, ")")

# ==============================================================================
# 4. GENERACIÓN DE LA GRÁFICA CON GGPLOT2 (Estilo DataDex)
# ==============================================================================

# Definimos la paleta de colores corporativos de DataDex Consulting (Azul y Gris profesional)
# Pero usaremos una paleta más "viva" para diferenciar Ataque de Defensa
colores_datadex <- c("Puntos de Ataque (Fortaleza)" = "#2196F3",    # Azul brillante para ataque
                     "Puntos de Defensa (Debilidad)" = "#FF9800") # Naranja para defensa

grafica_comparativa <- ggplot(df_long, aes(x = ejex_label, y = stat_value, fill = stat_type)) +
  # Barras agrupadas (position = "dodge") con borde sutil
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7, color = "#333333", size = 0.3) +
  
  # Etiquetas de valor sobre las barras
  geom_text(aes(label = stat_value), 
            position = position_dodge(width = 0.8), 
            vjust = -0.5, size = 3.5, fontface = "bold", color = "#444444") +
  
  # Escalas de color y etiquetas
  scale_fill_manual(values = colores_datadex) +
  labs(title = "Análisis Comparativo de Capacidades de Combate",
       subtitle = "Mejores exponentes por tipo elemental (Top 1 Base Stat Total)",
       caption = "Fuente: Base de Datos Enciclopedia Pokémon (DataDex Consulting)",
       x = "Tipo Elemental (y su mejor representante)",
       y = "Puntos de Estadística Base",
       fill = "Métrica de Combate") +
  
  # TEMA Y ESTILO 
  theme_minimal() +
  theme(
    text = element_text(family = "sans"),
    plot.title = element_text(face = "bold", size = 16, color = "#1a1a1a"),
    plot.subtitle = element_text(size = 11, color = "#555555", margin = margin(b = 15)),
    axis.title.x = element_text(face = "bold", margin = margin(t = 15)),
    axis.title.y = element_text(face = "bold", margin = margin(r = 15)),
    axis.text.x = element_text(angle = 45, hjust = 1, size = 10, color = "#333333"),
    legend.position = "bottom",
    legend.title = element_text(face = "bold"),
    panel.grid.major.x = element_blank(), # Quitamos líneas verticales para limpieza
    panel.grid.minor = element_blank()
  ) +
  
  # Ajuste del límite del eje Y para que no se corten las etiquetas
  scale_y_continuous(expand = expansion(mult = c(0, 0.1)))

# ==============================================================================
# 5. VISUALIZACIÓN Y GUARDADO
# ==============================================================================
print(grafica_comparativa)

# Para guardar la imagen
ggsave("docs/assets/grafica_comparativa_fortalezas.png", grafica_comparativa, width = 10, height = 7, dpi = 300)