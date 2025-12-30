import os
import subprocess
import requests
import shutil
from config import WHISPER_ROOT, WHISPER_MODEL, WHISPER_MODEL_PATH, TRANSCRIPT_DIR

def download_model_if_needed():
    """
    Checks if the configured Whisper model exists.
    If not, downloads it from Hugging Face.
    """
    if os.path.exists(WHISPER_MODEL_PATH):
        return

    print(f"Model {WHISPER_MODEL} not found at {WHISPER_MODEL_PATH}. Downloading...")
    
    # Ensure models directory exists
    os.makedirs(os.path.dirname(WHISPER_MODEL_PATH), exist_ok=True)

    url = f"https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-{WHISPER_MODEL}.bin"
    
    try:
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(WHISPER_MODEL_PATH, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        print(f"Model downloaded to {WHISPER_MODEL_PATH}")
    except Exception as e:
        print(f"Failed to download model: {e}")
        # cleanup
        if os.path.exists(WHISPER_MODEL_PATH):
            os.remove(WHISPER_MODEL_PATH)
        raise

def convert_to_wav_16k(input_path):
    """
    Converts input audio to 16kHz WAV using ffmpeg.
    Returns a tuple (path to the wav file, boolean indicating if it was newly created).
    """
    output_path = input_path + ".wav"
    
    if os.path.exists(output_path):
        print(f"WAV file already exists, skipping conversion: {output_path}")
        return output_path, False
    
    cmd = [
        "ffmpeg",
        "-y",             # overwrite
        "-i", input_path,
        "-ar", "16000",   # 16kHz sample rate
        "-ac", "1",       # mono
        "-c:a", "pcm_s16le",
        output_path
    ]
    
    # Run ffmpeg silently
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path, True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg conversion failed: {e}")
        return None, False

def transcribe(audio_path):
    """
    Transcribes the given audio file using whisper.cpp.
    """
    if not os.path.exists(audio_path):
        print(f"File not found: {audio_path}")
        return

    # Ensure output dir
    if not os.path.exists(TRANSCRIPT_DIR):
        os.makedirs(TRANSCRIPT_DIR)

    # 1. Prepare Model
    download_model_if_needed()

    # 2. Convert Audio
    print(f"Converting {audio_path} to 16kHz WAV...")
    wav_path, created_temp = convert_to_wav_16k(audio_path)
    if not wav_path:
        return

    # 3. Run Whisper
    # Output file base name (whisper.cpp adds .txt, .vtt etc)
    # We want the output in TRANSCRIPT_DIR
    filename = os.path.basename(audio_path)
    output_base = os.path.join(TRANSCRIPT_DIR, filename)
    expected_output = output_base + ".txt"

    if os.path.exists(expected_output):
        print(f"Transcript already exists: {expected_output}")
        # If we didn't do any work, we might still want to cleanup if we created the wav,
        # but logically if we skip transcription, maybe we shouldn't have converted?
        # But we check transcript existence AFTER conversion in the original code.
        # Let's keep the flow but respect created_temp cleanup.
        if created_temp and os.path.exists(wav_path):
            os.remove(wav_path)
        return

    print(f"Transcribing {filename}...")
    
    # whisper.cpp executable path
    executable = os.path.join(WHISPER_ROOT, "build/bin/whisper-cli")
    
    cmd = [
        executable,
        "-m", WHISPER_MODEL_PATH,
        "-f", wav_path,
        "-otxt",           # output text file
        "-of", output_base # output file prefix (will create output_base.txt)
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Transcription complete: {output_base}.txt")
    except subprocess.CalledProcessError as e:
        print(f"Whisper failed: {e}")
    finally:
        # Cleanup temporary wav file ONLY if we created it
        if created_temp and os.path.exists(wav_path):
            os.remove(wav_path)
