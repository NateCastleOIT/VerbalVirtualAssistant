# VerbalVirtualAssistant


---

# Voice-Activated GPT-3 Assistant

This project is a voice-activated assistant that uses OpenAI's GPT-3 model for generating responses and Eleven Labs API for text-to-speech functionality. The assistant listens for the activation keyword "computer", processes the user's speech, and generates a response.

## Requirements

- Python 3.6 or higher
- `openai` Python package
- `speech_recognition` Python package
- `pyttsx3` Python package
- `elevenlabs` Python package

## Setup

1. Clone the repository to your local machine.
2. Install the required Python packages using pip:

```bash
pip install openai speech_recognition pyttsx3 elevenlabs
```

3. Replace the `OPENAI_API_KEY` and `ELEVEN_LABS_API_KEY` constants in the script with your actual API keys.

## Usage

Run the script using Python:

```bash
python script_name.py
```

The assistant will start listening for the activation keyword "computer". After the keyword, you can ask a question or give a command. The assistant will process your speech, generate a response using GPT-3, and speak the response using Eleven Labs' text-to-speech.

You can also ask the assistant to "clear history" to clear the chat history.

## Limitations

The script uses Google's speech recognition service to recognize speech. This service may not be 100% accurate and may have trouble recognizing speech in noisy environments or with certain accents.

The quality of the assistant's responses depends on the capabilities of the GPT-3 model. The assistant may not always provide accurate or helpful responses.

The text-to-speech functionality is provided by Eleven Labs. The quality of the speech may vary depending on the text and the chosen voice.

## License

This project is licensed under the terms of the MIT license.

---

Please replace `script_name.py` with the actual name of your Python script. Also, you might want to add more sections to the README, such as "Contributing", "Support", "Roadmap", etc., depending on the needs of your project.
