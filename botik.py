import discord
from discord.ext import commands
import pickle
from discord.utils import get
import asyncio
from discord_components import DiscordComponents, Button, ButtonStyle
from datetime import datetime
import math
from parsers import get_wether
from parsers import hotline_parser
import psutil
import time
import os
import economyDiscord as economy
import random
import config
import languages
import mute as mutebase
if os.name == "posix":
    TOKEN = "ODAyMTA2OTU1MTMyMTc0MzQ2.YAqaUA.LCcHd5r4sQzzx9zf39KYTsyeZOc"
    here = os.path.dirname(os.path.abspath(__file__)) + "/data"
else:
    TOKEN = 'ODQwNDk3NDU4ODAzMTE0MDI2.YJZEQQ.1izdDkzRRDCOfu6refvD1Wid3Mw'  # Dev Token
    here = os.path.dirname(os.path.abspath(__file__)) + "\data"
intents = discord.Intents.all()
version = "0.65alpha"
temperature = ''


def get_prefix(client, message):
    if os.name != "posix":
        pass
        #return "$"  # Dev prefix
    return config.getprefix(int(message.guild.id))


bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None, owner_id=466620407114498048)


@bot.event
async def on_guild_join(guild):  # when the bot joins the guild
    config.setprefix(int(guild.id), "^")

@bot.event
async def on_member_join(member):  # when the bot joins the guild
    economy.addmember(member.guild.id, member.id)


@bot.event
async def on_guild_remove(guild):  # when the bot joins the guild
    with open(f'prefixes.pickle', "wb") as f:
        prefixes = pickle.load(f)

    prefixes.pop(str(guild.id))
    with open(f'prefixes.pickle', "wb") as f:
        pickle.dump(prefixes, f)


@bot.event
async def on_ready():
    print(f'Login as {bot.user} ({here}):')
    game = discord.Game(f"Mention me to help")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    DiscordComponents(bot)


@bot.event
async def on_raw_reaction_add(payload):
    try:
        user = bot.get_user(id=payload.user_id)
        guild = await bot.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(user.id)
        if user.bot == False:
            emoji = str(payload.emoji)

            message_id = payload.message_id
            r = readroles(payload.guild_id, message_id)
            id_role = int(r[emoji])

            role = guild.get_role(id_role)
            await member.add_roles(role)
    except Exception:
        pass


@bot.event
async def on_raw_reaction_remove(payload):
    try:
        emoji = str(payload.emoji)
        message_id = payload.message_id
        r = readroles(payload.guild_id, message_id)
        id_role = int(r[emoji])
        user = bot.get_user(id=payload.user_id)
        guild = await bot.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(user.id)
        if user.bot == False:
            role = guild.get_role(id_role)
            await member.remove_roles(role)
    except Exception:
        pass


@bot.command()
async def botstats(ctx):
    temperature_def()
    owner = ctx.guild.owner
    emb = discord.Embed(title="Bot stats", colour=discord.Colour.green())
    emb.set_author(name=f'{bot.user.name}: {temperature}')
    emb.set_footer(text=f'request from: {ctx.author}')
    emb.set_thumbnail(url=bot.user.avatar_url)
    emb.add_field(name=f"Servers, that have bot:\n",
                  value=f"{len(bot.guilds)} servers", inline=False)
    emb.add_field(name=f"Sum of player, that uses the bot:\n",
                  value=f"{len(bot.users)} players", inline=False)
    emb.add_field(name=f"Created at:\n",
                  value=f"1 Aug 2021", inline=False)
    emb.add_field(name=f"My creator\n",
                  value=f"<@{bot.owner_id}>", inline=False)

    msg = await ctx.reply(embed=emb)


@bot.command()
async def stats(ctx):
    temperature_def()
    prefix = get_prefix(bot, ctx)

    voice_count = len(ctx.guild.text_channels)
    text_count = len(ctx.guild.voice_channels)
    created_at = ctx.guild.created_at
    member_count = ctx.guild.member_count
    owner = ctx.guild.owner
    emb = discord.Embed(title="Server Stats", colour=discord.Colour.green())
    emb.set_author(name=f'{bot.user.name}: {temperature}')
    emb.set_footer(text=f'request from: {ctx.author}')
    emb.set_thumbnail(url=bot.user.avatar_url)
    emb.add_field(name=f"Voice channels count:\n",
                  value=f"{voice_count} channels", inline=False)
    emb.add_field(name=f"Text channels count:\n",
                  value=f"{text_count} channels", inline=False)
    emb.add_field(name=f"Created at:\n",
                  value=f"{created_at.strftime('%d %B %Y %H:%M:%S')}", inline=False)
    emb.add_field(name=f"Members count\n",
                  value=f"{member_count} members", inline=False)
    emb.add_field(name=f"Owner of the server: \n",
                  value=f"{owner}")
    msg = await ctx.reply(embed=emb)


