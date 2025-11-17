#!/usr/bin/env python3
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
import os

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# Color principal: ROJO
PRIMARY_RED = RGBColor(192, 57, 43)
DARK_RED = RGBColor(142, 68, 73)
LIGHT_GRAY = RGBColor(236, 240, 241)
DARK_GRAY = RGBColor(52, 73, 94)

def add_title_slide():
    """Portada"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = DARK_GRAY

    title = slide.shapes.add_textbox(Inches(0.5), Inches(2), Inches(9), Inches(3.5))
    tf = title.text_frame
    tf.word_wrap = True

    p1 = tf.paragraphs[0]
    p1.text = "¿Niño o niña?"
    p1.font.size = Pt(54)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "La percepción del género en las voces infantiles"
    p2.font.size = Pt(38)
    p2.font.color.rgb = PRIMARY_RED
    p2.alignment = PP_ALIGN.CENTER

def add_header(slide, title_text):
    """Agregar encabezado rojo"""
    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0), Inches(10), Inches(1)
    )
    header.fill.solid()
    header.fill.fore_color.rgb = PRIMARY_RED
    header.line.fill.background()

    title_box = slide.shapes.add_textbox(Inches(0.2), Inches(0.15), Inches(9.6), Inches(0.7))
    tf = title_box.text_frame
    tf.text = title_text
    tf.paragraphs[0].font.size = Pt(34)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

def add_audio_slides():
    """Diapositivas de audio con reproductores embebidos"""

    # Slide 1: Audios 1-2
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Actividad inicial: ¿Quién está hablando?")

    subtitle = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(9), Inches(0.6))
    tf = subtitle.text_frame
    tf.text = "Escuchad estas voces y responded: ¿es un niño o una niña?"
    tf.paragraphs[0].font.size = Pt(26)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.bold = True

    audios = [("Audio 1", "audio_ninio_2.wav", 2, 2.1), ("Audio 2", "audio_ninia_1.wav", 6, 2.1)]
    for label, file, x, y in audios:
        # Marco
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x-0.2), Inches(y), Inches(3), Inches(3))
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_GRAY
        box.line.color.rgb = PRIMARY_RED
        box.line.width = Pt(3)

        # Label
        lbl = slide.shapes.add_textbox(Inches(x), Inches(y+0.3), Inches(2.6), Inches(0.5))
        lbl.text_frame.text = label
        lbl.text_frame.paragraphs[0].font.size = Pt(28)
        lbl.text_frame.paragraphs[0].font.bold = True
        lbl.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

        # Audio embebido
        if os.path.exists(file):
            slide.shapes.add_movie(file, Inches(x+0.5), Inches(y+1), Inches(1.5), Inches(1.5))

    # Slide 2: Audios 3-4
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Actividad inicial (II)")

    audios = [("Audio 3", "audio_ninio_3.wav", 2, 2), ("Audio 4", "audio_ninia3.wav", 6, 2)]
    for label, file, x, y in audios:
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x-0.2), Inches(y), Inches(3), Inches(3.5))
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_GRAY
        box.line.color.rgb = PRIMARY_RED
        box.line.width = Pt(3)

        lbl = slide.shapes.add_textbox(Inches(x), Inches(y+0.3), Inches(2.6), Inches(0.5))
        lbl.text_frame.text = label
        lbl.text_frame.paragraphs[0].font.size = Pt(28)
        lbl.text_frame.paragraphs[0].font.bold = True
        lbl.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

        if os.path.exists(file):
            slide.shapes.add_movie(file, Inches(x+0.5), Inches(y+1.2), Inches(1.5), Inches(1.5))

    # Slide 3: Audios 5-6 + Pregunta
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Actividad inicial (III)")

    audios = [("Audio 5", "audio_ninio_1.wav", 2, 1.5), ("Audio 6", "audio_ninia_2.wav", 6, 1.5)]
    for label, file, x, y in audios:
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x-0.2), Inches(y), Inches(3), Inches(3))
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_GRAY
        box.line.color.rgb = PRIMARY_RED
        box.line.width = Pt(3)

        lbl = slide.shapes.add_textbox(Inches(x), Inches(y+0.3), Inches(2.6), Inches(0.5))
        lbl.text_frame.text = label
        lbl.text_frame.paragraphs[0].font.size = Pt(28)
        lbl.text_frame.paragraphs[0].font.bold = True
        lbl.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

        if os.path.exists(file):
            slide.shapes.add_movie(file, Inches(x+0.5), Inches(y+1), Inches(1.5), Inches(1.5))

    question = slide.shapes.add_textbox(Inches(0.5), Inches(5.5), Inches(9), Inches(1.5))
    tf = question.text_frame
    tf.word_wrap = True
    tf.text = "Pregunta: ¿habéis podido identificar el género de cada voz?\n¿Con qué grado de certeza?"
    tf.paragraphs[0].font.size = Pt(24)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = PRIMARY_RED
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

def add_enigma_slide():
    """El enigma científico"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "El enigma científico")

    y = 1.3

    # Subtítulo
    sub = slide.shapes.add_textbox(Inches(0.5), Inches(y), Inches(9), Inches(0.5))
    sub.text_frame.text = "Lo que dice la investigación"
    sub.text_frame.paragraphs[0].font.size = Pt(28)
    sub.text_frame.paragraphs[0].font.color.rgb = DARK_GRAY
    sub.text_frame.paragraphs[0].font.bold = True
    y += 0.7

    # Texto principal
    txt = slide.shapes.add_textbox(Inches(0.7), Inches(y), Inches(8.6), Inches(1))
    tf = txt.text_frame
    tf.word_wrap = True
    tf.text = "Según Funk & Simpson (2023), identificamos el género de voces infantiles con una precisión del 70-84%, muy por encima del azar, pero:"
    tf.paragraphs[0].font.size = Pt(24)
    y += 1.2

    # Cita
    quote_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(y), Inches(8.4), Inches(1.8))
    quote_box.fill.solid()
    quote_box.fill.fore_color.rgb = LIGHT_GRAY
    quote_box.line.color.rgb = PRIMARY_RED
    quote_box.line.width = Pt(2)

    quote = slide.shapes.add_textbox(Inches(1.2), Inches(y+0.2), Inches(7.6), Inches(1.4))
    tf = quote.text_frame
    tf.word_wrap = True
    tf.text = '"Las diferencias en el aparato fonador entre niños y niñas antes de la pubertad son prácticamente inexistentes"\n\n— Fitch & Giedd (1999)'
    tf.paragraphs[0].font.size = Pt(22)
    tf.paragraphs[0].font.italic = True
    tf.paragraphs[0].font.color.rgb = DARK_GRAY
    y += 2

    # Pregunta final
    q = slide.shapes.add_textbox(Inches(0.5), Inches(y), Inches(9), Inches(0.8))
    q.text_frame.text = "Entonces, ¿cómo lo hacemos?"
    q.text_frame.paragraphs[0].font.size = Pt(32)
    q.text_frame.paragraphs[0].font.bold = True
    q.text_frame.paragraphs[0].font.color.rgb = PRIMARY_RED
    q.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

