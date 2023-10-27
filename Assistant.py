import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os


recognizer = sr.Recognizer()
text_to_speech = pyttsx3.init()







# Function to convert text to speech
def speak(text):
    text_to_speech.say(text)
    text_to_speech.runAndWait()

# Function to recognize speech
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said: " + command)
        return command
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print("Error with the request; {0}".format(e))

while True:
    command = listen().lower()

    if "hello" in command:
        speak("Hello! How can I assist you today?")

    elif "what is the time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak("The current time is " + current_time)
    elif "open gpt" in command:
         webbrowser.open("https://chat.openai.com")
         speak("Opening chatGPT")
    elif "open youtube" in command:
         webbrowser.open("https://www.youtube.com")
         speak("Opening Youtube")
    elif "shutdown system" in command:
         speak("Shuting Down the System")
         os.system("shutdown /s /f /t 0")
          
    
    elif "restart system" in command:
          speak("Restarting System")
          os.system("shutdown /r /f /t 0")
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")

    elif "exit" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("I'm sorry, I don't understand that command.")

# You can add more features, like weather information, reminders, and more, by extending the if-elif statements.