@bot.command()
async def RRA(ctx):
    try:
        content = ctx.message.content.split()
        message_id = content[1]
        emoji = content[2]
        role = content[3]
    except Exception:
        prefix = get_prefix(bot, ctx)
        await ctx.reply(f":x:**Check syntax:** *{prefix}RRA [message id] [emoji] [role]*")
        return
    if ctx.author.guild_permissions.administrator or int(ctx.author.id) == int(bot.owner_id):
        await ReactRoleAdd(ctx, message_id, emoji, role)

    else:
        await ctx.message.reply(":x:**You have no perm to do that**")


@bot.command()
async def RRR(ctx):
    try:
        content = ctx.message.content.split()
        message_id = content[1]
        emoji = content[2]
    except Exception:
        prefix = get_prefix(bot, ctx)
        await ctx.reply(f":x:**Check syntax:** *{prefix}RRR [message id] [emoji]*")
        return
    if ctx.author.guild_permissions.administrator or int(ctx.author.id) == int(bot.owner_id):
        await ReactRoleRemove(ctx, message_id, emoji)

    else:
        await ctx.message.reply(":x:**You have no perm to do that**")


@bot.command()
async def RRD(ctx):
    try:
        content = ctx.message.content.split()
        message_id = content[1]
    except Exception:
        prefix = get_prefix(bot, ctx)
        await ctx.reply(f":x:**Check syntax:** *{prefix}RRA [message id]*")
        return
    if ctx.author.guild_permissions.administrator or int(ctx.author.id) == int(bot.owner_id):
        await ReactRoleDelete(ctx, message_id)

    else:
        await ctx.message.reply(":x:**You have no perm to do that**")


async def ReactRoleCreate(ctx, message_id):
    if ctx.author.guild_permissions.administrator == False and int(ctx.author.id) != int(bot.owner_id):
        return
    try:
        await ctx.fetch_message(message_id)

    except Exception:
        # prefix = get_prefix(bot, ctx)
        # await ctx.reply(f":x:**Check syntax:** *{prefix}RRC [message id] **(MESSAGE MUST BE AT THE SAME CHANNEl)***")

        return
        # Check permissions
    data = {
        "message_id": message_id,
    }

    writeroles(data, ctx.guild.id, message_id)
    prefix = get_prefix(bot, ctx)
    # await ctx.send(f"**Okay, now let's add new roles by {prefix}RRA**")


async def ReactRoleAdd(ctx, message_id, emoji, role):
    if ctx.author.guild_permissions.administrator == False and int(ctx.author.id) != int(bot.owner_id):
        return
    if True:  # Check permissions
        try:

            readroles(ctx.guild.id, message_id)
        except Exception:

            await ReactRoleCreate(ctx, message_id)
        try:

            await ctx.fetch_message(message_id)

        except Exception:
            prefix = get_prefix(bot, ctx)
            await ctx.reply(
                f":x:**Check syntax:** *{prefix}RRA [message id] [emoji] [role] **MESSAGE MUST BE AT THE SAME CHANNEl***")
            return

        try:
            rolecheck = ctx.guild.get_role(int(role))
            member = await ctx.guild.fetch_member(bot.user.id)
            await member.add_roles(rolecheck)
            await member.remove_roles(rolecheck)

        except Exception as ex:

            prefix = get_prefix(bot, ctx)
            await ctx.reply(
                f":x:**Invalid role or bot have no permissions**")
            return
        data = {
            emoji: role,
        }

        message = await ctx.fetch_message(message_id)
        try:
            addroles(data, ctx.guild.id, message_id)
            await message.add_reaction(emoji)
            await ctx.message.add_reaction("✅")
            await ctx.message.delete(delay=5)
        except Exception as ex:

            await ctx.reply(f"Something went wrong: {ex}")


