import sqlite3
import os
pdir = os.path.abspath('databases')
pdir = os.path.join(pdir, "warns.db")



def createTable(): #Создание таблицы
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS guild (guild_id INT, player INT , reason TEXT, time INT)")
    con.commit()

def readWarns(guild_id: int, player: int):
    createTable()

    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM guild WHERE player = {player} AND guild_id = {guild_id}")
    return cur.fetchall()

def addWarn(guild_id: int, player: int, reason: str, seconds: int):
    createTable()

    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute("INSERT INTO guild VALUES(?, ?, ?, ?)", (guild_id, player, reason, seconds))
    con.commit()
    return readWarns(guild_id, player)

def delWarn(guild_id: int, player: int, num: int):
    createTable()
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    reason = readWarns(player)[num - 1]

    if type(reason) is tuple:
        reason = str(reason[1])

    cur.execute("DELETE FROM guild WHERE guild_id = ? AND player = ? AND reason = ?", (guild_id, player, reason))
    con.commit()

def delWarnByReason(guild_id: int, player: int, reason: int):
    createTable()
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute("DELETE FROM guild WHERE guild_id = ? AND player = ? AND reason = ?", (guild_id, player, reason))
    con.commit()

def delWarns(guild_id: int, player: int):
    createTable()
    con = sqlite3.connect(pdir)
    cur = con.cursor()

    cur.execute("DELETE FROM guild WHERE player = ? AND guild_id = ?", (player, guild_id))
    con.commit()