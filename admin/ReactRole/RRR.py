from admin.ReactRole import RRConfig
from nextcord import Message
from perm_error import perm_error
from emb import emb
from config import getlang, getprefix
import nextcord
from nextcord.ext.commands import Context, Bot
async def ReactRole(bot, ctx: Context, message_id: int = 0, emoji: str = None):
    lan = getlang(ctx.guild.id)

    from admin.translate import RRR_translate
    if message_id == 0 or emoji == 0:
        return await ctx.reply(embed=emb(bot, ctx, RRR_translate(part=0, p=getprefix(ctx.guild.id))[lan]))
    from utils.message import fetch_message
    message = await fetch_message(bot, ctx, message_id)
    if message == None:
        return

    try:
        await message.remove_reaction(emoji)


    except nextcord.errors.HTTPException:
        from utils.error_fetch import fetch_emoji_error
        return await ctx.reply(embed=emb(bot, ctx, fetch_emoji_error[lan]))


    if ctx.author.guild_permissions.manage_roles == False:
        return await ctx.send(embed=emb(bot, ctx, perm_error()[lan]))









    RRConfig.deleterole(ctx.guild.id, message.id, emoji)
    await ctx.message.add_reaction("✅")
    await ctx.message.delete(delay=5)

