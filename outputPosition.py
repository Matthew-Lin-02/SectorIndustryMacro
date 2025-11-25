import pyautogui
import time 
# to shift monitors add 1920 to the x value
time.sleep(3)
# Get the current position of the mouse cursor
x, y = pyautogui.position()

# Print the results
print(f"Current position: x={x}, y={y}")

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