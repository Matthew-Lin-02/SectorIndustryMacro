import pyautogui
from pynput import keyboard

# Define the callback function for key presses

is_ctrl_pressed = False

def on_press(key):
    # Create a controller object
    #controller = keyboard.Controller()
    global is_ctrl_pressed
    # Check if the Ctrl+L key combination was pressed

    if key == keyboard.Key.ctrl_l:
        is_ctrl_pressed = True

    if is_ctrl_pressed == True and key == keyboard.KeyCode(char='l'):
        #do stuff
        pyautogui.typewrite("Hello, world!", interval=0.25)

# Define the callback function for key releases
def on_release(key):

    global is_ctrl_pressed
    if key != keyboard.Key.ctrl_l:
        is_ctrl_pressed = False
    
    if key == keyboard.Key.esc:
        return False
    
# Create a listener for keyboard events
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
