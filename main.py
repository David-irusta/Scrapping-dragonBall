import time
from scraper import (
    obtener_titulos_personajes,
    obtener_personajes_por_lotes,
    guardar_todos_los_personajes
)

print("Obteniendo personajes de Dragon Ball...\n")

inicio = time.perf_counter()

# 1. Obtener todos los títulos.
titulos = obtener_titulos_personajes()

print(f"\nTotal de páginas encontradas: {len(titulos)}")
print(f"Tiempo buscando categorías: {time.perf_counter() - inicio:.2f} segundos")

# 2. Consultar las páginas en lotes.
inicio = time.perf_counter()

personajes = obtener_personajes_por_lotes(titulos)

print(f"Tiempo extrayendo personajes: {time.perf_counter() - inicio:.2f} segundos")

# 3. Guardar todos los personajes.
guardar_todos_los_personajes(personajes)

# 4. Mostrar estadísticas.
print("\n--- ESTADÍSTICAS DE LOS PERSONAJES ---")

campos = ["nombre", "raza", "genero", "altura", "peso", "imagen"]

print(f"Total de personajes: {len(personajes)}\n")

for campo in campos:
    completos = sum(
        1 for personaje in personajes
        if personaje.get(campo)
    )

    incompletos = len(personajes) - completos

    print(f"{campo.capitalize()}:")
    print(f"  Completos: {completos}")
    print(f"  Incompletos: {incompletos}")

# 5. Detectar personajes duplicados.
print("\n--- DETECCIÓN DE DUPLICADOS ---")

nombres_vistos = set()
duplicados = set()

for personaje in personajes:
    nombre = personaje.get("nombre")

    if not nombre:
        continue

    nombre_normalizado = nombre.strip().casefold()

    if nombre_normalizado in nombres_vistos:
        duplicados.add(nombre)
    else:
        nombres_vistos.add(nombre_normalizado)

print(f"Personajes duplicados: {len(duplicados)}")

if duplicados:
    print("\nNombres duplicados:")
    for nombre in sorted(duplicados):
        print(f"- {nombre}")
else:
    print("No se encontraron duplicados.")

print("\nProceso finalizado.")
