import urllib.request as request
import re
import time
from datetime import datetime
import mysql.connector
from update_decks import updateDecks
import requests
from update_cards import update_cards

mydb = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="mtgPrices"
    )

cursor = mydb.cursor()

updateDecks(cursor, mydb)

update_cards(cursor, mydb)


        