async def ReactRoleRemove(ctx, message_id, emoji):
    if ctx.author.guild_permissions.administrator == False and int(ctx.author.id) != int(bot.owner_id):
        return
    if True:  # Check permissions
        # r.pop(str(emoji))
        try:
            r = readroles(ctx.guild.id, message_id)
            r.pop(str(emoji))
        except Exception:
            await ctx.send(":x:**Invalid message id or emoji**")
            return
        with open(os.path.join(here, f'{ctx.guild.id}_{message_id}.pickle'), "wb") as f:
            data = r
            pickle.dump(data, f)
            msg = await ctx.fetch_message(message_id)
            await msg.clear_reaction(emoji)
        await ctx.message.add_reaction("✅")
        await ctx.message.delete(delay=5)


@bot.command()
async def ReactRoleDelete(ctx, message_id):
    if ctx.author.guild_permissions.administrator == False and int(ctx.author.id) != int(bot.owner_id):
        return
    if True:  # Check permissions

        try:
            r = readroles(ctx.guild.id, message_id)
        except Exception as r:
            await ctx.send(":x:**Invalid message id**")
            return

        os.remove(os.path.join(here, f'{ctx.guild.id}_{message_id}.pickle'))
        msg = await ctx.fetch_message(message_id)
        for emoji in msg.reactions:
            await msg.clear_reaction(emoji)
        await ctx.message.add_reaction("✅")
        await ctx.message.delete(delay=5)


@bot.command(pass_context=True)
# ensure that only administrators can use this command
async def guildlist(ctx):
    if ctx.author.id != bot.owner_id:
        return
    else:
        for i in bot.guilds:
            await ctx.author.send(f"{i} - {i.icon_url}")


@bot.command()
async def prefix(ctx):
    try:
        content = ctx.message.content.split()
        prefix = content[1]
    except Exception:
        await ctx.reply(f":x:**Please, check the syntax**: {get_prefix(bot, ctx)}prefix [prefix]**")
    if ctx.author.guild_permissions.administrator or int(ctx.author.id) == int(bot.owner_id):
        config.setprefix(int(ctx.guild.id), prefix)
        await ctx.message.add_reaction("✅")
        await ctx.send(f'Prefix changed to: {prefix}')  # confirms the prefix it's been changed to
        # next step completely optional: changes bot nickname to also have prefix in the nickname
        name = f'{prefix}BotBot'


@bot.command()
async def price(ctx, *product):
    author = ctx.message.author
    temperature_def()
    await ctx.send('Search...')
    hs_clean = (" ".join(product))
    hs = hotline_parser(hs_clean)
    if hs != 'error':

        emb = embtemplate(ctx,
                          f'{hs}',
                          discord.Colour.orange())
        msg = await ctx.reply(embed=emb)

    else:
        emb = embtemplate(ctx,
                          f':x:**Something went error...**',
                          discord.Colour.orange())
        msg = await ctx.reply(embed=emb)



@bot.command()
async def help(ctx):
    lang = config.getlang(int(ctx.guild.id)) #0 - en, 1 - ru
    try:
        splited = ctx.content.split()
    except Exception:
        splited = ctx.message.content.split()
    prefix = get_prefix(bot, ctx)
    temperature_def()
    try:
        if splited[1] == "info":
            emb = embtemplate(ctx, title=f"help info")
            help_info = languages.help_info
            for field in help_info:
                value = help_info[field]
                emb.add_field(name=f"{prefix}{field}", value=value[lang], inline=False)
            await ctx.reply(embed = emb)
            return

        elif splited[1] == "admin":
            emb = embtemplate(ctx, title=f"help admin")
            help_admin = languages.help_admin
            for field in help_admin:
                value = help_admin[field]
                emb.add_field(name=f"{prefix}{field}", value=value[lang], inline=False)
            await ctx.reply(embed=emb)
            return

        elif splited[1] == "eco":
            emb = embtemplate(ctx, title=f"help eco")
            help_eco = languages.help_eco
            for field in help_eco:
                value = help_eco[field]
                emb.add_field(name=f"{prefix}{field}", value=value[lang], inline=False)
            await ctx.reply(embed=emb)
            return

    except Exception:
        pass
    emb = embtemplate(ctx, title=f"help")
    help_main = languages.help_main
    for field in help_main:
        description = [f"**The prefix is {prefix}** \n You can change it by **{prefix}prefix [prefix]**", f"**Префикс: {prefix}**\n Вы можете сменить его используя **{prefix}prefix [prefix]**"]
        name = help_main[field]
        emb.add_field(name=f"{prefix}{name[lang]}", value=field.replace("^", prefix), inline=False)
    emb.description = description[lang]
    await ctx.reply(embed=emb)
    return


