import pyautogui
import pyperclip
from pynput import keyboard
import time
file_path ="IndustrySectorTickers.txt"
import re
from yahooquery import Ticker
# importing module
from pandas import *
import numpy as np
from lxml import html
import requests
# reading CSV file
from screeninfo import get_monitors

file_path = 'IndustrySectorTickers.txt'  # replace with your file path
ticker_per_industry = "CorrespondingTickersPerIndustry.txt"
input_string = 'hello'  # replace with your input string

# all values are the left side monitor
# Coordinates
symbolSearchButtonX = 92
symbolSearchButtonY = 54
# closeSymbolSearchButtonX = 1345
# closeSymbolSearchButtonY = 225
indicatorSettingsX = 150
#indicator1SettingsY = 517 not needed at the moment
indicator2SettingsY = 550
indicator3SettingsY = 583
referenceSymbolButtonX = 1110
referenceSymbolButtonY = 395
# closeReferenceSymbolButtonX = 1144
# closeReferenceSymbolButtonY = 290
leftScreenPixelsX = 1920

# resetWindowX = 1105
# resetWindowY = 107
resetWindowX = 157
resetWindowY = 374
rightPanelX = 1477
rightPanelY = 181

arePixelsLeftMonitor = True
filterButtonHoverRGB = (31, 84, 231)
filterButtonRGB = (41, 98, 255)
filterButtonX = 1822
filterButtonY = 760
fullWindowIndicatorSettings2Y = 800
fullWindowIndicatorSettings3Y = 850
greyDividerColor = (46,46,46)
greyVerticalDividerX = 1606
greyVerticalDividerY = 715
greyHorizontalDividerX = 900
greyHorizontalDividerY = 693

#x=1778, y=770

def search_file(filename, search_word):
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith(search_word):
                return line.strip()
            
def parseLine(line):
    values = line.split(":")
    ticker = values[0]
    sectorTicker = values[1]
    industryTicker = values[2]

    return ticker, sectorTicker, industryTicker   

# A binarySearch of the sector and industry as outputs         
def getSectorIndustry(sectorIndustryData, tickerSearch):

    left = 0 
    right = len(sectorIndustryData)

    try:
        while left <= right:
            mid = (left + right) // 2
            
            midline = sectorIndustryData[mid]
        
            ticker, sectorTicker, industryTicker= parseLine(midline)
            if ticker == tickerSearch:
            
                return sectorTicker,industryTicker
            elif ticker > tickerSearch:
                right = mid - 1
            else:
                left = mid + 1
    except:
        return 0

    return 0

def addTickers(symbols):

    numAdditions = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for ticker in symbols:
 
        try:
            url = "https://eodhd.com/financial-summary/%s.US" % ticker

            response = requests.get(url)
            if response.status_code == 200:
                # Parse the HTML content of the page
                page_content = html.fromstring(response.text)

                # Use XPath to extract article titles and authors
                sector = page_content.xpath('//*[@id="fund_api"]/div[1]/div[2]/div[18]/span/text()')
                industry = page_content.xpath('//*[@id="fund_api"]/div[1]/div[2]/div[19]/span/text()')
                sector = sector[0].strip("'\"")
                industry = industry[0].strip("'\"")

                industry = re.sub("—", "->", industry)
                sector = re.sub("—", "->", sector)
                industry = re.sub(" - ", "->",industry)
                sector = re.sub(" - ", "->",industry)
                industryDataStr = search_file(ticker_per_industry,industry)
                print(ticker)
                print("sector: "+ sector)
                print("industry: " + industry)
            else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

            # yahooQueryTicker = Ticker(ticker)
            
            # industry = yahooQueryTicker.asset_profile[ticker]['industry']
            # sector = yahooQueryTicker.asset_profile[ticker]['sector']
            
            # industry = re.sub("—", "->", industry)
            # sector = re.sub("—", "->", sector)
            # industryDataStr = search_file(ticker_per_industry,industry)
 
            #only works when the ticker is new
            if getSectorIndustry(lines, ticker) == 0:
                industryDataStr = industryDataStr.split(':',1)
                industryDataStr = industryDataStr[1]
                data = ticker.upper() + ":" + industryDataStr + ":" +  sector + ":" +  industry+ "\n"
                lines.append(data)
                numAdditions += 1

            

        except Exception as e:
            print("no fundamental data")
    lines.sort()
    with open(file_path, 'w', encoding='utf-8') as f:
       f.writelines(lines)
    if numAdditions == 0:
        return 0
    return 1


# def assignPixelsToMonitor():
#     global symbolSearchButtonX 
#     global indicatorSettingsX
#     global referenceSymbolButtonX
#     global resetWindowX
#     global rightPanelX
#     global arePixelsLeftMonitor
#     global filterButtonX
#     global greyDividerX
#     x , y =  pyautogui.position()

