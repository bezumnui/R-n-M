import os
import sqlite3



pdir = os.path.abspath('databases')
pdir = os.path.join(pdir, "config.db")



config = {
    "token": "ODAyMTA2OTU1MTMyMTc0MzQ2.YAqaUA.LCcHd5r4sQzzx9zf39KYTsyeZOc",
    "dev_token": "ODg0NzM2NjI5OTYzNjMyNjUw.YTc1Mg.H-yNlee37uvCew0rcM7b8ISW-fk",
    "dev_token2": "ODQwNDk3NDU4ODAzMTE0MDI2.YJZEQQ.mfr31PBaYp6tleLwUQZ-vruioNE",
    "eco": "ODk2NDU2NTAwNDkzNTUzNzA0.YWHYLQ.tNEz4lunEDmQfIDAmUQSKYdpp2A"
}

def createconfig(guild_id: int):
    createTable()
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"INSERT INTO config VALUES (?, ?, ?, ?, ?)", (guild_id, 'TRUE', '^', 'en', '0'))
    con.commit()
    return 0

def setprefix(guild_id: int, prefix: str):
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"UPDATE config SET Prefix = ? WHERE Guild = ?", (prefix, guild_id))
    con.commit()
    return 0

def setlang(guild_id: int, lang: str):
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"UPDATE config SET Lang = ? WHERE Guild = ?", (lang, guild_id))
    con.commit()
    return 0

def getprefix(guild_id: int):
    createTable()
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM config WHERE Guild = {guild_id}")
    guild = cur.fetchone()
    if guild == None:
        createconfig(guild_id)
        cur.execute(f"SELECT * FROM config WHERE Guild = {guild_id}")
        guild = cur.fetchone()
    con.commit()

    return guild[2]

def getlang(guild_id: int):
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM config WHERE Guild = {guild_id}")
    guild = cur.fetchone()
    con.commit()
    if guild == None:
        createconfig(guild_id)
        cur.execute(f"SELECT * FROM config WHERE Guild = {guild_id}")
        guild = cur.fetchone()
    if guild[3] == "en":
        return 0
    if guild[3] == "ru":
        return 1

def deleteconfig(guild_id: int):
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"DELETE FROM config WHERE Guild = {guild_id}")
    con.commit()
    return 0

def addmuterole(guild_id: int, role: int):
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"UPDATE config SET Muterole = ? WHERE Guild = ?", (role, guild_id))
    con.commit()
    return 0

def readmuterole(guild_id: int):
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM config WHERE Guild = {guild_id}")
    guild = cur.fetchone()
    return guild[4]

#print(deleteconfig(1231241))
def createTable():

    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS config (Guild INT, Economic bool,  Prefix text, Lang text, Muterole int)""")
    con.commit()