@bot.command()
async def language(ctx):
    if ctx.author.guild_permissions.administrator == False and ctx.author != bot.owner_id:
        #emb = embtemplate(ctx, )
        return
    content = ctx.message.content.split()
    lang = config.getlang(ctx.guild.id)
    prefix = get_prefix(bot, ctx)
    lans = ("en", "ru")
    messages = languages.language
    try:
        if content[1] not in lans:
            emb = embtemplate(ctx, f"{messages[0][lang]} \n**{lans}**", discord.Colour.red())
            await ctx.send(embed=emb)
            return
        config.setlang(ctx.guild.id, content[1])
        lang = config.getlang(ctx.guild.id)
        emb = embtemplate(ctx, f"{messages[2][lang]}")
        await ctx.send(embed=emb)
        return
    except Exception:
        emb = embtemplate(ctx, f"{messages[1][lang].replace('^', prefix)}", discord.Colour.red())
        await ctx.send(embed=emb)
@bot.command()
async def mute(ctx):
    prefix = get_prefix(bot, ctx)
    lang = config.getlang(int(ctx.guild.id))
    messages = languages.mute
    try:
        muting = ctx.message.mentions[0]
    except Exception:
        emb = embtemplate(ctx,
                          messages[0][lang].replace("^", prefix),
                          discord.Colour.red())
        msg = await ctx.reply(embed=emb)
        await msg.delete(delay=5)
        return
    if muting.bot:
        await ctx.message.add_reaction("❌")
        emb = embtemplate(ctx,
                          messages[1][lang].replace("^", prefix),
                          discord.Colour.red())
        msg = await ctx.reply(embed=emb)
        return
    elif muting.guild_permissions.administrator:
        await ctx.message.add_reaction("❌")
        emb = embtemplate(ctx,
                          messages[2][lang].replace("^", prefix),
                          discord.Colour.red())
        msg = await ctx.reply(embed=emb)
        return
    author = ctx.author
    cont_split = ctx.message.content.split()
    seconds = 0
    if cont_split[1].isdigit():
        seconds = cont_split[1]
    prefix = get_prefix(bot, ctx)
    if author.guild_permissions.mute_members:
        muterole_id = readmuterole(server_id=ctx.guild.id)
        if True:

            muting_roles = muting.roles
            for i in muting_roles:
                if i.id == muterole_id:
                    await ctx.message.add_reaction("❌")
                    emb = embtemplate(ctx,
                                      messages[3][lang].replace("^", prefix),
                                      discord.Colour.red())
                    msg = await ctx.reply(embed=emb)
                    await msg.delete(delay=10)
                    return
            try:
                await muting.add_roles(ctx.guild.get_role(int(muterole_id)))
            except Exception:
                emb = embtemplate(ctx,
                                  messages[4][lang].replace("^", prefix),
                                  discord.Colour.orange())
                msg = await ctx.reply(embed=emb)
                await msg.delete(delay=5)

            if time == 0:
                if add_mute_member(ctx.guild.id, muting.id, 0) == 0:
                    await ctx.message.add_reaction("✅")
                else:
                    await ctx.message.add_reaction("❌")
                    emb = embtemplate(ctx,
                                      messages[3][lang].replace("^", prefix),
                                      discord.Colour.red())
                    await ctx.reply(embed=emb)
                    return

            else:
                if add_mute_member(ctx.guild.id, muting.id, 0) == 0:
                    add_mute_member(ctx.guild.id, muting.id, int(time.time()) + int(seconds))
                    emb = embtemplate(ctx,
                                      messages[5][lang].replace("^", prefix).replace("{muting}", muting).replace("{seconds}", seconds),
                                      discord.Colour.orange())
                    msg = await ctx.reply(embed=emb)
                    await ctx.message.add_reaction("✅")
                    return
                else:
                    await ctx.message.add_reaction("❌")
                    emb = embtemplate(ctx,
                                      messages[3][lang].replace("^", prefix),
                                      discord.Colour.red())
                    await ctx.reply(embed = emb)
                    return

    else:
        await ctx.message.add_reaction("❌")
        emb = embtemplate(ctx, messages[5][lang].replace("^", prefix))
        msg = await ctx.reply(f":x:***You have no permissions!***")
        await msg.delete(delay=5)