#     if x > leftScreenPixelsX and arePixelsLeftMonitor:
#         symbolSearchButtonX += leftScreenPixelsX
#         indicatorSettingsX += leftScreenPixelsX
#         referenceSymbolButtonX += leftScreenPixelsX
#         resetWindowX += leftScreenPixelsX
#         rightPanelX += leftScreenPixelsX
#         filterButtonX += leftScreenPixelsX
#         greyDividerX += leftScreenPixelsX
#         arePixelsLeftMonitor = False
#     elif arePixelsLeftMonitor == False and x < leftScreenPixelsX:
#         symbolSearchButtonX -= leftScreenPixelsX
#         indicatorSettingsX -= leftScreenPixelsX
#         referenceSymbolButtonX -= leftScreenPixelsX
#         resetWindowX -= leftScreenPixelsX
#         rightPanelX -= leftScreenPixelsX
#         filterButtonX -= leftScreenPixelsX
#         greyDividerX -= leftScreenPixelsX
#         arePixelsLeftMonitor = True



def getTicker():

    pyautogui.doubleClick(symbolSearchButtonX, symbolSearchButtonY)

    pyautogui.hotkey('ctrl', 'c')

    ticker = pyperclip.paste()
    time.sleep(0.7)
    pyautogui.click(resetWindowX, resetWindowY)
    return ticker

# indicator is in thirds top y value is 500

# ticker param is the ticker of industry or sector
def changeIndicatorSymbolInput(ticker,indicatorSettingsX,indicatorSettingsY):

    pyautogui.doubleClick(indicatorSettingsX,indicatorSettingsY)
    time.sleep(0.3)
    pyautogui.click(referenceSymbolButtonX,referenceSymbolButtonY)
    pyautogui.typewrite(ticker, interval=0.001)
    pyautogui.press('enter')
    time.sleep(0.7)
    pyautogui.click(resetWindowX,resetWindowY)

def changeRightPanel(ticker):
    print("this is the industry")
    pyautogui.click(resetWindowX+leftScreenPixelsX,resetWindowY)
    pyautogui.click(symbolSearchButtonX+leftScreenPixelsX,symbolSearchButtonY)
    pyautogui.typewrite(ticker, interval=0.001)
    pyautogui.press('enter')
    time.sleep(0.7)
    pyautogui.click(resetWindowX,resetWindowY)

    


def implementIndicators(setting2Y, setting3Y):
    try:
        # assignPixelsToMonitor()
        ticker = getTicker()
        print("ticker: ")
        print(ticker)
        sectorSymbol, industrySymbol = getSectorIndustry(sectorIndustryData,ticker)
        print(sectorSymbol)
        print(industrySymbol)
        changeIndicatorSymbolInput(sectorSymbol, indicatorSettingsX, setting2Y)
        changeIndicatorSymbolInput(industrySymbol, indicatorSettingsX, setting3Y)
        if len(get_monitors()) > 1:
            changeRightPanel(industrySymbol)
    except:
        return ticker
    return 1
    
with open(file_path, 'r') as file:
    sectorIndustryData = file.readlines()

is_ctrl_pressed = False

def on_press(key):
    global sectorIndustryData
    # Create a controller object
    #controller = keyboard.Controller()
    global is_ctrl_pressed
    # Check if the Ctrl+L key combination was pressed

    if key == keyboard.Key.ctrl_l:
        is_ctrl_pressed = True

    if is_ctrl_pressed == True and key == keyboard.KeyCode(char='l'):
        # dividerVerticalPixelColor = pyautogui.pixel(greyVerticalDividerX,greyVerticalDividerY) 
        # dividerOpen = greyDividerColor == dividerVerticalPixelColor
        # # watchlist_pixel_color == watchlistHoverColor
        # print(dividerVerticalPixelColor)
        # filterButtonXOffset = 265 if dividerOpen else 0
        # print("greyDividerColor")
        # print(greyDividerColor)
        # print("filterbuttonXoffset")
        # print(filterButtonXOffset)

        # filter_pixel_color = pyautogui.pixel(filterButtonX - filterButtonXOffset, filterButtonY)
        # print("filter_pixel_color:")
        # print(filter_pixel_color)
        
        dividerHorizontalPixelColor = pyautogui.pixel(greyHorizontalDividerX, greyHorizontalDividerY)
        print(dividerHorizontalPixelColor)

        # screener_open = filter_pixel_color == filterButtonRGB or filter_pixel_color == filterButtonHoverRGB # Highlighted, not highlighted
        screener_open = greyDividerColor == dividerHorizontalPixelColor
        print("screener open:")
        print(screener_open)
        setting2Y = 0
        setting3Y = 0                                                    

        if screener_open :
            setting2Y = indicator2SettingsY
            setting3Y = indicator3SettingsY
        else:
            setting2Y = fullWindowIndicatorSettings2Y
            setting3Y = fullWindowIndicatorSettings3Y

        print(setting2Y)
        print(setting3Y)

        
        #
        ticker = implementIndicators(setting2Y, setting3Y)

        if isinstance(ticker, int):
            pass
        else:
            if addTickers([ticker]) > 0:
                with open(file_path, 'r') as file:
                    sectorIndustryData = file.readlines()

                implementIndicators(setting2Y, setting3Y)

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