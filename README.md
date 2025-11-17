# Análisis Acústico de Voces Infantiles 🎤🔬

Este proyecto analiza características acústicas de grabaciones de voces de niños y genera visualizaciones educativas atractivas.

## 📋 Descripción

El script `analyze_voices.py` realiza un análisis acústico completo y científicamente confiable de grabaciones de voz, extrayendo métricas verificables y generando visualizaciones coloridas perfectas para mostrar a niños.

## 🎯 Métricas Analizadas

Todas las métricas son **confiables y verificables**, utilizando estándares de la industria (Praat/Parselmouth):

### 1. **Frecuencia Fundamental (Pitch/F0)**
- El "tono" de la voz
- Medido en Hertz (Hz)
- Indica qué tan aguda o grave es la voz
- En niños: típicamente 200-400 Hz

### 2. **Formantes (F1, F2, F3)**
- Resonancias vocales que dan carácter único a cada voz
- F1 y F2 son cruciales para identificar vocales
- Medidos en Hz

### 3. **Intensidad**
- "Volumen" de la voz
- Medido en decibelios (dB)
- Incluye intensidad media y rango dinámico

### 4. **Características Espectrales**
- **Centroide Espectral**: "brillo" del sonido
- **Ancho de Banda Espectral**: "riqueza" del sonido
- **Rolloff Espectral**: distribución de energía
- **Zero Crossing Rate**: complejidad de la señal

### 5. **Duración**
- Tiempo total de la grabación en segundos

## 📊 Visualizaciones Generadas

### Reportes Individuales (6 archivos)
Cada grabación obtiene su propio reporte visual con:
- Forma de onda (cómo "se ve" el sonido)
- Espectrograma (mapa de frecuencias en el tiempo)
- Contorno de pitch (la "melodía" de la voz)
- Distribución de pitch
- Resumen de todas las métricas

### Comparaciones Entre Voces
1. **`comparacion_pitch.png`**: Compara el tono de voz de todos
2. **`comparacion_formantes.png`**: Espacio de formantes F1-F2
3. **`comparacion_intensidad.png`**: Compara volumen y dinámica
4. **`comparacion_espectral.png`**: Características del "color" del sonido

### Resumen Tabular
- **`tabla_resumen.png`**: Tabla visual con todas las métricas
- **`resumen_metricas.csv`**: Datos en formato CSV para análisis posterior

## 🚀 Uso

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar el Análisis

```bash
python analyze_voices.py
```

El script automáticamente:
1. Busca todos los archivos `audio_*.wav` en el directorio
2. Analiza cada uno acústicamente
3. Genera todas las visualizaciones
4. Guarda los resultados

## 📁 Estructura de Archivos

```
.
├── audio_ninia_1.wav          # Grabación niña 1
├── audio_ninia_2.wav          # Grabación niña 2
├── audio_ninia3.wav           # Grabación niña 3
├── audio_ninio_1.wav          # Grabación niño 1
├── audio_ninio_2.wav          # Grabación niño 2
├── audio_ninio_3.wav          # Grabación niño 3
├── analyze_voices.py          # Script principal
├── requirements.txt           # Dependencias
└── README.md                  # Este archivo
```

### Archivos Generados

Después de ejecutar el script:

```
.
├── reporte_audio_ninia_1.png      # Reporte individual niña 1
├── reporte_audio_ninia_2.png      # Reporte individual niña 2
├── reporte_audio_ninia3.png       # Reporte individual niña 3
├── reporte_audio_ninio_1.png      # Reporte individual niño 1
├── reporte_audio_ninio_2.png      # Reporte individual niño 2
├── reporte_audio_ninio_3.png      # Reporte individual niño 3
├── comparacion_pitch.png          # Comparación de tonos
├── comparacion_formantes.png      # Comparación de formantes
├── comparacion_intensidad.png     # Comparación de intensidad
├── comparacion_espectral.png      # Comparación espectral
├── tabla_resumen.png              # Tabla resumen visual
└── resumen_metricas.csv           # Datos en CSV
```

## 🔬 Fundamentos Científicos

Este análisis utiliza herramientas y técnicas estándar en fonética acústica:

- **Praat/Parselmouth**: Software de referencia en análisis de voz
- **Librosa**: Biblioteca estándar para análisis de audio en Python
- Algoritmos validados científicamente para extracción de pitch y formantes
- Configuraciones optimizadas para voces infantiles (rango de pitch 75-500 Hz)

## 🎨 Características Visuales

- Colores diferenciados: **Rosa para niñas**, **Azul para niños**
- Gráficos grandes y claros
- Etiquetas en español
- Diseño atractivo para presentaciones educativas

## 📖 Para Niños

Las visualizaciones son perfectas para mostrar a niños porque:

1. **Son coloridas y atractivas**
2. **Muestran su propia voz de forma visual**
3. **Permiten comparar voces entre amigos**
4. **Enseñan conceptos de física del sonido de forma intuitiva**:
   - La forma de onda muestra las vibraciones
   - El espectrograma es como un "arcoíris del sonido"
   - El pitch muestra si hablan agudo o grave
   - Los formantes muestran qué hace única su voz

## 🛠️ Tecnologías Utilizadas

- Python 3.x
- NumPy: Cálculos numéricos
- SciPy: Procesamiento de señales
- Matplotlib/Seaborn: Visualizaciones
- Librosa: Análisis de audio
- Praat-Parselmouth: Análisis fonético profesional
- Pandas: Manejo de datos

## 📚 Referencias Académicas

El proyecto incluye PDFs de investigación sobre análisis acústico de voces infantiles:
- Barreda & Assmann (2021)
- Funk & Simpson (2023) - Correlatos acústicos y perceptuales de género en voces infantiles

## ⚙️ Personalización

Para modificar el análisis:

1. **Cambiar rango de pitch**: Línea 87 de `analyze_voices.py`
   ```python
   pitch = call(self.snd, "To Pitch", 0.0, 75, 500)  # min, max en Hz
   ```

2. **Ajustar formantes**: Línea 114
   ```python
   formant = call(self.snd, "To Formant (burg)", 0.0, 5, 5500, 0.025, 50)
   ```

3. **Colores**: Líneas 25-27
   ```python
   COLORS_GIRLS = ['#FF69B4', '#FFB6C1', '#FF1493']
   COLORS_BOYS = ['#4169E1', '#87CEEB', '#1E90FF']
   ```

## 📊 Ejemplo de Resultados

Análisis típico para una grabación infantil:
- **Pitch medio**: 250-300 Hz
- **F1**: 600-750 Hz
- **F2**: 1400-1800 Hz
- **F3**: 2600-3000 Hz
- **Intensidad**: 65-75 dB

## 🤝 Contribuciones

Este script está diseñado para ser:
- Educativo
- Científicamente riguroso
- Fácil de entender y modificar
- Visualmente atractivo

## 📝 Licencia

Proyecto educativo de análisis acústico.

## 👨‍🔬 Notas Técnicas

- Todos los audios deben estar en formato WAV
- Frecuencia de muestreo: 44.1 kHz (estándar)
- Resolución: 16-bit
- Canal: Mono
- Los análisis toman aproximadamente 5-10 segundos por archivo

---

**¡Disfruta explorando las voces!** 🎉