@bot.command()
async def unmute(ctx):
    prefix = get_prefix(bot, ctx)
    try:
        muting = ctx.message.mentions[0]
    except Exception:
        emb = embtemplate(ctx, f':x:Usage:\n**{prefix}unmute [@user]**\n***DO NOT COPPY USER MENTION, HAND-WRITE ONLY!***', discord.Colour.red())
        msg = await ctx.reply(embed=emb)
        await msg.delete(delay=5)
        return

    author = ctx.author
    prefix = get_prefix(bot, ctx)
    if author.guild_permissions.mute_members:
        muterole_id = readmuterole(server_id=ctx.guild.id)
        if muterole_id == 0:
            emb = embtemplate(ctx,
                              f'❓***Recommendation: setup visual mute role by {prefix}addmuterole [role_id]***',
                              discord.Colour.orange())
            msg = await ctx.reply(embed=emb)
            await msg.delete(delay=5)
        muterole = ctx.guild.get_role(int(muterole_id))

        try:
            if mute_remove(ctx.guild.id, muterole.id) == 1:
                emb = embtemplate(ctx, f"Member was not muted", discord.Colour.red())
                await ctx.reply(embed=emb)
                return
        except Exception:
            pass
        try:

            await muting.remove_roles(muterole)

        except Exception:
            pass

        mutebase.deleteplayer(ctx.guild.id, muting.id)
        await ctx.message.add_reaction("✅")
        return


    else:
        await ctx.message.add_reaction("❌")
        emb = embtemplate(ctx,
                          f':x:***You have no permissions!***',
                          discord.Colour.red())
        msg = await ctx.reply(ember=emb)
        await msg.delete(delay=5)


@bot.command()
async def info(ctx):
    prefix = get_prefix(bot, ctx)
    emb = discord.Embed(title="Bot's info", colour=discord.Colour.green())
    emb.set_thumbnail(url=bot.user.avatar_url)
    emb.set_author(name=f'{bot.user.name}: {temperature}')
    emb.set_footer(text=f'request from: {ctx.author}')

    emb.add_field(name="Hello discord!", value='''My name is R'n'M, cause... cause
    my creator loves this cartoon? maybe.. :slight_smile: My creator so fkin retarded,
    so... don't worry if something is going not as well, as u want, but anyway
    he have the mail (gmdevelopersstudio@gmail.com)''')
    emb.add_field(inline=False, name="Bot version:", value=version)

    msg = await ctx.reply(embed=emb, components=[
        Button(style=ButtonStyle.URL, emoji="📧", label="Mail", url="https://mail.google.com/mail")
    ])
    response = await bot.wait_for("button_click")
    if response.message.id == msg.id:
        if response.author == ctx.author:
            # if response.component.label == "Ok, thanks":
            await msg.delete()
    await msg.delete(delay=3600)


@bot.command()
async def user(ctx):
    i = 0
    try:
        ctx.message.content.split()[1]
    except Exception:
        prefix = get_prefix(bot, ctx)
        await ctx.send(f"**:x:Error: check syntax:** *{prefix} [@mention]*")
    temperature_def()
    if len(ctx.message.mentions) <= 3:
        for user in ctx.message.mentions:
            status = user.status
            emb = discord.Embed(title=f"{user.name}'s info", colour=discord.Colour.green())
            emb.set_thumbnail(url=user.avatar_url)
            emb.add_field(inline=False, name="**Main information:**\n", value=f'''

            **User name:** {user}
**Discord status:** {status_emoji(str(status))}
**With Discord from:** {user.created_at.strftime("%d %B %Y %H:%M:%S")}
**User name:** {user.joined_at.strftime("%d %B %Y %H:%M:%S")}
**User id:** `{user.id}`''')

            emb.set_footer(text=f"request: {ctx.author}")
            emb.set_author(name="R'n'M")
            await ctx.send(embed=emb)
    else:
        await ctx.send("**:x:Error: you can choose only until 3 users**")


