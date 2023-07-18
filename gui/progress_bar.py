import dearpygui.dearpygui as dpg
import PySimpleGUI as sg
import pyaudio
import numpy as np

# PyAudio INIT:
CHUNK = 1024  # Samples: 1024,  512, 256, 128
RATE = 44100  # Equivalent to Human Hearing at 40 kHz
INTERVAL = 4  # Sampling Interval in Seconds ie Interval to listen

dpg.create_context()

def listen_to_audio(sender):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    # Loop through chunks:
    for i in range(int(INTERVAL*RATE/CHUNK)):
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        chunkMax = np.amax(data)
        
        chunkMax /= 10000
        print(chunkMax)

        # Update the progressBar using tag
        dpg.set_value("progress-bar", chunkMax)

    # reset the progress bar after listening.
    dpg.set_value("progress-bar", 0)

    # Tiddy up, this time this code runs:
    stream.stop_stream()
    stream.close()
    print('closing stream')
    p.terminate()
    print('terminating PyAudio')


with dpg.window(tag="Primary Window"):
    dpg.add_text("Audio Level")
    dpg.add_progress_bar(label="Volume", tag="progress-bar")

    dpg.add_button(label="Listen", tag="increment-btn", callback=listen_to_audio)

dpg.create_viewport(title='Window', width=800, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_primary_window("Primary Window", True)

# Animation and Timed function calls
while dpg.is_dearpygui_running():
    # dpg.set_value("speech-img", 1)
    dpg.render_dearpygui_frame()

dpg.start_dearpygui()
dpg.destroy_context()