import urllib.request as request
import re
import time
from datetime import datetime
import mysql.connector
import os


def updateDecks(cursor, mydb):
    url = "https://www.mtggoldfish.com/metagame/modern/full#paper"
    page = request.urlopen(url)
    date = datetime.now().strftime('%Y-%m-%d')

    hbytes = page.read()
    modern = hbytes.decode("utf-8")
    rootUrl = "https://www.mtggoldfish.com"
    lastPrice = modern.find('''deck-price-paper''')+1

    deckUpdate = '''INSERT INTO DECKS (uid, name, price, date) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE price=%s, date=%s'''
    priceUpdate = '''INSERT INTO PHISTORY (uid, price, date, list) VALUES (%s, %s, %s, %s)'''
    deckLUpdate = '''INSERT INTO DECKLIST (uid, list, date) VALUES (%s, %s, %s)'''

    
    for i in range(25):
        lastPrice = modern.find('''deck-price-paper''', lastPrice)+1
        index = modern.find("/archetype/", lastPrice)
        temp = modern[index:modern.find("\"", index)]
        deckUrl = rootUrl + temp
        deckName = modern[modern.find(">", index)+1:modern.find("<", index)].replace("&#39;", "\'")
        lastPrice = modern.find('''deck-price-paper''', lastPrice)+1
        #read the new page
        print(deckUrl)
        page = request.urlopen(deckUrl)
        deckPage = page.read().decode("utf-8")
        #get deck price
        priceL = deckPage.find("$")
        price = int(deckPage[priceL+2:deckPage.find("<", priceL)].replace(',',''))
        #create uid
        uidL = deckPage.find('''Farchetype''') + 13
        uid = deckPage[uidL:deckPage.find('''"''', uidL)]
        #download deck
        j = deckPage.find("/deck/download")
        downloadLink = rootUrl + deckPage[j:deckPage.find("\"", j)]
        request.urlretrieve(downloadLink, "./" + deckName + ".txt")
        f = open(deckName + ".txt", 'r')
        s = ""
        for i in f:
            s += i

        
        data = (uid, deckName, price, date, price, date)
        cursor.execute(deckUpdate, data)
        cursor.execute(priceUpdate, (uid, price, date, s))
        cursor.execute(deckLUpdate, (uid, s, date))
        os.remove(deckName + ".txt")
        time.sleep(1)

    mydb.commit()