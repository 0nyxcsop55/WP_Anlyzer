#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Reporte HTML para Auditoría de WordPress
Crea un reporte visual moderno con Tailwind CSS y librerías atractivas
"""

import json
import os
from datetime import datetime

def generar_html(data, versiones_data=None):
    """Genera el HTML del reporte con diseño moderno"""
    
    # Contar estadísticas
    total_sitios = len(data)
    total_plugins = sum(len(sitio['plugins_detectados']) for sitio in data)
    plugins_desactualizados = 0
    plugins_actualizados = 0
    
    # Contar plugins por estado
    for sitio in data:
        for plugin, version in sitio['plugins_detectados'].items():
            if version != "versión no visible":
                plugins_actualizados += 1
            else:
                plugins_desactualizados += 1
    
    # Crear diccionario de versiones para búsqueda rápida
    versiones_dict = {}
    if versiones_data:
        for item in versiones_data:
            if 'sitio' in item and 'plugin' in item:
                key = f"{item['sitio']}_{item['plugin']}"
                versiones_dict[key] = {
                    'version_actual': item.get('version_actual'),
                    'version_oficial': item.get('version_oficial'),
                    'desactualizado': item.get('desactualizado', False)
                }
    
    html = f"""
<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auditoría de Seguridad WordPress</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- AOS Animation -->
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        'sans': ['Inter', 'sans-serif'],
                    }},
                    animation: {{
                        'fade-in': 'fadeIn 0.5s ease-in-out',
                        'slide-up': 'slideUp 0.5s ease-out',
                        'pulse-slow': 'pulse 3s infinite',
                    }}
                }}
            }}
        }}
    </script>
    
    <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .gradient-bg {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        .glass-effect {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .card-hover {{
            transition: all 0.3s ease;
        }}
        
        .card-hover:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }}
        
        .status-badge {{
            transition: all 0.3s ease;
        }}
        
        .status-badge:hover {{
            transform: scale(1.05);
        }}
    </style>
</head>
<body class="bg-gray-50 font-sans">
    <!-- Header con gradiente -->
    <header class="gradient-bg text-white py-16">
        <div class="container mx-auto px-6">
            <div class="text-center" data-aos="fade-up">
                <div class="mb-6">
                    <i class="fas fa-shield-alt text-6xl mb-4"></i>
                </div>
                <h1 class="text-5xl font-bold mb-4 tracking-tight">
                    Auditoría de Seguridad WordPress
                </h1>
                <p class="text-xl opacity-90 max-w-2xl mx-auto">
                    Reporte completo de plugins detectados y análisis de vulnerabilidades
                </p>
                <div class="mt-8 flex justify-center space-x-4">
                    <span class="glass-effect px-4 py-2 rounded-full text-sm">
                        <i class="fas fa-calendar-alt mr-2"></i>
                        {datetime.now().strftime('%d/%m/%Y')}
                    </span>
                    <span class="glass-effect px-4 py-2 rounded-full text-sm">
                        <i class="fas fa-clock mr-2"></i>
                        {datetime.now().strftime('%H:%M')}
                    </span>
                </div>
            </div>
        </div>
    </header>

    <!-- Estadísticas principales -->
    <section class="py-16 bg-white">
        <div class="container mx-auto px-6">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                <div class="text-center card-hover bg-gradient-to-br from-blue-500 to-blue-600 text-white p-8 rounded-2xl shadow-lg" data-aos="fade-up" data-aos-delay="100">
                    <i class="fas fa-globe text-4xl mb-4"></i>
                    <div class="text-3xl font-bold mb-2">{total_sitios}</div>
                    <div class="text-blue-100">Sitios Analizados</div>
                </div>
                
                <div class="text-center card-hover bg-gradient-to-br from-green-500 to-green-600 text-white p-8 rounded-2xl shadow-lg" data-aos="fade-up" data-aos-delay="200">
                    <i class="fas fa-puzzle-piece text-4xl mb-4"></i>
                    <div class="text-3xl font-bold mb-2">{total_plugins}</div>
                    <div class="text-green-100">Plugins Detectados</div>
                </div>
                
                <div class="text-center card-hover bg-gradient-to-br from-yellow-500 to-yellow-600 text-white p-8 rounded-2xl shadow-lg" data-aos="fade-up" data-aos-delay="300">
                    <i class="fas fa-eye text-4xl mb-4"></i>
                    <div class="text-3xl font-bold mb-2">{plugins_actualizados}</div>
                    <div class="text-yellow-100">Versiones Visibles</div>
                </div>
                
                <div class="text-center card-hover bg-gradient-to-br from-red-500 to-red-600 text-white p-8 rounded-2xl shadow-lg" data-aos="fade-up" data-aos-delay="400">
                    <i class="fas fa-eye-slash text-4xl mb-4"></i>
                    <div class="text-3xl font-bold mb-2">{plugins_desactualizados}</div>
                    <div class="text-red-100">Versiones Ocultadas</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Gráfico de estadísticas -->
    <section class="py-16 bg-gray-50">
        <div class="container mx-auto px-6">
            <div class="max-w-4xl mx-auto">
                <h2 class="text-3xl font-bold text-center mb-12 text-gray-800">
                    <i class="fas fa-chart-pie mr-3"></i>
                    Análisis de Plugins
                </h2>
                <div class="bg-white rounded-2xl shadow-xl p-8">
                    <canvas id="pluginsChart" width="400" height="200"></canvas>
                </div>
            </div>
        </div>
    </section>

    <!-- Lista de sitios -->
    <section class="py-16 bg-white">
        <div class="container mx-auto px-6">
            <h2 class="text-3xl font-bold text-center mb-12 text-gray-800">
                <i class="fas fa-list mr-3"></i>
                Detalle por Sitio
            </h2>
            
            <div class="space-y-8">
