from admin.ReactRole import RRConfig
from nextcord import Message
from perm_error import perm_error
from emb import emb
from config import getlang, getprefix
import nextcord
from nextcord.ext.commands import Context, Bot
async def ReactRole(bot, ctx: Context, message_id: int = 0, emoji: str = None, role_id: int = 0, ra="+"):
    lan = getlang(ctx.guild.id)
    if ra != "+" and ra != "-":
        ra = "+"

    from admin.translate import RRA_translate
    if message_id == 0 or emoji == 0 or role_id == 0:
        return await ctx.reply(embed=emb(bot, ctx, RRA_translate(part=0, p=getprefix(ctx.guild.id))[lan]))
    from utils.message import fetch_message
    message = await fetch_message(bot, ctx, message_id)
    if message == None:
        return
    from utils.message import fetch_role
    role = await fetch_role(bot, ctx, role_id)

    if role == None:
        return
    try:
        await message.add_reaction(emoji)
    except nextcord.errors.HTTPException:
        from utils.error_fetch import fetch_emoji_error
        return await ctx.reply(embed=emb(bot, ctx, fetch_emoji_error[lan]))


    if ctx.author.guild_permissions.manage_roles == False:
        return await ctx.send(embed=emb(bot, ctx, perm_error()[lan]))




    member = await ctx.guild.fetch_member(bot.user.id)
    try:
        await member.add_roles(role)
        await member.remove_roles(role)

    except nextcord.errors.Forbidden:
        from utils import error_fetch
        await message.remove_reaction(emoji=emoji, member=bot.user)
        return await ctx.reply(embed=emb(bot, ctx, error_fetch.fetch_getrole_permission_error[lan]))


    roles = RRConfig.returnrole(ctx.guild.id, message_id, emoji)
    for rolelis in roles:
        if rolelis[3] == ra:
            return

    RRConfig.addrole(ctx.guild.id, message.id, role.id, emoji, ra)
    await message.add_reaction(emoji)
    await ctx.message.add_reaction("✅")
    await ctx.message.delete(delay=5)

