import nextcord
from info.temperature import temperature
from info.translate import emb_translate
from config import getlang
def emb(bot, ctx, title, col=nextcord.Colour.green()):

    emb = nextcord.Embed(title=title, colour=col)
    emb.set_thumbnail(url=bot.user.avatar.url)
    emb.set_author(name=f'{bot.user.name}: {temperature()}')
    try:
        lan = getlang(guild_id=ctx.guild.id)
    except IndexError:
        lan = 0
    footer = emb_translate(ctx, part=0)[lan]
    emb.set_footer(text=footer)
    return emb
