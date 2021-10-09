import nextcord
from nextcord.ext.commands import Context, Bot
from nextcord import Member
import config
from nextcord.ext.commands.errors import CommandInvokeError
import re
from emb import emb
from economy import eco_config
import time
import random
import asyncio

async def pay(bot, ctx: Context, pay_to=None, money = "0"):
    from economy import translate
    lan = config.getlang(ctx.guild.id)
    if pay_to == None or money == "0" or not money.isdigit():
        await ctx.message.add_reaction("❌")
        return await ctx.reply(embed=emb(bot, ctx, translate.pay_usage[lan].format(config.getprefix(ctx.guild.id))))
    money = int(money)
    money = abs(money)
    if re:
        pay_to = re.sub(r'[<>@!]', '', pay_to)
    try:
        pay_to = await ctx.guild.fetch_member(pay_to)
    except CommandInvokeError:
        await ctx.message.add_reaction("❌")
        return await ctx.reply(embed=emb(bot, ctx, translate.no_fetch_user[lan]))
    except nextcord.errors.NotFound:
        await ctx.message.add_reaction("❌")
        return await ctx.reply(embed=emb(bot, ctx, translate.no_fetch_user[lan]))
    pay_c = eco_config.pay(ctx.guild.id, ctx.author.id, pay_to.id, money)
    if pay_c == 1:
        await ctx.message.add_reaction("❌")
        return await ctx.reply(embed=emb(bot, ctx, translate.unknown_error[lan]))
    if pay_c == 2:
        await ctx.message.add_reaction("❌")
        return await ctx.reply(embed=emb(bot, ctx, translate.not_enough_money[lan]))
    await ctx.message.add_reaction("✅")

async def money(bot, ctx: Context):
    from economy import translate
    lan = config.getlang(ctx.guild.id)
    money = eco_config.checkBalance(ctx.guild.id, ctx.author.id)
    await ctx.reply(embed=emb(bot, ctx, translate.balance[lan].format(ctx.author.name, money)))

job_lastMinute = []
async def job(bot, ctx: Context):
    from economy import translate
    lan = config.getlang(ctx.guild.id)
    if ctx.author.id in job_lastMinute:
        return await ctx.reply(embed=emb(bot, ctx, translate.already_worked[lan]))
    count = random.randint(1, 4)
    eco_config.addMoney(ctx.guild.id, ctx.author.id, count)
    await ctx.reply(embed=emb(bot, ctx, translate.job_under_paid[lan].format(count)))
    job_lastMinute.append(ctx.author.id)
    await asyncio.sleep(60)
    job_lastMinute.remove(ctx.author.id)