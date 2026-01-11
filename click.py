import pyautogui
from pynput import keyboard
import sys
import argparse
# from pprint import pprint as pp

# probably a way to store the bindings directly in the config and iterate
def make_key_methods(device, pressed, enabled):
    def on_press(key):
        import pokemonConfig
        pressed.add(key)

        # this non local is needed due to reassignment of the variable
        # happening which the static parser then assumes the variable is local and is being reassigned from local.
        nonlocal enabled 

        if key == keyboard.KeyCode(char='X') and keyboard.Key.shift in pressed:
            enabled = not enabled
            
        if not enabled:
            return
        # other option is to use a mutable and just modify that value which is not a reassignment run_status = {'enabled': True}
        # run_status['enabled'] = not run_status['enabled]

        device_config = getattr(pokemonConfig, device)

        match key:
            case keyboard.Key.enter | keyboard.Key.space:
                pyautogui.click(*device_config['centre'])
            case keyboard.KeyCode(char='b'):
                pyautogui.click(*device_config['bag'])
            case keyboard.KeyCode(char='f'):
                pyautogui.click(*device_config['fight'])
            case keyboard.KeyCode(char='p'):
                pyautogui.click(*device_config['pokemon'])
            case keyboard.KeyCode(char='r'):
                pyautogui.click(*device_config['run'])
            case keyboard.KeyCode(char='1') | keyboard.KeyCode(char='j'):
                pyautogui.click(*device_config['attack1'])
            case keyboard.KeyCode(char='2') | keyboard.KeyCode(char='i') | keyboard.KeyCode(char='k'):
                pyautogui.click(*device_config['attack2'])
            case keyboard.KeyCode(char='3') | keyboard.KeyCode(char='l'):
                pyautogui.click(*device_config['attack3'])
            case keyboard.KeyCode(char='4') | keyboard.KeyCode(char=';'):
                pyautogui.click(*device_config['attack4'])
            case keyboard.KeyCode(char='y'):
                pyautogui.click(*device_config['yes'])
                pyautogui.click(*device_config['yesBattle'])
            case keyboard.KeyCode(char='n'):
                pyautogui.click(*device_config['noBattle'])
                pyautogui.click(*device_config['no'])
            case keyboard.KeyCode(char='m'):
                pyautogui.click(*device_config['megaDynamax'])
            case keyboard.KeyCode(char='5'):
                pyautogui.click(*device_config['rejoin'])
            case keyboard.KeyCode(char='6'):
                pyautogui.click(*device_config['rejoinYes'])
            case keyboard.KeyCode(char='7'):
                pyautogui.click(*device_config['rejoinNo'])
            case keyboard.Key.esc:
                return False
    
    def on_release(key):
        pressed.discard(key)
        pass
    
    return on_press, on_release


# def on_press(key):


    
#     match key:
#         case keyboard.Key.enter:
#             pyautogui.click(1000, 1000)
#         case keyboard.Key.esc:
#             return False


# # Define the callback function for key releases
# def on_release(key):
#     pass


if __name__ == "__main__":
    print("Total arguments:", len(sys.argv))
    print("Script name:", sys.argv[0])
    print("Arguments:", sys.argv[1:])
    """
        Arguments:
            device: string(optional) default: Mac
    """
    parser = argparse.ArgumentParser(description="A script demonstrating positional arguments.")

    # Define a positional argument (not optional)
    parser.add_argument("-d", "--device", default='Mac', help="device that is running the code")

    # Parse the arguments
    args = parser.parse_args()
    on_press, on_release = make_key_methods(args.device, set(), enabled = True)
    # Create a listener for keyboard events
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()