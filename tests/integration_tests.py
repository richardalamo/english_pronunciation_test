import pytest
import soundfile as sf
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "main"))
from record_vad import record_audio_with_vad
from speech_test import assess_pronunciation, load_reference_text, save_json_to_file, is_audio_valid

@pytest.mark.integration
def test_silence_detection():
    """Test that silence stops recording early and Azure doesn't return a result."""
    silence_file = "silence_test.wav"

    # Record silence (just stay quiet!)
    record_audio_with_vad(output_filename=silence_file, max_duration=10)

    # Check the duration is < 3s
    with sf.SoundFile(silence_file) as f:
        silence_duration = len(f) / f.samplerate

    assert silence_duration < 3, f"Silence recording lasted {silence_duration:.2f}s, expected < 3s"

    # Load reference text
    reference_text = load_reference_text("reference_text.txt")
    assert reference_text != "", "Reference text file is empty or missing."

    # Assess pronunciation (should return None or fail gracefully)
    result = assess_pronunciation(silence_file, reference_text)
    assert result is None, f"Expected no result from Azure on silence, got: {result}"

@pytest.mark.integration
def test_reading_recording_and_assessment():
    """Test that recording spoken text returns a JSON response from Azure."""
    reading_file = "reading_test.wav"

    # Record yourself reading out loud
    #record_audio_with_vad(output_filename=reading_file, max_duration=10)

    # Validate audio before sending
    assert is_audio_valid(reading_file), "Audio validation failed."

    reference_text = load_reference_text("reference_text.txt")
    assert reference_text != "", "Reference text file is empty or missing."

    # Get pronunciation assessment
    result = assess_pronunciation(reading_file, reference_text)

    assert result is not None, "Expected a result from Azure, got None."
    assert "PronunciationScore" in result, "PronunciationScore missing in Azure response."

    # Save JSON for manual review
    save_json_to_file(result, "reading_test_result.json")
