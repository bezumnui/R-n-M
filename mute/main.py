from mute import mute_config as m
import nextcord
from nextcord.ext.commands import Context
from config import getlang, getprefix
from emb import emb
import asyncio
from datetime import datetime
import time

async def unmute(bot, ctx: Context = None, player: nextcord.Member=None, Alert=True):
    lan = getlang(ctx.guild.id)
    prefix = getprefix(ctx.guild.id)
    if ctx.author.guild_permissions.mute_members == False:
        from perm_error import perm_error
        if Alert:
            embed=emb(bot, ctx, title=perm_error()[lan])

            await ctx.reply(embed=embed)
        return

    if player == None:
        if Alert:

            from mute.translate import unmute_ussage
            embed = emb(bot, ctx, unmute_ussage[lan].format(prefix))
            await ctx.reply(embed=embed)
        return

    try:
        m.delMute(ctx.guild.id, player.id)
    except Exception:
        if Alert:
            return await ctx.message.add_reaction("❌")
    if Alert:
        await ctx.message.add_reaction("👍")

async def unmute_system(bot: nextcord.ext.commands.Bot, message: nextcord.Message, player: nextcord.Member=None, Alert=True):
        m.delMute(message.guild.id, player.id)
        try:
            from mute.role_mute import readRole
            roleid = readRole(message.guild.id)[1]

            role = message.guild.get_role(roleid)

            await player.remove_roles(role)
        except AttributeError as e:
            print("exception: ", e)

        from mute.previous import popRole
        liststr = popRole(message.guild.id, player.id)
        liststr = liststr.split(";")
        for roleid in liststr:
            try:
                role = message.guild.get_role(int(roleid))
                await player.add_roles(role)
            except:
                pass #будущий я, прости меня, опять

async def mute(bot, ctx: nextcord.ext.commands.Context, player: nextcord.Member=None, seconds="0"):

    lan = getlang(ctx.guild.id)
    prefix = getprefix(ctx.guild.id)

    if player == None:
        from mute.translate import mute_ussage
        return await ctx.reply(embed=emb(bot, ctx, title=mute_ussage[lan].format(prefix)))

    if ctx.author.guild_permissions.mute_members == False or player.guild_permissions.administrator:
        from perm_error import perm_error
        return await ctx.reply(embed=emb(bot, ctx, title=perm_error()[lan]))


    if seconds[0].isdigit() == False:
        valid = ['d', 's', 'h', 'w', 'm']
        time_table = {
            "d": 60 * 60 * 24,
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

    seconds = int(seconds)
    invoke = 0
    if seconds != 0:
        invoke = seconds
        seconds = int(time.time()) + seconds

    m.addMute(ctx.guild.id, player.id, seconds)
    if seconds == 0:
        seconds = "Никогда"
    else:
        seconds = datetime.fromtimestamp(seconds)
    from mute.previous import addRoles as archive
    from mute.translate import mute_given
    roleid_list = ""
    for role in player.roles:
        roleid_list += f"{role.id};"
        try:
            await player.remove_roles(role)
        except Exception:
            pass #прости меня, мой будующий я, мне лень делать иначе
    archive(ctx.guild.id, player.id, roleid_list)
    await addRoles(bot, ctx, player)
    embed = emb(bot, ctx, title=mute_given[lan].format(player, seconds))
    await ctx.reply(embed=embed)
    if seconds != 0:

        await asyncio.sleep(invoke)
        await unmute_system(bot, ctx.message, player)

async def addRoles(bot, ctx: Context, player: nextcord.Member):
    from mute import role_mute
    mute_list = role_mute.readRole(ctx.guild.id)
    if mute_list == None:

        role = await ctx.guild.create_role(name=f"{bot.user}-Mute", colour=nextcord.Colour.purple())
        role_mute.addRole(ctx.guild.id, role.id)
    role_id = role_mute.readRole(ctx.guild.id)
    role = ctx.guild.get_role(role_id[1])
    try:
        await player.add_roles(role)
    except AttributeError:
        role_mute.deleteRole(ctx.guild.id)
        role = await ctx.guild.create_role(name=f"{bot.user}-Mute", colour=nextcord.Colour.purple())
        role_mute.addRole(ctx.guild.id, role.id)
        await player.add_roles(role)