def add_table_slide():
    """Tabla de datos"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Los datos acústicos")

    sub = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(9), Inches(0.4))
    sub.text_frame.text = "Parámetros de las grabaciones que escuchasteis"
    sub.text_frame.paragraphs[0].font.size = Pt(24)
    sub.text_frame.paragraphs[0].font.color.rgb = DARK_GRAY

    # Tabla
    table = slide.shapes.add_table(7, 7, Inches(0.2), Inches(1.8), Inches(9.6), Inches(4.5)).table

    headers = ["Grabación", "Palabras", "Vocales", "Tono (Hz)", "F1 (Hz)", "F2 (Hz)", "F3 (Hz)"]
    data = [
        ["Niña 1", "4", "28", "300±38", "678±206", "1603±682", "2918±494"],
        ["Niña 2", "1", "16", "259±39", "702±186", "1376±339", "2568±583"],
        ["Niña 3", "3", "13", "238±23", "687±130", "1220±356", "2844±633"],
        ["Niño 1", "7", "23", "280±34", "660±132", "1741±494", "2697±406"],
        ["Niño 2", "2", "9", "268±39", "666±57", "1750±292", "2879±500"],
        ["Niño 3", "5", "15", "302±44", "681±140", "1598±501", "2800±573"],
    ]

    for col_idx, header in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_RED
        cell.text_frame.paragraphs[0].font.size = Pt(18)
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    for row_idx, row_data in enumerate(data):
        for col_idx, value in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = value
            cell.text_frame.paragraphs[0].font.size = Pt(16)
            cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
            if row_idx % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(250, 250, 250)

    # Observación
    obs = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(9), Inches(0.8))
    obs.text_frame.text = "Los rangos se solapan completamente"
    obs.text_frame.paragraphs[0].font.size = Pt(24)
    obs.text_frame.paragraphs[0].font.bold = True
    obs.text_frame.paragraphs[0].font.color.rgb = PRIMARY_RED
    obs.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

def add_text_slide(title, subtitle, bullets, start_y=1.3):
    """Diapositiva genérica con texto"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, title)

    y = start_y

    if subtitle:
        sub = slide.shapes.add_textbox(Inches(0.5), Inches(y), Inches(9), Inches(0.6))
        sub.text_frame.text = subtitle
        sub.text_frame.paragraphs[0].font.size = Pt(26)
        sub.text_frame.paragraphs[0].font.color.rgb = DARK_GRAY
        sub.text_frame.paragraphs[0].font.bold = True
        y += 0.8

    for bullet in bullets:
        b = slide.shapes.add_textbox(Inches(0.8), Inches(y), Inches(8.4), Inches(0.55))
        b.text_frame.word_wrap = True
        b.text_frame.text = f"• {bullet}"
        b.text_frame.paragraphs[0].font.size = Pt(24)
        y += 0.6

