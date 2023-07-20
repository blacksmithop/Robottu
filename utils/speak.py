import pyttsx3

# speech
def text2speech(message):
    # Initialize the engine
    engine = pyttsx3.init()
    print("Response:", message)
    engine.say(message)
    engine.runAndWait()