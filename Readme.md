# Dragon Ball Scraper 🐉

Scraper desarrollado en Python para obtener información de personajes de Dragon Ball desde la wiki española de Fandom, utilizando su API de MediaWiki.

El proyecto permite consultar personajes individualmente o recorrer las categorías de la wiki para recopilar información de múltiples personajes y almacenarla en un archivo JSON.

## Características

- Consulta de personajes mediante la API de MediaWiki.
- Búsqueda recursiva de categorías y subcategorías.
- Obtención masiva de personajes mediante procesamiento por lotes.
- Procesamiento concurrente para reducir los tiempos de consulta.
- Extracción de información exclusivamente de la ficha de cada personaje (`{{Personaje}}`).
- Limpieza de datos extraídos de las plantillas de MediaWiki.
- Obtención de imágenes mediante las miniaturas proporcionadas por la API.
- Almacenamiento de los resultados en formato JSON.
- Actualización de personajes existentes para evitar duplicados.

## Tecnologías utilizadas

- **Python 3.9 o superior**
- **Requests:** para realizar solicitudes HTTP a la API.
- **Regular Expressions (re):** para identificar y extraer información