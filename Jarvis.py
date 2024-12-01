from openai import OpenAI
import speech_recognition as sr
import base64
import pyttsx3

import os
from dotenv import load_dotenv

load_dotenv()

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")
VOICE_NAME = "Onyx"
ACTIVATION_KEYWORD = "computer"
END_KEYWORD = "end message"
PAUSE_KEYWORD = "pause"
UNPAUSE_KEYWORD = "unpause"
LISTENING_TIMEOUT = 300  # Timeout duration in seconds
VOLUME = 0.7

# GPT-4 interaction
class GPTInteraction:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.engine.setProperty("volume", VOLUME)  # Set the volume of the text-to-speech output
        self.is_paused = False
        self.is_listening = False
        self.current_message = ""
        self.messages = []
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            organization=ORGANIZATION_ID,
            project=PROJECT_ID,
        )

    def start(self):
        self.say("Hello, I'm " + ACTIVATION_KEYWORD + ".", has_context=False)
        print("Say the activation keyword to start a conversation (" + ACTIVATION_KEYWORD+ ").")

        while True:
            try:
                with self.microphone as source:
                    print("Listening...")
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source, phrase_time_limit=10)
                    print("Processing audio...")

                recognized_text = self.recognize_speech(audio)
                print("You:", recognized_text)

                if ACTIVATION_KEYWORD in recognized_text.lower():
                    self.start_message()
                    continue
                    # user_message = recognized_text.lower().split(ACTIVATION_KEYWORD, 1)[1].strip()
                    
                    # if (user_message == "clear history"):
                    #     self.messages.clear()
                    #     self.say("Chat history cleared.")
                    #     continue
                    
                    # if (not self.messages):
                    #     self.messages.append({"role": "system", "content": "You are a helpful assistant."})7
                        
                    # self.messages.append({"role": "user", "content": user_message})
                    # response = self.get_response()
                    # self.messages.append({"role": "assistant", "content": response})
                    # self.say(response)

            except sr.WaitTimeoutError:
                print("Listening timeout reached. Please try again.")
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that. Could you please repeat?")
            except sr.RequestError:
                self.say("Sorry, I'm having trouble accessing the microphone. Please try again.")

    def recognize_speech(self, audio):
        return self.recognizer.recognize_google(audio)

    def get_response(self):
        response = self.client.chat.completions.create(
            model="gpt-4", 
            messages=self.messages
        )

        answer = response.choices[0].message.content.strip()
        return answer

    def say(self, text, has_context=True):
        print("GPT:", text)
        
        try:
            audio = generate(
                text=text,
                voice=VOICE_NAME,
                )
 
            play(audio)
        except:
            self.engine.say(text)
            self.engine.runAndWait()
        
    def start_message(self):
        print("Activated. Start speaking your message...")
        self.is_listening = True
        while self.is_listening:
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source, timeout=None)
                    print("Processing audio...")

                recognized_text = self.recognize_speech(audio)
                print("You:", recognized_text)

                # Handle pause, unpause, stop, and other keywords
                if END_KEYWORD in recognized_text.lower():
                    self.finish_message()
                    break

                if PAUSE_KEYWORD in recognized_text.lower():
                    self.pause_message()
                    continue

                if UNPAUSE_KEYWORD in recognized_text.lower():
                    self.unpause_message()
                    continue

                # Only add text to the message if not paused
                if not self.is_paused:
                    self.current_message += recognized_text + " "

            except sr.WaitTimeoutError:
                print("Timeout. Still listening...")
            except sr.RequestError:
                self.say("Error with the microphone. Please try again.")

    def pause_message(self):
        self.is_paused = True
        self.say("Message paused. Speak 'unpause' to continue.")

    def unpause_message(self):
        self.is_paused = False
        self.say("Message resumed.")

    def finish_message(self):
        print(f"Final message: {self.current_message}")

        # Process the message to remove the content between pause and unpause
        if PAUSE_KEYWORD in self.current_message and UNPAUSE_KEYWORD in self.current_message:
            parts = self.current_message.split(PAUSE_KEYWORD)
            final_message = parts[0]  # Keep the part before the first "pause"
            for part in parts[1:]:
                # Keep everything after "unpause" in each segment
                final_message += part.split(UNPAUSE_KEYWORD)[-1]
            self.current_message = final_message

        print(f"Cleaned final message: {self.current_message.strip()}")
        
        # Append the message and get response from GPT (simulated here)
        self.messages.append({"role": "user", "content": self.current_message.strip()})
        self.get_response()

    ### Attempting to use OpenAI Audio Generation. Claims I am not using an API key which I am
    
    # def say(self, text, has_context=True):
    #     if not has_context:
    #         self.messages.append({"role": "assistant", "content": text})

    #     audio = self.client.chat.completions.create(
    #         model="gpt-4o-audio-preview",
    #         modalities=["text", "audio"],
    #         audio={"voice": "onyx", "format": "mp3"},
    #         messages=self.messages[len(self.messages)-1],
    #     )

    #     print(audio.choices[0].message.content)

        
        
        
# Main entry point
if __name__ == "__main__":
    interaction = GPTInteraction()
    interaction.start()
