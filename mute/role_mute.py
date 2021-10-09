import sqlite3
import os
pdir = os.path.abspath('databases')
pdir = os.path.join(pdir, "mute_role.db")

def createTable(): #Создание таблицы
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS guild (guild_id INT, role INT)")
    con.commit()

def readRole(guild_id: int):
    createTable()
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM guild WHERE guild_id = {guild_id}")
    return cur.fetchone()

def addRole(guild_id: int, role: int):
    createTable()
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"INSERT INTO guild VALUES(?, ?)", [guild_id, role])
    con.commit()
    return cur.fetchone()

def deleteRole(guild_id: int):
    createTable()
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"DELETE FROM guild WHERE guild_id = ?", [guild_id])
    con.commit()
    return cur.fetchone()