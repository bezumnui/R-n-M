import os
import sqlite3

def _addguild(guild_id: int):
    con = sqlite3.connect("reactrole.db")
    cur = con.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS G{guild_id} (Message int, Role int, Emoji text, RA text)""")
    con.commit()
    return 0

def addrole(guild_id: int, message_id: int, role: int, emoji:str, ra = "+"):
    _addguild(guild_id)
    con = sqlite3.connect("reactrole.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO G{guild_id} VALUES (?, ?, ?, ?)", (message_id, role, emoji, ra))
    con.commit()
    return 0

def returnrole(guild_id: int, message_id: int, emoji:str):
    _addguild(guild_id)
    con = sqlite3.connect("reactrole.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM G{guild_id} WHERE Message = ? AND Emoji = ?", (message_id, emoji))
    lis = cur.fetchall()
    con.commit()
    try:
        return lis
    except Exception:
        return 0

def deleterole(guild_id: int, message_id: int, emoji: str):
    _addguild(guild_id)
    con = sqlite3.connect("reactrole.db")
    cur = con.cursor()
    cur.execute(f"DELETE FROM G{guild_id} WHERE Message = '{message_id}' AND Emoji = '{emoji}'")
    con.commit()

def deletemessage(guild_id: int, message_id: int):
    _addguild(guild_id)
    con = sqlite3.connect("reactrole.db")
    cur = con.cursor()
    cur.execute(f"DELETE FROM G{guild_id} WHERE Message = {(message_id)}", )
    con.commit()


