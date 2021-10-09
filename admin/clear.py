from perm_error import perm_error
from emb import emb
import asyncio
from admin.translate import clear_translate
from config import  getlang
from nextcord.ext.commands import Bot, Context

async def clear(bot: Bot, ctx: Context, count: int):

    lan = getlang(ctx.guild.id)
    if ctx.author.guild_permissions.manage_messages == False:
        try:
            text = perm_error()[lan]
        except IndexError:
            text = perm_error()[0]
        return await ctx.send(embed=emb(bot, ctx, text))

    deleted = await ctx.channel.purge(limit=count)


    try:
        text = clear_translate(part=0, c=len(deleted))[lan]
    except IndexError:

        text = clear_translate(part=0, c=len(deleted))[0]

    await ctx.send(embed=emb(bot, ctx, text))