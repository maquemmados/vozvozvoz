# Cómo convertir la presentación a formato visual

## Opción 1: Marp (recomendado, gratis)
Convierte Markdown a presentación HTML/PDF con diseño profesional.

```bash
# Instalar Marp CLI
npm install -g @marp-team/marp-cli

# Convertir a HTML (presentación interactiva)
marp presentacion.md -o presentacion.html

# Convertir a PDF
marp presentacion.md -o presentacion.pdf --pdf
```

## Opción 2: Reveal.js (presentación web interactiva)
Usa Pandoc para convertir a reveal.js:

```bash
# Instalar pandoc (si no lo tienes)
sudo apt-get install pandoc

# Convertir a reveal.js
pandoc presentacion.md -t revealjs -s -o presentacion.html
```

## Opción 3: PowerPoint/Google Slides (manual)
1. Abre PowerPoint o Google Slides
2. Copia cada sección del archivo `presentacion.md`
3. Pega en una diapositiva nueva
4. Añade las imágenes manualmente

## Opción 4: Visual Studio Code con extensión
1. Instala VS Code
2. Instala la extensión "Marp for VS Code"
3. Abre `presentacion.md`
4. Click en el icono de Marp (lado derecho)
5. Exporta a PDF/PPTX/HTML

## Para añadir las imágenes automáticamente:
Las rutas ya están en el archivo:
- `![Comparación de vocales](comparacion_vocales_rigurosa.png)`
- `![Comparación de pitch](comparacion_pitch_rigurosa.png)`

Estas se cargarán automáticamente si usas Marp o Reveal.js.
