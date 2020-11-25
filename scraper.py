import urllib.request as request
import re

url = "https://www.mtggoldfish.com/metagame/modern/full#paper"
page = request.urlopen(url)

hbytes = page.read()
modern = hbytes.decode("utf-8")
root_url = "https://www.mtggoldfish.com"
last_price = modern.find('''deck-price-paper''')+1

for i in range(25):
    last_price = modern.find('''deck-price-paper''', last_price)+1
    index = modern.find("/archetype/", last_price)
    temp = modern[index:modern.find("\"", index)]
    deck_url = root_url + temp
    deck_name = modern[modern.find(">", index)+1:modern.find("<", index)]
    last_price = modern.find('''deck-price-paper''', last_price)+1
    #read the new page
    page = request.urlopen(deck_url)
    deck_page = page.read().decode("utf-8")
    j = deck_page.find("/deck/download")
    download_link = root_url + deck_page[j:deck_page.find("\"", j)]
    print(download_link)
    request.urlretrieve(download_link, "./" + deck_name + ".txt")
    
url = "https://www.mtggoldfish.com/deck/download/3576392"
request.urlretrieve(url, "./temp.txt")