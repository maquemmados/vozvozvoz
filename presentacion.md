# ¿Niño o niña? La percepción del género en las voces infantiles

---

## Actividad inicial: escuchad estas voces

Vais a escuchar 6 voces diferentes. Intentad identificar: **¿es un niño o una niña?**

### Audio 1
🔊 *[Se reproduce audio_ninio_2.wav]*

### Audio 2
🔊 *[Se reproduce audio_ninia_1.wav]*

### Audio 3
🔊 *[Se reproduce audio_ninio_3.wav]*

### Audio 4
🔊 *[Se reproduce audio_ninia3.wav]*

### Audio 5
🔊 *[Se reproduce audio_ninio_1.wav]*

### Audio 6
🔊 *[Se reproduce audio_ninia_2.wav]*

**Pregunta:** ¿Habéis podido identificar el género de cada voz? ¿Qué os ha ayudado a decidir?

---

## ¿Qué sabemos sobre las voces infantiles?

### Evidencia de estudios previos

Los estudios en percepción de voz infantil muestran que:

- **Los oyentes adultos pueden identificar el género de voces infantiles** con una precisión del 70-84% (Funk & Simpson, 2023)
- **La precisión mejora con la edad** del hablante y con más contexto lingüístico
- **Incluso niños muy pequeños** (4-5 años) pueden ser identificados mejor que el azar

### Pero existe un problema anatómico

> *"Las diferencias anatómicas y fisiológicas en la laringe y el tracto vocal de niños y niñas prepuberales son prácticamente inexistentes"*
>
> — Fitch & Giedd (1999)

**Pregunta de investigación:** Si las diferencias anatómicas son mínimas, ¿qué información acústica permite esta identificación?

---

## Fundamentos acústicos de la voz: qué estamos midiendo

Antes de ver nuestros resultados, es importante entender **qué parámetros acústicos analizamos** y qué representan.

### Parámetros vocales fundamentales

#### 1. **Frecuencia fundamental (pitch, F₀)**

**¿Qué es?**
- La **frecuencia de vibración de las cuerdas vocales**
- Determina si percibimos una voz como **grave o aguda**
- Se mide en herzios (Hz): número de vibraciones por segundo

**¿Cómo se produce?**
- Las cuerdas vocales se abren y cierran rápidamente
- A mayor frecuencia de vibración → voz más aguda
- A menor frecuencia → voz más grave

**Valores de referencia:**
- Voces infantiles (prepuberales): **200-350 Hz**
- Mujeres adultas: ~220 Hz
- Hombres adultos: ~120 Hz

**¿De qué depende?**
En adultos, principalmente de:
- **Longitud** de las cuerdas vocales (más cortas → más agudo)
- **Masa** de las cuerdas vocales (más finas → más agudo)
- **Tensión** (voluntaria o no)

---

#### 2. **Formantes (F1, F2, F3...)**

**¿Qué son?**
- Son las **frecuencias de resonancia del tracto vocal**
- Determinan la **calidad** o **timbre** de cada vocal
- Son las "huellas acústicas" que diferencian /a/, /e/, /i/, /o/, /u/

**¿Cómo se producen?**
- El aire desde los pulmones vibra las cuerdas vocales (fuente)
- Este sonido viaja por la garganta, boca y nariz (filtro)
- El tracto vocal **amplifica** ciertas frecuencias y **atenúa** otras
- Las frecuencias amplificadas son los formantes

**Metáfora:** Imagina soplar en una botella vacía. El tono que escuchas depende del tamaño y forma de la botella. Los formantes funcionan de manera similar.

**Los tres primeros formantes:**

**F1 (primer formante):**
- Relacionado con la **apertura de la mandíbula**
- F1 bajo (~300 Hz): vocal cerrada como /i/ o /u/
- F1 alto (~700 Hz): vocal abierta como /a/

**F2 (segundo formante):**
- Relacionado con la **posición de la lengua** (anterior/posterior)
- F2 bajo (~1000 Hz): vocal posterior como /u/
- F2 alto (~2200 Hz): vocal anterior como /i/

**F3 (tercer formante):**
- Configuración más compleja del tracto vocal
- Importante para diferenciar ciertas consonantes y vocales

---

