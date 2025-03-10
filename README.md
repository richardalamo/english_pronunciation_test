# English Pronunciation Assessment Tool 🎙️

This project provides an **automated English pronunciation assessment tool** designed for language students. It leverages **Azure Cognitive Services Speech API** to evaluate a student's pronunciation based on a reference text.

Students read a predefined paragraph or answer open-ended questions. The tool records their speech, processes the audio, and provides detailed feedback on pronunciation accuracy, fluency, completeness, and more.

---

## ✨ Features

- 🎙 **Voice Activity Detection (VAD):** Automatically starts and stops recording when speech is detected or silence persists.
- 🔍 **Pronunciation Assessment:** Grades pronunciation against a reference paragraph using Azure Speech Services.
- 📄 **Open-ended Evaluation:** Supports analysis of unscripted responses (with slightly less accurate transcripts).
- 📈 **JSON Reports:** Outputs detailed pronunciation metrics for easy review.

---

## 🚀 How It Works

1. **Student Reads Aloud:** The system records the student reading a reference text (or answers an open question).
2. **Voice Activity Detection:** `record_vad.py` listens and automatically stops recording after 3 seconds of silence.
3. **Pronunciation Assessment:** `speech_test.py` validates the audio, sends it to Azure, and retrieves scoring.
4. **Grading & Reporting:** The results are saved as a JSON file with scores for pronunciation, fluency, accuracy, and completeness.

---

## 🏧 Project Structure

```
azure-speech/
├── main/
│   ├── record_vad.py            # Records audio with VAD, saves to WAV
│   ├── speech_test.py           # Sends audio to Azure Speech Service, gets grades
│   ├── reference_text.txt       # Reference text students are graded against
├── tests/
│   ├── integration_tests.py     # Pytest integration tests
├── results/                     # JSON results and audio outputs
├── .env                         # Azure credentials (not included in repo)
├── README.md                    # Project documentation (this file)
├── requirements.txt             # Project dependencies
└── pytest.ini                   # Pytest config for custom markers
```

---

## ⚙️ Requirements

- Python 3.10
- Azure Cognitive Services Speech SDK
- PyTorch
- Silero VAD model via TorchHub
- Sounddevice & Soundfile for audio processing
- dotenv for environment variable management

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root directory with the following content:

```
SPEECH_KEY=your_azure_speech_key
SPEECH_REGION=your_azure_region
```

---

## 🏁 How to Use

### 1. **Record a Pronunciation Test with a Predefined Paragraph**

```bash
python main/speech_test.py
```

- Records audio (auto-stops on silence).
- Assesses pronunciation based on `reference_text.txt`.
- Saves results to `english_test_1.json`.

### 2. **Run Tests**

```bash
pytest tests/integration_tests.py -v
```

- `test_silence_detection()`:
  - Verifies recording stops on silence and no valid speech is detected.
- `test_reading_recording_and_assessment()`:
  - Runs a full pronunciation assessment using pre-recorded or live audio.

---

## 🥪 Tests Overview

- **`integration_tests.py`**  
  Runs integration tests for:
  - VAD (auto-stop on silence).
  - Azure Pronunciation Assessment integration.
  - JSON response validation and file saving.

Custom pytest marker `@pytest.mark.integration` is used for integration tests.  
Run integration tests with:

```bash
pytest -m integration
```

---

## 🗂️ How Recording Works

- `record_vad.py` loads the **Silero VAD model** to detect speech.
- Recording starts immediately and stops automatically when silence is detected (after 3 seconds).
- Saves recorded audio as a WAV file.

---

## ✅ Current Functionality

- **Predefined Text Evaluation**  
  Students read from a script. The tool returns accurate pronunciation scores.
  
- **Open-ended Answer Evaluation**  
  Students respond without a predefined text. The tool analyzes the spontaneous response, though transcripts may be less accurate.

---

## 🔨 Potential Improvements

- We dont have a proper flow on how the english test is gonna be.

---

## 📚 References

- [Azure Cognitive Services Speech](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/)
- [Silero VAD](https://github.com/snakers4/silero-vad)
- [PyTorch Hub](https://pytorch.org/hub/)

---

## 👨‍💻 Author

**Richard (Ricardo Alamo)**  
Data Engineer & Data Scientist | Toronto, Canada
```

