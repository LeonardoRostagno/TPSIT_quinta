import socket as sck
import threading as thr
import sqlite3 as sql

client = []

def verifica_pericolo_misurazione(val_guardia, misurazione):
    pguardia20 = 20/100 * val_guardia
    pguardia70 = 70/100 * val_guardia

    lv_pericolo =""
     main()