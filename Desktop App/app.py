from dearpygui.core import *
from dearpygui.simple import *

#functions.py Imports
from functions import categorize_words, pre_process, predict

pred = []
#button callbak function
#runs each time when the "Check" button is clicked
def check_spam(pred):
    with window("Spam Filter"):
        if pred == []:
            #runs only once - the the button is first clicked
            #and pred[-1] widget doesn't exist
            add_spacing(count=12)
            add_separator()
            add_spacing(count=12)
        else:
            #hide prediction widget
            hide_item(pred[-1])
        #collect input, pre-process and get prediction
        input_value = get_value("Input")
        input_value = pre_process(input_value)
        pred_text, text_colour = predict(input_value)
        #store prediction inside the pred list
        pred.append(pred_text)
        #display prediction to user
        add_text(pred[-1], color=text_colour)

#window object settings
set_main_window_size(720, 720)
set_global_font_scale(1.25)
set_theme("Purple")
set_style_window_padding(30,30)

with window("Spam Filter", width=720, height=677):
    print("GUI is running...")
    set_window_pos("Spam Filter", 0, 0)

    add_separator()
    add_spacing(count=12)
    #text instructions
    add_text("Enter a message of your choice to check if it's spam or not",color=[192,192,192])
    add_spacing(count=12)
    #collect input
    add_input_text("Input", width=415, default_value="type message here!")
    add_spacing(count=12)
    #action button
    add_button("Check", callback=lambda x,y:check_spam(pred))

start_dearpygui()
print("Bye, GUI")