import pyautogui
import time 
# to shift monitors add 1920 to the x value
time.sleep(2)
# Get the current position of the mouse cursor
x, y = pyautogui.position()

# Print the results
print(f"Current position: x={x}, y={y}")
screenshot = pyautogui.screenshot()
pixel_color = screenshot.getpixel((x, y))
print(pixel_color)
from screeninfo import get_monitors

print(len(get_monitors()))
# top left hand corner x = 100 y= 50
# close the ticker input x=1345, y=224
# test click
pyautogui.doubleClick(x,y)


# x=1778
# y=763
# pixel_color = pyautogui.pixel(x, y)

# # Print the color of the pixel
# print(pixel_color)
# Monitor 1 symbol input tab  x = 100 y= 50