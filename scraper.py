import requests
import re
import json
import os
from concurrent.futures import ThreadPoolExecutor

API_URL = "https://dragonball.fandom.com/es/api.php"

HEADERS = {
    "User-Agent": "DragonBallScraper/1.0 (proyecto educativo)"
}

CAMPOS = {
    "nombre": "Nombre",
    "raza": "raza",
    "genero": "sexo"
}

PATRONES_LIMPIEZA = [
    (r"<ref\b[^>]*>.*?</ref>", ""),
    (r"<ref\b[^>]*/>", ""),
    (r"\[\[(?:[^\]|]*\|)?([^\]]+)\]\]", r"\1"),
    (r"\{\{\s*Small\s*\|(.*?)\}\}", r"\1"),
    (r"\{\{\s*Former\s*\}\}", "formerly"),
    (r"<[^>]+>", " "),
    (r"\{\{\s*Masculino\s*\}\}", "Masculino"),
    (r"\{\{\s*Femenino\s*\}\}", "Femenino")
]

def consultar_api(sesion, parametros, timeout=15):
    respuesta = sesion.get(
        API_URL,
        params=parametros,
        headers=HEADERS,
        timeout=timeout
    )

    respuesta.raise_for_status()
    return respuesta.json()


def obtener_contenido(pagina):
    return (
        pagina.get("revisions", [{}])[0]
        .get("slots", {})
        .get("main", {})
        .get("*", "")
    )


def limpiar_texto(texto):
    if texto is None:
        return None

    for patron, reemplazo in PATRONES_LIMPIEZA:
        texto = re.sub(
            patron,
            reemplazo,
            texto,
            flags=re.DOTALL | re.IGNORECASE
        )

    texto = texto.replace("'''", "").replace("''", "")

    return re.sub(r"\s+", " ", texto).strip()


def limpiar_datos(datos):
    for campo, valor in datos.items():
        if isinstance(valor, list):
            datos[campo] = [
                limpiar_texto(elemento)
                for elemento in valor
            ]
        elif valor is not None:
            datos[campo] = limpiar_texto(valor)

    return datos


