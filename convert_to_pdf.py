#!/usr/bin/env python3
import markdown
from weasyprint import HTML, CSS
import re

# Leer el archivo Markdown
with open('presentacion.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Reemplazar tags de audio con indicadores visuales
def replace_audio(match):
    audio_file = match.group(1)
    return f'<div class="audio-indicator">🔊 Audio: {audio_file}</div>'

md_content = re.sub(r'<audio controls>\s*<source src="([^"]+)"[^>]*>\s*</audio>', replace_audio, md_content)

# Convertir Markdown a HTML
md = markdown.Markdown(extensions=['extra', 'nl2br', 'sane_lists'])
html_body = md.convert(md_content)

# Crear HTML completo con estilos para presentación
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>¿Niño o niña? La percepción del género en las voces infantiles</title>
    <style>
        @page {{
            size: A4 landscape;
            margin: 1.5cm;
        }}
        body {{
            font-family: 'Arial', sans-serif;
            font-size: 16pt;
            line-height: 1.5;
        }}
        h1 {{
            font-size: 36pt;
            color: #2c3e50;
            text-align: center;
            page-break-after: always;
            margin-top: 3cm;
        }}
        h2 {{
            font-size: 28pt;
            color: #34495e;
            page-break-before: always;
            margin-top: 0.5cm;
            margin-bottom: 0.8cm;
            border-bottom: 4px solid #3498db;
            padding-bottom: 0.3cm;
        }}
        h3 {{
            font-size: 22pt;
            color: #555;
            margin-top: 0.5cm;
            margin-bottom: 0.5cm;
        }}
        h4 {{
            font-size: 18pt;
            color: #666;
            font-style: italic;
            margin-top: 0.3cm;
        }}
        table {{
            width: 95%;
            margin: 0.8cm auto;
            border-collapse: collapse;
            font-size: 13pt;
        }}
        th, td {{
            border: 1px solid #bdc3c7;
            padding: 10px;
            text-align: center;
        }}
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        img {{
            max-width: 90%;
            max-height: 13cm;
            display: block;
            margin: 1cm auto;
        }}
        blockquote {{
            background: #ecf0f1;
            border-left: 6px solid #3498db;
            margin: 0.8cm 1cm;
            padding: 0.6cm 1cm;
            font-style: italic;
            font-size: 15pt;
        }}
        ul, ol {{
            margin-left: 1.2cm;
            font-size: 16pt;
        }}
        li {{
            margin: 0.4cm 0;
        }}
        hr {{
            display: none;
        }}
        strong {{
            color: #2980b9;
        }}
        .audio-indicator {{
            background: #e8f4f8;
            border: 2px solid #3498db;
            border-radius: 8px;
            padding: 0.5cm;
            margin: 0.5cm auto;
            text-align: center;
            font-size: 16pt;
            color: #2c3e50;
            width: 60%;
        }}
        p {{
            text-align: left;
            margin: 0.4cm 0;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

# Guardar HTML temporal
with open('temp_presentation.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# Convertir HTML a PDF
print("Generando PDF...")
HTML('temp_presentation.html').write_pdf('presentacion.pdf')
print("PDF generado: presentacion.pdf")
