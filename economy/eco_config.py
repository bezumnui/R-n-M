import sqlite3
import os

pdir = os.path.abspath('databases')
if not os.path.isdir(pdir):
    pdir = ""
pdir = os.path.join(pdir, "economy.db")


def createTable(guild_id: int):
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS G{guild_id} (player INT, money INT)')
    con.commit()

def pay(guild_id: int, pay_from: int, pay_to: int, money: int):
    createTable(guild_id)
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM G{guild_id} WHERE player = ?", [pay_to])
    fetch_to = cur.fetchone()
    if not fetch_to:
        return 1 # player was not found
    cur.execute(f"SELECT * FROM G{guild_id} WHERE player = ?", [pay_from])
    fetch_from = cur.fetchone()
    if not fetch_from:
        addMember(guild_id, pay_from)
        return 2 # not enough money to pay
    if fetch_from[1] < money:
        return 2 # not enough money to pay
    cur.execute(f"UPDATE FROM G{guild_id} SET money = {fetch_to[1] + money} WHERE player = {fetch_to[0]}")
    cur.execute(f"UPDATE FROM G{guild_id} SET money = {fetch_from[1] - money} WHERE player = {fetch_from[0]}")
    con.commit()

def checkBalance(guild_id: int, player: int):
    createTable(guild_id)
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM G{guild_id} WHERE player = ?", [player])
    fetch = cur.fetchone()
    if not fetch:
        return -1
    return fetch[1]

def addMember(guild_id, player):
    createTable(guild_id)
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM G{guild_id} WHERE player = ?", [player])
    if not cur.fetchone():
        cur.execute(f"INSERT INTO G{guild_id} VALUES (?, ?)", [player, 0])
    con.commit()

def addMoney(guild_id: int, player: int, money: int):
    con = sqlite3.connect(pdir)
    cur = con.cursor()
    balance = checkBalance(guild_id, player)
    if balance == -1:
        return balance
    cur.execute(f"UPDATE FROM G{guild_id} SET money = {balance + money} WHERE player = {player}")
    con.commit()