def guardar_json(personajes, ruta):
    directorio = os.path.dirname(ruta)

    if directorio:
        os.makedirs(directorio, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(
            personajes,
            archivo,
            indent=4,
            ensure_ascii=False
        )

def obtener_pagina(nombre_personaje):
    parametros = {
        "action": "query",
        "titles": nombre_personaje,
        "prop": "revisions|pageimages",
        "rvprop": "content",
        "rvslots": "main",
        "piprop": "thumbnail",
        "pithumbsize": 500,
        "redirects": 1,
        "format": "json"
    }

    with requests.Session() as sesion:
        datos = consultar_api(sesion, parametros)

    paginas = datos.get("query", {}).get("pages", {})
    personaje = next(iter(paginas.values()), {})

    if not personaje or "missing" in personaje:
        return None

    return {
        "nombre": personaje.get("title"),
        "contenido": obtener_contenido(personaje),
        "imagen": personaje.get("thumbnail", {}).get("source")
    }

def extraer_datos_personaje(contenido):
    datos = {}

    for clave, campo in CAMPOS.items():
        patron = rf"(?im)^\|{campo}[ \t]*=[ \t]*(.*)$"
        resultado = re.search(patron, contenido)

        if not resultado or not resultado.group(1).strip():
            datos[clave] = None
            continue

        valores = [
            valor.strip()
            for valor in resultado.group(1).split("<br>")
            if valor.strip()
        ]

        datos[clave] = (
            valores[0] if clave == "nombre" else valores
        )

    return datos

def guardar_personaje(personaje, ruta="data/personajes.json"):
    nombre = personaje.get("nombre")

    if not isinstance(nombre, str) or not nombre.strip():
        print("No se puede guardar el personaje: falta un nombre válido.")
        return

    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as archivo:
            personajes = json.load(archivo)
    else:
        personajes = []

    actualizado = False

    for indice, existente in enumerate(personajes):
        if not isinstance(existente, dict):
            continue

        nombre_existente = existente.get("nombre")

        if (
            isinstance(nombre_existente, str)
            and nombre_existente.lower() == nombre.lower()
        ):
            personajes[indice] = personaje
            actualizado = True
            break

    if not actualizado:
        personajes.append(personaje)

    guardar_json(personajes, ruta)

    mensaje = "actualizado" if actualizado else "agregado"
    print(f"Personaje {mensaje} correctamente.")


def guardar_todos_los_personajes(
    personajes,
    ruta="data/personajes.json"
):
    guardar_json(personajes, ruta)

    print(
        f"\nSe guardaron {len(personajes)} personajes correctamente."
    )

def obtener_titulos_personajes():
    pendientes = ["Categoría:Personajes"]
    visitadas = set()
    titulos = set()

    def procesar_categoria(categoria):
        parametros = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": categoria,
            "cmtype": "page|subcat",
            "cmlimit": "max",
            "format": "json"
        }

        miembros = []

        with requests.Session() as sesion:
            while True:
                datos = consultar_api(sesion, parametros)

                miembros.extend(
                    datos.get("query", {}).get("categorymembers", [])
                )

                continuacion = datos.get("continue")

                if not continuacion:
                    break

                parametros.update(continuacion)

        return miembros

    with ThreadPoolExecutor(max_workers=8) as executor:
        while pendientes:
            lote_categorias = []

            while pendientes and len(lote_categorias) < 8:
                categoria = pendientes.pop()

                if categoria not in visitadas:
                    visitadas.add(categoria)
                    lote_categorias.append(categoria)

            resultados = executor.map(
                procesar_categoria,
                lote_categorias
            )

            for miembros in resultados:
                for miembro in miembros:
                    if miembro["ns"] == 0:
                        titulos.add(miembro["title"])

                    elif miembro["ns"] == 14:
                        categoria = miembro["title"]

                        if categoria not in visitadas:
                            pendientes.append(categoria)

            print(
                f"Categorías consultadas: {len(visitadas)} "
                f"| Páginas encontradas: {len(titulos)}"
            )

    return sorted(titulos)

def obtener_personajes_por_lotes(titulos, tamano_lote=50):
    personajes = []

    lotes = [
        titulos[inicio:inicio + tamano_lote]
        for inicio in range(0, len(titulos), tamano_lote)
    ]

    def procesar_lote(lote):
        parametros = {
            "action": "query",
            "titles": "|".join(lote),
            "prop": "revisions|pageimages",
            "rvprop": "content",
            "rvslots": "main",
            "piprop": "thumbnail",
            "pithumbsize": 500,
            "redirects": 1,
            "format": "json"
        }

        with requests.Session() as sesion:
            datos = consultar_api(
                sesion,
                parametros,
                timeout=30
            )

        personajes_lote = []
        paginas = datos.get("query", {}).get("pages", {})

        for pagina in paginas.values():
            if "missing" in pagina:
                continue

            contenido = obtener_contenido(pagina)

            if not re.search(
                r"\{\{\s*Personaje\b",
                contenido,
                re.IGNORECASE
            ):
                continue

            datos_personaje = limpiar_datos(
                extraer_datos_personaje(contenido)
            )

            datos_personaje["imagen"] = (
                pagina.get("thumbnail", {}).get("source")
            )

            if datos_personaje.get("nombre"):
                personajes_lote.append(datos_personaje)

        return personajes_lote

    with ThreadPoolExecutor(max_workers=3) as executor:
        for indice, resultado in enumerate(
            executor.map(procesar_lote, lotes),
            start=1
        ):
            personajes.extend(resultado)

            procesados = min(
                indice * tamano_lote,
                len(titulos)
            )

            print(
                f"Lotes procesados: {procesados}/{len(titulos)} "
                f"| Personajes encontrados: {len(personajes)}"
            )

    return personajes