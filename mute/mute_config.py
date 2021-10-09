import sqlite3
import os

pdir = os.path.abspath('databases')
pdir = os.path.join(pdir, "mutes.db")

def createTable(): #Создание таблицы
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS guild (guild_id INT, player INT, time INT)")
    con.commit()

def readMute(guild_id: int, player: int):
    createTable()
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM guild WHERE player = {player} AND guild_id = {guild_id}")
    return cur.fetchone()

def addMute(guild_id, player: int, seconds: int):
    createTable()
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute("INSERT INTO guild VALUES(?, ?, ?)", (guild_id, player, seconds))
    con.commit()
    return readMute(guild_id, player)

def delMute(guild_id: int ,player: int):
    createTable()
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute("DELETE FROM guild WHERE player = ? AND guild_id = ?", (player, guild_id))
    con.commit()