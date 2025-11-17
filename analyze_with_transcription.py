#!/usr/bin/env python3
"""
Análisis Acústico Basado en Transcripción Automática
====================================================
Usa Whisper para transcribir el audio y obtener palabras reales con timestamps.
Luego segmenta y analiza basándose en las palabras transcritas (no en silencios).

Análisis comparativo riguroso entre niños y niñas:
- Pruebas estadísticas de diferencias
- Relacionado con literatura sobre percepción de género
"""

import numpy as np
import librosa
import matplotlib.pyplot as plt
import seaborn as sns
import parselmouth
from parselmouth.praat import call
import pandas as pd
from pathlib import Path
from scipy import stats
import warnings
import whisper
import json

warnings.filterwarnings('ignore')

# Configuración visual
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
COLORS_GIRLS = ['#FF1493', '#FF69B4', '#FFB6C1']
COLORS_BOYS = ['#1E90FF', '#4169E1', '#87CEEB']


class WhisperTranscriber:
    """Transcribe audio usando Whisper y extrae palabras con timestamps."""

    def __init__(self, model_name="base"):
        """
        Args:
            model_name: Modelo Whisper (tiny, base, small, medium, large)
        """
        print(f"Cargando modelo Whisper '{model_name}'...")
        self.model = whisper.load_model(model_name)
        print("✓ Modelo cargado")

    def transcribe(self, audio_path):
        """
        Transcribe audio y extrae palabras con timestamps.

        Args:
            audio_path: Ruta al archivo de audio

        Returns:
            dict con transcripción completa y lista de palabras con timestamps
        """
        print(f"\nTranscribiendo: {Path(audio_path).name}")

        # Transcribir con timestamps a nivel de palabra
        result = self.model.transcribe(
            str(audio_path),
            language="es",  # Español
            word_timestamps=True,
            verbose=False
        )

        # Extraer palabras con timestamps
        words = []
        for segment in result['segments']:
            if 'words' in segment:
                for word_info in segment['words']:
                    words.append({
                        'word': word_info['word'].strip(),
                        'start': word_info['start'],
                        'end': word_info['end'],
                        'duration': word_info['end'] - word_info['start']
                    })

        transcription = {
            'text': result['text'].strip(),
            'language': result['language'],
            'words': words,
            'num_words': len(words)
        }

        print(f"  Transcripción: '{transcription['text']}'")
        print(f"  Palabras detectadas: {len(words)}")

        return transcription