#### 3. **Relación entre formantes y anatomía**

**Principio fundamental:**
> Cuanto más **largo** es el tracto vocal, más **bajas** son las frecuencias de los formantes

**Fórmula aproximada:**
- Un tracto vocal de 17 cm (hombre adulto típico) produce formantes ~15% más bajos que uno de 14 cm (mujer adulta típica)
- La relación es **inversamente proporcional**: longitud × frecuencia = constante

**En niños prepuberales:**
- Tracto vocal similar en niños y niñas (Fitch & Giedd, 1999)
- **Por tanto, formantes deberían ser similares**
- Rangos típicos para F1: 400-800 Hz
- Rangos típicos para F2: 1000-2500 Hz
- Rangos típicos para F3: 2500-3500 Hz

---

#### 4. **Visualización: el espacio vocálico**

Un gráfico F1 vs F2 permite representar todas las vocales de una persona:

```
F1 (Hz)
↑ /a/
|         /e/
|                  /o/
|    /i/                    /u/
|________________________→ F2 (Hz)
```

**Interpretación:**
- Cada punto = una realización de una vocal
- La posición depende de la articulación (lengua, mandíbula)
- El tamaño del "triángulo vocálico" puede relacionarse con:
  - Precisión articulatoria
  - Claridad del habla
  - Características individuales del hablante

---

## Nuestro análisis: diseño del estudio

### Participantes
- **6 niños** de edad escolar (3 niños, 3 niñas)
- Hablantes nativos de español
- Grabaciones de **habla espontánea** describiendo imágenes

### Metodología de análisis acústico

**Procesamiento automático:**
1. **Transcripción automática** de todo el habla (texto + timing)
2. **Segmentación en palabras** con marcas temporales precisas
3. **Identificación de vocales** basada en características acústicas
4. **Extracción de parámetros** en el punto medio de cada vocal:
   - Pitch (F₀) mediante autocorrelación
   - F1, F2, F3 mediante análisis LPC (Linear Predictive Coding)

