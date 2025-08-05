#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Simple de Auditoría de WordPress
Lee dominios desde un archivo y detecta plugins
"""

import requests
import re
import json
import os

# Configuración
API_WPSCAN_TOKEN = os.getenv('WPSCAN_API_KEY', '')

# Regex para plugins con versión
plugin_version_regex = re.compile(r"/wp-content/plugins/([a-zA-Z0-9_-]+)/.*?ver=([0-9.]+)")
plugin_simple_regex = re.compile(r"/wp-content/plugins/([a-zA-Z0-9_-]+)/")

def leer_dominios(archivo):
    """Lee dominios desde un archivo"""
    dominios = []
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                dominio = linea.strip()
                if dominio and not dominio.startswith('#'):
                    # Añadir https:// si no está presente
                    if not dominio.startswith(('http://', 'https://')):
                        dominio = f'https://{dominio}'
                    dominios.append(dominio)
        return dominios
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo {archivo}")
        return []

def detectar_plugins(url):
    """Detecta plugins en un sitio WordPress"""
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        html = response.text

        # Buscar plugins con versiones
        plugins_con_version = plugin_version_regex.findall(html)
        plugins_detectados = {}

        for plugin, version in plugins_con_version:
            plugins_detectados[plugin] = version

        # Buscar plugins sin versión (para complementar)
        plugins_simples = plugin_simple_regex.findall(html)
        for plugin in plugins_simples:
            if plugin not in plugins_detectados:
                plugins_detectados[plugin] = "versión no visible"

        return plugins_detectados

    except Exception as e:
        print(f"[ERROR] Error al acceder a {url}: {e}")
        return {}

def main():
    """Función principal"""
    print("[INFO] Iniciando escaneo de sitios WordPress...\n")
    
    # Leer dominios desde archivo
    dominios = leer_dominios('dominios.txt')
    if not dominios:
        print("[ERROR] No se pudieron cargar dominios. Verifica el archivo dominios.txt")
        return
    
    print(f"[INFO] Se cargaron {len(dominios)} dominios\n")
    
    # Detectar plugins
    resultados = []
    for url in dominios:
        plugins_detectados = detectar_plugins(url)
        resultados.append({
            "sitio": url,
            "plugins_detectados": plugins_detectados
        })
        print(f"[OK] {url} -> {len(plugins_detectados)} plugin(s): {', '.join(f'{k} ({v})' for k,v in plugins_detectados.items())}")

    # Guardar resultados
    with open("plugins_detectados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    print(f"\n[INFO] Resultados guardados en 'plugins_detectados.json'")
    print(f"[INFO] Total de sitios analizados: {len(dominios)}")
    print(f"[INFO] Total de plugins detectados: {sum(len(r['plugins_detectados']) for r in resultados)}")

if __name__ == "__main__":
    main() 