class WordBasedVoiceAnalyzer:
    """Analiza características acústicas basándose en palabras transcritas."""

    def __init__(self, audio_path, transcription):
        """
        Args:
            audio_path: Ruta al archivo de audio
            transcription: Resultado de WhisperTranscriber
        """
        self.audio_path = Path(audio_path)
        self.name = self.audio_path.stem
        self.transcription = transcription

        # Cargar audio
        self.y, self.sr = librosa.load(audio_path, sr=None)
        self.duration = len(self.y) / self.sr

        # Objeto Parselmouth
        self.snd = parselmouth.Sound(str(audio_path))

        # Resultados
        self.words_analysis = []
        self.vowels_analysis = []
        self.results = {
            'name': self.name,
            'duration': self.duration,
            'transcription': transcription['text'],
            'num_words': len(transcription['words'])
        }

    def analyze_word(self, word_info):
        """
        Analiza una palabra individual.

        Args:
            word_info: dict con 'word', 'start', 'end'

        Returns:
            dict con análisis de la palabra
        """
        start_time = word_info['start']
        end_time = word_info['end']
        duration = end_time - start_time

        # Extraer audio de la palabra
        start_sample = int(start_time * self.sr)
        end_sample = int(end_time * self.sr)
        word_audio = self.y[start_sample:end_sample]

        # Crear objeto Sound para esta palabra
        try:
            word_snd = parselmouth.Sound(word_audio, sampling_frequency=self.sr)
        except:
            return None

        # Analizar pitch en la palabra
        try:
            pitch = call(word_snd, "To Pitch", 0.0, 150, 500)
            pitch_values = []
            for i in range(pitch.n_frames):
                f0 = call(pitch, "Get value in frame", i+1, "Hertz")
                if f0 and not np.isnan(f0) and f0 > 0:
                    pitch_values.append(f0)

            pitch_mean = np.mean(pitch_values) if pitch_values else 0
        except:
            pitch_mean = 0
            pitch_values = []

        # Detectar vocales dentro de la palabra
        vowels = self._detect_vowels_in_word(word_snd, start_time)

        analysis = {
            'word': word_info['word'],
            'start': start_time,
            'end': end_time,
            'duration': duration,
            'audio': word_audio,
            'pitch_mean': pitch_mean,
            'pitch_values': pitch_values,
            'num_vowels': len(vowels),
            'vowels': vowels
        }

        return analysis

    def _detect_vowels_in_word(self, word_snd, word_start_time):
        """Detecta vocales dentro de una palabra."""
        vowels = []

        try:
            duration = call(word_snd, "Get total duration")
            if duration < 0.05:  # Muy corto
                return vowels

            # Extraer pitch e intensidad
            pitch = call(word_snd, "To Pitch", 0.0, 150, 500)
            intensity = call(word_snd, "To Intensity", 75, 0.0, "yes")

            # Muestrear cada 10ms
            time_step = 0.01
            t = 0
            pitch_vals = []
            intensity_vals = []
            times = []

            while t < duration:
                f0 = call(pitch, "Get value at time", t, "Hertz", "Linear")
                intens = call(intensity, "Get value at time", t, "Cubic")

                pitch_vals.append(f0 if f0 and not np.isnan(f0) else 0)
                intensity_vals.append(intens if intens and not np.isnan(intens) else 0)
                times.append(t)
                t += time_step

            pitch_vals = np.array(pitch_vals)
            intensity_vals = np.array(intensity_vals)
            times = np.array(times)

            # Detectar segmentos sonoros
            is_voiced = (pitch_vals > 0) & (intensity_vals > np.percentile(intensity_vals[intensity_vals > 0], 20))

            # Encontrar intervalos vocálicos
            in_vowel = False
            start_idx = 0

            for i, voiced in enumerate(is_voiced):
                if voiced and not in_vowel:
                    start_idx = i
                    in_vowel = True
                elif not voiced and in_vowel:
                    if (times[i] - times[start_idx]) >= 0.04:  # Mínimo 40ms
                        vowel = self._extract_vowel_features(
                            word_snd,
                            times[start_idx],
                            times[i],
                            word_start_time
                        )
                        if vowel:
                            vowels.append(vowel)
                    in_vowel = False

            if in_vowel and (times[-1] - times[start_idx]) >= 0.04:
                vowel = self._extract_vowel_features(
                    word_snd,
                    times[start_idx],
                    times[-1],
                    word_start_time
                )
                if vowel:
                    vowels.append(vowel)

        except Exception as e:
            pass

        return vowels

    def _extract_vowel_features(self, word_snd, start, end, word_start_time):
        """Extrae características de una vocal."""
        mid_time = (start + end) / 2
        duration = end - start

        try:
            # Formantes en el punto medio
            formant = call(word_snd, "To Formant (burg)", 0.0, 5, 5500, 0.025, 50)
            f1 = call(formant, "Get value at time", 1, mid_time, "Hertz", "Linear")
            f2 = call(formant, "Get value at time", 2, mid_time, "Hertz", "Linear")
            f3 = call(formant, "Get value at time", 3, mid_time, "Hertz", "Linear")

            # Validar
            if f1 and f2 and f3 and not np.isnan(f1) and not np.isnan(f2) and not np.isnan(f3):
                if f1 > 0 and f2 > f1 and f3 > f2 and f1 < 1500 and f2 < 3500:
                    # Pitch
                    pitch = call(word_snd, "To Pitch", 0.0, 150, 500)
                    f0 = call(pitch, "Get value at time", mid_time, "Hertz", "Linear")

                    return {
                        'start': start,
                        'end': end,
                        'mid_time': mid_time,
                        'global_time': word_start_time + mid_time,
                        'duration': duration,
                        'f1': f1,
                        'f2': f2,
                        'f3': f3,
                        'pitch': f0 if f0 and not np.isnan(f0) else 0
                    }
        except:
            pass

        return None

    def analyze_all(self):
        """Analiza todas las palabras transcritas."""
        print(f"\nAnalizando palabras de: {self.name}")

        for word_info in self.transcription['words']:
            analysis = self.analyze_word(word_info)
            if analysis:
                self.words_analysis.append(analysis)

                # Agregar vocales a la lista global
                for vowel in analysis['vowels']:
                    vowel['word'] = analysis['word']
                    self.vowels_analysis.append(vowel)

        # Calcular estadísticas
        if self.vowels_analysis:
            pitch_values = [v['pitch'] for v in self.vowels_analysis if v['pitch'] > 0]
            f1_values = [v['f1'] for v in self.vowels_analysis]
            f2_values = [v['f2'] for v in self.vowels_analysis]
            f3_values = [v['f3'] for v in self.vowels_analysis]

            if pitch_values:
                self.results['pitch_mean'] = np.mean(pitch_values)
                self.results['pitch_std'] = np.std(pitch_values)
                self.results['pitch_median'] = np.median(pitch_values)

            if f1_values:
                self.results['f1_mean'] = np.mean(f1_values)
                self.results['f1_std'] = np.std(f1_values)
            if f2_values:
                self.results['f2_mean'] = np.mean(f2_values)
                self.results['f2_std'] = np.std(f2_values)
            if f3_values:
                self.results['f3_mean'] = np.mean(f3_values)
                self.results['f3_std'] = np.std(f3_values)

        self.results['num_vowels'] = len(self.vowels_analysis)
        self.results['words_analyzed'] = len(self.words_analysis)

        print(f"  ✓ Palabras analizadas: {len(self.words_analysis)}")
        print(f"  ✓ Vocales detectadas: {len(self.vowels_analysis)}")
        if self.results.get('pitch_mean'):
            print(f"  ✓ Pitch medio: {self.results['pitch_mean']:.1f} ± {self.results['pitch_std']:.1f} Hz")
        if self.results.get('f1_mean'):
            print(f"  ✓ F1: {self.results['f1_mean']:.0f} ± {self.results['f1_std']:.0f} Hz")
            print(f"  ✓ F2: {self.results['f2_mean']:.0f} ± {self.results['f2_std']:.0f} Hz")

        return self.results


