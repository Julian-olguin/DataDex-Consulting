import pandas as pd

print("Cargando datos originales de pokemon.csv...")
# Lee el archivo original que está en la carpeta principal
df = pd.read_csv("C:/Users/julie/Downloads/pokemon.csv")

# LIMPIEZA BÁSICA
df = df.rename(columns={
    'No_Pokedex': 'id_pokemon', 
    'peso_(kg)': 'peso_kg', 
    'altura_(m)': 'altura_m',
    'Puntos_de_salud': 'puntos_salud'
})

# Llenar valores nulos los que no tienen tipo2 dirán Ninguno
df['tipo2'] = df['tipo2'].fillna('Ninguno')

# Limpiar espacios basura en la columna de captura
df['Probabilidad_de_captura'] = df['Probabilidad_de_captura'].astype(str).str.strip()

# NORMALIZACIÓN (Separar en tablas)
print("Limpiando y separando en tablas...")

# 1. Tabla Pokemon
tabla_pokemon = df[['id_pokemon', 'nombre', 'generacion', 'es_legendario', 'altura_m', 'peso_kg', 'Probabilidad_de_captura', 'clasificacion']]
tabla_pokemon = tabla_pokemon.drop_duplicates(subset=['id_pokemon'])

# 2. Tabla Estadisticas
tabla_estadisticas = df[['id_pokemon', 'puntos_salud', 'ataque', 'defensa', 'ataque_especial', 'defensa_especial', 'velocidad', 'total_base']]

# 3. Tabla Tipos
todos_los_tipos = pd.concat([df['tipo1'], df['tipo2']]).unique()
tabla_tipos = pd.DataFrame({'nombre_tipo': todos_los_tipos})
tabla_tipos['id_tipo'] = tabla_tipos.index + 1

# 4. Tabla Pokemon_Tipo (Relaciones)
tipo_a_id = dict(zip(tabla_tipos['nombre_tipo'], tabla_tipos['id_tipo']))
relaciones = []
for index, row in df.iterrows():
    relaciones.append({'id_pokemon': row['id_pokemon'], 'id_tipo': tipo_a_id[row['tipo1']], 'es_tipo_principal': 1})
    if row['tipo2'] != 'Ninguno':
        relaciones.append({'id_pokemon': row['id_pokemon'], 'id_tipo': tipo_a_id[row['tipo2']], 'es_tipo_principal': 0})
tabla_pokemon_tipo = pd.DataFrame(relaciones)

# exportar
print("Generando archivos CSV limpios...")
tabla_pokemon.to_csv('pokemon_limpio.csv', index=False)
tabla_estadisticas.to_csv('estadisticas_limpias.csv', index=False)
tabla_tipos.to_csv('tipos_limpios.csv', index=False)
tabla_pokemon_tipo.to_csv('pokemon_tipo_relacion.csv', index=False)

print("¡Proceso terminado con éxito!")