def add_image_slide(title, subtitle, img_path, interpretation):
    """Diapositiva con imagen"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, title)

    sub = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(9), Inches(0.5))
    sub.text_frame.text = subtitle
    sub.text_frame.paragraphs[0].font.size = Pt(24)
    sub.text_frame.paragraphs[0].font.color.rgb = DARK_GRAY

    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(1.5), Inches(1.9), height=Inches(4.5))

    interp = slide.shapes.add_textbox(Inches(0.5), Inches(6.6), Inches(9), Inches(0.7))
    interp.text_frame.word_wrap = True
    interp.text_frame.text = f"Interpretación: {interpretation}"
    interp.text_frame.paragraphs[0].font.size = Pt(20)
    interp.text_frame.paragraphs[0].font.italic = True
    interp.text_frame.paragraphs[0].font.color.rgb = DARK_GRAY

# Generar presentación
add_title_slide()
add_audio_slides()
add_enigma_slide()
add_table_slide()

add_text_slide("Entendiendo la acústica de la voz", "El tono (frecuencia fundamental, F₀)", [
    'la "altura" de la voz (grave o aguda)',
    "producido por la vibración de las cuerdas vocales",
    "en niños prepuberales: 200-350 Hz (similar en ambos géneros)",
    "para comparar: adultos varones ~120 Hz, mujeres adultas ~220 Hz"
])

# Formantes
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide, "Entendiendo la acústica de la voz (II)")
sub = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(9), Inches(0.5))
sub.text_frame.text = "Los formantes (F1, F2, F3)"
sub.text_frame.paragraphs[0].font.size = Pt(26)
sub.text_frame.paragraphs[0].font.color.rgb = DARK_GRAY
sub.text_frame.paragraphs[0].font.bold = True

y = 2
for txt in ["frecuencias de resonancia del tracto vocal",
            "determinan la calidad de las vocales (/a/, /e/, /i/, /o/, /u/)",
            "relacionados con la longitud del tracto vocal"]:
    b = slide.shapes.add_textbox(Inches(0.8), Inches(y), Inches(8.4), Inches(0.5))
    b.text_frame.text = f"• {txt}"
    b.text_frame.paragraphs[0].font.size = Pt(24)
    y += 0.6

y += 0.2
for detail in ["F1: apertura de la boca (bajo = cerrada /i/, alto = abierta /a/)",
               "F2: posición de la lengua (bajo = posterior /u/, alto = anterior /i/)",
               "F3: configuración más compleja del tracto vocal"]:
    d = slide.shapes.add_textbox(Inches(0.8), Inches(y), Inches(8.4), Inches(0.5))
    d.text_frame.word_wrap = True
    d.text_frame.text = detail
    d.text_frame.paragraphs[0].font.size = Pt(22)
    d.text_frame.paragraphs[0].font.bold = True
    d.text_frame.paragraphs[0].font.color.rgb = PRIMARY_RED
    y += 0.6

add_image_slide("Las visualizaciones acústicas", "Espacio vocálico F1-F2",
                "vowel_spaces_overlap_small.png",
                "las elipses muestran la distribución de las vocales de cada hablante. El solapamiento es evidente.")

add_image_slide("Las visualizaciones acústicas (II)", "Distribución del tono",
                "gender_comparison_statistical_small.png",
                "las barras de error muestran que los rangos de tono son muy similares entre niños y niñas.")

# Percepción
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide, "La paradoja: ¿cómo diferenciamos entonces?")
sub = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(9), Inches(0.5))
sub.text_frame.text = "Lo que sabemos de la percepción - Barreda & Assmann (2021)"
sub.text_frame.paragraphs[0].font.size = Pt(24)
sub.text_frame.paragraphs[0].font.color.rgb = DARK_GRAY
sub.text_frame.paragraphs[0].font.bold = True

quote_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.1), Inches(8.4), Inches(1.6))
quote_box.fill.solid()
quote_box.fill.fore_color.rgb = LIGHT_GRAY
quote_box.line.color.rgb = PRIMARY_RED
quote_box.line.width = Pt(2)

quote = slide.shapes.add_textbox(Inches(1.2), Inches(2.3), Inches(7.6), Inches(1.2))
tf = quote.text_frame
tf.word_wrap = True
tf.text = '"La percepción del género y la edad del hablante están entrelazadas. Los oyentes usan información sobre la edad para informar sus juicios de género"'
tf.paragraphs[0].font.size = Pt(22)
tf.paragraphs[0].font.italic = True

impl = slide.shapes.add_textbox(Inches(0.8), Inches(4.2), Inches(8.4), Inches(0.6))
impl.text_frame.text = "Implicación: el contexto y las expectativas importan."
impl.text_frame.paragraphs[0].font.size = Pt(26)
impl.text_frame.paragraphs[0].font.bold = True
impl.text_frame.paragraphs[0].font.color.rgb = PRIMARY_RED

add_text_slide("Lo que sabemos de la percepción (II)", "Funk & Simpson (2023)", [
    "Pitch como predictor principal (aunque con mucho solapamiento)",
    "Espectro de sibilantes (/s/, /z/): los niños tienden a producirlas con energía más baja",
    "Correlación con conformidad de género: los niños que expresan mayor conformidad muestran diferencias más marcadas"
], 1.2)

add_text_slide("La respuesta: no es solo la anatomía", "Factor 1: diferencias comportamentales", [
    "Desde los 2-3 años, los niños internalizan estereotipos de género",
    'Pueden modificar voluntariamente su voz para sonar más "masculinos" o "femeninos"',
    "Cartei et al. (2019): niños de 6-10 años pueden controlar la expresión de masculinidad/feminidad"
], 1.2)

add_text_slide("La respuesta: no es solo la anatomía (II)", "Factor 2: información prosódica", [
    "Patrones de entonación",
    "Ritmo del habla",
    "Variabilidad temporal y espectral",
    "Mucho más evidente en frases completas que en sílabas aisladas"
], 1.2)

add_text_slide("La respuesta: no es solo la anatomía (III)", "Factor 3: información contextual", [
    "Duración del estímulo (mejor en oraciones que en vocales aisladas)",
    "Conocimiento de la edad aproximada del hablante",
    "Expectativas culturales"
], 1.2)

add_text_slide("Conclusiones", "Las diferencias acústicas prepuberales son sutiles", [
    "No hay dimorfismo sexual anatómico significativo antes de la pubertad",
    "Los parámetros acústicos básicos (tono, formantes) se solapan completamente"
], 1.2)

add_text_slide("Conclusiones (II)", "Pero la percepción es robusta", [
    "Identificamos correctamente el género en ~70-80% de los casos",
    "La precisión mejora con más contexto (oraciones vs sílabas aisladas)"
], 1.2)

add_text_slide("Conclusiones (III)", "La voz como práctica social", [
    "Los niños aprenden y practican patrones de habla asociados a su género",
    "La voz no solo refleja anatomía, sino identidad de género",
    "Implicaciones: desarrollo del lenguaje, identidad de género, terapia de voz"
], 1.2)

# Reflexión final
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide, "Reflexión final")

q1 = slide.shapes.add_textbox(Inches(0.5), Inches(1.4), Inches(9), Inches(0.6))
q1.text_frame.text = 'La pregunta no es solo "¿cómo diferenciamos?"'
q1.text_frame.paragraphs[0].font.size = Pt(30)
q1.text_frame.paragraphs[0].font.bold = True
q1.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

q2 = slide.shapes.add_textbox(Inches(0.5), Inches(2.2), Inches(9), Inches(0.8))
q2.text_frame.word_wrap = True
q2.text_frame.text = "Es también: ¿Qué nos dice esto sobre cómo se construye el género?"
q2.text_frame.paragraphs[0].font.size = Pt(28)
q2.text_frame.paragraphs[0].font.bold = True
q2.text_frame.paragraphs[0].font.color.rgb = PRIMARY_RED
q2.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

y = 3.5
for concept in ["Es performativo: se practica y se expresa",
                "Es perceptivo: lo interpretamos con expectativas culturales",
                "Es dinámico: evoluciona con el desarrollo"]:
    c = slide.shapes.add_textbox(Inches(1), Inches(y), Inches(8), Inches(0.6))
    c.text_frame.word_wrap = True
    c.text_frame.text = f"• {concept}"
    c.text_frame.paragraphs[0].font.size = Pt(26)
    c.text_frame.paragraphs[0].font.bold = True
    y += 0.8

# Preguntas debate
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide, "Preguntas para el debate")

questions = [
    '¿Creéis que los niños son conscientes de que modifican su voz para sonar más "masculinos" o "femeninos"?',
    "Si las diferencias anatómicas son mínimas, ¿de dónde aprenden los niños estos patrones vocales?",
    "¿Qué implicaciones tiene esto para nuestra comprensión del género como constructo social vs biológico?",
    "¿Debería esto cambiar nuestra aproximación a la terapia de voz para niños transgénero?"
]

y = 1.5
for idx, q in enumerate(questions):
    qbox = slide.shapes.add_textbox(Inches(0.5), Inches(y), Inches(9), Inches(0.8))
    qbox.text_frame.word_wrap = True
    qbox.text_frame.text = f"{idx+1}. {q}"
    qbox.text_frame.paragraphs[0].font.size = Pt(22)
    y += 1.2

prs.save('presentacion.pptx')
print(f"✓ Presentación generada: presentacion.pptx ({len(prs.slides)} diapositivas)")
