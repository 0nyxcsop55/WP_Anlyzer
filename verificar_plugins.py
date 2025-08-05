#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Verificar Versiones y Vulnerabilidades de Plugins
Lee el archivo JSON generado por wp_auditor_simple.py
"""

import json
import requests
import time
import os

# Configuración
API_WPSCAN_TOKEN = os.getenv('WPSCAN_API_KEY', '')

def obtener_version_oficial(plugin_slug):
    """Obtiene la versión oficial del plugin desde WordPress.org"""
    url = f'https://api.wordpress.org/plugins/info/1.0/{plugin_slug}.json'
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            info = resp.json()
            return info.get('version')
        else:
            return None
    except:
        return None

def consultar_vulnerabilidades_wpscan(slug, api_token):
    """Consulta vulnerabilidades en WPScan"""
    if api_token == 'TU_API_KEY_AQUI':
        return []
    
    url = f"https://wpscan.com/api/v3/plugins/{slug}"
    headers = {"Authorization": f"Token token={api_token}"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("vulnerabilities", [])
        else:
            return []
    except Exception as e:
        return []

def version_desactualizada(version_actual, version_oficial):
    """Compara versiones para determinar si está desactualizada"""
    if not version_actual or not version_oficial:
        return False
    if "no visible" in str(version_actual).lower():
        return False

    def parsear(v):
        partes = []
        for x in v.split('.'):
            try:
                partes.append(int(x))
            except:
                break
        return partes

    actual = parsear(version_actual)
    oficial = parsear(version_oficial)
    return actual < oficial

def normalizar_slug(nombre_plugin):
    """Normaliza el nombre del plugin para la API"""
    return nombre_plugin.lower().replace(" ", "-")

def verificar_plugins(data, api_token):
    """Verifica el estado de los plugins detectados"""
    resultados = []
    cache_versiones = {}
    cache_vulns = {}

    for sitio_info in data:
        sitio = sitio_info['sitio']
        plugins = sitio_info['plugins_detectados']

        if isinstance(plugins, dict):
            for plugin, version_actual in plugins.items():
                slug = normalizar_slug(plugin)

                # Obtener versión oficial
                if slug in cache_versiones:
                    version_oficial = cache_versiones[slug]
                else:
                    version_oficial = obtener_version_oficial(slug)
                    cache_versiones[slug] = version_oficial
                    time.sleep(0.5)

                desactualizado = version_desactualizada(version_actual, version_oficial)

                # Obtener vulnerabilidades
                if slug in cache_vulns:
                    vulnerabilidades = cache_vulns[slug]
                else:
                    vulnerabilidades = consultar_vulnerabilidades_wpscan(slug, api_token)
                    cache_vulns[slug] = vulnerabilidades
                    time.sleep(0.5)

                resultados.append({
                    'sitio': sitio,
                    'plugin': plugin,
                    'version_actual': version_actual,
                    'version_oficial': version_oficial,
                    'desactualizado': desactualizado,
                    'vulnerabilidades': vulnerabilidades
                })
        else:
            resultados.append({
                'sitio': sitio,
                'plugin': None,
                'version_actual': None,
                'version_oficial': None,
                'desactualizado': False,
                'vulnerabilidades': [],
                'error': plugins
            })

    return resultados

def main():
    """Función principal"""
    print("[INFO] Verificando versiones y vulnerabilidades de plugins...\n")
    
    # Leer datos del archivo JSON
    try:
        with open('plugins_detectados.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[ERROR] No se encontró el archivo 'plugins_detectados.json'")
        print("[INFO] Ejecuta primero: python wp_auditor_simple.py")
        return

    if API_WPSCAN_TOKEN == "TU_API_KEY_AQUI":
        print("[WARNING] Para verificar vulnerabilidades, configura tu API token de WPScan:")
        print("   1. Obtén una clave gratuita en: https://wpscan.com/api/")
        print("   2. Configura la variable de entorno: $env:WPSCAN_API_KEY='tu_clave_aqui'")
        print("\n[INFO] Continuando solo con verificación de versiones...")

    print(f"[INFO] Analizando {len(data)} sitios...")
    resultados = verificar_plugins(data, API_WPSCAN_TOKEN)

    # Guardar resultados completos
    with open("reporte_completo.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    # Mostrar reporte
    print("\n[INFO] Reporte de estado de plugins:\n")
    for r in resultados:
        if 'error' in r:
            print(f"{r['sitio']}: [ERROR] -> {r['error']}")
            continue

        estado = "[DESACTUALIZADO]" if r['desactualizado'] else "[OK]"
        print(f"{r['sitio']} - {r['plugin']}: {r['version_actual']} / Oficial {r['version_oficial']} -> {estado}")

        if r['vulnerabilidades']:
            print(f"   [WARNING] Vulnerabilidades encontradas ({len(r['vulnerabilidades'])}):")
            for v in r['vulnerabilidades']:
                cve = v.get("cve") or "Sin CVE"
                title = v.get("title", "Sin título")
                url = v.get("references", {}).get("url", [])
                link = url[0] if url else "Sin enlace"
                print(f"     - {title} ({cve})")
                print(f"       -> {link}")
        print()

    print("[INFO] Reporte completo guardado en 'reporte_completo.json'")

if __name__ == "__main__":
    main() 