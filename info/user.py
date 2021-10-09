import nextcord

from emb import emb
from info.translate import user_translate
from nextcord.ext.commands import Context
from config import getlang, getprefix

async def user(bot: nextcord.ext.commands.Bot, ctx: Context, member: nextcord.Member):
    lan = getlang(ctx.guild.id)
    try:
        title = user_translate(ctx, 0, member)[lan]
    except IndexError:
        title = user_translate(ctx, 0, member)[0]
    embed = emb(bot, ctx, title)
    description = ""

    message = user_translate(ctx, 1, member)
    try:
        text = message[lan]
    except IndexError:
        text = message[0]
    description += f"\n{text}"

    embed.description = description
    embed.set_thumbnail(url=ctx.author.avatar.url)
    await ctx.reply(embed=embed)