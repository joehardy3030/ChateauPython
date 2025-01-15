from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from pydub.utils import make_chunks
import os


def chunk_audio(audio, chunk_size=10 * 60 * 1000):
    """
    Splits the audio into smaller chunks to handle large files.
    Parameters:
        audio (AudioSegment): The audio to chunk.
        chunk_size (int): Size of each chunk in milliseconds (default 10 minutes).
    Returns:
        list: List of AudioSegment chunks.
    """
    return make_chunks(audio, chunk_size)


def process_chunk(chunk, chunk_start, output_dir, min_silence_len=2000, silence_thresh=-20):
    """
    Processes a single chunk for silence detection and splits into smaller audio files.
    Parameters:
        chunk (AudioSegment): The audio chunk to process.
        chunk_start (int): The start time of the chunk in the original audio.
        output_dir (str): Directory to save the smaller audio files.
        min_silence_len (int): Minimum length of silence to detect in milliseconds.
        silence_thresh (int): Silence threshold in dBFS.
    """
    nonsilent_ranges = detect_nonsilent(chunk, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    print(f"Detected {len(nonsilent_ranges)} nonsilent segments in this chunk.")

    for i, (start, end) in enumerate(nonsilent_ranges):
        segment = chunk[start:end]
        segment_start = chunk_start + start
        segment_end = chunk_start + end

        # Save the segment
        output_file = os.path.join(output_dir, f"segment_{segment_start}_{segment_end}.mp3")
        segment.export(output_file, format="mp3")
        print(f"Saved segment: {output_file}")


def split_audio_with_chunks(big_mp3_path, output_dir, chunk_size=10 * 60 * 1000, min_silence_len=2000, silence_thresh=-20):
    """
    Splits a large MP3 file into smaller segments by processing it in chunks.
    Parameters:
        big_mp3_path (str): Path to the large MP3 file.
        output_dir (str): Directory to save the output segments.
        chunk_size (int): Size of each chunk in milliseconds (default 10 minutes).
        min_silence_len (int): Minimum length of silence to detect in milliseconds.
        silence_thresh (int): Silence threshold in dBFS.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the large MP3 file
    audio = AudioSegment.from_file(big_mp3_path)
    chunks = chunk_audio(audio, chunk_size)

    print(f"Audio split into {len(chunks)} chunks of approximately {chunk_size / 1000 / 60} minutes each.")

    for i, chunk in enumerate(chunks):
        chunk_start = i * chunk_size
        print(f"Processing chunk {i + 1}/{len(chunks)}, start time: {chunk_start}ms")
        process_chunk(chunk, chunk_start, output_dir, min_silence_len, silence_thresh)

'''
# Example usage
big_mp3 = "large_audio_file.mp3"  # Replace with your large MP3 file path
output_directory = "output_segments"  # Directory to save the output segments
split_audio_with_chunks(big_mp3, output_directory, chunk_size=10 * 60 * 1000, min_silence_len=2000, silence_thresh=-20)
'''