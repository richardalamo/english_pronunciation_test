import json
import os
import wave
import numpy as np
import soundfile as sf
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from record import record_audio

# Load environment variables
load_dotenv()
SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")

def is_audio_valid(file_path):
    """Checks if the audio file meets Azure Speech API requirements."""
    if not os.path.exists(file_path):
        print("Error: File does not exist.")
        return False
    
    try:
        # Read audio file
        with sf.SoundFile(file_path) as audio:
            sample_rate = audio.samplerate
            channels = audio.channels
            format_type = audio.subtype
            duration = len(audio) / sample_rate  # Duration in seconds
            
            print(f"Audio properties: Sample Rate = {sample_rate} Hz, Channels = {channels}, Format = {format_type}, Duration = {duration:.2f}s")
            
            # Check format
            if format_type.lower() not in ["pcm_16"]:
                print("Error: Audio format must be 16-bit PCM (WAV).")
                return False
            
            # Check sample rate
            if sample_rate not in [16000, 8000]:
                print("Error: Sample rate must be 16 kHz or 8 kHz.")
                return False

            # Check channels
            if channels != 1:
                print("Error: Audio must be mono (1 channel).")
                return False

            # Check duration
            if duration < 0.5 or duration > 600:
                print("Error: Audio duration must be between 0.5 and 600 seconds.")
                return False

            print("Audio file is valid ✅")
            return True
    except Exception as e:
        print(f"Error reading audio file: {e}")
        return False

def assess_pronunciation(audio_file, reference_text):
    """Runs pronunciation assessment if the audio is valid."""
    if not is_audio_valid(audio_file):
        print("Invalid audio file. Please check the format.")
        return
    
    print("Processing pronunciation assessment...")

    # Set up Speech SDK config
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)

    # Pronunciation assessment config
    pronunciation_config = speechsdk.PronunciationAssessmentConfig(
        reference_text=reference_text,
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
        granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme
    )

    # Recognizer setup
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    pronunciation_config.apply_to(recognizer)

    # Start recognition
    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        assessment_result = speechsdk.PronunciationAssessmentResult(result)

        raw_response_json = json.loads(result.json)  

        response = {
            "PronunciationScore": assessment_result.pronunciation_score,
            "AccuracyScore": assessment_result.accuracy_score,
            "FluencyScore": assessment_result.fluency_score,
            "CompletenessScore": assessment_result.completeness_score,
            "RecognizedText": result.text,
            "RawResponse": raw_response_json
        }
        
        return response
    else:
        print("Error: Could not process the speech.")

def save_json_to_file(data, filename="pronunciation_result.json"):
    """Saves the JSON data to a file in a readable format."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)  
        print(f" JSON saved successfully as {filename}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

def load_reference_text(file_path="reference_text.txt"):
    """Reads the reference text from an external .txt file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()  # Remove leading/trailing spaces or newlines
    except FileNotFoundError:
        print(f"Error: {file_path} not found! Please create the file.")
        return ""


if __name__ == "__main__":

    # Set custom file name
    audio_file_name = "user_test_R_3.wav"

    # Record audio with the given file name
    record_audio(output_filename=audio_file_name, duration=8)  # duration in seconds

    # Load reference text and assess pronunciation
    reference_text = load_reference_text("reference_text.txt")
    result_object = assess_pronunciation(audio_file_name, reference_text)
    
    if result_object:
        save_json_to_file(result_object, "user_test_R_3_no_reference.json")  # Save results


