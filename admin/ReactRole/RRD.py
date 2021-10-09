from admin.ReactRole import RRConfig
from nextcord import Message
from perm_error import perm_error
from emb import emb
from config import getlang, getprefix
import nextcord
from nextcord.ext.commands import Context, Bot
async def ReactRole(bot, ctx: Context, message_id):
    lan = getlang(ctx.guild.id)

    from admin.translate import RRD_translate
    if message_id == 0:
        return await ctx.reply(embed=emb(bot, ctx, RRD_translate(part=0, p=getprefix(ctx.guild.id))[lan]))
    from utils.message import fetch_message
    message = await fetch_message(bot, ctx, message_id)
    if message == None:
        return

    RRConfig.deletemessage(message.id)
    await ctx.message.add_reaction("✅")
    await ctx.message.delete(delay=5)