**Análisis estadístico:**
- Comparación entre niños y niñas usando **pruebas t de Student**
- Análisis por vocal individual (/a/, /e/, /i/, /o/, /u/)
- Cálculo de **tamaños del efecto (Cohen's d)** para evaluar magnitud
- Nivel de significancia: p < 0.05

---

## Resultados: comparación acústica entre géneros

### Comparación global (todas las vocales juntas)

| Parámetro | Niñas (media ± sd) | Niños (media ± sd) | p-valor | Significativo |
|-----------|--------------------|--------------------|---------|---------------|
| **Pitch (Hz)** | 288.5 ± 58.0 | 290.8 ± 45.4 | 0.79 | **No** |
| **F1 (Hz)** | 633.4 ± 181.3 | 653.4 ± 130.8 | 0.45 | **No** |
| **F2 (Hz)** | 1483.6 ± 587.5 | 1598.8 ± 426.7 | 0.18 | **No** |

**Interpretación:**
- Los valores medios son **prácticamente idénticos**
- Las desviaciones estándar son **muy grandes** (mucho solapamiento)
- Ninguna diferencia es estadísticamente significativa (p > 0.05)
- Cohen's d < 0.25 en todos los casos (efecto trivial)

### Visualización del solapamiento

![Comparación estadística entre géneros](datos_para_presentacion/gender_comparison_statistical.png)

**Lo que muestra esta figura:**
- Distribuciones de pitch y formantes para niños (azul) y niñas (rojo)
- Las distribuciones **se solapan casi completamente**
- No hay un valor de corte claro que separe ambos géneros

---

## Resultados: análisis por vocal individual

### ¿Quizás algunas vocales específicas muestran diferencias?

| Vocal | Parámetro | Niñas (Hz) | Niños (Hz) | p-valor | Significativo |
|-------|-----------|------------|------------|---------|---------------|
| **/a/** | Pitch | 279.5 | 288.7 | 0.59 | No |
|  | F1 | 735.0 | 689.8 | 0.51 | No |
|  | F2 | 1656.4 | 1594.5 | 0.78 | No |
| **/e/** | Pitch | 286.2 | 291.2 | 0.75 | No |
|  | F1 | 640.0 | 639.0 | 0.98 | No |
|  | F2 | 1488.0 | 1567.1 | 0.71 | No |
| **/i/** | Pitch | 285.8 | 265.4 | 0.30 | No |
|  | F1 | 560.4 | 605.9 | 0.58 | No |
|  | F2 | 1454.5 | 1525.5 | 0.72 | No |
| **/o/** | Pitch | 264.9 | 291.7 | 0.14 | No |
|  | F1 | 683.0 | 674.5 | 0.89 | No |
|  | F2 | 1386.3 | 1681.4 | 0.14 | No |
| **/u/** | Pitch | 282.2 | 311.3 | 0.22 | No |
|  | F1 | 536.7 | 603.4 | 0.36 | No |
|  | F2 | 1247.6 | 1528.7 | 0.26 | No |

**Conclusión:** Ni una sola comparación alcanza significancia estadística (p < 0.05)

---

## Espacios vocálicos: solapamiento completo

![Espacios vocálicos superpuestos](datos_para_presentacion/vowel_spaces_overlap.png)

**Interpretación del gráfico:**
- Cada elipse representa el espacio vocálico F1-F2 de un hablante
- **Niñas en rojo, niños en azul**
- Las elipses se superponen casi por completo
- No hay un patrón claro que separe sistemáticamente ambos géneros

**Implicación:**
> Si analizáramos una vocal aislada de un hablante desconocido, **no podríamos predecir su género** basándonos únicamente en F1 y F2

---

## La paradoja científica

### ¿Qué hemos encontrado?

#### Por un lado (evidencia perceptiva):
✓ Los adultos identifican el género de voces infantiles con 70-84% de precisión
✓ Incluso niños de 4-5 años pueden ser identificados mejor que el azar
✓ La identificación es consistente entre diferentes oyentes

#### Por otro lado (evidencia acústica):
✗ **Pitch:** no hay diferencias significativas (p = 0.79)
✗ **F1:** no hay diferencias significativas (p = 0.45)
✗ **F2:** no hay diferencias significativas (p = 0.18)
✗ **Ninguna vocal individual** muestra diferencias
✗ **Solapamiento casi total** en espacios vocálicos

#### Y además (evidencia anatómica):
✗ Las cuerdas vocales de niños y niñas son muy similares en longitud y masa
✗ La longitud del tracto vocal no difiere sistemáticamente antes de la pubertad
✗ No hay dimorfismo sexual anatómico apreciable hasta los 12-13 años

### Formulación de la paradoja

> **Si no hay diferencias anatómicas significativas, y no detectamos diferencias acústicas estadísticamente significativas en los parámetros básicos de la voz, ¿cómo es posible que podamos identificar el género con 70-80% de precisión?**

Esta paradoja sugiere que:
1. Hay información acústica **más sutil** que no capturamos con estos análisis simples
2. La información relevante puede ser **dinámica** (patrones temporales, no valores puntuales)
3. El género en la voz no es solo el resultado de **diferencias anatómicas**, sino también de **diferencias conductuales**

---

## Resolviendo la paradoja: tres niveles de explicación

### 1. Información acústica más sutil

**Más allá de medias puntuales:**
- Nuestro análisis mide **valores medios** en el punto medio de vocales
- Pero hay mucha más información acústica:
  - **Variabilidad espectral:** cómo varían los formantes dentro de cada vocal
  - **Transiciones formánticas:** cómo se mueven los formantes entre sonidos
  - **Espectro de consonantes:** especialmente fricativas como /s/ y /z/
  - **Características de la fuente:** medidas espectrales más finas (H1-H2, HNR, etc.)

**Evidencia de Funk & Simpson (2023):**
- El **espectro de sibilantes** (/s/, /z/) correlaciona con la conformidad de género percibida
- Los niños tienden a producir /s/ con **centro de gravedad más bajo** (energía en frecuencias más bajas)
- Esta diferencia **no se explica por anatomía**, sino por articulación aprendida

---

### 2. Información prosódica y dinámica

**La importancia del contexto:**

**Observación clave de Barreda & Assmann (2021):**
> "La percepción del género de un hablante mejora sustancialmente cuando se presentan oraciones completas en lugar de sílabas o vocales aisladas"

**¿Qué añaden las oraciones?**

**A. Patrones de entonación:**
- Melodía del habla (curvas de F₀)
- Rango de variación del pitch
- Uso de énfasis prosódico

**B. Características temporales:**
- **Velocidad del habla** (sílabas por segundo)
- **Duración de segmentos** (vocales, consonantes, pausas)
- **Ritmo:** algunos estudios encuentran que las niñas pueden producir habla con menos variabilidad temporal

**C. Variabilidad articulatoria:**
- Precisión articulatoria (¿qué tan "claras" son las vocales?)
- Coarticulación (¿cuánto influye un sonido en el siguiente?)
- Reducción vocálica en sílabas átonas

**Estos patrones son:**
- Difíciles de capturar con análisis de vocales aisladas
- Requieren tramos largos de habla
- Se aprenden durante el desarrollo del lenguaje

---

### 3. Aprendizaje y performance de género

**La voz como conducta social**

**Evidencia de Cartei et al. (2019):**
- Niños de 6-10 años pueden **modificar voluntariamente** su voz para sonar más "masculinos" o "femeninos"
- Cuando se les pide imitar niños del sexo opuesto:
  - Modifican su pitch
  - Modifican el espaciado de formantes
  - Modifican características prosódicas
- Esto demuestra **control consciente** sobre marcadores de género en la voz

**Conformidad de género y acústica (Funk & Simpson, 2023):**
- Midieron la **conformidad de género autorreportada** en niños (preferencias de juguetes, colores, comportamientos estereotipados)
- Encontraron **correlación significativa** entre conformidad de género y características acústicas de las voces
- Especialmente en el **espectro de sibilantes** para niños varones

**Interpretación:**
- Los niños no solo tienen diferencias anatómicas (que son mínimas)
- También **practican y aprenden** patrones de habla asociados a su género
- Estos patrones se internalizan desde edades muy tempranas (2-3 años)

**Mecanismo:**
1. Los niños son expuestos a modelos de habla "masculina" y "femenina" (padres, televisión, etc.)
2. Internalizan estereotipos de género alrededor de los 2-3 años
3. Comienzan a **imitar** y **practicar** patrones vocales asociados a su identidad de género
4. Estos patrones se refuerzan socialmente (feedback de adultos y compañeros)
5. Se automatizan y se convierten en parte del "habla natural" del niño

---

## Integración: edad, género y voz

### La percepción de género no ocurre en el vacío

**Hallazgo clave de Barreda & Assmann (2021):**
> "La edad y el género del hablante se estiman **conjuntamente** en el proceso de percepción del habla"

**¿Qué significa esto?**

Imagina que escuchas una voz con:
- Pitch: 290 Hz
- F1 medio: 650 Hz
- F2 medio: 1600 Hz

**Si esta voz proviene de un niño de 7 años:**
- Estos valores son **típicos** para esa edad
- No proporcionan mucha información sobre género
- La identificación será cercana al azar

**Si esta voz proviene de un adolescente de 15 años:**
- 290 Hz es **muy alto** para un chico post-puberal (esperado ~150 Hz)
- 290 Hz es **normal** para una chica de esa edad
- La probabilidad de que sea una chica es **mucho mayor**

**Consecuencia:**
Los oyentes no solo analizan los parámetros acústicos, sino que los **interpretan en contexto**, considerando:
1. La edad aparente del hablante
2. El desarrollo vocal esperado para esa edad
3. Las distribuciones poblacionales de pitch/formantes por edad y género

---

## Síntesis: ¿por qué podemos identificar el género?

La identificación del género en voces infantiles es posible gracias a una combinación de factores:

### 1. Información acústica sutil (no capturada en nuestro análisis básico)
- Espectro de consonantes fricativas
- Variabilidad espectral y temporal
- Características finas de la fuente glotal

### 2. Información prosódica y dinámica
- Patrones de entonación
- Ritmo y timing del habla
- Transiciones formánticas

### 3. Aprendizaje de patrones de género
- Los niños internalizan y practican "formas de hablar" asociadas a su género
- Estos patrones son adquiridos y reforzados socialmente
- No son consecuencia directa de la anatomía

### 4. Integración de edad y género
- Los oyentes interpretan las características acústicas en función de la edad percibida
- La ambigüedad acústica se reduce considerando el desarrollo esperado

**Conclusión:**
> La voz infantil transmite información de género no solo a través de la anatomía, sino fundamentalmente a través de **patrones articulatorios y prosódicos aprendidos y practicados** que se desarrollan en el contexto de la socialización de género.

---

## Implicaciones y reflexión

### Implicaciones científicas

**1. Metodológicas:**
- Los análisis basados únicamente en medias de formantes y pitch son **insuficientes** para caracterizar las voces
- Necesitamos métodos que capturen **información dinámica y prosódica**
- Importancia del análisis de **habla conectada** vs vocales aisladas

**2. Teóricas:**
- El género en la voz no es simplemente un reflejo de diferencias anatómicas
- La voz es un **comportamiento social** que se aprende y se practica
- La construcción del género comienza mucho antes de los cambios puberales

### Implicaciones aplicadas

**1. Desarrollo del lenguaje:**
- Los niños adquieren no solo fonemas, sino también **estilos de habla** asociados al género
- Este proceso comienza desde edades muy tempranas (2-3 años)

**2. Identidad de género:**
- Los niños con identidades de género diversas pueden experimentar **incongruencia** entre su voz "natural" y la voz con la que se identifican
- Esto ocurre incluso antes de la pubertad

**3. Terapia de voz pediátrica:**
- Los niños transgénero pueden beneficiarse de intervención vocal **antes de la pubertad**
- El objetivo no es solo modificar pitch, sino **patrones prosódicos y articulatorios**
- La evidencia de Cartei et al. (2019) muestra que los niños tienen control voluntario sobre estos aspectos

---

## Reflexión final: la voz como performance

### Más allá de la biología

Hemos visto que:
- Las diferencias anatómicas prepuberales son **mínimas**
- Las diferencias acústicas básicas (pitch, formantes) son **no significativas**
- Pero la identificación de género es **robusta (70-80%)**

Esto nos lleva a una conclusión importante:

> **La voz no es simplemente el producto de nuestra anatomía, sino una práctica social que construimos activamente**

### La voz como práctica performativa

**El concepto de performance:**
- El género no es algo que **somos**, sino algo que **hacemos**
- La voz es uno de los medios principales a través de los cuales "hacemos género"
- Este "hacer género" con la voz comienza en la infancia temprana

**La voz como espacio de identidad:**
- A través de la voz, los niños **expresan** su identidad de género
- La voz es un espacio donde **practicamos** quiénes somos
- No esperamos pasivamente a que la pubertad "nos dé" una voz masculina o femenina
- Activamente **construimos** nuestra voz de género desde la infancia

### Consecuencias de esta visión

**1. Para la ciencia de la voz:**
- No podemos estudiar la voz solo como fenómeno biológico-acústico
- Debemos incorporar perspectivas sociales y conductuales
- La variabilidad vocal refleja tanto anatomía como identidad y práctica social

**2. Para la comprensión del género:**
- El género tiene componentes **biológicos** (anatomía post-puberal)
- Pero también tiene componentes **performativos** que preceden y trascienden la biología
- La voz es evidencia clara de este aspecto performativo del género

**3. Para las personas:**
- Nuestra voz es **maleable** y está bajo nuestro control (en cierta medida)
- Podemos modificar nuestra voz para alinearla con nuestra identidad
- La voz es un **derecho expresivo**: tenemos derecho a que nuestra voz refleje quiénes somos

### Pregunta final

> Si podéis identificar el género de voces infantiles a pesar de la ausencia de diferencias anatómicas significativas, ¿qué os dice esto sobre la **naturaleza del género en sí mismo**?

La voz nos enseña que el género es simultáneamente:
- **Corporal:** involucra nuestro cuerpo físico
- **Acústico:** se materializa en ondas sonoras
- **Perceptivo:** existe en cómo somos escuchados
- **Social:** se construye en relación con normas culturales
- **Identitario:** expresa quiénes somos
- **Performativo:** se practica y se hace en actos cotidianos

**La voz infantil revela que mucho antes de que la pubertad "escriba" el género en nuestros cuerpos, ya lo estamos "hablando" al mundo.**

---

## Preguntas para el debate

1. **Sobre aprendizaje:** ¿Creéis que los niños son **conscientes** de que modifican su voz para sonar más "masculinos" o "femeninos"? ¿O es un proceso automático?

2. **Sobre la sociedad:** Si los patrones vocales de género son **aprendidos**, ¿de dónde los aprenden los niños? ¿Qué papel juegan los padres, los medios, los compañeros?

3. **Sobre la identidad:** ¿Qué implicaciones tiene este descubrimiento para nuestra comprensión del género como categoría? ¿Es más "biológico" o más "social"?

4. **Sobre la intervención:** ¿Deberíamos ofrecer terapia de voz a niños transgénero **antes** de la pubertad? ¿Cuáles serían los beneficios y riesgos?

5. **Sobre la metodología:** ¿Qué otros aspectos de la voz podríamos medir para capturar mejor las diferencias entre voces masculinas y femeninas en niños?

---

## Referencias principales

**Barreda, S., & Assmann, P. F. (2021).** Perception of gender in children's voices. *Journal of the Acoustical Society of America*, 150(5), 3949-3963.
- Demuestra la estimación conjunta de edad y género
- Muestra el uso de información contextual dependiente de la edad

**Cartei, V., Garnham, A., Oakhill, J., Banerjee, R., Roberts, L., & Reby, D. (2019).** Children can control the expression of masculinity and femininity through the voice. *Royal Society Open Science*, 6(7), 190656.
- Primera evidencia de control voluntario en niños de 6-10 años
- Demuestra la naturaleza performativa del género en la voz

**Fitch, W. T., & Giedd, J. (1999).** Morphology and development of the human vocal tract: A study using magnetic resonance imaging. *Journal of the Acoustical Society of America*, 106(3), 1511-1522.
- Estudio anatómico definitivo sobre desarrollo del tracto vocal
- Demuestra ausencia de dimorfismo sexual prepuberal

**Funk, R., & Simpson, A. P. (2023).** The acoustic and perceptual correlates of gender in children's voices. *Journal of Speech, Language, and Hearing Research*, 66, 3346-3363.
- Análisis comprehensivo de 62 niños de primer grado
- Identifica pitch como predictor principal, pero no único
- Correlación entre conformidad de género y características acústicas (especialmente sibilantes)

---

## Metodología de nuestro análisis

### Datos
- 6 niños (3 niños, 3 niñas) de edad escolar
- Grabaciones de habla espontánea (descripciones de imágenes)
- Total de vocales analizadas: cientos de tokens por hablante

### Procesamiento
1. **Transcripción automática** (Whisper)
2. **Segmentación temporal** automática en palabras
3. **Extracción de parámetros acústicos:**
   - Pitch (F₀): autocorrelación (Praat)
   - Formantes (F1, F2, F3): análisis LPC
   - Punto de medición: centro temporal de cada vocal

### Análisis estadístico
- **Pruebas t de Student** para comparaciones entre géneros
- **Tamaño del efecto (Cohen's d)** para evaluar magnitud
- **Análisis global** (todas las vocales) y **por vocal** (/a/, /e/, /i/, /o/, /u/)
- Nivel de significancia: α = 0.05

### Limitaciones reconocidas
- Muestra pequeña (n=6)
- Solo habla espontánea (no controlada fonéticamente)
- No analiza aspectos prosódicos en detalle
- No incluye medidas de consonantes (especialmente fricativas)

---

## Agradecimientos

- **Participantes:** Los niños y niñas que generosamente nos permitieron grabar sus voces
- **Referencias:** Los investigadores cuyos estudios forman la base de nuestra comprensión

---

## ¿Preguntas?

### Materiales disponibles

Todos los datos, código y visualizaciones están disponibles en:
📁 `datos_para_presentacion/`

**Archivos de datos:**
- `gender_comparison_stats.json` - Comparaciones estadísticas globales
- `gender_by_vowel_stats.json` - Análisis por vocal individual
- Archivos de transcripción para cada hablante

**Visualizaciones:**
- `gender_comparison_statistical.png`
- `vowel_spaces_overlap.png`

**Código:**
- `analyze_with_transcription.py` - Script completo de análisis
