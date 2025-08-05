#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Principal de Auditoría WordPress
Ejecuta todo el proceso: detección, verificación y reporte HTML
"""

import subprocess
import sys
import os

def ejecutar_script(script_name, descripcion):
    """Ejecuta un script y muestra el progreso"""
    print(f"\n[INFO] {descripcion}...")
    print("=" * 50)
    
    try:
        resultado = subprocess.run([sys.executable, script_name], 
                                 capture_output=True, text=True, encoding='utf-8')
        
        if resultado.returncode == 0:
            print(resultado.stdout)
            print("[OK] Completado exitosamente")
            return True
        else:
            print("[ERROR] Error al ejecutar el script")
            print(resultado.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Función principal que ejecuta todo el proceso"""
    print("[INFO] Iniciando Auditoría Completa de WordPress")
    print("=" * 50)
    
    # Verificar que existan los archivos necesarios
    scripts_requeridos = [
        ('wp_auditor_simple.py', 'Detección de plugins'),
        ('verificar_plugins.py', 'Verificación de versiones'),
        ('generar_reporte_html.py', 'Generación de reporte HTML')
    ]
    
    for script, descripcion in scripts_requeridos:
        if not os.path.exists(script):
            print(f"[ERROR] No se encontró el archivo: {script}")
            return
    
    # Paso 1: Detectar plugins
    if not ejecutar_script('wp_auditor_simple.py', 'Paso 1: Detectando plugins'):
        print("[ERROR] Falló la detección de plugins. Deteniendo proceso.")
        return
    
    # Paso 2: Verificar versiones
    if not ejecutar_script('verificar_plugins.py', 'Paso 2: Verificando versiones'):
        print("[WARNING] Falló la verificación de versiones, pero continuando...")
    
    # Paso 3: Generar reporte HTML
    if not ejecutar_script('generar_reporte_html.py', 'Paso 3: Generando reporte HTML'):
        print("[ERROR] Falló la generación del reporte HTML.")
        return
    
    # Resumen final
    print("\n" + "=" * 50)
    print("[SUCCESS] AUDITORÍA COMPLETADA EXITOSAMENTE")
    print("=" * 50)
    print("[INFO] Archivos generados:")
    print("   • plugins_detectados.json - Lista de plugins detectados")
    print("   • reporte_completo.json - Análisis completo con versiones")
    print("   • reporte_wordpress.html - Reporte visual en HTML")
    print("\n[INFO] Para ver el reporte:")
    print("   • Abre 'reporte_wordpress.html' en tu navegador")
    print("   • O ejecuta: start reporte_wordpress.html")
    print("\n[INFO] Para análisis adicional:")
    print("   • Revisa 'reporte_completo.json' para detalles técnicos")
    print("   • Configura API key de WPScan para análisis de vulnerabilidades")

if __name__ == "__main__":
    main() 