#!/usr/bin/env python3
"""
Análisis Acústico de Voces Infantiles
======================================
Script para analizar características acústicas de grabaciones de voces de niños
y generar visualizaciones educativas.

Métricas analizadas (todas verificables y confiables):
- Frecuencia fundamental (pitch/F0)
- Formantes (F1, F2, F3)
- Intensidad y dinámica
- Duración
- Características espectrales
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
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo para visualizaciones atractivas
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
COLORS_GIRLS = ['#FF69B4', '#FFB6C1', '#FF1493']  # Rosas
COLORS_BOYS = ['#4169E1', '#87CEEB', '#1E90FF']   # Azules
COLORS_ALL = COLORS_GIRLS + COLORS_BOYS


class VoiceAnalyzer:
    """Analizador de características acústicas de voz."""

    def __init__(self, audio_path):
        """
        Inicializa el analizador con un archivo de audio.

        Args:
            audio_path: Ruta al archivo de audio (.wav)
        """
        self.audio_path = Path(audio_path)
        self.name = self.audio_path.stem

        # Cargar audio con librosa
        self.y, self.sr = librosa.load(audio_path, sr=None)

        # Cargar con Parselmouth para análisis más precisos
        self.snd = parselmouth.Sound(str(audio_path))

        # Almacenar resultados
        self.results = {}

    def analyze_all(self):
        """Ejecuta todos los análisis acústicos."""
        print(f"Analizando: {self.name}")

        self.analyze_duration()
        self.analyze_pitch()
        self.analyze_formants()
        self.analyze_intensity()
        self.analyze_spectral_features()

        return self.results

    def analyze_duration(self):
        """Analiza la duración de la grabación."""
        duration = len(self.y) / self.sr
        self.results['duration'] = duration
        print(f"  ✓ Duración: {duration:.2f} segundos")

    def analyze_pitch(self):
        """
        Analiza la frecuencia fundamental (pitch) usando Parselmouth/Praat.
        Praat es el estándar de oro para análisis de voz.
        """
        # Configuración específica para voces infantiles (rango más alto)
        pitch = call(self.snd, "To Pitch", 0.0, 75, 500)  # 75-500 Hz para niños

        # Extraer valores de pitch
        pitch_values = []
        for i in range(pitch.n_frames):
            f0 = call(pitch, "Get value in frame", i+1, "Hertz")
            if f0 and not np.isnan(f0) and f0 > 0:
                pitch_values.append(f0)

        if pitch_values:
            self.results['pitch_mean'] = np.mean(pitch_values)
            self.results['pitch_std'] = np.std(pitch_values)
            self.results['pitch_min'] = np.min(pitch_values)
            self.results['pitch_max'] = np.max(pitch_values)
            self.results['pitch_median'] = np.median(pitch_values)
            self.results['pitch_values'] = pitch_values
            self.results['pitch_times'] = np.linspace(0, self.results['duration'], len(pitch_values))

            print(f"  ✓ Pitch medio: {self.results['pitch_mean']:.1f} Hz")
            print(f"    Rango: {self.results['pitch_min']:.1f} - {self.results['pitch_max']:.1f} Hz")
        else:
            print("  ⚠ No se pudo extraer información de pitch")

    def analyze_formants(self):
        """
        Analiza los formantes (resonancias vocales) F1, F2, F3.
        Los formantes son cruciales para identificar vocales.
        """
        # Crear objeto Formant con configuración para voces infantiles
        formant = call(self.snd, "To Formant (burg)", 0.0, 5, 5500, 0.025, 50)

        f1_values, f2_values, f3_values = [], [], []

        # Extraer formantes en el punto medio (más estable)
        n_frames = call(formant, "Get number of frames")

        for i in range(1, n_frames + 1):
            f1 = call(formant, "Get value at time", 1, i * 0.025, "Hertz", "Linear")
            f2 = call(formant, "Get value at time", 2, i * 0.025, "Hertz", "Linear")
            f3 = call(formant, "Get value at time", 3, i * 0.025, "Hertz", "Linear")

            if f1 and not np.isnan(f1) and f1 > 0:
                f1_values.append(f1)
            if f2 and not np.isnan(f2) and f2 > 0:
                f2_values.append(f2)
            if f3 and not np.isnan(f3) and f3 > 0:
                f3_values.append(f3)

        if f1_values:
            self.results['f1_mean'] = np.mean(f1_values)
            self.results['f1_std'] = np.std(f1_values)
            print(f"  ✓ F1 medio: {self.results['f1_mean']:.1f} Hz")

        if f2_values:
            self.results['f2_mean'] = np.mean(f2_values)
            self.results['f2_std'] = np.std(f2_values)
            print(f"  ✓ F2 medio: {self.results['f2_mean']:.1f} Hz")

        if f3_values:
            self.results['f3_mean'] = np.mean(f3_values)
            self.results['f3_std'] = np.std(f3_values)
            print(f"  ✓ F3 medio: {self.results['f3_mean']:.1f} Hz")

    def analyze_intensity(self):
        """Analiza la intensidad (volumen) de la grabación."""
        intensity = call(self.snd, "To Intensity", 75, 0.0, "yes")

        intensity_values = []
        for i in range(intensity.n_frames):
            value = call(intensity, "Get value in frame", i+1)
            if value and not np.isnan(value):
                intensity_values.append(value)

        if intensity_values:
            self.results['intensity_mean'] = np.mean(intensity_values)
            self.results['intensity_std'] = np.std(intensity_values)
            self.results['intensity_max'] = np.max(intensity_values)
            self.results['intensity_min'] = np.min(intensity_values)
            self.results['intensity_values'] = intensity_values

            print(f"  ✓ Intensidad media: {self.results['intensity_mean']:.1f} dB")

    def analyze_spectral_features(self):
        """
        Analiza características espectrales que describen el 'color' del sonido.
        """
        # Centroide espectral (brillo del sonido)
        spectral_centroids = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)[0]
        self.results['spectral_centroid_mean'] = np.mean(spectral_centroids)
        self.results['spectral_centroid_std'] = np.std(spectral_centroids)

        # Ancho de banda espectral
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=self.y, sr=self.sr)[0]
        self.results['spectral_bandwidth_mean'] = np.mean(spectral_bandwidth)

        # Rolloff espectral (frecuencia por debajo de la cual está el 85% de la energía)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=self.y, sr=self.sr)[0]
        self.results['spectral_rolloff_mean'] = np.mean(spectral_rolloff)

        # Zero Crossing Rate (útil para distinguir voz de ruido)
        zcr = librosa.feature.zero_crossing_rate(self.y)[0]
        self.results['zcr_mean'] = np.mean(zcr)

        print(f"  ✓ Centroide espectral: {self.results['spectral_centroid_mean']:.1f} Hz")
        print(f"  ✓ Ancho de banda espectral: {self.results['spectral_bandwidth_mean']:.1f} Hz")

    def plot_waveform(self, ax=None):
        """Dibuja la forma de onda."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 4))

        times = np.linspace(0, self.results['duration'], len(self.y))
        ax.plot(times, self.y, linewidth=0.5, alpha=0.7)
        ax.set_xlabel('Tiempo (segundos)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Amplitud', fontsize=12, fontweight='bold')
        ax.set_title(f'Forma de Onda - {self.name}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        return ax

    def plot_spectrogram(self, ax=None):
        """Dibuja el espectrograma (mapa de frecuencias en el tiempo)."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))

        D = librosa.amplitude_to_db(np.abs(librosa.stft(self.y)), ref=np.max)
        img = librosa.display.specshow(D, sr=self.sr, x_axis='time', y_axis='hz',
                                        ax=ax, cmap='viridis')
        ax.set_ylabel('Frecuencia (Hz)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Tiempo (segundos)', fontsize=12, fontweight='bold')
        ax.set_title(f'Espectrograma - {self.name}', fontsize=14, fontweight='bold')

        return ax, img

    def plot_pitch_contour(self, ax=None, color='blue'):
        """Dibuja el contorno de pitch (melodía de la voz)."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 4))

        if 'pitch_values' in self.results:
            ax.plot(self.results['pitch_times'], self.results['pitch_values'],
                   linewidth=2, color=color, alpha=0.7)
            ax.axhline(self.results['pitch_mean'], color='red', linestyle='--',
                      linewidth=2, label=f'Media: {self.results["pitch_mean"]:.1f} Hz')
            ax.fill_between(self.results['pitch_times'],
                           self.results['pitch_mean'] - self.results['pitch_std'],
                           self.results['pitch_mean'] + self.results['pitch_std'],
                           alpha=0.2, color=color, label='±1 desviación estándar')
            ax.set_xlabel('Tiempo (segundos)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Frecuencia (Hz)', fontsize=12, fontweight='bold')
            ax.set_title(f'Contorno de Pitch - {self.name}', fontsize=14, fontweight='bold')
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)

        return ax