@bot.command()
async def addmuterole(ctx):
    cont_split = ctx.message.content.split()
    server_id = ctx.guild.id

    role_id = cont_split[1]
    with open("mute_role.pickle", "rb") as f:
        try:
            data = pickle.load(f)
        except Exception:
            data = {}
    try:
        data.pop(server_id)
    except Exception:
        pass
    data[server_id] = role_id
    with open('mute_role.pickle', "wb") as f:
        pickle.dump(data, f)


def readmuterole(server_id):
    with open("mute_role.pickle", "rb") as f:
        data = pickle.load(f)
        try:
            muterole = data[server_id]
            return muterole
        except Exception:
            return 0


def status_emoji(mode):
    if mode == "idle":
        return "<:idle:871732859080146996>inactive"
    elif mode == "dnd":
        return "<:dnd:871732915439013949>do not disturb"
    elif mode == "online":
        return "<:online:871732915669708880>online"
    elif mode == "offline":
        return "<:offline:871732915845877760>offline"
    else:
        print(mode)
        return


@bot.command()
async def getemoji(ctx):
    emojis = ctx.guild.emojis
    for emoji in emojis:
        await ctx.send(f"{emoji} - {emoji.id}")


@bot.command()
async def getid(ctx):
    await ctx.send(ctx.guild.id)


@bot.command()
async def cancelanarhy(ctx):
    adminrole = 794249074399772712
    members = ctx.guild.members
    role = ctx.guild.get_role(adminrole)
    for member in members:
        await member.remove_roles(role)
        print(f"У {member} забрали роль {role}")


@bot.command()
async def clear(ctx, count=10):
    if ctx.author.guild_permissions.administrator or int(ctx.author.id) == int(bot.owner_id):
        if count > 100:
            if ctx.author.guild_permissions.administrator == False and int(ctx.author.id) != int(bot.owner_id):
                msg = await ctx.reply("*Error: you have no perms to delete more than 100 messages*")
                msg.delete(5)
                return

        msg = await ctx.reply("*Starting clean...*")
        deleted = await ctx.channel.purge(limit=count)
        msg = await ctx.send(f"**Bot finished cleaning with {len(deleted)} deleted messages!**")
        await msg.delete(delay=10)


def writeroles(data, server_id, message_id):
    with open(os.path.join(here, f'{server_id}_{message_id}.pickle'), "wb") as f:
        try:

            pickle.dump(obj=data, file=f)
        except Exception as ex:
            print(ex)


def addroles(data, server_id, message_id):
    oldData = readroles(server_id, message_id)
    with open(os.path.join(here, f'{server_id}_{message_id}.pickle'), "wb") as f:
        data.update(oldData)
        pickle.dump(data, f)

    return "ok"


def readroles(server_id, message_id):
    with open(os.path.join(here, f'{server_id}_{message_id}.pickle'), 'rb') as f:
        return pickle.load(f)




inChannelMute = []


@bot.event
async def on_voice_state_update(member, before, after):
    if (member in inChannelMute) == False:
        muterole_id = readmuterole(member.guild.id)
        muting_roles = member.roles

        for i in muting_roles:
            if i.id == muterole_id:
                await member.edit(mute=True)


