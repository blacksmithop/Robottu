import gradio as gr
import speech_recognition as sr

r = sr.Recognizer()


def transcribe(audio_source, state=""):
    print("Recognising...")
    print(audio_source)
    audio = sr.AudioFile(audio_source)

    result = ""

    try:
        with audio as source:
            audio = r.record(source)                  
            result = r.recognize_google(audio)

    except sr.RequestError as e:
        pass

    except sr.UnknownValueError:
        pass

    state += result + " "

    return state, state

# Set the starting state to an empty string

gr.Interface(
    fn=transcribe, 
    inputs=[
        gr.Audio(source="microphone", type="filepath", streaming=True), 
        "state" 
    ],
    outputs=[
        "textbox",
    ],
    live=True).launch()