def create_comparison_plots(analyzers):
    """Crea visualizaciones comparativas para todas las grabaciones."""

    # Organizar por género
    girls = [a for a in analyzers if 'ninia' in a.name.lower()]
    boys = [a for a in analyzers if 'ninio' in a.name.lower()]

    # 1. Comparación de Pitch
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    # Pitch medio por grabación
    names = [a.name for a in analyzers]
    pitch_means = [a.results.get('pitch_mean', 0) for a in analyzers]
    pitch_stds = [a.results.get('pitch_std', 0) for a in analyzers]

    colors = []
    for a in analyzers:
        if 'ninia' in a.name.lower():
            idx = len([c for c in colors if c in COLORS_GIRLS])
            colors.append(COLORS_GIRLS[min(idx, len(COLORS_GIRLS)-1)])
        else:
            idx = len([c for c in colors if c in COLORS_BOYS])
            colors.append(COLORS_BOYS[min(idx, len(COLORS_BOYS)-1)])

    bars = axes[0].bar(range(len(names)), pitch_means, yerr=pitch_stds,
                       color=colors, alpha=0.7, capsize=5)
    axes[0].set_xticks(range(len(names)))
    axes[0].set_xticklabels(names, rotation=45, ha='right')
    axes[0].set_ylabel('Frecuencia (Hz)', fontsize=12, fontweight='bold')
    axes[0].set_title('Comparación de Pitch Medio (Tono de Voz)', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')

    # Añadir valores sobre las barras
    for i, (bar, value) in enumerate(zip(bars, pitch_means)):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + pitch_stds[i],
                    f'{value:.0f} Hz', ha='center', va='bottom', fontweight='bold')

    # Distribución de pitch por género
    all_girls_pitch = []
    all_boys_pitch = []

    for a in girls:
        if 'pitch_values' in a.results:
            all_girls_pitch.extend(a.results['pitch_values'])

    for a in boys:
        if 'pitch_values' in a.results:
            all_boys_pitch.extend(a.results['pitch_values'])

    if all_girls_pitch:
        axes[1].hist(all_girls_pitch, bins=50, alpha=0.6, color='#FF69B4',
                    label='Niñas', density=True)
    if all_boys_pitch:
        axes[1].hist(all_boys_pitch, bins=50, alpha=0.6, color='#4169E1',
                    label='Niños', density=True)

    axes[1].set_xlabel('Frecuencia (Hz)', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Densidad', fontsize=12, fontweight='bold')
    axes[1].set_title('Distribución de Pitch por Género', fontsize=14, fontweight='bold')
    axes[1].legend(fontsize=11)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('comparacion_pitch.png', dpi=150, bbox_inches='tight')
    print("✓ Guardado: comparacion_pitch.png")
    plt.close()

    # 2. Comparación de Formantes
    fig, ax = plt.subplots(figsize=(12, 10))

    for i, a in enumerate(analyzers):
        f1 = a.results.get('f1_mean', None)
        f2 = a.results.get('f2_mean', None)

        if f1 and f2:
            color = colors[i]
            marker = 'o' if 'ninia' in a.name.lower() else 's'
            ax.scatter(f2, f1, s=300, c=color, marker=marker,
                      alpha=0.7, edgecolors='black', linewidth=2,
                      label=a.name)
            ax.annotate(a.name, (f2, f1), fontsize=10, fontweight='bold',
                       xytext=(10, 10), textcoords='offset points')

    ax.set_xlabel('F2 - Segunda Formante (Hz)', fontsize=12, fontweight='bold')
    ax.set_ylabel('F1 - Primera Formante (Hz)', fontsize=12, fontweight='bold')
    ax.set_title('Espacio de Formantes F1-F2\n(Características Vocales)',
                fontsize=14, fontweight='bold')
    ax.invert_xaxis()  # Convención en fonética
    ax.invert_yaxis()
    ax.legend(fontsize=10, loc='best')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('comparacion_formantes.png', dpi=150, bbox_inches='tight')
    print("✓ Guardado: comparacion_formantes.png")
    plt.close()

    # 3. Comparación de Intensidad
    fig, ax = plt.subplots(figsize=(12, 6))

    intensity_means = [a.results.get('intensity_mean', 0) for a in analyzers]
    intensity_ranges = [(a.results.get('intensity_max', 0) - a.results.get('intensity_min', 0))
                        for a in analyzers]

    x = np.arange(len(names))
    width = 0.35

    bars1 = ax.bar(x - width/2, intensity_means, width, label='Intensidad Media',
                   color=colors, alpha=0.7)
    bars2 = ax.bar(x + width/2, intensity_ranges, width, label='Rango Dinámico',
                   color=colors, alpha=0.4)

    ax.set_xlabel('Grabación', fontsize=12, fontweight='bold')
    ax.set_ylabel('Intensidad (dB)', fontsize=12, fontweight='bold')
    ax.set_title('Comparación de Intensidad y Dinámica', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('comparacion_intensidad.png', dpi=150, bbox_inches='tight')
    print("✓ Guardado: comparacion_intensidad.png")
    plt.close()

    # 4. Características Espectrales
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    features = [
        ('spectral_centroid_mean', 'Centroide Espectral (Brillo)', 'Hz'),
        ('spectral_bandwidth_mean', 'Ancho de Banda Espectral', 'Hz'),
        ('spectral_rolloff_mean', 'Rolloff Espectral', 'Hz'),
        ('zcr_mean', 'Zero Crossing Rate', 'Tasa')
    ]

    for idx, (feature, title, unit) in enumerate(features):
        ax = axes[idx // 2, idx % 2]
        values = [a.results.get(feature, 0) for a in analyzers]

        bars = ax.bar(range(len(names)), values, color=colors, alpha=0.7)
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45, ha='right')
        ax.set_ylabel(unit, fontsize=11, fontweight='bold')
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

        # Añadir valores
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                   f'{value:.1f}', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig('comparacion_espectral.png', dpi=150, bbox_inches='tight')
    print("✓ Guardado: comparacion_espectral.png")
    plt.close()


def create_individual_reports(analyzers):
    """Crea reportes visuales individuales para cada grabación."""

    for i, analyzer in enumerate(analyzers):
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(4, 2, hspace=0.3, wspace=0.3)

        # Determinar color según género
        if 'ninia' in analyzer.name.lower():
            color = COLORS_GIRLS[i % len(COLORS_GIRLS)]
        else:
            color = COLORS_BOYS[i % len(COLORS_BOYS)]

        # 1. Forma de onda
        ax1 = fig.add_subplot(gs[0, :])
        analyzer.plot_waveform(ax1)

        # 2. Espectrograma
        ax2 = fig.add_subplot(gs[1, :])
        analyzer.plot_spectrogram(ax2)

        # 3. Contorno de pitch
        ax3 = fig.add_subplot(gs[2, :])
        analyzer.plot_pitch_contour(ax3, color=color)

        # 4. Resumen de métricas
        ax4 = fig.add_subplot(gs[3, 0])
        ax4.axis('off')

        summary_text = f"""
        RESUMEN DE MÉTRICAS ACÚSTICAS
        ═══════════════════════════════

        📏 Duración: {analyzer.results.get('duration', 0):.2f} segundos

        🎵 Pitch (Tono):
           • Media: {analyzer.results.get('pitch_mean', 0):.1f} Hz
           • Rango: {analyzer.results.get('pitch_min', 0):.1f} - {analyzer.results.get('pitch_max', 0):.1f} Hz
           • Desv. Est.: {analyzer.results.get('pitch_std', 0):.1f} Hz

        🔊 Intensidad:
           • Media: {analyzer.results.get('intensity_mean', 0):.1f} dB
           • Máxima: {analyzer.results.get('intensity_max', 0):.1f} dB

        🎤 Formantes:
           • F1: {analyzer.results.get('f1_mean', 0):.1f} Hz
           • F2: {analyzer.results.get('f2_mean', 0):.1f} Hz
           • F3: {analyzer.results.get('f3_mean', 0):.1f} Hz

        ✨ Características Espectrales:
           • Centroide: {analyzer.results.get('spectral_centroid_mean', 0):.1f} Hz
           • Ancho Banda: {analyzer.results.get('spectral_bandwidth_mean', 0):.1f} Hz
        """

        ax4.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
                verticalalignment='center', bbox=dict(boxstyle='round',
                facecolor=color, alpha=0.2))

        # 5. Distribución de pitch
        ax5 = fig.add_subplot(gs[3, 1])
        if 'pitch_values' in analyzer.results:
            ax5.hist(analyzer.results['pitch_values'], bins=30, color=color,
                    alpha=0.7, edgecolor='black')
            ax5.set_xlabel('Frecuencia (Hz)', fontsize=10, fontweight='bold')
            ax5.set_ylabel('Frecuencia', fontsize=10, fontweight='bold')
            ax5.set_title('Distribución de Pitch', fontsize=11, fontweight='bold')
            ax5.grid(True, alpha=0.3)

        # Título general
        fig.suptitle(f'ANÁLISIS ACÚSTICO COMPLETO - {analyzer.name}',
                    fontsize=16, fontweight='bold', y=0.995)

        filename = f'reporte_{analyzer.name}.png'
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✓ Guardado: {filename}")
        plt.close()


def create_summary_table(analyzers):
    """Crea una tabla resumen con todas las métricas."""

    data = []
    for a in analyzers:
        row = {
            'Grabación': a.name,
            'Duración (s)': f"{a.results.get('duration', 0):.2f}",
            'Pitch Medio (Hz)': f"{a.results.get('pitch_mean', 0):.1f}",
            'Pitch Rango (Hz)': f"{a.results.get('pitch_min', 0):.0f}-{a.results.get('pitch_max', 0):.0f}",
            'F1 (Hz)': f"{a.results.get('f1_mean', 0):.0f}",
            'F2 (Hz)': f"{a.results.get('f2_mean', 0):.0f}",
            'F3 (Hz)': f"{a.results.get('f3_mean', 0):.0f}",
            'Intensidad (dB)': f"{a.results.get('intensity_mean', 0):.1f}",
            'Centroide Espectral (Hz)': f"{a.results.get('spectral_centroid_mean', 0):.0f}",
        }
        data.append(row)

    df = pd.DataFrame(data)

    # Guardar como CSV
    df.to_csv('resumen_metricas.csv', index=False, encoding='utf-8')
    print("✓ Guardado: resumen_metricas.csv")

    # Crear visualización de la tabla
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.axis('tight')
    ax.axis('off')

    table = ax.table(cellText=df.values, colLabels=df.columns,
                    cellLoc='center', loc='center',
                    colWidths=[0.15, 0.1, 0.12, 0.12, 0.08, 0.08, 0.08, 0.12, 0.15])

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)

    # Colorear encabezados
    for i in range(len(df.columns)):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')

    # Colorear filas por género
    for i in range(len(df)):
        color = '#FFE6F0' if 'ninia' in df.iloc[i]['Grabación'].lower() else '#E6F2FF'
        for j in range(len(df.columns)):
            table[(i+1, j)].set_facecolor(color)

    plt.title('TABLA RESUMEN - MÉTRICAS ACÚSTICAS DE TODAS LAS GRABACIONES',
             fontsize=14, fontweight='bold', pad=20)
    plt.savefig('tabla_resumen.png', dpi=150, bbox_inches='tight')
    print("✓ Guardado: tabla_resumen.png")
    plt.close()

    return df


