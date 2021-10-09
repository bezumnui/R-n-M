import sqlite3
import os
pdir = os.path.abspath('databases')
pdir = os.path.join(pdir, "previous_role.db")

def createTable(guild_id: int): #Создание таблицы
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS G{guild_id} (player_id INT, role TEXT)")
    con.commit()

def readRoles(guild_id: int, player_id: int):
    createTable(guild_id)
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM G{guild_id} WHERE player_id = ?", [player_id])
    return cur.fetchone()

def addRoles(guild_id: int, player_id: int, role: str):
    createTable(guild_id)
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"INSERT INTO G{guild_id} VALUES(?, ?)", [player_id, role])
    con.commit()
    return cur.fetchone()

def deleteRole(guild_id: int, player_id: int):
    createTable(guild_id)
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"DELETE FROM G{guild_id} WHERE player_id = ?", [player_id])
    con.commit()
    return cur.fetchone()

def popRole(guild_id: int, player_id: int):
    roles = readRoles(guild_id, player_id)[1]
    deleteRole(guild_id, player_id)
    return roles