# gui
import dearpygui.dearpygui as dpg
# volume visualization
import pyaudio
import numpy as np
# threading
import threading
import speech_recognition as sr


def set_highlighted_excepthook():
    import sys, traceback
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import TerminalFormatter

    lexer = get_lexer_by_name("pytb" if sys.version_info.major < 3 else "py3tb")
    formatter = TerminalFormatter()

    def myexcepthook(type, value, tb):
        tbtext = ''.join(traceback.format_exception(type, value, tb))
        sys.stderr.write(highlight(tbtext, lexer, formatter))

    sys.excepthook = myexcepthook

# Better error highlighting
set_highlighted_excepthook()

# PyAudio INIT:
CHUNK = 1024  # Samples: 1024,  512, 256, 128
RATE = 44100  # Equivalent to Human Hearing at 40 kHz
INTERVAL = 4  # Sampling Interval in Seconds ie Interval to listen

pAud = pyaudio.PyAudio()

dpg.create_context()

session = {}

def callback(in_data, frame_count, time_info, status):
    # pyaudio visalizer
    data = np.frombuffer(in_data, dtype=np.int16)
    chunkMax = np.amax(data)
    chunkMax /= 10000
    dpg.set_value("progress-bar", chunkMax,)

    return (in_data, pyaudio.paContinue)

def listen():
    dpg.set_value("listening-status", "Audio Level (listening)")
    session['stream'] = pAud.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK, stream_callback=callback)
    session['stream'].start_stream()

    session["recognize"] = threading.Thread(target = recognize_speech)
    session["recognize"].start()

def stop():
    dpg.set_value("listening-status", "Audio Level (not-listening)")
    dpg.set_value("progress-bar", 0)
    session['stream'].close()


def recognize_speech():
    r = sr.Recognizer()
    while True:
        try:
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

                    dpg.set_value("spoken-text", spoken_text)
        except sr.RequestError as e:
            pass
            # print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            pass
            # print("unknown error occurred")


with dpg.window(tag="Primary Window"):
    dpg.add_text("Audio Level (not-listening)", tag="listening-status", color=(175, 195, 227))

    with dpg.tooltip("listening-status"):
        dpg.add_text("Shows current listening status")

    dpg.add_progress_bar(label="Volume", tag="progress-bar")

    dpg.add_button(label="Listen", tag="listen-btn", callback=listen)
    dpg.add_button(label="Stop", tag="stop-btn", callback=stop)

    dpg.add_text("", tag="spoken-text")

dpg.create_viewport(title='Window', width=800, height=400)
dpg.set_viewport_small_icon("./assets/images/icon.ico")
dpg.set_viewport_large_icon("./assets/images/icon.ico")

dpg.set_primary_window("Primary Window", True)


if __name__=='__main__':
    dpg.setup_dearpygui()
    dpg.show_viewport()

    # Animation and Timed function calls
    while dpg.is_dearpygui_running():
        # dpg.set_value("speech-img", 1)
        dpg.render_dearpygui_frame()

    dpg.start_dearpygui()
    dpg.destroy_context()