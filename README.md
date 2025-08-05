# Auditor de Seguridad para Sitios WordPress

Scripts simplificados para detectar y auditar plugins de WordPress con reportes HTML.

## 📁 Archivos del Proyecto

- **`wp_auditor_simple.py`** - Script principal que detecta plugins
- **`verificar_plugins.py`** - Script que verifica versiones y vulnerabilidades
- **`generar_reporte_html.py`** - Genera reporte HTML visual
- **`dominios.txt`** - Lista de dominios a analizar
- **`plugins_detectados.json`** - Resultados de detección de plugins
- **`reporte_completo.json`** - Reporte completo con versiones y vulnerabilidades
- **`reporte_wordpress.html`** - Reporte visual en HTML

## 🚀 Uso Rápido

### 1. Detectar Plugins
```bash
python wp_auditor_simple.py
```

### 2. Verificar Versiones y Vulnerabilidades
```bash
python verificar_plugins.py
```

### 3. Generar Reporte HTML
```bash
python generar_reporte_html.py
```

## 📋 Funcionalidades

### ✅ Detección de Plugins
- Detecta plugins instalados en sitios WordPress
- Extrae versiones cuando están disponibles
- Identifica plugins con versiones ocultas
- Guarda resultados en JSON

### ✅ Verificación de Versiones
- Compara versiones instaladas vs. oficiales
- Identifica plugins desactualizados
- Usa la API de WordPress.org
- Cache para evitar consultas repetidas

### ✅ Análisis de Vulnerabilidades (con API key)
- Consulta vulnerabilidades en WPScan
- Muestra CVE y enlaces de referencia
- Requiere API key gratuita de WPScan

### ✅ Reporte HTML Visual Moderno
- **Tailwind CSS** para diseño moderno y responsive
- **Font Awesome** para iconos profesionales
- **AOS Animations** para efectos de entrada
- **Chart.js** para gráficos interactivos
- **Google Fonts** (Inter) para tipografía moderna
- **Comparación de versiones** (actual vs. última disponible)
- **Código de colores** para estados de plugins
- **Efectos hover** y animaciones suaves
- **Gradientes** y efectos glass morphism
- **Diseño profesional** y atractivo
- **Fácil de compartir** por email o web

## 🔧 Configuración

### Configurar API Key de WPScan (Opcional)

1. **Obtener API key gratuita**: https://wpscan.com/api/
2. **Configurar variable de entorno**:

#### Windows (PowerShell):
```powershell
$env:WPSCAN_API_KEY="tu_clave_aqui"
```

#### Windows (CMD):
```cmd
set WPSCAN_API_KEY=tu_clave_aqui
```

#### Linux/Mac:
```bash
export WPSCAN_API_KEY="tu_clave_aqui"
```

### Editar Lista de Dominios

Edita el archivo `dominios.txt`:
```txt
# Lista de dominios a analizar
# Un dominio por línea (sin http:// o https://)

sitioweb1.com
sitioweb2.com
```

## 📈 Resultados

### Sin API Key:
- ✅ Detección de plugins
- ✅ Verificación de versiones
- ✅ Reporte HTML visual
- ❌ Análisis de vulnerabilidades

### Con API Key:
- ✅ Detección de plugins
- ✅ Verificación de versiones
- ✅ Análisis de vulnerabilidades
- ✅ Reportes detallados
- ✅ Reporte HTML visual

## 📄 Archivos de Salida

### `plugins_detectados.json`
```json
[
    {
        "sitio": "https://sitio1.com",
        "plugins_detectados": {
            "wp-whatsapp": "3.4",
            "contact-form-7": "5.7.5.1",
            "revslider": "6.2.23"
        }
    }
]
```

### `reporte_completo.json`
```json
[
    {
        "sitio": "https://sitio2.com",
        "plugin": "contact-form-7",
        "version_actual": "5.7.5.1",
        "version_oficial": "6.1.1",
        "desactualizado": true,
        "vulnerabilidades": []
    }
]
```

### `reporte_wordpress.html`
- **Reporte visual moderno** con Tailwind CSS
- **Gráfico interactivo** de estadísticas con Chart.js
- **Animaciones suaves** con AOS (Animate On Scroll)
- **Iconos profesionales** con Font Awesome
- **Comparación de versiones** para plugins desactualizados
- **Código de colores**: Rojo (actual), Verde (última disponible)
- **Efectos hover** y gradientes modernos
- **Diseño responsive** y completamente atractivo
- **Fácil de compartir** por email o web

## 🔍 Ejemplo de Reporte

```
📋 Reporte de estado de plugins:

https://sitio1.com - wp-whatsapp: 3.4 / Oficial 3.7.3 -> 🟠 DESACTUALIZADO
https://sitio1.com - contact-form-7: 5.7.5.1 / Oficial 6.1.1 -> 🟠 DESACTUALIZADO
https://sitio1.com - google-analytics-for-wordpress: 9.6.1 / Oficial 9.6.1 -> ✅ OK
```

## ⚡ Características Técnicas

- **Detección por regex**: Busca plugins en el código HTML
- **Cache inteligente**: Evita consultas repetidas a APIs
- **Manejo de errores**: Continúa aunque algunos sitios fallen
- **Rate limiting**: Pausas automáticas entre consultas
- **Formato JSON**: Resultados estructurados y legibles
- **Reporte HTML**: Interfaz visual profesional

## 🛠️ Requisitos

```bash
pip install requests
```

## 📝 Notas

- Los scripts funcionan sin API key (solo detección y versiones)
- Para vulnerabilidades, se requiere API key de WPScan
- Los resultados se guardan en archivos JSON para análisis posterior
- El script maneja timeouts y errores de conexión automáticamente
- El reporte HTML es completamente autónomo (no requiere internet)

## 🔒 Seguridad

- Nunca compartas tu API key en código público
- Usa variables de entorno para configurar claves
- Los scripts solo realizan consultas de lectura
- No modifican ningún sitio web

## 📞 Soporte

Para problemas o preguntas:
- Verifica que los dominios sean accesibles
- Confirma que los sitios usen WordPress
- Revisa la configuración de la API key
- Consulta los archivos de log generados 

