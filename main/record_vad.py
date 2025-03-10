import logging
import time
import numpy as np
import sounddevice as sd
import torch
import wave

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_silero_vad():
    """
    Load the Silero VAD model and return it along with its get_speech_timestamps utility.
    """
    model, utils = torch.hub.load(
        repo_or_dir='snakers4/silero-vad',
        model='silero_vad',
        force_reload=False
    )
    get_speech_timestamps, _, _, _, _ = utils
    return model, get_speech_timestamps

def record_audio_with_vad(output_filename, sample_rate=16000, channels=1, chunk=512, 
                          silence_threshold=0.3, silence_duration=3, max_duration=60):
    """
    Records audio using a voice activity detection (VAD) model.
    The recording stops when silence persists for a specified duration or when the max duration is reached.
    
    Parameters:
        output_filename (str): Path to the output WAV file.
        sample_rate (int): Audio sampling rate.
        channels (int): Number of audio channels.
        chunk (int): Number of samples per chunk.
        silence_threshold (float): Confidence threshold below which the audio is considered silent.
        silence_duration (float): Duration in seconds of continuous silence to trigger stop.
        max_duration (int): Maximum recording duration in seconds (fallback stop condition).
    
    Returns:
        output_filename (str): The path to the saved WAV file.
    """
    logging.info("Loading Silero VAD model...")
    model, _ = load_silero_vad()

    raw_audio = []
    silent_chunks = 0
    max_silent_chunks = int(silence_duration / (chunk / sample_rate))
    stop_recording = False
    start_time = time.time()  # Track recording start time

    def callback(indata, frames, time_info, status):
        nonlocal silent_chunks, stop_recording

        if status:
            logging.warning(f"Sounddevice status: {status}")

        # Store a copy of the raw audio chunk
        raw_audio.append(indata.copy())

        # Process the chunk for VAD: squeeze to remove extra dimensions.
        audio_int16 = np.squeeze(indata)
        # Normalize to float32 in range [-1, 1] for VAD
        audio_float32 = audio_int16.astype(np.float32) / 32768.0

        if len(audio_float32) == chunk:
            confidence = model(torch.from_numpy(audio_float32), sample_rate).item()
            logging.debug(f"VAD Confidence: {confidence:.3f}")

            if confidence < silence_threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0

            if silent_chunks >= max_silent_chunks:
                logging.info("Silence detected. Stopping recording.")
                stop_recording = True
                raise sd.CallbackStop  # Stop further callback invocations

    logging.info("Recording started. Speak now.")
    with sd.InputStream(samplerate=sample_rate,
                        channels=channels,
                        dtype='int16',
                        callback=callback,
                        blocksize=chunk):
        while not stop_recording:
            elapsed_time = time.time() - start_time
            if elapsed_time >= max_duration:
                logging.info(f"Maximum recording duration of {max_duration} seconds reached. Stopping recording.")
                break
            time.sleep(0.01)  # Sleep to reduce CPU usage

    logging.info("Recording stopped.")

    # Concatenate all recorded chunks into one array and flatten to 1D.
    audio_data = np.concatenate(raw_audio, axis=0).flatten()

    logging.info("Saving recorded audio to WAV file...")
    with wave.open(output_filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 2 bytes per sample for 16-bit audio
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())
    logging.info(f"Audio saved to {output_filename}")

    return output_filename

# Standalone execution check
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    record_audio_with_vad("speech_test.wav", max_duration=20)
