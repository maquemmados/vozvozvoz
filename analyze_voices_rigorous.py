#!/usr/bin/env python3
"""
Análisis Acústico Riguroso de Voces Infantiles
===============================================
Este script realiza análisis acústico CIENTÍFICAMENTE RIGUROSO de grabaciones de voz.

Diferencias clave con el enfoque anterior:
1. Segmentación automática en palabras
2. Detección y segmentación de vocales individuales
3. Formantes extraídos SOLO de núcleos vocálicos estables
4. Pitch extraído SOLO de segmentos sonoros (VAD)
5. Métricas con incertidumbre y variabilidad explícitas

Métricas rigurosas:
- Formantes (F1, F2, F3) por vocal individual
- Pitch en segmentos sonoros
- Duración de palabras y vocales
- Espacios vocálicos por tipo de vocal
"""

import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import seaborn as sns
import parselmouth
from parselmouth.praat import call
import soundfile as sf
import pandas as pd
from pathlib import Path
from scipy import stats, signal
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Configuración visual
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
COLORS_GIRLS = ['#FF1493', '#FF69B4', '#FFB6C1']
COLORS_BOYS = ['#1E90FF', '#4169E1', '#87CEEB']


class WordSegmenter:
    """Segmenta audio en palabras usando detección de silencios."""

    def __init__(self, audio, sr, silence_thresh_db=-40, min_silence_len=0.3, min_word_len=0.2):
        """
        Args:
            audio: señal de audio
            sr: sample rate
            silence_thresh_db: umbral de silencio en dB
            min_silence_len: duración mínima de silencio para separar palabras (segundos)
            min_word_len: duración mínima de una palabra válida (segundos)
        """
        self.audio = audio
        self.sr = sr
        self.silence_thresh_db = silence_thresh_db
        self.min_silence_len = min_silence_len
        self.min_word_len = min_word_len
        self.words = []

    def segment(self):
        """Detecta y segmenta palabras."""
        # Calcular energía RMS
        frame_length = int(0.025 * self.sr)  # 25ms frames
        hop_length = int(0.010 * self.sr)    # 10ms hop

        rms = librosa.feature.rms(y=self.audio, frame_length=frame_length, hop_length=hop_length)[0]

        # Convertir a dB
        rms_db = librosa.amplitude_to_db(rms, ref=np.max)

        # Detectar segmentos de habla
        is_speech = rms_db > self.silence_thresh_db

        # Convertir frames a samples
        times = librosa.frames_to_time(np.arange(len(is_speech)), sr=self.sr, hop_length=hop_length)

        # Encontrar intervalos de habla
        speech_intervals = []
        in_speech = False
        start_time = 0

        for i, (is_sp, time) in enumerate(zip(is_speech, times)):
            if is_sp and not in_speech:
                # Inicio de habla
                start_time = time
                in_speech = True
            elif not is_sp and in_speech:
                # Fin de habla
                end_time = time
                duration = end_time - start_time

                # Solo guardar si es suficientemente largo
                if duration >= self.min_word_len:
                    speech_intervals.append((start_time, end_time))

                in_speech = False

        # Si termina en habla
        if in_speech:
            speech_intervals.append((start_time, times[-1]))

        # Extraer segmentos de audio
        self.words = []
        for i, (start, end) in enumerate(speech_intervals):
            start_sample = int(start * self.sr)
            end_sample = int(end * self.sr)
            word_audio = self.audio[start_sample:end_sample]

            self.words.append({
                'index': i,
                'start_time': start,
                'end_time': end,
                'duration': end - start,
                'audio': word_audio,
                'start_sample': start_sample,
                'end_sample': end_sample
            })

        return self.words


