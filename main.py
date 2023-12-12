import pyttsx3
import speech_recognition as sr
import re

def speak(text):
    engine = pyttsx3.init(driverName='sapi5')  # Use the SAPI5 driver for Microsoft Speech Platform
    voices = engine.getProperty('voices')

    # Set the desired voice using its ID
    desired_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    for voice in voices:
        if voice.id == desired_voice_id:
            engine.setProperty('voice', voice.id)
            break

    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.energy_threshold = 150
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print("You said:", query)
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Error occurred while recognizing speech:", e)
        return ""

def calculate(expression):
    try:
        numbers = []
        operators = []
        pattern = r"[-+]?\d*\.\d+|\d+|[-+*/]"
        matches = re.findall(pattern, expression)

        for match in matches:
            if match in ['+', '-', '*', '/']:
                operators.append(match)
            else:
                numbers.append(float(match))

        result = numbers[0]
        for i in range(len(operators)):
            operator = operators[i]
            operand = numbers[i + 1]
            if operator == '+':
                result += operand
            elif operator == '-':
                result -= operand
            elif operator == '*':
                result *= operand
            elif operator == '/':
                result /= operand

        return result
    except Exception as e:
        print("Error occurred while calculating:", e)
        return None

def main():
    listening = False

    while True:
        command = listen()

        if "hey lidiya" in command:
            listening = True
            speak("Hello! How can I assist you?")
            command = listen()  # Get the next command after wake word

        if listening:
            if "your name" in command or "name" in command or "what is your name" in command:
                speak("I am a virtual assistant.")
            elif "calculate" in command:
                expression = command.replace("calculate", "")
                result = calculate(expression)
                if result is not None:
                    speak("The result is: " + str(result))
            elif "exit" in command:
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    main()