"""
    
    # Generar contenido para cada sitio
    for i, sitio in enumerate(data):
        url = sitio['sitio']
        plugins = sitio['plugins_detectados']
        
        html += f"""
                <div class="card-hover bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100" data-aos="slide-up" data-aos-delay="{i * 100}">
                    <div class="bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-6">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-4">
                                <i class="fas fa-globe text-2xl"></i>
                                <div>
                                    <h3 class="text-xl font-semibold">{url}</h3>
                                    <p class="text-indigo-100">{len(plugins)} plugin(s) detectado(s)</p>
                                </div>
                            </div>
                            <div class="text-right">
                                <div class="text-3xl font-bold">{len(plugins)}</div>
                                <div class="text-indigo-100 text-sm">plugins</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="p-6">
"""
        
        if not plugins:
            html += f"""
                        <div class="text-center py-8">
                            <i class="fas fa-exclamation-triangle text-4xl text-yellow-500 mb-4"></i>
                            <p class="text-gray-600 text-lg">No se detectaron plugins</p>
                            <p class="text-gray-500">Posiblemente no es un sitio WordPress</p>
                        </div>
"""
        else:
            html += f"""
                        <div class="grid gap-4">
"""
            
            for plugin, version in plugins.items():
                # Buscar información de versiones
                version_key = f"{url}_{plugin}"
                version_info = versiones_dict.get(version_key, {})
                
                # Determinar estado y clases
                if version == "versión no visible":
                    status_class = "bg-yellow-100 text-yellow-800 border-yellow-200"
                    status_icon = "fas fa-eye-slash"
                    status_text = "Versión Ocultada"
                    version_html = f"""
                                <div class="text-sm text-gray-600">
                                    <i class="fas fa-info-circle mr-1"></i>
                                    Versión: {version}
                                </div>
"""
                else:
                    # Verificar si está desactualizado
                    if version_info.get('desactualizado', False):
                        status_class = "bg-red-100 text-red-800 border-red-200"
                        status_icon = "fas fa-exclamation-triangle"
                        status_text = "DESACTUALIZADO"
                        version_oficial = version_info.get('version_oficial', 'Desconocida')
                        version_html = f"""
                                <div class="text-sm text-gray-600 mb-2">
                                    <i class="fas fa-info-circle mr-1"></i>
                                    Versión actual: <span class="font-semibold text-red-600">{version}</span>
                                </div>
                                <div class="text-sm text-gray-600">
                                    <i class="fas fa-arrow-up mr-1"></i>
                                    Última versión: <span class="font-semibold text-green-600">{version_oficial}</span>
                                </div>
"""
                    else:
                        status_class = "bg-green-100 text-green-800 border-green-200"
                        status_icon = "fas fa-check-circle"
                        status_text = "ACTUALIZADO"
                        version_html = f"""
                                <div class="text-sm text-gray-600">
                                    <i class="fas fa-info-circle mr-1"></i>
                                    Versión: <span class="font-semibold text-green-600">{version}</span>
                                </div>
