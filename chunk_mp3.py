from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import librosa
import numpy as np
import os


def detect_silence_ranges(audio, min_silence_len=1000, silence_thresh=-40):
    """
    Detect nonsilent ranges using pydub.
    """
    return detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)


def refine_boundaries_with_librosa(audio_path, ranges, frame_size=2048, hop_size=512):
    """
    Refine segment boundaries using spectral analysis.
    """
    y, sr = librosa.load(audio_path, sr=None)

    # Calculate onset strength
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_size)

    # Detect structural transitions within ranges
    refined_ranges = []
    for start_ms, end_ms in ranges:
        start_sample = int((start_ms / 1000) * sr)
        end_sample = int((end_ms / 1000) * sr)

        # Analyze this section of the audio
        section = y[start_sample:end_sample]
        section_onset_env = librosa.onset.onset_strength(y=section, sr=sr, hop_length=hop_size)
        peaks = librosa.util.peak_pick(section_onset_env, pre_max=3, post_max=3, pre_avg=3, post_avg=3, delta=0.3,
                                       wait=10)
        time_peaks = librosa.frames_to_time(peaks, sr=sr, hop_length=hop_size)

        # Convert refined peaks to ms
        refined_peaks = [(start_ms + int(t * 1000)) for t in time_peaks]
        refined_ranges.extend(refined_peaks)

    return refined_ranges


def split_audio_combined(big_mp3_path, output_dir, min_silence_len=1000, silence_thresh=-40):
    """
    Combine silence detection and spectral analysis to split MP3 into songs.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the large MP3 file
    audio = AudioSegment.from_file(big_mp3_path)

    # Step 1: Detect initial ranges using silence
    initial_ranges = detect_silence_ranges(audio, min_silence_len, silence_thresh)
    print(f"Initial nonsilent ranges: {initial_ranges}")

    # Step 2: Refine boundaries using spectral analysis
    refined_ranges = refine_boundaries_with_librosa(big_mp3_path, initial_ranges)
    print(f"Refined boundaries: {refined_ranges}")

    # Step 3: Split and save each segment
    for i, (start, end) in enumerate(refined_ranges):
        song_segment = audio[start:end]
        output_file = os.path.join(output_dir, f"Song_{i + 1}.mp3")
        song_segment.export(output_file, format="mp3")
        print(f"Saved: {output_file}")


# Example usage
'''
big_mp3 = "large_audio_file.mp3"
output_directory = "output_songs_combined"
split_audio_combined(big_mp3, output_directory, min_silence_len=1000, silence_thresh=-40)
'''