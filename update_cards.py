import urllib.request as request
import re
import time
from datetime import datetime
import mysql.connector
from update_decks import updateDecks
import requests

def update_cards(cursor, mydb):
    date = datetime.now().strftime('%Y-%m-%d')
    queryCard = '''SELECT name FROM CARDS WHERE name=%s and date=%s'''
    insertQuery = '''INSERT INTO CARDS (name, date, colors, type, otext, price) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE price=%s, date=%s'''
    creatureInsert = '''INSERT INTO CARDS (name, date, colors, type, power, tough, otext, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE price=%s, date=%s'''
    insertPW = '''INSERT INTO CARDS (name, date, colors, type, otext, price, loyalty) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE price=%s, date=%s'''
    cursor.execute("SELECT list FROM DECKLIST")
    result = cursor.fetchall()
    for i in result:
        temp = ''.join([j for j in i[0] if not j.isdigit()])
        for j in temp.splitlines():
            j = j[1:]

            
            if not j.isspace() and j != '':
                cursor.execute(queryCard, (j,date))
                r = cursor.fetchall()
                if r == []:
                    payload = {"fuzzy":j}
                    response = requests.get("https://api.scryfall.com/cards/named", params=payload)
                    js = response.json()
                    if js and js["object"] != "error":
                        typeLine = js["type_line"]
                        if js.get('oracle_text') == None:
                            flip = []
                            for k in js['card_faces']:
                                flip.append(k['name'])
                            counter = 1
                            for k in js['card_faces']:
                                if "Creature" in k['type_line']:
                                    cursor.execute(
                                        '''INSERT INTO CARDS (name, date, colors, type, power, tough, otext, price, flip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE price=%s, date=%s''', 
                                        (k["name"], date, k["mana_cost"], k["type_line"], k["power"],k["toughness"], k["oracle_text"], js["prices"]["usd"], flip[counter], js["prices"]["usd"], date)
                                    )
                                elif "Planeswalker" in k['type_line']:
                                    cursor.execute(
                                        '''INSERT INTO CARDS (name, date, colors, type, otext, price, loyalty, flip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE price=%s, date=%s''',
                                        (k["name"], date, k["mana_cost"], k["type_line"], k["oracle_text"], js["prices"]["usd"], k['loyalty'], flip[counter], js["prices"]["usd"], date)
                                    )
                                else:
                                    cursor.execute(
                                        '''INSERT INTO CARDS (name, date, colors, type, otext, price, flip) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE price=%s, date=%s''',
                                        (k["name"], date, k["mana_cost"], k["type_line"], k["oracle_text"], js["prices"]["usd"], flip[counter], js["prices"]["usd"], date)
                                    )
                                counter -= 1
                        elif "Creature" in typeLine:
                            cursor.execute(creatureInsert, (j, date, js["mana_cost"], js["type_line"], js["power"],js["toughness"], js["oracle_text"], js["prices"]["usd"], js["prices"]["usd"], date))
                        elif "Planeswalker" in typeLine:
                            cursor.execute(insertPW, (j, date, js["mana_cost"], js["type_line"], js["oracle_text"], js["prices"]["usd"], js["loyalty"], js["prices"]["usd"], date))
                        else:
                            cursor.execute(insertQuery, (j, date, js["mana_cost"], js["type_line"], js["oracle_text"], js["prices"]["usd"], js["prices"]["usd"], date))
                        mydb.commit()  
                    
                    time.sleep(0.05)

    cursor.execute("SELECT name FROM CARDS")
    result = cursor.fetchall()
    insertCHistory = "INSERT INTO CHISTORY (name, date, price) VALUES (%s, %s, %s)"
    for i in result:
        s = i[0]
        payload = {"fuzzy":s}
        response = requests.get("https://api.scryfall.com/cards/named", params=payload)
        js = response.json()
        if js and js["object"] != "error":
            typeLine = js["type_line"]
            if js.get('oracle_text') == None:
                for k in js['card_faces']:
                    cursor.execute(insertCHistory, (k["name"], date, js["prices"]["usd"]))
            else: 
                cursor.execute(insertCHistory, (s, date, js["prices"]["usd"]))
            mydb.commit()  
                    
            time.sleep(0.05)