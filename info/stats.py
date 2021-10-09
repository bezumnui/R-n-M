from nextcord import ButtonStyle
from nextcord.ui import Button

from info.translate import stats_translate
from emb import emb
from config import getlang
async def stats(bot, ctx):
    lan = getlang(ctx.guild.id)
    embed = emb(bot, ctx, title=stats_translate(ctx, 0)[lan])


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