def main():
    """Función principal que ejecuta todo el análisis."""

    print("=" * 70)
    print("ANÁLISIS ACÚSTICO DE VOCES INFANTILES")
    print("=" * 70)
    print()

    # Buscar archivos de audio
    audio_files = sorted(Path('.').glob('audio_*.wav'))

    if not audio_files:
        print("❌ No se encontraron archivos de audio (audio_*.wav)")
        return

    print(f"📁 Se encontraron {len(audio_files)} archivos de audio:")
    for f in audio_files:
        print(f"   • {f.name}")
    print()

    # Analizar cada archivo
    analyzers = []
    for audio_file in audio_files:
        print(f"\n{'='*70}")
        analyzer = VoiceAnalyzer(audio_file)
        analyzer.analyze_all()
        analyzers.append(analyzer)

    print(f"\n{'='*70}")
    print("GENERANDO VISUALIZACIONES")
    print("=" * 70)
    print()

    # Crear reportes individuales
    print("📊 Creando reportes individuales...")
    create_individual_reports(analyzers)
    print()

    # Crear comparaciones
    print("📊 Creando gráficos comparativos...")
    create_comparison_plots(analyzers)
    print()

    # Crear tabla resumen
    print("📊 Creando tabla resumen...")
    df = create_summary_table(analyzers)
    print()

    print("=" * 70)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 70)
    print()
    print("Archivos generados:")
    print("  📄 Reportes individuales: reporte_audio_*.png (6 archivos)")
    print("  📄 Comparación de pitch: comparacion_pitch.png")
    print("  📄 Comparación de formantes: comparacion_formantes.png")
    print("  📄 Comparación de intensidad: comparacion_intensidad.png")
    print("  📄 Comparación espectral: comparacion_espectral.png")
    print("  📄 Tabla resumen visual: tabla_resumen.png")
    print("  📄 Datos tabulados: resumen_metricas.csv")
    print()
    print("🎉 ¡Listo para mostrar a los niños!")
    print()


if __name__ == "__main__":
    main()
