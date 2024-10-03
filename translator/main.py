from deep_translator import GoogleTranslator
import pyttsx3
import speech_recognition as sr

# Initialize text-to-speech engine and speech recognizer
tts_engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Set properties for the TTS engine
tts_engine.setProperty('rate', 150)  # Speed of speech
tts_engine.setProperty('volume', 1)  # Volume level

# A list of 28 language codes you might want to use for translations
language_codes = [
    'en', 'es', 'fr', 'de', 'zh-cn', 'ja', 'hi', 'ar', 'ru', 'ko',
    'it', 'pt', 'nl', 'tr', 'sv', 'pl', 'cs', 'uk', 'ro', 'hu',
    'el', 'da', 'fi', 'no', 'th', 'vi', 'he', 'ms'
]


def speak(text):
    """Function to convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()


def translate_text(text, target_language):
    """Function to translate text to the target language using deep-translator."""
    try:
        translated = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translated
    except Exception as e:
        print(f"Translation error for {target_language}: {e}")
        return None


def recognize_speech():
    """Function to recognize speech using the microphone."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
        return ""


def main():
    """Main function to run the real-time translator app."""
    print("Welcome to the real-time translator app!")
    speak("Please speak the text you want to translate.")

    user_input = recognize_speech()
    if not user_input:
        return

    user_lang = input("Enter the target language code (e.g., 'en' for English, 'es' for Spanish): ").strip().lower()

    if user_lang not in language_codes:
        print(f"Unsupported language code: {user_lang}. Please choose from: {', '.join(language_codes)}")
        return

    # Translate to 28 languages and optionally read them out
    for code in language_codes:
        translated_text = translate_text(user_input, code)
        if translated_text:
            print(f"Translation in {code}: {translated_text}")
            if code == user_lang:  # Optionally read out the translation in the user's requested language
                speak(translated_text)


if __name__ == "__main__":
    main()
