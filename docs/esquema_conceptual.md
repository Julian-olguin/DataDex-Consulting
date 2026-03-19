# Esquema Conceptual de la Base de Datos
## Proyecto: Enciclopedia Pokémon - DataDex Consulting

A continuación se define la estructura conceptual diseñada para resolver el problema de organización de datos del archivo CSV inicial, aplicando reglas de normalización para evitar redundancia de información.

### 1. Tablas Principales Definidas
Se decidió dividir la información plana del archivo original en cuatro entidades principales:

* **Entidad `Pokemon`:** Actuará como el catálogo principal. Almacenará los datos biológicos y descriptivos únicos de cada criatura (nombre, generación, si es legendario, altura, peso y probabilidad de captura).
* **Entidad `Estadisticas`:** Separada por normalización, esta tabla almacenará los atributos de combate (puntos de salud, ataque, defensa, velocidad y el total base) ligados a cada Pokémon.
* **Entidad `Tipos`:** Un catálogo único y sin repeticiones de los elementos existentes (ej. Fuego, Agua, Planta).
* **Entidad `Pokemon_Tipo`:** Una tabla transaccional o puente. Dado que la relación de los tipos es compleja, esta tabla registrará qué tipo(s) posee cada Pokémon.

### 2. Relaciones entre Tablas
Las entidades interactúan bajo las siguientes reglas lógicas:
* **Relación 1 a 1 (Pokemon - Estadisticas):** Un Pokémon específico tiene un solo set de estadísticas base, y ese set pertenece únicamente a ese Pokémon.
* **Relación de Muchos a Muchos (Pokemon - Tipos):** Un Pokémon puede tener hasta dos tipos diferentes (ej. Bulbasaur es Planta y Veneno), y un Tipo (ej. Fuego) puede pertenecer a muchos Pokémon distintos. Esta relación se resuelve utilizando la tabla intermedia `Pokemon_Tipo`.

### 3. Metadatos Necesarios
Para asegurar la integridad de la información al pasar a SQL, se definen los siguientes metadatos principales:
* **Llaves Primarias (PK):** Se utilizará el `id_pokemon` (entero) como identificador único para los Pokémon y un `id_tipo` (entero autoincrementable) para el catálogo de tipos.
* **Llaves Foráneas (FK):** La tabla `Estadisticas` y la tabla `Pokemon_Tipo` heredarán el `id_pokemon` para vincular los datos correctamente.
* **Tipos de Datos:** - Textos (`STRING`/`VARCHAR`) para nombres y clasificaciones.
  - Enteros (`INT`) para estadísticas de combate y generaciones.
  - Decimales (`FLOAT`) para métricas físicas como altura y peso.
  - Booleanos (`BOOLEAN`) para banderas lógicas como `es_legendario` (0 = No, 1 = Sí).