"""
                
                html += f"""
                            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-200">
                                <div class="flex-1">
                                    <div class="flex items-center space-x-3 mb-2">
                                        <i class="fas fa-puzzle-piece text-blue-500"></i>
                                        <h4 class="font-semibold text-gray-800">{plugin}</h4>
                                    </div>
                                    {version_html}
                                </div>
                                <div class="ml-4">
                                    <span class="status-badge inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border {status_class}">
                                        <i class="{status_icon} mr-1"></i>
                                        {status_text}
                                    </span>
                                </div>
                            </div>
"""
            
            html += """
                        </div>
"""
        
        html += """
                    </div>
                </div>
"""
    
    html += f"""
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-12">
        <div class="container mx-auto px-6 text-center">
            <div class="mb-6">
                <i class="fas fa-shield-alt text-4xl text-blue-400 mb-4"></i>
                <h3 class="text-2xl font-bold mb-2">Auditoría de Seguridad WordPress</h3>
                <p class="text-gray-400">Script de Detección y Análisis de Plugins</p>
            </div>
            <div class="flex justify-center space-x-6 text-gray-400">
                <span><i class="fas fa-calendar mr-2"></i>Generado el {datetime.now().strftime('%d/%m/%Y')}</span>
                <span><i class="fas fa-clock mr-2"></i>A las {datetime.now().strftime('%H:%M:%S')}</span>
            </div>
        </div>
    </footer>

    <!-- Scripts -->
    <script>
        // Inicializar AOS
        AOS.init({{
            duration: 800,
            easing: 'ease-in-out',
            once: true
        }});

        // Gráfico de estadísticas
        const ctx = document.getElementById('pluginsChart').getContext('2d');
        new Chart(ctx, {{
            type: 'doughnut',
            data: {{
                labels: ['Versiones Visibles', 'Versiones Ocultadas'],
                datasets: [{{
                    data: [{plugins_actualizados}, {plugins_desactualizados}],
                    backgroundColor: [
                        'rgba(34, 197, 94, 0.8)',
                        'rgba(239, 68, 68, 0.8)'
                    ],
                    borderColor: [
                        'rgba(34, 197, 94, 1)',
                        'rgba(239, 68, 68, 1)'
                    ],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 20,
                            usePointStyle: true,
                            font: {{
                                size: 14,
                                family: 'Inter'
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Efectos de hover y animaciones adicionales
        document.addEventListener('DOMContentLoaded', function() {{
            // Añadir efectos de hover a las tarjetas
            const cards = document.querySelectorAll('.card-hover');
            cards.forEach(card => {{
                card.addEventListener('mouseenter', function() {{
                    this.style.transform = 'translateY(-5px)';
                }});
                card.addEventListener('mouseleave', function() {{
                    this.style.transform = 'translateY(0)';
                }});
            }});

            // Animación de contadores
            const counters = document.querySelectorAll('.text-3xl');
            counters.forEach(counter => {{
                const target = parseInt(counter.textContent);
                let current = 0;
                const increment = target / 50;
                const timer = setInterval(() => {{
                    current += increment;
                    if (current >= target) {{
                        current = target;
                        clearInterval(timer);
                    }}
                    counter.textContent = Math.floor(current);
                }}, 30);
            }});
        }});
    </script>
</body>
</html>
"""
    
    return html

def main():
    """Función principal"""
    print("[INFO] Generando reporte HTML moderno...")
    
    # Leer datos del archivo JSON de plugins detectados
    try:
        with open('plugins_detectados.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[ERROR] No se encontró el archivo 'plugins_detectados.json'")
        print("[INFO] Ejecuta primero: python wp_auditor_simple.py")
        return
    
    # Leer datos de versiones (opcional)
    versiones_data = None
    try:
        with open('reporte_completo.json', 'r', encoding='utf-8') as f:
            versiones_data = json.load(f)
        print("[INFO] Información de versiones cargada")
    except FileNotFoundError:
        print("[INFO] No se encontró información de versiones, generando reporte básico")
    
    # Generar HTML
    html_content = generar_html(data, versiones_data)
    
    # Guardar archivo HTML
    with open('reporte_wordpress.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("[OK] Reporte HTML moderno generado: 'reporte_wordpress.html'")
    print(f"[INFO] Se analizaron {len(data)} sitios")
    print(f"[INFO] Total de plugins detectados: {sum(len(sitio['plugins_detectados']) for sitio in data)}")
    print("[INFO] Abre el archivo en tu navegador para ver el reporte moderno")

if __name__ == "__main__":
    main() 