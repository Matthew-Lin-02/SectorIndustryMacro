
import requests
from lxml import html
# Sample HTML content
# html_content = """
# <html>
#   <body>
#     <div>Some other content</div>
#     <div>
#       Sector
#       <span>Fw(600)">Technology</span>
#     </div>
#     <div>Some more content</div>
#   </body>
# </html>
# """


# url = "https://eodhd.com/financial-summary/TSLA.US"
# response = requests.get(url)



def addTickers(symbols):
    for symbol in symbols:
        url = "https://eodhd.com/financial-summary/%s.US" % symbol

        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content of the page
            page_content = html.fromstring(response.text)

            # Use XPath to extract article titles and authors
            sector = page_content.xpath('//*[@id="fund_api"]/div[1]/div[2]/div[18]/span/text()')
            industry = page_content.xpath('//*[@id="fund_api"]/div[1]/div[2]/div[19]/span/text()')
            print(symbol)
            print("sector: "+ sector[0].strip("'\""))
            print("industry: " + industry[0].strip("'\""))
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

inputStr = input("Enter symbols separated by commas: ").upper()
symbols = inputStr.split(",")
symbols = [symbol.strip() for symbol in symbols]
addTickers(symbols)