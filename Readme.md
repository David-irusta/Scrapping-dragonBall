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
- **Regular Expressions (re):** para identificar y extraer información de las fichas.
- **JSON:** para almacenar los datos.
- **ThreadPoolExecutor:** para ejecutar consultas concurrentes.

## Estructura del proyecto

```text
DragonBallScrapper/
│
├── data/
│   └── personajes.json
│
├── main.py
├── scraper.py
├── requirements.txt
└── README.md
```

### Descripción de los archivos

| Archivo | Descripción |
|---|---|
| `main.py` | Punto de entrada del programa. Coordina la ejecución del scraper y muestra las estadísticas. |
| `scraper.py` | Contiene las funciones de consulta, extracción, limpieza y almacenamiento de datos. |
| `requirements.txt` | Lista las dependencias del proyecto. |
| `data/personajes.json` | Archivo donde se almacenan los personajes obtenidos. |
| `README.md` | Documentación del proyecto. |

## Instalación

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

También podés descargar el proyecto directamente desde GitHub.

### 2. Ingresar al directorio

```bash
cd DragonBallScrapper
```

### 3. Crear un entorno virtual

```bash
python -m venv .venv
```

### 4. Activar el entorno virtual

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## Ejecución

Para iniciar el scraper, ejecutá:

```bash
python main.py
```

El programa realizará las consultas necesarias a la API, buscará las categorías de personajes, procesará las páginas encontradas y almacenará los resultados.

## Información extraída

Actualmente, el scraper obtiene los siguientes datos de cada personaje:

| Campo | Descripción |
|---|---|
| `nombre` | Nombre del personaje. |
| `raza` | Raza o razas del personaje. |
| `genero` | Género del personaje. |
| `imagen` | URL de la imagen en miniatura. |

Los datos se extraen de la ficha de información de los personajes y no de sus biografías o descripciones.

### Ejemplo de resultado JSON

```json
{
    "nombre": "Son Goku",
    "raza": [
        "Saiyano"
    ],
    "genero": [
        "Masculino"
    ],
    "imagen": "URL_DE_LA_IMAGEN"
}
```

*El resultado es ilustrativo; los datos reales dependen de la información disponible en la wiki.*

## Funcionamiento general

El proceso de extracción se divide en las siguientes etapas:

1. **Consulta de categorías:** comienza desde la categoría principal de personajes y recorre sus subcategorías.
2. **Obtención de páginas:** recopila los títulos de las páginas encontradas.
3. **Procesamiento por lotes:** consulta varias páginas en una misma solicitud para reducir la cantidad de peticiones.
4. **Identificación de fichas:** verifica que el contenido de la página incluya la plantilla `{{Personaje}}`.
5. **Extracción:** obtiene los campos definidos en la configuración del scraper.
6. **Limpieza:** elimina etiquetas, referencias y determinadas plantillas de MediaWiki.
7. **Almacenamiento:** guarda los resultados en `data/personajes.json`.

## Consideraciones

- El proyecto utiliza la API de la wiki española de Dragon Ball en Fandom.
- Los datos dependen del contenido disponible y de cómo estén estructuradas las fichas de cada personaje.
- Algunos personajes pueden no tener todos los campos completos.
- Las imágenes se obtienen mediante las miniaturas disponibles en la API.
- El procesamiento concurrente puede reducir los tiempos de ejecución, aunque estos dependen de la conexión y de los límites del servidor.
- Se recomienda evitar realizar solicitudes excesivas a la API.

## Objetivo del proyecto

Este proyecto tiene como objetivo practicar el consumo de APIs, la extracción y transformación de datos, el uso de expresiones regulares, el procesamiento concurrente y el almacenamiento de información estructurada utilizando Python.

---

**Fuente de datos:** [Dragon Ball Wiki - Fandom (español)](https://dragonball.fandom.com/es/wiki/Dragon_Ball_Wiki)

Proyecto educativo, independiente y no oficial. No está afiliado a Fandom, Toei Animation ni a los titulares de los derechos de Dragon Ball.