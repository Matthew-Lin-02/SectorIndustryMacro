# from yahooquery import Ticker
# aapl = Ticker('aapl')

# aapl.summary_detail
# print(aapl.summary_detail)
import re
from yahooquery import Ticker
# importing module
from pandas import *
import numpy as np
import requests
from lxml import html
# reading CSV file

ticker_data_file_path = 'Test.txt'  # replace with your file path
ticker_per_industry = "CorrespondingTickersPerIndustry.txt"
input_string = 'hello'  # replace with your input string

def read_col_csv():
    data = read_csv("america_2023-03-17.csv")
    list = data['Ticker'].tolist()
    array = np.array(list)
    strArray = [str(i) for i in array]
    return strArray



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
    with open(ticker_data_file_path, 'r', encoding='utf-8') as f:
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
                print("entered")

                industryDataStr = industryDataStr.split(':',1)
                industryDataStr = industryDataStr[1]
                data = ticker.upper() + ":" + industryDataStr + ":" +  sector + ":" +  industry+ "\n"
                lines.append(data)
                numAdditions += 1

            

        except Exception as e:
            print(e)
            print("no fundamental data")
    lines.sort()
    with open(ticker_data_file_path, 'w', encoding='utf-8') as f:
       f.writelines(lines)
    if numAdditions == 0:
        return 0
    return 1

 

# symbols = read_col_csv() 
inputStr = input("Enter symbols separated by commas: ").upper()
symbols = inputStr.split(",")
symbols = [symbol.strip() for symbol in symbols]


addTickers(symbols)
