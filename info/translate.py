# 0 - en
# 1 - ru
import nextcord

from config import getlang, getprefix
def emb_translate(ctx, part): #p - prefix
    if part == 0:
        return [f"request from: {ctx.author}", f"запрос от: {ctx.author}"]
def help(p, part): #p - prefix
    if part == 0:
        return ["Help", "Помощь"]
    if part == 1:
        return [

            [f"**Bot prefix:** `{p}`", f"**Префикс:** `{p}`"],
            [f"You can change it by: **{p}prefix {{prefix}}**", f"Вы можете сменить его используя: **{p}prefix {{префикс}}**"],
            [f"You can also change the language by **{p}lan {{language}}** "],
        ]
    if part == 2:
        return [
            [[f"Info:", "Информация:"],
            [f"`{p}help` `{p}stats` `{p}user` `{p}botstats`"]],

            [[f"Administrate:", "Администрирование"],
            [f"`{p}clear` `{p}prefix`\n"
             f"`{p}RRAdd` `{p}RRRemove` `{p}RRDelete`\n"
             ]],
            [["Moderating:", "Модерирование:"],
             [f"`{p}warn` `{p}dewarn` `{p}warns`\n"
              f"`{p}mute` `{p}unmute`"]]

        ]

def stats_translate(ctx, part: int):
    voice_count = len(ctx.guild.text_channels)
    text_count = len(ctx.guild.voice_channels)
    created_at = ctx.guild.created_at
    member_count = ctx.guild.member_count
    owner = ctx.guild.owner

    if part == 0:
        return ["Server stats:", "Статистика сервера:"]
    if part == 1:
        e = ["<:voicechannel:875313262890217472>", "<:textchannel:875313263158628413>",
                 "<:shop:875313262735024188>", "<:members:875313262927970334>",
                 "<:moderatorcerified:875313262944722955>"]

        return [
            [[f"{e[0]}Voice channels count:", f"{e[0]}Голосовые каналы:"],
             [f"{voice_count} channels", f"{voice_count} каналов"]],

            [[f"{e[1]}Text channels count:", f"{e[1]}Текстовые каналы:"],
             [f"{text_count} channels", f"{voice_count} каналов"]],

            [[f"{e[2]}Created at:", f"{e[3]}Создан:"],
             [f"{created_at.strftime('%d %B %Y %H:%M:%S')}"]],

            [[f"{e[3]}Members count:", f"{e[3]}Участников:"],
             [f"{member_count} members", f"{member_count} учасников"]],

            [[f"{e[4]}Owner of the server:", f"{e[4]}Создатель сервера:"],
            [f"{owner}"]],
        ]

def user_translate(ctx, part, member: nextcord.Member):
    prefix = getprefix(ctx.guild.id)
    if part == 0:
        return ["User's info:", "Информация об игроке:"]

    if part == 1:

        return [
            f'''
            **User name:** {member}
            **Discord status:** {status_emoji(str(member.status))}
            **With Discord from:** {member.created_at.strftime("%d %B %Y %H:%M:%S")}
            **At the server from:** {member.joined_at.strftime("%d %B %Y %H:%M:%S")}
            **User id:** `{member.id}`''',

            f'''
            **Имя:** {member}
            **Статус:** {status_emoji(str(member.status))}
            **В дискорде с:** {member.created_at.strftime("%d %B %Y %H:%M:%S")}
            **На сервере с:** {member.joined_at.strftime("%d %B %Y %H:%M:%S")}
            **Айди:** `{member.id}`'''
        ]

    if part == 2:
        return [
            f":x:Error: check syntax: **{prefix}user [@mention]**",
            f":x:Ошибка: проверьте синтаксис: **{prefix}user [@участник]**"
        ]

    if part == 3:
        return [
            "**:x:Error: you can choose only until 3 users**",
            "**:x:Ошибка: Вы можете выбрать до 3 участников**"
        ]

def botstats(bot, part: int):
    if part == 1:
        return ["Bot stats:", "Статистика бота"]
    if part == 2:
        return [
            [["Servers, that have bot:", "Сервера, на которых стоит бот:"],
             [f"{len(bot.guilds)} servers", f"{len(bot.guilds)} серверов" ]],

            [["Count of player, that uses the bot:", "Количество пользователей:"],
             [f"{len(bot.users)} players", f"{len(bot.users)} игроков"]],

            [["Created at:", "Создан:"],
             ["1 Aug 2021", "1 Авг 2021"]],
            [["My batya:", "Мой батя"],
             ["<@{bot.owner_id}>"]]

        ]


def status_emoji(mode):
    if mode == "idle":
        return "<:idle:871732859080146996>"
    elif mode == "dnd":
        return "<:dnd:871732915439013949>"
    elif mode == "online":
        return "<:online:871732915669708880>"
    elif mode == "offline":
        return "<:offline:871732915845877760>"
    else:
        print(mode)
        return