@bot.command()
async def sendembed(ctx):
    temperature_def()
    print(ctx.author.id, bot.owner_id)
    if ctx.author.guild_permissions.administrator == False and int(ctx.author.id) != int(bot.owner_id):
        emb = discord.Embed(title=':x:**You have no permissions**', color=discord.Colour.red())
        botmsg = await ctx.send(embed=emb)
        return

    text = ctx.message.content.split()
    channel_id = text[1]
    prefix = get_prefix(bot, ctx)
    try:
        channel = ctx.guild.get_channel(int(channel_id))
        if channel == None:
            await ctx.reply(f":x:**Please check the syntax**: {prefix}sendembed [channel id]")
            return
    except Exception:
        await ctx.reply(f":x:**Please check the syntax**: {prefix}sendembed [channel id]")
        return
    await ctx.reply("**Choose name for the Embed:**")
    label = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    embed = discord.Embed(title=label.content)
    embed.set_author(name="R'n'M")

    await ctx.reply("**Type the Embed description (0 - stay empty)**:")
    description = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    if description != 0:
        embed.description = description.content
    await ctx.reply("**Type the filed name**:")
    name_field = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    await ctx.reply(f"**Type the field value**:")
    value_field = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    await ctx.reply(f"**Inline? (Y/n)**")
    inLine = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    if inLine.content.lower() == "n":
        embed.add_field(name=name_field.content, value=value_field.content, inline=True)
    else:
        embed.add_field(name=name_field.content, value=value_field.content, inline=False)
    await ctx.send(f"**You can also adding new field until you type *0*** ")
    for i in range(100):
        await ctx.reply("**Type the filed name *(0 - finish)*:**")
        name_field = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
        if name_field.content == "0":
            break
        await ctx.reply(f"**Type the field value**:")
        value_field = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
        await ctx.reply(f"**Inline? (Y/n)**")
        inLine = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
        if inLine.content.lower() == "n":
            embed.add_field(name=name_field.content, value=value_field.content, inline=True)
        else:
            embed.add_field(name=name_field.content, value=value_field.content, inline=False)

    await ctx.reply(f"**Nice! Now time to footer, type it:**")
    footer = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    embed.set_footer(text=footer.content)

    await ctx.reply(f"**You want to add the right-side image? *y/N*:**")
    answer = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    if answer.content.lower() == "y":
        await ctx.reply(f"**Drop the photo, please:**")
        try:
            photo = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
            embed.set_thumbnail(url=photo.attachments[0].url)
        except Exception():
            await ctx.reply(":x:**Something went error**")

    await ctx.reply(f"**You want to add the bottom-side image? *y/N*:**")
    answer = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    if answer.content.lower() == "y":
        await ctx.reply(f"**Drop the photo, please:**")
        try:
            photo = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
            embed.set_image(url=photo.attachments[0].url)
        except Exception():
            await ctx.reply(":x:**Something went error**")

    await ctx.reply(f"**Choose the color using RGB, example: 10 250 65:**")
    try:
        RGB = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
        R_G_B = RGB.content.split()
        r = int(R_G_B[0])
        g = int(R_G_B[1])
        b = int(R_G_B[2])
        embed.colour = discord.Colour.from_rgb(r, g, b)

    except Exception:
        await ctx.reply(f"**Something went error, color will have default color:**")
        embed.colour = discord.Colour.green()

    await ctx.send(embed=embed)
    await ctx.send(f"**Message will look same. Send it to the {channel}? y/N**")
    issend = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    try:
        if issend.content.lower() == "y":
            await channel.send(embed=embed)
        else:
            await ctx.send("**Action was canceled**")
    except Exception:
        await ctx.send("**:x:Something went wrong!**")


@bot.command()
async def weather(ctx):
    prefix = get_prefix(bot, ctx)
    splits = ctx.message.content.split()

    try:
        city = splits[1]
        country = splits[2]
    except Exception:
        emb = embtemplate(ctx, f"""**:x:Please check syntax: *{prefix}weather [city] [country]***""", discord.Colour.red())
        emb.set_footer(text="source code by maxutka ©")
        botmsg = await ctx.send(embed=emb)
        return

    author = ctx.message.author
    temperature_def()
    await ctx.send('Searching...')
    weather = get_wether(city, country)
    if weather != 'error':
        emb = embtemplate(ctx, f"""***Weather:\n\n{weather}***""")
        emb.set_footer(text="source code by maxutka ©")
        botmsg = await ctx.send(embed=emb)

    else:
        emb = embtemplate(ctx, f"""***:x:Nothing was found... :(***""", discord.Colour.red())
        emb.set_footer(text="source code by maxutka ©")
        botmsg = await ctx.send(embed=emb)


def temperature_def():
    global temperature
    try:
        temps = psutil.sensors_temperatures()
        for name, entries in temps.items():
            for entry in entries:
                a = ("%.1f" % entry.current)
                temperature = (f"{a}°C")
    except Exception:
        temperature = (f"0°C")


