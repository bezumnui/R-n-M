from emb import emb
from config import getlang, setprefix, getprefix
from perm_error import perm_error
from admin.translate import prefix_translate
async def change_prefix(bot, ctx, prefix:str):

    lan = getlang(guild_id=ctx.guild.id)
    if ctx.author.guild_permissions.ban_members == False:
        try:
            text = perm_error()[lan]
        except IndexError:
            text = perm_error()[0]
        return await ctx.reply(embed=emb(bot, ctx, title=text))
    if prefix == "0":
        try:
            text = prefix_translate(ctx, p=getprefix(ctx.guild.id), part=0)[lan]
        except IndexError:
            text = prefix_translate(ctx, p=getprefix(ctx.guild.id), part=0)[0]
        return await ctx.reply(embed=emb(bot, ctx, title=text))

    setprefix(ctx.guild.id, prefix)
    try:
        text = prefix_translate(ctx, p=getprefix(ctx.guild.id), part=1)[lan]
    except IndexError:
        text = prefix_translate(ctx, p=getprefix(ctx.guild.id), part=1)[0]

    return await ctx.reply(embed=emb(bot, ctx, title=text.format(prefix)))