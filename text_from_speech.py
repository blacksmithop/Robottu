import speech_recognition as sr
import pyttsx3
from utils.core import ai_response

# Initialize the recognizer
r = sr.Recognizer()


# Function to convert text to
# speech
def SpeakText(message):
    # Initialize the engine
    engine = pyttsx3.init()

    response = ai_response(message=message)

    engine.say(response)
    engine.runAndWait()


# Loop infinitely for user to
# speak

while 1:
    # Exception handling to handle
    # exceptions at the runtime
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source:
            print("Listening")
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source)

            # listens for the user's input
            audio = r.listen(source)

            # Using google to recognize audio
            spoken_text = r.recognize_google(audio)
            spoken_text = spoken_text.lower() # type: ignore

            print("Speech:", spoken_text)
            SpeakText(spoken_text)

    except sr.RequestError as e:
        pass
        # print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        pass
        # print("unknown error occurred")