@bot.event
async def on_message(message):
    try:
        members = mutebase.checktime(message.guild.id)
        for member in members:
            mutebase.deleteplayer(message.guild.id, member)
    except Exception:
        pass
    if message.author.bot == False:
        async def mute_check():
            if mutebase.checkmute(message.guild.id, message.author.id) == None:
                await bot.process_commands(message)
            else:
                if mutebase.checkmute(message.guild.id, message.author.id) != 0:
                    emb = embtemplate(message, f"YOU HAVE MUTED AT {mutebase.checkmute(message.guild.id, message.author.id)} seconds")
                else:
                    emb = embtemplate(message, f"YOU HAVE PERMAMENT MUTED")
                await message.author.send(embed=emb)
                await message.delete()
                return


        await mute_check()

        if bot.user.mentioned_in(message):
            content_split = message.content.split()
            try:
                content_split[1]
            except Exception:
                await help(ctx=message)


def add_mute_member(guild_id: int, user_id: int, expried = 0):
    data = {f'{guild_id}{user_id}': expried}
    if mutebase.checkmute(int(guild_id), int(user_id)) == None:
        mutebase.addmute(guild_id, user_id, expried)
        return 0

def mute_expried(guild_id):
    members = mutebase.checktime(guild_id)




def mute_remove(guild_id, user_id):
    if mutebase.checkmute(guild_id, user_id) == 0:
        mutebase.deleteplayer(guild_id, user_id)
    else:
        return 1


@bot.command()
async def setupEco(ctx):

    emb = embtemplate(ctx, "Setup")
    if ctx.author.guild_permissions.administrator == False and ctx.author.id != bot.owner_id:
        emb = embtemplate(ctx, """***You have no permissions!***""", discord.Colour.orange())
        await ctx.reply(embed=emb)
        return

    emb = embtemplate(ctx, """***LAST CONFIG WILL BE DELETED!***
    **Are you sure, that you want to setup economy at the server? y/N**
    """)
    await ctx.reply(embed=emb)
    ans = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    if ans.content.lower() != "y":
        emb = embtemplate(ctx, "Setup was canceled", discord.Colour.red())
        await ctx.reply(embed=emb)
        return

    members = []
    for i in ctx.guild.members:
        members.append(i.id)

    economy.createEconomy(ctx.guild.id, members)

    emb = embtemplate(ctx, """**Setup of the server was Successful!**""")
    await ctx.reply(embed=emb)

@bot.command()
async def job(ctx):
    payday = random.randint(1, 6)
    economy.pay(ctx.guild.id, ctx.author.id, payday)
    emb = embtemplate(ctx, f"""**Your payday: *${payday}* **""")
    await ctx.reply(embed=emb)


@bot.command()
async def money(ctx):
    count = economy.getMoney(ctx.guild.id, ctx.author.id)
    emb = embtemplate(ctx, f"""**Your wallet: *${count}***""")
    await ctx.reply(embed=emb)

@bot.command()
async def pay(ctx):
    prefix = get_prefix(bot, ctx)
    try:
        member = ctx.message.mentions[0]
        if member == ctx.author or member.bot:
            emb = embtemplate(ctx, f"""**Check syntax:** *{prefix}pay **[@mention] [count]***""", discord.Colour.red())
            await ctx.reply(embed=emb)
            return
        content = ctx.message.content.split()
        pay_count = int(content[2])
    except Exception as ex:
        emb = embtemplate(ctx, f"""**Check syntax:** *{prefix}pay **[@mention] [count]***""", discord.Colour.red())
        await ctx.reply(embed=emb)
        return


    trans = economy.send(ctx.guild.id, member.id, ctx.author.id, pay_count)
    if trans == 1:
        emb = embtemplate(ctx, f"""***Failed! Not enough money!***""", discord.Colour.red())
        await ctx.reply(embed=emb)
    elif trans == 0:
        count = economy.getMoney(ctx.guild.id, ctx.author.id)
        emb = embtemplate(ctx, f"""***Success! You have paid ${pay_count} to {member}***\n **Now your wallet have ${count}**""")
        await ctx.reply(embed=emb)

def embtemplate(ctx, title, col=discord.Colour.green()):
    temperature_def()
    emb = discord.Embed(title=title, colour=col)

    emb.set_thumbnail(url=bot.user.avatar_url)
    emb.set_author(name=f'{bot.user.name}: {temperature}')
    emb.set_footer(text=f'request from: {ctx.author}')
    return emb
bot.run(TOKEN)