def compare_genders(analyzers):
    """
    Análisis estadístico comparando niños vs niñas.

    Prueba la hipótesis de los papers: diferencias acústicas pequeñas
    pero diferencias perceptuales grandes.
    """
    print("\n" + "="*70)
    print("ANÁLISIS COMPARATIVO: NIÑOS vs NIÑAS")
    print("="*70)

    # Separar por género
    girls = [a for a in analyzers if 'ninia' in a.name.lower()]
    boys = [a for a in analyzers if 'ninio' in a.name.lower()]

    print(f"\nNiñas: {len(girls)} grabaciones")
    print(f"Niños: {len(boys)} grabaciones")

    # Recolectar todas las vocales
    girls_vowels = []
    boys_vowels = []

    for a in girls:
        girls_vowels.extend(a.vowels_analysis)

    for a in boys:
        boys_vowels.extend(a.vowels_analysis)

    print(f"\nVocales totales:")
    print(f"  Niñas: {len(girls_vowels)} vocales")
    print(f"  Niños: {len(boys_vowels)} vocales")

    # Extraer métricas
    girls_pitch = [v['pitch'] for v in girls_vowels if v['pitch'] > 0]
    boys_pitch = [v['pitch'] for v in boys_vowels if v['pitch'] > 0]

    girls_f1 = [v['f1'] for v in girls_vowels]
    boys_f1 = [v['f1'] for v in boys_vowels]

    girls_f2 = [v['f2'] for v in girls_vowels]
    boys_f2 = [v['f2'] for v in boys_vowels]

    # Pruebas estadísticas
    results = {}

    print("\n" + "-"*70)
    print("PRUEBAS ESTADÍSTICAS (t-test de Student)")
    print("-"*70)

    # Pitch
    if girls_pitch and boys_pitch:
        t_stat, p_value = stats.ttest_ind(girls_pitch, boys_pitch)
        cohen_d = (np.mean(girls_pitch) - np.mean(boys_pitch)) / np.sqrt((np.std(girls_pitch)**2 + np.std(boys_pitch)**2) / 2)

        results['pitch'] = {
            'girls_mean': np.mean(girls_pitch),
            'girls_std': np.std(girls_pitch),
            'boys_mean': np.mean(boys_pitch),
            'boys_std': np.std(boys_pitch),
            't_statistic': t_stat,
            'p_value': p_value,
            'cohen_d': cohen_d,
            'significant': p_value < 0.05
        }

        print(f"\nPITCH:")
        print(f"  Niñas: {np.mean(girls_pitch):.1f} ± {np.std(girls_pitch):.1f} Hz (n={len(girls_pitch)})")
        print(f"  Niños: {np.mean(boys_pitch):.1f} ± {np.std(boys_pitch):.1f} Hz (n={len(boys_pitch)})")
        print(f"  Diferencia: {abs(np.mean(girls_pitch) - np.mean(boys_pitch)):.1f} Hz")
        print(f"  t = {t_stat:.3f}, p = {p_value:.4f}")
        print(f"  Cohen's d = {cohen_d:.3f} (tamaño del efecto)")
        print(f"  ¿Significativo? {'SÍ' if p_value < 0.05 else 'NO'} (α=0.05)")

    # F1
    if girls_f1 and boys_f1:
        t_stat, p_value = stats.ttest_ind(girls_f1, boys_f1)
        cohen_d = (np.mean(girls_f1) - np.mean(boys_f1)) / np.sqrt((np.std(girls_f1)**2 + np.std(boys_f1)**2) / 2)

        results['f1'] = {
            'girls_mean': np.mean(girls_f1),
            'girls_std': np.std(girls_f1),
            'boys_mean': np.mean(boys_f1),
            'boys_std': np.std(boys_f1),
            't_statistic': t_stat,
            'p_value': p_value,
            'cohen_d': cohen_d,
            'significant': p_value < 0.05
        }

        print(f"\nF1 (Primera Formante):")
        print(f"  Niñas: {np.mean(girls_f1):.0f} ± {np.std(girls_f1):.0f} Hz (n={len(girls_f1)})")
        print(f"  Niños: {np.mean(boys_f1):.0f} ± {np.std(boys_f1):.0f} Hz (n={len(boys_f1)})")
        print(f"  Diferencia: {abs(np.mean(girls_f1) - np.mean(boys_f1)):.0f} Hz")
        print(f"  t = {t_stat:.3f}, p = {p_value:.4f}")
        print(f"  Cohen's d = {cohen_d:.3f}")
        print(f"  ¿Significativo? {'SÍ' if p_value < 0.05 else 'NO'}")

    # F2
    if girls_f2 and boys_f2:
        t_stat, p_value = stats.ttest_ind(girls_f2, boys_f2)
        cohen_d = (np.mean(girls_f2) - np.mean(boys_f2)) / np.sqrt((np.std(girls_f2)**2 + np.std(boys_f2)**2) / 2)

        results['f2'] = {
            'girls_mean': np.mean(girls_f2),
            'girls_std': np.std(girls_f2),
            'boys_mean': np.mean(boys_f2),
            'boys_std': np.std(boys_f2),
            't_statistic': t_stat,
            'p_value': p_value,
            'cohen_d': cohen_d,
            'significant': p_value < 0.05
        }

        print(f"\nF2 (Segunda Formante):")
        print(f"  Niñas: {np.mean(girls_f2):.0f} ± {np.std(girls_f2):.0f} Hz (n={len(girls_f2)})")
        print(f"  Niños: {np.mean(boys_f2):.0f} ± {np.std(boys_f2):.0f} Hz (n={len(boys_f2)})")
        print(f"  Diferencia: {abs(np.mean(girls_f2) - np.mean(boys_f2)):.0f} Hz")
        print(f"  t = {t_stat:.3f}, p = {p_value:.4f}")
        print(f"  Cohen's d = {cohen_d:.3f}")
        print(f"  ¿Significativo? {'SÍ' if p_value < 0.05 else 'NO'}")

    print("\n" + "-"*70)
    print("INTERPRETACIÓN (según Funk & Simpson 2023):")
    print("-"*70)
    print("""
    Los papers sobre percepción de género en voces infantiles muestran que:

    1. Las diferencias ACÚSTICAS son PEQUEÑAS o INEXISTENTES
       - Pitch: solapamiento considerable entre niños y niñas
       - Formantes: diferencias mínimas antes de la pubertad

    2. Las diferencias PERCEPTUALES son GRANDES
       - Los oyentes pueden identificar género con >70% de precisión
       - Incluso cuando las medidas acústicas son similares

    3. HIPÓTESIS:
       - La percepción se basa en sutiles diferencias espectrales
       - O en pistas socio-fonéticas aprendidas
       - No solo en pitch y formantes básicos
    """)

    if results.get('pitch'):
        if not results['pitch']['significant']:
            print("    ✓ Nuestros datos CONFIRMAN: no hay diferencia significativa en pitch")
        else:
            print(f"    ⚠ Nuestros datos muestran diferencia en pitch (p={results['pitch']['p_value']:.4f})")

    if results.get('f1') and results.get('f2'):
        sig_count = sum([results['f1']['significant'], results['f2']['significant']])
        if sig_count == 0:
            print("    ✓ Nuestros datos CONFIRMAN: formantes similares entre géneros")
        else:
            print(f"    ⚠ Encontramos {sig_count}/2 formantes con diferencias significativas")

    return results, girls_vowels, boys_vowels


