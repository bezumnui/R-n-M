import nextcord
from nextcord.ext.commands import Context
from info.temperature import temperature

from emb import emb
from info.translate import stats_translate
from info.stats import getlang
async def botstats(bot: nextcord.ext.commands.Bot, ctx: Context):
    lan = getlang(ctx.guild.id)
    try:
        name = stats_translate(ctx, part=0)[lan]
    except IndexError:
        name = stats_translate(ctx, part=0)[0]

    embed = emb(bot, ctx, title=name)
    for message in stats_translate(ctx, part=1):
        try:
            name = message[0][lan]
        except IndexError:
            name = message[0][0]
        try:
            value = message[1][lan]
        except IndexError:
            value = message[1][0]

        embed.add_field(name=name, value=value, inline=False)

    msg = await ctx.reply(embed=embed)
