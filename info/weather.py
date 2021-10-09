from embtemplate import embtemplate
import nextcord
from parsers import get_wether
async def weather(bot, ctx, prefix):

    splits = ctx.message.content.split()

    try:
        city = splits[1]
        country = splits[2]
    except Exception:
        emb = embtemplate(bot, ctx, f"""**:x:Please check syntax: *{prefix}weather [city] [country]***""", nextcord.Colour.red())
        emb.set_footer(text="source code by maxutka ©")
        botmsg = await ctx.send(embed=emb)
        return

    author = ctx.message.author

    await ctx.send('Searching...')
    weather = get_wether(city, country)
    if weather != 'error':
        emb = embtemplate(bot, ctx, f"""***Weather:\n\n{weather}***""")
        emb.set_footer(text="source code by maxutka ©")
        botmsg = await ctx.send(embed=emb)

    else:
        emb = embtemplate(bot, ctx, f"""***:x:Nothing was found... :(***""", nextcord.Colour.red())
        emb.set_footer(text="source code by maxutka ©")
        botmsg = await ctx.send(embed=emb)
