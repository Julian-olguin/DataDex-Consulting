import pandas as pd
import matplotlib.pyplot as plt

# Actualmente leemos de los CSV limpios (Desarrollo Modular - Paso A).

df_pokemon = pd.read_csv('pokemon_limpio.csv')
df_estadisticas = pd.read_csv('estadisticas_limpias.csv')
df_completo = pd.merge(df_pokemon, df_estadisticas, on='id_pokemon')

# 1. SELECCIONAR EL EQUIPO CONTRA TAPU LELE
nombres_escuadron = ['Aegislash', 'Metagross', 'Scizor', 'Gengar']
escuadron = df_completo[df_completo['nombre'].isin(nombres_escuadron)].copy()

# 2. INFORMACIÓN ADICIONAL COMO Habilidades, Fortalezas y Probabilidades
# Estos son  datos ajenos al CSV 
datos_tacticos = {
    'Aegislash': {
        'habilidad': 'Cambio Táctico',
        'fortaleza': 'Inmunidad a Veneno, daño letal de Fantasma/Acero.',
        'probabilidad': 35
    },
    'Metagross': {
        'habilidad': 'Cuerpo Puro',
        'fortaleza': 'Resiste ataques Psíquicos y Hada como un tanque.',
        'probabilidad': 25
    },
    'Scizor': {
        'habilidad': 'Experto',
        'fortaleza': 'Ataques rápidos de Acero (Puño Bala) para rematar.',
        'probabilidad': 20
    },
    'Gengar': {
        'habilidad': 'Cuerpo Maldito',
        'fortaleza': 'Daño masivo de Veneno antes de caer debilitado.',
        'probabilidad': 15
    }
}

#  los datos tacticos al DataFrame
escuadron['habilidad'] = escuadron['nombre'].apply(lambda x: datos_tacticos[x]['habilidad'])
escuadron['fortaleza'] = escuadron['nombre'].apply(lambda x: datos_tacticos[x]['fortaleza'])
escuadron['prob_victoria'] = escuadron['nombre'].apply(lambda x: datos_tacticos[x]['probabilidad'])

# Ordenamos de mayor a menor aportacion
escuadron = escuadron.sort_values('prob_victoria', ascending=True)

# 3. DISEÑO DE LA GRAFICA 
fig, ax = plt.subplots(figsize=(12, 7))

# Colores corporativos de amenaza
colores = ['#8E44AD', '#E67E22', '#3498DB', '#C0392B']

# Grafica de barras horizontales mostrando el % de victoria que aporta cada uno
barras = ax.barh(escuadron['nombre'], escuadron['prob_victoria'], color=colores, height=0.6)

# Agregar los textos explicativos dentro de la grafica
for index, barra in enumerate(barras):
    nombre = escuadron.iloc[index]['nombre']
    habilidad = escuadron.iloc[index]['habilidad']
    fortaleza = escuadron.iloc[index]['fortaleza']
    prob = escuadron.iloc[index]['prob_victoria']
    
    # Texto de Habilidad y Fortaleza a la derecha de la barra
    ax.text(barra.get_width() + 1, barra.get_y() + barra.get_height()/2, 
            f" Habilidad: {habilidad}\n Rol: {fortaleza}", 
            va='center', ha='left', fontsize=10, color='#2C3E50')
    
    # Texto del % de victoria dentro de la barra
    ax.text(barra.get_width() - 2, barra.get_y() + barra.get_height()/2, 
            f"{prob}%", va='center', ha='right', fontsize=12, color='white', fontweight='bold')

# Detalles de diseño
probabilidad_total = escuadron['prob_victoria'].sum()
plt.title(f'Simulación de Combate vs Legendario: Tapu Lele (Psíquico/Hada)\nProbabilidad de Victoria Combinada: {probabilidad_total}%', 
          fontsize=14, fontweight='bold', color='#2C3E50')
plt.xlabel('Aportación a la Probabilidad de Victoria (%)', fontsize=11)
plt.xlim(0, 100) # El eje X llega hasta 100 para dar espacio al texto
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()

# 4. GUARDAR ARCHIVOS
plt.savefig('grafica_tapu_lele.png', dpi=300)
print("¡Gráfica 'grafica_tapu_lele.png' generada con éxito!")

# 5. GENERAR EXPLICACION
explicacion = f"""# Explicación Gráfica 4: Simulación de Combate vs Tapu Lele
**Objetivo:** Mostrar un escuadrón táctico de 4 Pokémon capaces de derrotar al legendario Tapu Lele, justificando sus fortalezas.
**Justificación de Diseño:** Se optó por una gráfica de barras horizontales acumulativas. En lugar de solo mostrar estadísticas planas, la gráfica ilustra el **Porcentaje de Aportación a la Victoria** de cada Pokémon, sumando un contundente {probabilidad_total}% de éxito. Se integró la información adicional (Habilidades y Rol estratégico) directamente en el área de trazado para que el cliente pueda evaluar el "porqué" de un solo vistazo sin tener que cruzar datos con otras tablas.
"""
with open('explicacion_grafica_tapu_lele.md', 'w', encoding='utf-8') as f:
    f.write(explicacion)
print("¡Archivo de explicación generado con éxito!")