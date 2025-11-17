#!/usr/bin/env python3
import markdown
from weasyprint import HTML, CSS
import re

# Leer el archivo Markdown
with open('presentacion.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

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
            margin: 2cm;
        }}
        body {{
            font-family: 'Arial', sans-serif;
            font-size: 14pt;
            line-height: 1.4;
        }}
        h1 {{
            font-size: 28pt;
            color: #2c3e50;
            text-align: center;
            page-break-after: always;
            margin-top: 2cm;
        }}
        h2 {{
            font-size: 24pt;
            color: #34495e;
            page-break-before: always;
            margin-top: 1cm;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.3cm;
        }}
        h3 {{
            font-size: 18pt;
            color: #555;
            margin-top: 0.5cm;
        }}
        h4 {{
            font-size: 16pt;
            color: #666;
            font-style: italic;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1cm 0;
            font-size: 12pt;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        img {{
            max-width: 100%;
            max-height: 12cm;
            display: block;
            margin: 0.5cm auto;
        }}
        blockquote {{
            background: #f9f9f9;
            border-left: 5px solid #3498db;
            margin: 1cm 0;
            padding: 0.5cm 1cm;
            font-style: italic;
        }}
        ul, ol {{
            margin-left: 1.5cm;
        }}
        li {{
            margin: 0.3cm 0;
        }}
        hr {{
            display: none;
        }}
        strong {{
            color: #2980b9;
        }}
        audio {{
            display: block;
            margin: 0.5cm auto;
            width: 80%;
        }}
        p {{
            text-align: justify;
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
