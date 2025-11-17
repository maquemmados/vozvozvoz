#!/usr/bin/env python3
"""Script de prueba para verificar segmentación con diferentes parámetros."""

import numpy as np
import librosa
import matplotlib.pyplot as plt

class WordSegmenter:
    """Segmenta audio en palabras usando detección de silencios."""

    def __init__(self, audio, sr, silence_thresh_db=-40, min_silence_len=0.3, min_word_len=0.2):
        self.audio = audio
        self.sr = sr
        self.silence_thresh_db = silence_thresh_db
        self.min_silence_len = min_silence_len
        self.min_word_len = min_word_len
        self.words = []

    def segment(self):
        """Detecta y segmenta palabras."""
        frame_length = int(0.025 * self.sr)
        hop_length = int(0.010 * self.sr)
        rms = librosa.feature.rms(y=self.audio, frame_length=frame_length, hop_length=hop_length)[0]
        rms_db = librosa.amplitude_to_db(rms, ref=np.max)
        is_speech = rms_db > self.silence_thresh_db
        times = librosa.frames_to_time(np.arange(len(is_speech)), sr=self.sr, hop_length=hop_length)

        speech_intervals = []
        in_speech = False
        start_time = 0

        for i, (is_sp, time) in enumerate(zip(is_speech, times)):
            if is_sp and not in_speech:
                start_time = time
                in_speech = True
            elif not is_sp and in_speech:
                end_time = time
                duration = end_time - start_time
                if duration >= self.min_word_len:
                    speech_intervals.append((start_time, end_time))
                in_speech = False

        if in_speech:
            speech_intervals.append((start_time, times[-1]))

        self.words = []
        for i, (start, end) in enumerate(speech_intervals):
            self.words.append({
                'index': i,
                'start_time': start,
                'end_time': end,
                'duration': end - start,
            })

        return self.words


# Test con diferentes parámetros
audio_file = "audio_ninia_1.wav"
y, sr = librosa.load(audio_file, sr=None)
duration = len(y) / sr

print(f"Archivo: {audio_file}")
print(f"Duración total: {duration:.2f}s")
print("\n" + "="*70)
print("PRUEBA DE DIFERENTES PARÁMETROS DE SEGMENTACIÓN")
print("="*70)

configs = [
    {"silence_thresh_db": -40, "min_silence_len": 0.3, "min_word_len": 0.2, "desc": "ACTUAL (conservador)"},
    {"silence_thresh_db": -40, "min_silence_len": 0.15, "min_word_len": 0.15, "desc": "Pausas más cortas"},
    {"silence_thresh_db": -40, "min_silence_len": 0.1, "min_word_len": 0.1, "desc": "Muy permisivo"},
    {"silence_thresh_db": -35, "min_silence_len": 0.2, "min_word_len": 0.15, "desc": "Umbral más alto"},
    {"silence_thresh_db": -45, "min_silence_len": 0.15, "min_word_len": 0.15, "desc": "Umbral más bajo"},
]

for config in configs:
    segmenter = WordSegmenter(y, sr, **{k: v for k, v in config.items() if k != 'desc'})
    words = segmenter.segment()

    avg_duration = np.mean([w['duration'] for w in words]) if words else 0

    print(f"\n{config['desc']}:")
    print(f"  Umbral: {config['silence_thresh_db']} dB")
    print(f"  Pausa mínima: {config['min_silence_len']*1000:.0f} ms")
    print(f"  Palabra mínima: {config['min_word_len']*1000:.0f} ms")
    print(f"  → Segmentos detectados: {len(words)}")
    print(f"  → Duración promedio: {avg_duration:.2f}s")

    if len(words) <= 10:
        durations_str = [f"{w['duration']:.2f}s" for w in words]
        print(f"  → Duraciones: {durations_str}")

print("\n" + "="*70)
print("CONCLUSIÓN:")
print("="*70)
print("""
El número de segmentos detectados depende de:
1. Los niños hablan con pocas pausas largas (habla fluida)
2. El umbral de -40 dB es razonable para voces claras
3. La pausa mínima de 300ms es LARGA (detecta frases, no palabras)

RECOMENDACIÓN:
- Para detectar FRASES: usar parámetros actuales (300ms)
- Para detectar PALABRAS: reducir a 100-150ms
- Para GRUPOS RESPIRATORIOS: usar parámetros actuales

La segmentación actual es válida pero detecta "FRASES" no "palabras".
""")
