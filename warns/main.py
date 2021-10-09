from warns import warn_config as w
import nextcord
from nextcord.ext.commands import Context
from config import getlang, getprefix
from emb import emb
from warns.translate import warns_list
from datetime import datetime
import time
async def dewarn(bot, ctx: Context, player: nextcord.Member=None, num: int=None):

    lan = getlang(ctx.guild.id)
    prefix = getprefix(ctx.guild.id)
    if ctx.author.guild_permissions.mute_members == False:
        from perm_error import perm_error

        embed=emb(bot, ctx, title=perm_error()[lan])
        await ctx.reply(embed=embed)
        return

    if player == None or num == None:
        from warns.translate import dewarn_ussage
        embed = emb(bot, ctx, dewarn_ussage[lan].format(prefix))
        await ctx.reply(embed=embed)
        return
    w.delWarn(ctx.guild.id, player.id, num)
    await ctx.message.add_reaction("👍")


async def warns(bot, ctx, player: nextcord.Member=None):
    lan = getlang(ctx.guild.id)
    prefix = getprefix(ctx.guild.id)
    if player == None :
        from warns.translate import warn_ussage
        embed = emb(bot, ctx, warn_ussage[lan].format(prefix))
        await ctx.reply(embed=embed)

        return
    l = w.readWarns(ctx.guild.id, player.id)
    if l == []:
        from warns.translate import empty_list
        return await ctx.reply(embed=emb(bot, ctx, empty_list[lan]))
    ret = ""
    i = 1
    print(l[0])
    for text in l:
        exp = text[2]
        if exp != 0:
            exp = datetime.fromtimestamp(text[2])
        else:
            exp = "no"
        ret += warns_list[lan].format(i, text[1], exp)
        i+=1
    await ctx.reply(embed=emb(bot, ctx, title=ret))


async def warn(bot, ctx, player: nextcord.Member=None, seconds="0", *reason):
    lan = getlang(ctx.guild.id)
    prefix = getprefix(ctx.guild.id)
    if ctx.author.guild_permissions.mute_members == False:
        from perm_error import perm_error
        return await ctx.reply(embed=emb(bot, ctx, title=perm_error()[lan]))
    if player == None:
        from warns.translate import warn_give
        return await ctx.reply(embed=emb(bot, ctx, title=warn_give[lan].format(prefix)))
    reason = list(reason)

    if seconds[0].isdigit() == False:
        valid = ['d', 's', 'h', 'w', 'm']
        time_table = {
            "d": 60 * 60 * 24, #секунды
            "s": 1,
            "h": 60 * 60,
            "w": 60 * 60 * 24 * 7,
            "m": 60
        }
        for i in valid:
            if seconds[0] == i:

                seconds = list(seconds)

                seconds.pop(0)

                seconds = "".join(seconds)
                try:
                    seconds = str(int(seconds) * int(time_table[i]))
                except Exception:
                    pass

    if seconds.isdigit():
        seconds = int(seconds)
    else:
        reason.reverse()
        reason.append(seconds)
        reason.reverse()
        seconds = 0

    if reason == []:
        reason = 'None'
    else:
        reason = " ".join(reason)


    seconds = int(seconds)
    if seconds != 0:
        seconds = int(time.time()) + seconds
    w.addWarn(ctx.guild.id, player.id, reason, seconds)
    if seconds == 0:
        seconds = "Никогда"
    else:
        seconds = datetime.fromtimestamp(seconds)
    from warns.translate import warn_given
    embed = emb(bot, ctx, title=warn_given[lan].format(player, len(w.readWarns(ctx.guild.id, player.id)), ctx.author, reason, seconds))
    await ctx.reply(embed=embed)
    if len(w.readWarns(ctx.guild.id, player.id)) > 2:
        w.delWarns(ctx.guild.id, player.id)
        try:
            await ctx.guild.ban(user=player)
            from warns.translate import was_banned
            embed = emb(bot, ctx, was_banned[lan].format(player.name))
            await ctx.reply(embed=embed)
        except nextcord.errors.Forbidden:
            from warns.translate import bot_not_permitted
            embed = emb(bot, ctx, bot_not_permitted[lan].format(player))
            await ctx.author.send(embed=embed)
