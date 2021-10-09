from info.translate import help
from emb import emb
from config import getlang

async def help_cmd(bot, ctx, p: str):
    lan = getlang(ctx.guild.id)
    embed = emb(bot, ctx, title=help(p, 0)[lan])
    description = ""
    for message in help(p, part=1):
        try:
            text = message[lan]
        except IndexError:
            text = message[0]
        description += f"\n{text}"
    embed.description = description

    for message in help(p, part=2):
        try:
            name = message[0][lan]
        except IndexError:
            name = message[0][0]
        try:
            value = message[1][lan]
        except IndexError:
            value = message[1][0]

        embed.add_field(name=name, value=value, inline=False)

    await ctx.reply(embed=embed)