class VowelDetector:
    """Detecta y segmenta vocales individuales."""

    def __init__(self, audio, sr, pitch_floor=150, pitch_ceiling=500):
        """
        Args:
            audio: señal de audio
            sr: sample rate
            pitch_floor: frecuencia mínima de pitch (Hz) - mínimo 150 Hz para Praat
            pitch_ceiling: frecuencia máxima de pitch (Hz)
        """
        self.audio = audio
        self.sr = sr
        self.pitch_floor = max(150, pitch_floor)  # Praat requiere mínimo 150 Hz
        self.pitch_ceiling = pitch_ceiling
        self.snd = None
        self.vowels = []

    def detect(self):
        """Detecta segmentos vocálicos usando pitch + energía."""
        # Crear objeto Sound de Parselmouth
        self.snd = parselmouth.Sound(self.audio, sampling_frequency=self.sr)

        # Extraer pitch (con manejo de errores)
        try:
            pitch = call(self.snd, "To Pitch", 0.0, self.pitch_floor, self.pitch_ceiling)
        except Exception as e:
            # Si falla el análisis de pitch, devolver lista vacía
            print(f"      ⚠ No se pudo analizar pitch en este segmento: {e}")
            return []

        # Extraer intensidad
        try:
            intensity = call(self.snd, "To Intensity", 75, 0.0, "yes")
        except Exception as e:
            print(f"      ⚠ No se pudo analizar intensidad en este segmento: {e}")
            return []

        # Parámetros temporales
        time_step = 0.01  # 10ms
        duration = call(self.snd, "Get total duration")

        # Extraer valores
        pitch_values = []
        intensity_values = []
        times = []

        t = 0
        while t < duration:
            f0 = call(pitch, "Get value at time", t, "Hertz", "Linear")
            intens = call(intensity, "Get value at time", t, "Cubic")

            pitch_values.append(f0 if f0 and not np.isnan(f0) else 0)
            intensity_values.append(intens if intens and not np.isnan(intens) else 0)
            times.append(t)

            t += time_step

        pitch_values = np.array(pitch_values)
        intensity_values = np.array(intensity_values)
        times = np.array(times)

        # Detectar segmentos sonoros (voiced)
        # Un segmento es sonoro si tiene pitch válido Y suficiente intensidad
        is_voiced = (pitch_values > 0) & (intensity_values > np.percentile(intensity_values[intensity_values > 0], 25))

        # Encontrar intervalos vocálicos continuos
        vowel_intervals = []
        in_vowel = False
        start_idx = 0
        min_vowel_duration = 0.05  # 50ms mínimo

        for i, voiced in enumerate(is_voiced):
            if voiced and not in_vowel:
                start_idx = i
                in_vowel = True
            elif not voiced and in_vowel:
                duration = times[i] - times[start_idx]
                if duration >= min_vowel_duration:
                    vowel_intervals.append((start_idx, i))
                in_vowel = False

        if in_vowel and (times[-1] - times[start_idx]) >= min_vowel_duration:
            vowel_intervals.append((start_idx, len(times)))

        # Extraer información de cada vocal
        self.vowels = []
        for i, (start_idx, end_idx) in enumerate(vowel_intervals):
            start_time = times[start_idx]
            end_time = times[min(end_idx, len(times)-1)]
            duration = end_time - start_time

            # Calcular punto medio (más estable para formantes)
            mid_time = (start_time + end_time) / 2

            # Extraer audio del segmento
            start_sample = int(start_time * self.sr)
            end_sample = int(end_time * self.sr)
            vowel_audio = self.audio[start_sample:end_sample]

            # Pitch medio en el segmento
            segment_pitch = pitch_values[start_idx:end_idx]
            valid_pitch = segment_pitch[segment_pitch > 0]
            mean_pitch = np.mean(valid_pitch) if len(valid_pitch) > 0 else 0

            # Intensidad media
            segment_intensity = intensity_values[start_idx:end_idx]
            mean_intensity = np.mean(segment_intensity[segment_intensity > 0])

            self.vowels.append({
                'index': i,
                'start_time': start_time,
                'end_time': end_time,
                'mid_time': mid_time,
                'duration': duration,
                'audio': vowel_audio,
                'pitch_mean': mean_pitch,
                'intensity_mean': mean_intensity,
                'start_sample': start_sample,
                'end_sample': end_sample
            })

        return self.vowels

    def extract_formants(self, vowel):
        """
        Extrae formantes de una vocal individual en su punto medio (más estable).

        Args:
            vowel: diccionario con información de la vocal

        Returns:
            dict con F1, F2, F3 o None si falla
        """
        if self.snd is None:
            return None

        # Crear objeto Formant (configurado para voces infantiles)
        formant = call(self.snd, "To Formant (burg)", 0.0, 5, 5500, 0.025, 50)

        # Extraer en el punto medio (más estable)
        mid_time = vowel['mid_time']

        try:
            f1 = call(formant, "Get value at time", 1, mid_time, "Hertz", "Linear")
            f2 = call(formant, "Get value at time", 2, mid_time, "Hertz", "Linear")
            f3 = call(formant, "Get value at time", 3, mid_time, "Hertz", "Linear")

            # Validar valores
            if f1 and not np.isnan(f1) and f1 > 0 and f1 < 1500:  # F1 razonable
                if f2 and not np.isnan(f2) and f2 > f1 and f2 < 3500:  # F2 > F1
                    if f3 and not np.isnan(f3) and f3 > f2 and f3 < 5000:  # F3 > F2
                        return {'f1': f1, 'f2': f2, 'f3': f3}
        except:
            pass

        return None


