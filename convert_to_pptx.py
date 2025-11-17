#!/usr/bin/env python3
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import re
import os

# Crear presentación
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# Leer archivo Markdown
with open('presentacion.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Dividir por diapositivas (separadas por ---)
slides_content = content.split('---\n')

def add_title_slide(prs, title):
    """Crear diapositiva de título"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Layout en blanco

    # Título principal
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(9), Inches(2))
    tf = txBox.text_frame
    tf.text = title
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.size = Pt(44)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(44, 62, 80)

    return slide

def parse_markdown_line(line):
    """Parsear una línea de markdown"""
    # Headers
    if line.startswith('#### '):
        return ('h4', line[5:].strip())
    elif line.startswith('### '):
        return ('h3', line[4:].strip())
    elif line.startswith('## '):
        return ('h2', line[3:].strip())
    elif line.startswith('# '):
        return ('h1', line[2:].strip())
    # Listas
    elif re.match(r'^\d+\.\s', line):
        return ('ol', re.sub(r'^\d+\.\s', '', line))
    elif line.startswith('- ') or line.startswith('* '):
        return ('ul', line[2:].strip())
    # Imágenes
    elif line.startswith('!['):
        match = re.match(r'!\[([^\]]*)\]\(([^\)]+)\)', line)
        if match:
            return ('img', {'alt': match.group(1), 'src': match.group(2)})
    # Audios
    elif '<audio controls>' in line:
        return ('audio_start', None)
    elif '<source src=' in line:
        match = re.search(r'src="([^"]+)"', line)
        if match:
            return ('audio', match.group(1))
    # Blockquote
    elif line.startswith('> '):
        return ('quote', line[2:].strip())
    # Tablas
    elif '|' in line and not line.strip().startswith('|---'):
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        return ('table', cells)
    # Texto normal
    elif line.strip():
        return ('text', line.strip())

    return ('empty', None)

def add_content_slide(prs, slide_text):
    """Crear diapositiva de contenido"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Layout en blanco

    lines = slide_text.strip().split('\n')
    current_y = 0.5
    title_text = None
    subtitle_text = None

    # Buscar título
    for line in lines:
        parsed = parse_markdown_line(line)
        if parsed[0] == 'h2':
            title_text = parsed[1]
            break
        elif parsed[0] == 'h1':
            return add_title_slide(prs, parsed[1])

    # Agregar título
    if title_text:
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
        tf = title_box.text_frame
        tf.text = title_text
        tf.paragraphs[0].font.size = Pt(32)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = RGBColor(52, 73, 94)
        current_y = 1.2

    # Procesar contenido
    i = 0
    table_rows = []
    in_table = False
    audio_files = []

    while i < len(lines):
        line = lines[i]
        parsed = parse_markdown_line(line)

        if parsed[0] == 'h3':
            # Subtítulo
            if current_y < 7:
                sub_box = slide.shapes.add_textbox(Inches(0.5), Inches(current_y), Inches(9), Inches(0.5))
                tf = sub_box.text_frame
                tf.text = parsed[1]
                tf.paragraphs[0].font.size = Pt(24)
                tf.paragraphs[0].font.bold = True
                tf.paragraphs[0].font.color.rgb = RGBColor(85, 85, 85)
                current_y += 0.6

        elif parsed[0] == 'h4':
            # Sub-subtítulo
            if current_y < 7:
                sub_box = slide.shapes.add_textbox(Inches(0.7), Inches(current_y), Inches(8.5), Inches(0.4))
                tf = sub_box.text_frame
                tf.text = parsed[1]
                tf.paragraphs[0].font.size = Pt(20)
                tf.paragraphs[0].font.italic = True
                tf.paragraphs[0].font.color.rgb = RGBColor(102, 102, 102)
                current_y += 0.5

        elif parsed[0] in ['ul', 'ol']:
            # Lista
            if current_y < 6.5:
                bullet_box = slide.shapes.add_textbox(Inches(1), Inches(current_y), Inches(8), Inches(0.4))
                tf = bullet_box.text_frame
                # Remover markdown bold
                text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', parsed[1])
                tf.text = '• ' + text
                tf.paragraphs[0].font.size = Pt(18)
                current_y += 0.35

        elif parsed[0] == 'img':
            # Imagen
            img_path = parsed[1]['src']
            if os.path.exists(img_path) and current_y < 6:
                try:
                    pic = slide.shapes.add_picture(img_path, Inches(2), Inches(current_y), height=Inches(4))
                    current_y += 4.2
                except:
                    pass

        elif parsed[0] == 'audio':
            # Audio
            audio_files.append(parsed[1])

        elif parsed[0] == 'quote':
            # Cita
            if current_y < 6.5:
                quote_box = slide.shapes.add_textbox(Inches(1), Inches(current_y), Inches(8), Inches(0.8))
                tf = quote_box.text_frame
                text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', parsed[1])
                text = re.sub(r'\*([^\*]+)\*', r'\1', text)
                tf.text = text
                tf.paragraphs[0].font.size = Pt(16)
                tf.paragraphs[0].font.italic = True
                tf.paragraphs[0].font.color.rgb = RGBColor(52, 152, 219)
                current_y += 0.5

        elif parsed[0] == 'table':
            # Acumular filas de tabla
            if not in_table:
                table_rows = []
                in_table = True
            table_rows.append(parsed[1])

        elif parsed[0] == 'text':
            # Terminar tabla si estábamos en una
            if in_table and table_rows:
                # Crear tabla
                if current_y < 5 and len(table_rows) > 1:
                    rows = len(table_rows)
                    cols = len(table_rows[0])
                    table = slide.shapes.add_table(rows, cols, Inches(0.5), Inches(current_y), Inches(9), Inches(min(2.5, rows * 0.4))).table

                    # Llenar tabla
                    for row_idx, row_data in enumerate(table_rows):
                        for col_idx, cell_data in enumerate(row_data):
                            cell = table.cell(row_idx, col_idx)
                            cell.text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', cell_data)
                            cell.text_frame.paragraphs[0].font.size = Pt(14)
                            if row_idx == 0:
                                cell.fill.solid()
                                cell.fill.fore_color.rgb = RGBColor(52, 152, 219)
                                cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
                                cell.text_frame.paragraphs[0].font.bold = True

                    current_y += min(2.7, rows * 0.4 + 0.3)

                table_rows = []
                in_table = False

            # Texto normal
            if current_y < 6.8:
                text_box = slide.shapes.add_textbox(Inches(0.5), Inches(current_y), Inches(9), Inches(0.4))
                tf = text_box.text_frame
                text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', parsed[1])
                tf.text = text
                tf.paragraphs[0].font.size = Pt(16)
                current_y += 0.3

        i += 1

    # Agregar audios al final de la diapositiva
    for idx, audio_file in enumerate(audio_files):
        if os.path.exists(audio_file):
            try:
                # Posición para los audios
                audio_y = 6.5
                audio_x = 1 + (idx * 2.5)

                # Agregar el archivo de audio (PowerPoint lo mostrará con un ícono)
                movie = slide.shapes.add_movie(
                    audio_file,
                    Inches(audio_x), Inches(audio_y),
                    Inches(0.5), Inches(0.5)
                )
            except Exception as e:
                print(f"Error al agregar audio {audio_file}: {e}")

    return slide

# Procesar cada diapositiva
for slide_content in slides_content:
    if slide_content.strip():
        add_content_slide(prs, slide_content)

# Guardar presentación
prs.save('presentacion.pptx')
print("Presentación PowerPoint generada: presentacion.pptx")
print(f"Total de diapositivas: {len(prs.slides)}")