def create_comparison_visualizations(analyzers, stats_results, girls_vowels, boys_vowels):
    """Crea visualizaciones comparativas entre géneros."""

    print("\n" + "="*70)
    print("GENERANDO VISUALIZACIONES COMPARATIVAS")
    print("="*70)

    # 1. Comparación de distribuciones de pitch
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    girls_pitch = [v['pitch'] for v in girls_vowels if v['pitch'] > 0]
    boys_pitch = [v['pitch'] for v in boys_vowels if v['pitch'] > 0]

    # Histogramas
    axes[0, 0].hist(girls_pitch, bins=30, alpha=0.6, color='#FF1493', label='Niñas', density=True)
    axes[0, 0].hist(boys_pitch, bins=30, alpha=0.6, color='#1E90FF', label='Niños', density=True)
    axes[0, 0].axvline(np.mean(girls_pitch), color='#FF1493', linestyle='--', linewidth=2)
    axes[0, 0].axvline(np.mean(boys_pitch), color='#1E90FF', linestyle='--', linewidth=2)
    axes[0, 0].set_xlabel('Pitch (Hz)', fontweight='bold')
    axes[0, 0].set_ylabel('Densidad', fontweight='bold')
    axes[0, 0].set_title('Distribución de Pitch por Género', fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Box plots
    data_pitch = [girls_pitch, boys_pitch]
    bp = axes[0, 1].boxplot(data_pitch, labels=['Niñas', 'Niños'], patch_artist=True)
    bp['boxes'][0].set_facecolor('#FF1493')
    bp['boxes'][1].set_facecolor('#1E90FF')
    axes[0, 1].set_ylabel('Pitch (Hz)', fontweight='bold')
    axes[0, 1].set_title('Comparación de Pitch', fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3, axis='y')

    # Añadir significancia
    if stats_results.get('pitch'):
        p_val = stats_results['pitch']['p_value']
        sig_text = f"p = {p_val:.4f}\n{'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'n.s.'}"
        axes[0, 1].text(1.5, max(max(girls_pitch), max(boys_pitch)) * 0.95, sig_text,
                       ha='center', fontsize=11, fontweight='bold')

    # Formantes
    girls_f1 = [v['f1'] for v in girls_vowels]
    boys_f1 = [v['f1'] for v in boys_vowels]
    girls_f2 = [v['f2'] for v in girls_vowels]
    boys_f2 = [v['f2'] for v in boys_vowels]

    # F1 comparison
    data_f1 = [girls_f1, boys_f1]
    bp = axes[1, 0].boxplot(data_f1, labels=['Niñas', 'Niños'], patch_artist=True)
    bp['boxes'][0].set_facecolor('#FF1493')
    bp['boxes'][1].set_facecolor('#1E90FF')
    axes[1, 0].set_ylabel('F1 (Hz)', fontweight='bold')
    axes[1, 0].set_title('Comparación de F1 (Primera Formante)', fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3, axis='y')

    if stats_results.get('f1'):
        p_val = stats_results['f1']['p_value']
        sig_text = f"p = {p_val:.4f}\n{'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'n.s.'}"
        axes[1, 0].text(1.5, max(max(girls_f1), max(boys_f1)) * 0.95, sig_text,
                       ha='center', fontsize=11, fontweight='bold')

    # F2 comparison
    data_f2 = [girls_f2, boys_f2]
    bp = axes[1, 1].boxplot(data_f2, labels=['Niñas', 'Niños'], patch_artist=True)
    bp['boxes'][0].set_facecolor('#FF1493')
    bp['boxes'][1].set_facecolor('#1E90FF')
    axes[1, 1].set_ylabel('F2 (Hz)', fontweight='bold')
    axes[1, 1].set_title('Comparación de F2 (Segunda Formante)', fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3, axis='y')

    if stats_results.get('f2'):
        p_val = stats_results['f2']['p_value']
        sig_text = f"p = {p_val:.4f}\n{'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'n.s.'}"
        axes[1, 1].text(1.5, max(max(girls_f2), max(boys_f2)) * 0.95, sig_text,
                       ha='center', fontsize=11, fontweight='bold')

    plt.suptitle('Análisis Comparativo: Niños vs Niñas\n' +
                 '(Pruebas estadísticas: t-test, * p<0.05, ** p<0.01, *** p<0.001, n.s. = no significativo)',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('gender_comparison_statistical.png', dpi=150, bbox_inches='tight')
    print("  ✓ gender_comparison_statistical.png")
    plt.close()

    # 2. Espacios vocálicos superpuestos
    fig, ax = plt.subplots(figsize=(12, 10))

    ax.scatter(girls_f2, girls_f1, s=80, alpha=0.5, color='#FF1493', label=f'Niñas (n={len(girls_f1)})')
    ax.scatter(boys_f2, boys_f1, s=80, alpha=0.5, color='#1E90FF', label=f'Niños (n={len(boys_f1)})')

    # Medias
    ax.scatter([np.mean(girls_f2)], [np.mean(girls_f1)], s=400, color='#FF1493',
              marker='X', edgecolors='black', linewidth=3, label='Media niñas', zorder=10)
    ax.scatter([np.mean(boys_f2)], [np.mean(boys_f1)], s=400, color='#1E90FF',
              marker='X', edgecolors='black', linewidth=3, label='Media niños', zorder=10)

    ax.invert_xaxis()
    ax.invert_yaxis()
    ax.set_xlabel('F2 (Hz)', fontsize=13, fontweight='bold')
    ax.set_ylabel('F1 (Hz)', fontsize=13, fontweight='bold')
    ax.set_title('Espacios Vocálicos Superpuestos: ¿Hay Diferencia Acústica?\n' +
                 f'(Basado en {len(girls_vowels)} vocales de niñas y {len(boys_vowels)} vocales de niños)',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.savefig('vowel_spaces_overlap.png', dpi=150, bbox_inches='tight')
    print("  ✓ vowel_spaces_overlap.png")
    plt.close()


def main():
    """Función principal."""
    print("="*70)
    print("ANÁLISIS BASADO EN TRANSCRIPCIÓN AUTOMÁTICA")
    print("="*70)
    print("\nEste análisis:")
    print("  1. Transcribe el audio con Whisper (palabras reales con timestamps)")
    print("  2. Segmenta basándose en palabras transcritas (no en silencios)")
    print("  3. Extrae vocales de palabras reales")
    print("  4. Compara niños vs niñas estadísticamente")
    print("  5. Relaciona con literatura sobre percepción de género")
    print("="*70)

    # Buscar archivos
    audio_files = sorted(Path('.').glob('audio_*.wav'))
    if not audio_files:
        print("\n❌ No se encontraron archivos audio_*.wav")
        return

    print(f"\n📁 Archivos: {len(audio_files)}")
    for f in audio_files:
        print(f"   • {f.name}")

    # Transcribir con Whisper
    transcriber = WhisperTranscriber(model_name="base")

    transcriptions = {}
    for audio_file in audio_files:
        transcription = transcriber.transcribe(audio_file)
        transcriptions[audio_file] = transcription

        # Guardar transcripción
        trans_file = audio_file.stem + "_transcription.json"
        with open(trans_file, 'w', encoding='utf-8') as f:
            json.dump(transcription, f, ensure_ascii=False, indent=2)

    # Analizar cada archivo
    analyzers = []
    for audio_file in audio_files:
        print(f"\n{'='*70}")
        analyzer = WordBasedVoiceAnalyzer(audio_file, transcriptions[audio_file])
        analyzer.analyze_all()
        analyzers.append(analyzer)

    # Comparar géneros
    print(f"\n{'='*70}")
    stats_results, girls_vowels, boys_vowels = compare_genders(analyzers)

    # Visualizaciones
    create_comparison_visualizations(analyzers, stats_results, girls_vowels, boys_vowels)

    # Guardar resultados estadísticos
    with open('gender_comparison_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats_results, f, ensure_ascii=False, indent=2)
    print("  ✓ gender_comparison_stats.json")

    print("\n" + "="*70)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*70)
    print("\nArchivos generados:")
    print("  • *_transcription.json - Transcripciones con timestamps")
    print("  • gender_comparison_statistical.png - Comparaciones estadísticas")
    print("  • vowel_spaces_overlap.png - Espacios vocálicos superpuestos")
    print("  • gender_comparison_stats.json - Resultados estadísticos")
    print("\n🔬 Conclusión relacionada con Funk & Simpson (2023):")
    print("   Ver interpretación en la salida del análisis estadístico arriba")
    print("="*70)


if __name__ == "__main__":
    main()
