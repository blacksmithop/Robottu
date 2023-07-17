import dearpygui.dearpygui as dpg
import utils.dearpygui_animate as animate
from os import listdir, path
from itertools import cycle
from time import sleep
    
dpg.create_context()
dpg.create_viewport(title="AI Assitant", width=1280, height=720)

# dynamic image
ASSET_PATH = ".\\assets"
width, height, channels, data = dpg.load_image(path.join(ASSET_PATH, "speech.gif"))
speech_assets_list = listdir(path.join(ASSET_PATH, "speech"))
speech_assets_path = [path.join(ASSET_PATH, "speech", asset_name) for asset_name in speech_assets_list]
print(speech_assets_path[0])
speech_assets = cycle(speech_assets_path)

def print_me(sender):
    print(f"Menu Item: {sender}")

# Menu
with dpg.viewport_menu_bar():
    with dpg.menu(label="File"):
        dpg.add_menu_item(label="Save", callback=print_me)
        dpg.add_menu_item(label="Save As", callback=print_me)

        with dpg.menu(label="Settings"):
            dpg.add_menu_item(label="Setting 1", callback=print_me, check=True)
            dpg.add_menu_item(label="Setting 2", callback=print_me)

    dpg.add_menu_item(label="Help", callback=print_me)

    with dpg.menu(label="Widget Items"):
        dpg.add_checkbox(label="Pick Me", callback=print_me)
        dpg.add_button(label="Press Me", callback=print_me)
        dpg.add_color_picker(label="Color Me", callback=print_me)

# Speech Animation
with dpg.texture_registry(show=True):
    dpg.add_dynamic_texture(width=width, height=height, default_value=data, tag="speech-img")
        
with dpg.window(label="J.A.R.V.I.S", tag="Jarvis Window", width=width, height=height+50):
    img = dpg.add_image("speech-img")

# Button
with dpg.window(label="Chat", tag="Button Window", width=200, height=200):
    record = dpg.add_button(tag="talk-btn", label="Record")


animate.add("position", "Jarvis Window", [622, 800], [622, 304], [0, .06, .2, .99], 60)
animate.add("opacity", "Jarvis Window", 0, 1, [.57, .06, .61, .86], 60)


dpg.setup_dearpygui()
dpg.show_viewport()

# Animation and Timed function calls
while dpg.is_dearpygui_running():
    animate.run()
    asset_path = next(speech_assets)
    width, height, channels, data = dpg.load_image(asset_path)
    dpg.set_value("speech-img", data)
    dpg.render_dearpygui_frame()

dpg.save_init_file("dpg.ini")
dpg.destroy_context()
