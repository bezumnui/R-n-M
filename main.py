print("import libraries...")
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Context
from emb import emb
import config
from config import getlang, getprefix
from admin.ReactRole.RRConfig import returByMessage
from admin.ReactRole import RRConfig
from info import help as help_cmd
from admin import prefix as admin_prefix
from admin import language as admin_language
from info import stats as info_stats
from admin import ReactRole
import info
import time
from admin.ReactRole import RRR, RRA, RRD
from warns import warn_config as w

print(f"Imported! ver: {nextcord.__version__}")
def get_prefix(bot, ctx: Context):

    return config.getprefix(ctx.guild.id)

Intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=Intents, help_command=None)

@bot.event
async def on_raw_reaction_add(payload: nextcord.RawReactionActionEvent):

    guild = await bot.fetch_guild(payload.guild_id)
    member = await guild.fetch_member(payload.member.id)

    for rolelis in RRConfig.returnrole(guild.id, payload.message_id, str(payload.emoji)):
        role = rolelis[1]
        role = guild.get_role(role)
        if rolelis[3] == "+":
            await member.add_roles(role)
        elif rolelis[3] == "-":
            await member.remove_roles(role)


@bot.event
async def on_raw_reaction_remove(payload: nextcord.RawReactionActionEvent):

    guild = await bot.fetch_guild(payload.guild_id)

    member = await guild.fetch_member(payload.user_id)

    for rolelis in RRConfig.returnrole(guild.id, payload.message_id, str(payload.emoji)):
        role = rolelis[1]
        role = guild.get_role(role)
        await member.remove_roles(role)

@bot.event
async def on_raw_message_delete(payload: nextcord.RawMessageDeleteEvent):
    guild = await bot.fetch_guild(payload.guild_id)
    if returByMessage(guild.id,  payload.message_id) != []:
        from admin.ReactRole.RRConfig import deletemessage
        deletemessage(guild.id,  payload.message_id)

@bot.command()
async def help(ctx: Context):
    await help_cmd.help_cmd(bot, ctx, get_prefix(bot, ctx))

@bot.command()
async def warn(ctx:Context, player: nextcord.Member=None, seconds="0", *reason):
    from warns import main as warn_cmd
    await warn_cmd.warn(bot, ctx, player, seconds, *reason)

@bot.command()
async def dewarn(ctx, player: nextcord.Member=None, num: int=None):
    from warns import main as warn_cmd
    await warn_cmd.dewarn(bot, ctx, player, num)

@bot.command()
async def warns(ctx, player: nextcord.Member=None):
    from warns import main as warn_cmd
    await warn_cmd.warns(bot, ctx, player)

@bot.command()
async def mute(ctx, player: nextcord.Member=None, seconds = "0"):
    from mute import main as mute_cmd
    await mute_cmd.mute(bot, ctx, player, seconds)

@bot.command()
async def unmute(ctx, player: nextcord.Member=None):
    from mute import main as mute_cmd
    await mute_cmd.unmute(bot, ctx, player)


@bot.command()
async def prefix(ctx: Context, p="0"):
    await admin_prefix.change_prefix(bot, ctx, p)

@bot.command()
async def lan(ctx: Context, lang="0"):
    await admin_language.language(bot, ctx, lang)

@bot.command()
async def stats(ctx: Context):

    await info_stats.stats(bot, ctx)

@bot.command()
async def botstats(ctx: Context):

    await info.botstats.botstats(bot, ctx)

#@bot.command()
async def weather(ctx: Context):
    from info import weather

@bot.command()
async def clear(ctx: Context, count=5):
    from admin import clear
    await clear.clear(bot, ctx, count)


@bot.command()
async def user(ctx: Context, member: nextcord.Member = None):
    from info import user
    if member == None:
        member = ctx.author
    await user.user(bot, ctx, member)

@bot.command()
async def RRAdd(ctx: Context, message_id: int = 0, emoji: str = None, role_id: int = 0, ra="+"):

    await RRA.ReactRole(bot, ctx, message_id, emoji,role_id, ra)

@bot.command()
async def RRRemove(ctx: Context, message_id: int = 0, emoji: str = None):

    await RRR.ReactRole(bot, ctx, message_id, emoji)

@bot.command()
async def RRDelete(ctx: Context, message_id: int = 0):

    await RRD.ReactRole(bot, ctx, message_id)

@bot.command()
async def kick(ctx: Context, player=None, *reason):
    lan = getlang(ctx.guild.id)
    try:
        import re
        player = re.sub(r'[<>@!]', '', player)
        player = await ctx.guild.fetch_member(int(player))
    except AttributeError:
        from admin.translate import kick_ussage
        return await ctx.reply(embed=emb(bot, ctx, kick_ussage[lan].format(get_prefix(bot, ctx))))
    if ctx.author.guild_permissions.kick_members == False or player.guild_permissions.administrator:
        from perm_error import perm_error

        await ctx.reply(embed=emb(bot, ctx, perm_error()[lan]))
        return
    try:
        reason = ' '.join(tups for tups in reason)

        await player.kick(reason=reason)

    except Exception as e:
        print(e)


@bot.command()
async def ban(ctx: Context, player: nextcord.Member = None, *reason):
    lan = getlang(ctx.guild.id)
    try:
        player.id
    except AttributeError:
        from admin.translate import ban_ussage
    if ctx.author.guild_permissions.kick_members == False or player.guild_permissions.administrator:
        from perm_error import perm_error
        await ctx.reply(embed=emb(bot, ctx, perm_error()[lan]))
        return
    try:
        reason = ' '.join(tups for tups in reason)

        await player.ban(reason=reason)
    except Exception as e:
        print(e)

async def test(ctx: Context):
    from mute import role_mute
    mute_list = role_mute.readRole(ctx.guild.id)

    if mute_list == None:

        role = await ctx.guild.create_role(name=f"{bot.user}-Mute", colour=nextcord.Colour.purple())
        role_mute.addRole(ctx.guild.id, role.id)

    role_id = role_mute.readRole(ctx.guild.id)
    role = ctx.guild.get_role(role_id[1])

    try:
        await ctx.author.add_roles(role)
    except AttributeError:
        role_mute.deleteRole(ctx.guild.id)
        role = await ctx.guild.create_role(name=f"{bot.user}-Mute", colour=nextcord.Colour.purple())
        role_mute.addRole(ctx.guild.id, role.id)
        await ctx.author.add_roles(role)

@bot.event
async def on_ready():
    print("connected as: ", bot.user)
    game = nextcord.Game("with your mom")
    await bot.change_presence(status=nextcord.Status.idle, activity=game)


@bot.event
async def on_message(message: nextcord.Message):
    async def checkwarn():
        author = message.author
        warns = w.readWarns(message.guild.id, author.id)
        for warn in warns:
            expried = warn[3]
            if expried == 0:
                continue
            elif int(expried) <= time.time():
                w.delWarnByReason(message.guild.id, message.author.id, warn[2])

    await checkwarn()
    await checkmute(message)


async def checkmute(message: nextcord.Message):
    from mute.mute_config import readMute
    rmute = readMute(message.guild.id, message.author.id)
    if rmute == [] or rmute == None:
        await bot.process_commands(message)
        return
    elif rmute[2] == 0:
        await message.delete()
        return
    elif int(time.time()) > rmute[2]:
        from mute.main import unmute_system
        await unmute_system(bot, message, message.author)
        await bot.process_commands(message)
        return
    else:
        await message.delete()

bot.run(token=config.config["dev_token2"])