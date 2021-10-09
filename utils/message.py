from nextcord.ext.commands import Context
from nextcord.errors import NotFound
from emb import emb
from utils import error_fetch
from config import getlang

async def fetch_message(bot, ctx: Context, message_id: int, debug=True):
    lan = getlang(ctx.guild.id)
    message = None
    for channel in ctx.guild.text_channels:

        try:
            message = await channel.fetch_message(message_id)
            break
        except NotFound as e:
            message = None
            # print(e)
    if debug and message == None:
        await ctx.reply(embed=emb(bot, ctx, error_fetch.fetch_message_error[lan]))
    return message

async def fetch_role(bot, ctx: Context, role_id: int, debug=True):
    lan = getlang(ctx.guild.id)
    role = ctx.guild.get_role(role_id)
    if debug and role == None:
        await ctx.reply(embed=emb(bot, ctx, error_fetch.fetch_role_error[lan]))

    return role