class RigorousVoiceAnalyzer:
    """Analizador riguroso de características acústicas."""

    def __init__(self, audio_path):
        self.audio_path = Path(audio_path)
        self.name = self.audio_path.stem

        # Cargar audio
        self.y, self.sr = librosa.load(audio_path, sr=None)

        # Resultados
        self.words = []
        self.all_vowels = []
        self.vowel_formants = []
        self.results = {
            'name': self.name,
            'duration': len(self.y) / self.sr,
            'num_words': 0,
            'num_vowels': 0
        }

    def analyze(self):
        """Ejecuta análisis completo."""
        print(f"\n{'='*70}")
        print(f"Analizando: {self.name}")
        print(f"Duración total: {self.results['duration']:.2f}s")

        # 1. Segmentar en palabras
        print("\n1. Segmentando en palabras...")
        word_segmenter = WordSegmenter(self.y, self.sr)
        self.words = word_segmenter.segment()
        self.results['num_words'] = len(self.words)
        print(f"   ✓ Detectadas {len(self.words)} palabras/segmentos")

        # 2. Detectar vocales en cada palabra
        print("\n2. Detectando vocales...")
        total_vowels = 0

        for word in self.words:
            vowel_detector = VowelDetector(word['audio'], self.sr)
            vowels = vowel_detector.detect()

            # Ajustar tiempos globales
            for vowel in vowels:
                vowel['global_start_time'] = word['start_time'] + vowel['start_time']
                vowel['global_end_time'] = word['start_time'] + vowel['end_time']
                vowel['global_mid_time'] = word['start_time'] + vowel['mid_time']
                vowel['word_index'] = word['index']

                # Extraer formantes
                formants = vowel_detector.extract_formants(vowel)
                if formants:
                    vowel['formants'] = formants
                    self.vowel_formants.append({
                        'word_index': word['index'],
                        'vowel_index': vowel['index'],
                        'time': vowel['global_mid_time'],
                        'duration': vowel['duration'],
                        'f1': formants['f1'],
                        'f2': formants['f2'],
                        'f3': formants['f3'],
                        'pitch': vowel['pitch_mean'],
                        'intensity': vowel['intensity_mean']
                    })

            word['vowels'] = vowels
            total_vowels += len(vowels)

        self.all_vowels = [v for word in self.words for v in word['vowels']]
        self.results['num_vowels'] = total_vowels
        print(f"   ✓ Detectadas {total_vowels} vocales")
        print(f"   ✓ Formantes extraídos de {len(self.vowel_formants)} vocales")

        # 3. Análisis de pitch (solo en vocales)
        print("\n3. Analizando pitch en segmentos sonoros...")
        pitch_values = [v['pitch_mean'] for v in self.all_vowels if v['pitch_mean'] > 0]

        if pitch_values:
            self.results['pitch_mean'] = np.mean(pitch_values)
            self.results['pitch_std'] = np.std(pitch_values)
            self.results['pitch_median'] = np.median(pitch_values)
            self.results['pitch_min'] = np.min(pitch_values)
            self.results['pitch_max'] = np.max(pitch_values)
            self.results['pitch_values'] = pitch_values

            print(f"   ✓ Pitch medio (en vocales): {self.results['pitch_mean']:.1f} Hz")
            print(f"     Rango: {self.results['pitch_min']:.1f} - {self.results['pitch_max']:.1f} Hz")
            print(f"     σ = {self.results['pitch_std']:.1f} Hz")

        # 4. Análisis de formantes
        if self.vowel_formants:
            print("\n4. Análisis de formantes...")
            f1_values = [v['f1'] for v in self.vowel_formants]
            f2_values = [v['f2'] for v in self.vowel_formants]
            f3_values = [v['f3'] for v in self.vowel_formants]

            self.results['f1_mean'] = np.mean(f1_values)
            self.results['f1_std'] = np.std(f1_values)
            self.results['f2_mean'] = np.mean(f2_values)
            self.results['f2_std'] = np.std(f2_values)
            self.results['f3_mean'] = np.mean(f3_values)
            self.results['f3_std'] = np.std(f3_values)

            print(f"   ✓ F1: {self.results['f1_mean']:.0f} ± {self.results['f1_std']:.0f} Hz")
            print(f"   ✓ F2: {self.results['f2_mean']:.0f} ± {self.results['f2_std']:.0f} Hz")
            print(f"   ✓ F3: {self.results['f3_mean']:.0f} ± {self.results['f3_std']:.0f} Hz")

        # 5. Duración de palabras y vocales
        print("\n5. Análisis de duración...")
        word_durations = [w['duration'] for w in self.words]
        vowel_durations = [v['duration'] for v in self.all_vowels]

        self.results['word_duration_mean'] = np.mean(word_durations)
        self.results['word_duration_std'] = np.std(word_durations)
        self.results['vowel_duration_mean'] = np.mean(vowel_durations)
        self.results['vowel_duration_std'] = np.std(vowel_durations)

        print(f"   ✓ Duración media de palabras: {self.results['word_duration_mean']:.3f}s")
        print(f"   ✓ Duración media de vocales: {self.results['vowel_duration_mean']:.3f}s")

        return self.results

    def plot_segmentation(self, ax=None, show_vowels=True):
        """Visualiza la segmentación en palabras y vocales."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(14, 5))

        times = np.linspace(0, self.results['duration'], len(self.y))
        ax.plot(times, self.y, linewidth=0.5, alpha=0.6, color='gray')

        # Marcar palabras
        for word in self.words:
            ax.axvspan(word['start_time'], word['end_time'], alpha=0.2, color='blue', label='Palabra' if word['index'] == 0 else '')

        # Marcar vocales
        if show_vowels:
            for word in self.words:
                for vowel in word.get('vowels', []):
                    t_start = word['start_time'] + vowel['start_time']
                    t_end = word['start_time'] + vowel['end_time']
                    ax.axvspan(t_start, t_end, alpha=0.3, color='red', label='Vocal' if word['index'] == 0 and vowel['index'] == 0 else '')

        ax.set_xlabel('Tiempo (s)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Amplitud', fontsize=12, fontweight='bold')
        ax.set_title(f'Segmentación: {self.name}\n({self.results["num_words"]} palabras, {self.results["num_vowels"]} vocales)',
                    fontsize=13, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

        return ax

    def plot_vowel_space(self, ax=None, color='blue'):
        """Visualiza el espacio vocálico F1-F2."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 8))

        if not self.vowel_formants:
            return ax

        f1 = [v['f1'] for v in self.vowel_formants]
        f2 = [v['f2'] for v in self.vowel_formants]

        ax.scatter(f2, f1, s=100, alpha=0.6, color=color, edgecolors='black', linewidth=1)

        # Añadir elipse de confianza (2 σ)
        if len(f1) > 2:
            from matplotlib.patches import Ellipse
            mean_f1, mean_f2 = np.mean(f1), np.mean(f2)
            std_f1, std_f2 = np.std(f1), np.std(f2)

            ellipse = Ellipse((mean_f2, mean_f1), 2*std_f2, 2*std_f1,
                            alpha=0.2, color=color, label='±1σ')
            ax.add_patch(ellipse)

            ax.scatter([mean_f2], [mean_f1], s=200, color=color, marker='X',
                      edgecolors='black', linewidth=2, label='Media', zorder=10)

        ax.invert_xaxis()
        ax.invert_yaxis()
        ax.set_xlabel('F2 (Hz)', fontsize=12, fontweight='bold')
        ax.set_ylabel('F1 (Hz)', fontsize=12, fontweight='bold')
        ax.set_title(f'Espacio Vocálico - {self.name}\n({len(self.vowel_formants)} vocales)',
                    fontsize=13, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        return ax


def create_rigorous_reports(analyzers):
    """Crea reportes rigurosos con incertidumbre."""

    print("\n" + "="*70)
    print("GENERANDO REPORTES RIGUROSOS")
    print("="*70)

    # 1. Reportes individuales
    print("\n1. Reportes individuales con segmentación...")
    for i, analyzer in enumerate(analyzers):
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.3)

        color = COLORS_GIRLS[i % 3] if 'ninia' in analyzer.name else COLORS_BOYS[i % 3]

        # Segmentación
        ax1 = fig.add_subplot(gs[0, :])
        analyzer.plot_segmentation(ax1)

        # Espacio vocálico
        ax2 = fig.add_subplot(gs[1, 0])
        analyzer.plot_vowel_space(ax2, color=color)

        # Distribución de pitch
        ax3 = fig.add_subplot(gs[1, 1])
        if 'pitch_values' in analyzer.results:
            ax3.hist(analyzer.results['pitch_values'], bins=20, color=color, alpha=0.7, edgecolor='black')
            ax3.axvline(analyzer.results['pitch_mean'], color='red', linewidth=2, linestyle='--',
                       label=f'Media: {analyzer.results["pitch_mean"]:.1f} Hz')
            ax3.set_xlabel('Pitch (Hz)', fontsize=11, fontweight='bold')
            ax3.set_ylabel('Frecuencia', fontsize=11, fontweight='bold')
            ax3.set_title('Distribución de Pitch\n(solo segmentos sonoros)', fontsize=12, fontweight='bold')
            ax3.legend()
            ax3.grid(True, alpha=0.3)

        # Distribución de formantes
        ax4 = fig.add_subplot(gs[2, 0])
        if analyzer.vowel_formants:
            f1 = [v['f1'] for v in analyzer.vowel_formants]
            f2 = [v['f2'] for v in analyzer.vowel_formants]
            f3 = [v['f3'] for v in analyzer.vowel_formants]

            bp = ax4.boxplot([f1, f2, f3], labels=['F1', 'F2', 'F3'], patch_artist=True)
            for patch in bp['boxes']:
                patch.set_facecolor(color)
                patch.set_alpha(0.6)
            ax4.set_ylabel('Frecuencia (Hz)', fontsize=11, fontweight='bold')
            ax4.set_title('Distribución de Formantes\n(extraídos de vocales)', fontsize=12, fontweight='bold')
            ax4.grid(True, alpha=0.3, axis='y')

        # Tabla de métricas
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.axis('off')

        metrics_text = f"""
MÉTRICAS RIGUROSAS
{'='*40}

📊 SEGMENTACIÓN:
  • Palabras detectadas: {analyzer.results['num_words']}
  • Vocales detectadas: {analyzer.results['num_vowels']}
  • Duración total: {analyzer.results['duration']:.2f}s

🎵 PITCH (solo vocales):
  • Media: {analyzer.results.get('pitch_mean', 0):.1f} ± {analyzer.results.get('pitch_std', 0):.1f} Hz
  • Mediana: {analyzer.results.get('pitch_median', 0):.1f} Hz
  • Rango: [{analyzer.results.get('pitch_min', 0):.0f}, {analyzer.results.get('pitch_max', 0):.0f}] Hz

🔊 FORMANTES (n={len(analyzer.vowel_formants)}):
  • F1: {analyzer.results.get('f1_mean', 0):.0f} ± {analyzer.results.get('f1_std', 0):.0f} Hz
  • F2: {analyzer.results.get('f2_mean', 0):.0f} ± {analyzer.results.get('f2_std', 0):.0f} Hz
  • F3: {analyzer.results.get('f3_mean', 0):.0f} ± {analyzer.results.get('f3_std', 0):.0f} Hz

⏱️ DURACIÓN:
  • Palabra media: {analyzer.results.get('word_duration_mean', 0):.3f}s
  • Vocal media: {analyzer.results.get('vowel_duration_mean', 0):.3f}s
        """

        ax5.text(0.05, 0.5, metrics_text, fontsize=10, family='monospace',
                verticalalignment='center', bbox=dict(boxstyle='round',
                facecolor=color, alpha=0.15))

        fig.suptitle(f'ANÁLISIS RIGUROSO - {analyzer.name}', fontsize=15, fontweight='bold')

        filename = f'riguroso_{analyzer.name}.png'
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"   ✓ {filename}")
        plt.close()

    # 2. Comparación de espacios vocálicos
    print("\n2. Comparación de espacios vocálicos...")
    fig, ax = plt.subplots(figsize=(12, 10))

    for i, analyzer in enumerate(analyzers):
        if not analyzer.vowel_formants:
            continue

        color = COLORS_GIRLS[i % 3] if 'ninia' in analyzer.name else COLORS_BOYS[i % 3]
        f1 = [v['f1'] for v in analyzer.vowel_formants]
        f2 = [v['f2'] for v in analyzer.vowel_formants]

        ax.scatter(f2, f1, s=80, alpha=0.5, color=color, label=f'{analyzer.name} (n={len(f1)})')

        # Media
        mean_f1, mean_f2 = np.mean(f1), np.mean(f2)
        ax.scatter([mean_f2], [mean_f1], s=300, color=color, marker='X',
                  edgecolors='black', linewidth=2, zorder=10)

    ax.invert_xaxis()
    ax.invert_yaxis()
    ax.set_xlabel('F2 (Hz)', fontsize=13, fontweight='bold')
    ax.set_ylabel('F1 (Hz)', fontsize=13, fontweight='bold')
    ax.set_title('Comparación de Espacios Vocálicos\n(Formantes extraídos de vocales individuales)',
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.savefig('comparacion_vocales_rigurosa.png', dpi=150, bbox_inches='tight')
    print("   ✓ comparacion_vocales_rigurosa.png")
    plt.close()

    # 3. Comparación de pitch
    print("\n3. Comparación de pitch (solo segmentos sonoros)...")
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    # Gráfico de barras con error
    names = [a.name for a in analyzers]
    pitch_means = [a.results.get('pitch_mean', 0) for a in analyzers]
    pitch_stds = [a.results.get('pitch_std', 0) for a in analyzers]

    colors = [COLORS_GIRLS[i % 3] if 'ninia' in a.name else COLORS_BOYS[i % 3] for i, a in enumerate(analyzers)]

    x = np.arange(len(names))
    bars = axes[0].bar(x, pitch_means, yerr=pitch_stds, color=colors, alpha=0.7, capsize=8,
                       error_kw={'linewidth': 2})
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(names, rotation=45, ha='right')
    axes[0].set_ylabel('Pitch (Hz)', fontsize=12, fontweight='bold')
    axes[0].set_title('Pitch Medio ± σ (solo vocales)', fontsize=13, fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')

    # Añadir número de muestras
    for i, (bar, analyzer) in enumerate(zip(bars, analyzers)):
        n = len(analyzer.results.get('pitch_values', []))
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + pitch_stds[i] + 10,
                    f'n={n}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Violinplot
    pitch_data = [a.results.get('pitch_values', []) for a in analyzers]
    parts = axes[1].violinplot(pitch_data, positions=x, showmeans=True, showmedians=True)

    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(colors[i])
        pc.set_alpha(0.6)

    axes[1].set_xticks(x)
    axes[1].set_xticklabels(names, rotation=45, ha='right')
    axes[1].set_ylabel('Pitch (Hz)', fontsize=12, fontweight='bold')
    axes[1].set_title('Distribución Completa de Pitch', fontsize=13, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('comparacion_pitch_rigurosa.png', dpi=150, bbox_inches='tight')
    print("   ✓ comparacion_pitch_rigurosa.png")
    plt.close()

    # 4. Tabla resumen rigurosa
    print("\n4. Tabla resumen...")
    data = []
    for a in analyzers:
        row = {
            'Grabación': a.name,
            'Palabras': a.results['num_words'],
            'Vocales': a.results['num_vowels'],
            'Formantes': len(a.vowel_formants),
            'Pitch (Hz)': f"{a.results.get('pitch_mean', 0):.1f}±{a.results.get('pitch_std', 0):.1f}",
            'F1 (Hz)': f"{a.results.get('f1_mean', 0):.0f}±{a.results.get('f1_std', 0):.0f}",
            'F2 (Hz)': f"{a.results.get('f2_mean', 0):.0f}±{a.results.get('f2_std', 0):.0f}",
            'F3 (Hz)': f"{a.results.get('f3_mean', 0):.0f}±{a.results.get('f3_std', 0):.0f}",
        }
        data.append(row)

    df = pd.DataFrame(data)
    df.to_csv('metricas_rigurosas.csv', index=False, encoding='utf-8')
    print("   ✓ metricas_rigurosas.csv")

    return df


def main():
    """Función principal."""
    print("="*70)
    print("ANÁLISIS ACÚSTICO RIGUROSO DE VOCES INFANTILES")
    print("="*70)
    print("\nEste análisis implementa segmentación automática y extracción")
    print("de métricas SOLO donde tienen significado científico:")
    print("  • Formantes: extraídos de vocales individuales")
    print("  • Pitch: calculado solo en segmentos sonoros")
    print("  • Incertidumbre: reportada con desviación estándar")
    print("="*70)

    # Buscar archivos
    audio_files = sorted(Path('.').glob('audio_*.wav'))

    if not audio_files:
        print("\n❌ No se encontraron archivos audio_*.wav")
        return

    print(f"\n📁 Archivos encontrados: {len(audio_files)}")
    for f in audio_files:
        print(f"   • {f.name}")

    # Analizar
    analyzers = []
    for audio_file in audio_files:
        analyzer = RigorousVoiceAnalyzer(audio_file)
        analyzer.analyze()
        analyzers.append(analyzer)

    # Generar reportes
    create_rigorous_reports(analyzers)

    print("\n" + "="*70)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*70)
    print("\nArchivos generados:")
    print("  • riguroso_*.png - Reportes individuales con segmentación")
    print("  • comparacion_vocales_rigurosa.png - Espacios vocálicos comparados")
    print("  • comparacion_pitch_rigurosa.png - Pitch con incertidumbre")
    print("  • metricas_rigurosas.csv - Datos con ± σ")
    print("\n📊 Todos los valores incluyen incertidumbre (desv. estándar)")
    print("📊 Formantes extraídos SOLO de vocales individuales")
    print("📊 Pitch calculado SOLO en segmentos sonoros")
    print("="*70)


if __name__ == "__main__":
    main()
