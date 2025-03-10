import sounddevice as sd
import wave
import numpy as np

# Constants for recording
SAMPLE_RATE = 16000  
CHANNELS = 1  

def record_audio(output_filename, duration):
    """
    Records audio and saves it in 16kHz, mono, PCM_16 format.

    Parameters:
        output_filename (str): The file path where the recording will be saved.
        duration (float): Duration in seconds for the recording.
    """
    print(f"Recording for {duration} seconds...")
    audio_data = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=np.int16)
    sd.wait()  # Wait for the recording to finish

    # Save to WAV file
    with wave.open(output_filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 2 bytes for 16-bit audio
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())

    print(f"Recording saved as {output_filename}")

if __name__ == "__main__":
    record_audio("my_recording.wav", 5)