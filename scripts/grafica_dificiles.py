import pandas as pd
import matplotlib.pyplot as plt

df_pokemon = pd.read_csv('pokemon_limpio.csv')
df_estadisticas = pd.read_csv('estadisticas_limpias.csv')

# Unimos las dos tablas usando el id_pokemon 
df_completo = pd.merge(df_pokemon, df_estadisticas, on='id_pokemon')

# 2. LIMPIEZA MATEMÁTICA PARA LA GRÁFICA
# Convertimos la probabilidad de captura a número para poder ordenarlos
df_completo['Probabilidad_de_captura'] = pd.to_numeric(df_completo['Probabilidad_de_captura'], errors='coerce')

# Filtramos: Buscamos a los que tienen la captura más baja posible (3)
# Y para desempatar tomamos a los 10 con las Estadisticas Totales más altas 
top_10 = df_completo[df_completo['Probabilidad_de_captura'] <= 3].sort_values(by='total_base', ascending=False).head(10)

# 3. EL porque - INFORMACIÓN ADICIONAL 
# Diccionario con datos externos ajenos al CSV original
razones_dificultad = {
    'Beldum': 'Tasa de aparición <1% y usa ataques suicidas (Derribo).',
    'Mewtwo': 'Jefe final. Requiere Master Ball o paralizarlo con PS al límite.',
    'Arceus': 'Dios Pokémon. Requiere objeto de evento real (Flauta Azur).',
    'Lugia': 'Batalla de desgaste, se cura a sí mismo y tiene gran defensa.',
    'Ho-Oh': 'Daño altísimo que debilita a tu equipo antes de que lances la Pokéball.',
    'Raikou': 'Perro errante: Huye del combate en el primer turno.',
    'Entei': 'Perro errante: Usa Rugido para forzar el fin del combate.',
    'Suicune': 'Altamente evasivo y requiere persecución por todo el mapa.',
    'Giratina': 'Batalla en el Mundo Distorsión, mecánicas de inmunidad fantasma.',
    'Rayquaza': 'Poder de ataque abrumador, aniquila a tu equipo rápidamente.'
}

# Le asignamos la razon a cada Pokemon si no esta en la lista pone una razon generica
top_10['razon'] = top_10['nombre'].map(razones_dificultad).fillna('Tasa de captura mínima (3/255) y alto nivel.')

# 4. DIBUJAR LA GRAFICA 
plt.figure(figsize=(12, 7))

# Grafica de barras horizontales
barras = plt.barh(top_10['nombre'], top_10['total_base'], color='#2C3E50', edgecolor='#E74C3C', linewidth=2)

# Agregar el texto del "porqué" justo al lado de cada barra
for index, barra in enumerate(barras):
    nombre_pokemon = top_10.iloc[index]['nombre']
    razon = top_10.iloc[index]['razon']
    
    # Escribe la razón a la derecha de la barra
    plt.text(barra.get_width() + 5, barra.get_y() + barra.get_height()/2, 
             f" {razon}", 
             va='center', ha='left', fontsize=9, color='#34495E', style='italic')

# Formato visual corporativo
plt.title('Top 10 Pokémon Más Difíciles de Capturar\n(Ordenados por Poder Total y Complejidad)', fontsize=14, fontweight='bold')
plt.xlabel('Poder Total Base (Dificultad de Combate)', fontsize=11)
plt.ylabel('Nombre del Pokémon', fontsize=11)
plt.xlim(0, top_10['total_base'].max() + 350) # Dar espacio a la derecha para que quepa el texto
plt.gca().invert_yaxis() # Poner al número 1 hasta arriba
plt.tight_layout()

# 5. GUARDAR LA IMAGEN
plt.savefig('grafica_dificiles.png', dpi=300)
print("¡Gráfica 'grafica_dificiles.png' generada con éxito!")

# 6. GENERAR EL ARCHIVO DE EXPLICACIÓN (Requisito de la rúbrica)
explicacion = """# Explicación Gráfica 2: Pokémon más difíciles de capturar
**Objetivo:** Mostrar los 10 Pokémon con la tasa de captura más baja del juego (3/255) y el mayor poder de combate.
**Justificación de Diseño:** Se eligió una gráfica de barras horizontales porque permite leer claramente el nombre del Pokémon en el eje Y, y proporciona el espacio visual perfecto a la derecha de las barras para incrustar el *porqué* (información externa sobre mecánicas de juego, huidas o eventos especiales) de su dificultad.
"""
with open('explicacion_grafica_dificiles.md', 'w', encoding='utf-8') as f:
    f.write(explicacion)
print("¡Archivo de explicación generado con éxito!")