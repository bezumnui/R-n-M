from admin.translate import languages_translate
from perm_error import perm_error
from emb import emb
from config import getlang, getprefix, setlang
async def language(bot, ctx, lan2: str):
    languages = ["en", "ru"]
    p = getprefix(ctx.guild.id)
    lan = getlang(guild_id=ctx.guild.id)
    if ctx.author.guild_permissions.ban_members == False:
        try:
            text = perm_error()[lan]
        except IndexError:
            text = perm_error()[0]
        return await ctx.reply(embed=emb(bot, ctx, title=text))
    if lan2 in languages:
        setlang(ctx.guild.id, lan2)
        lan = getlang(ctx.guild.id)
        try:
            text = languages_translate(p, part=3)[lan]
        except:
            text = languages_translate(p, part=3)[0]
        return await ctx.reply(embed=emb(bot, ctx, title=text))
    else:
        try:
            title = languages_translate(p, part=0)[lan]
        except IndexError:
            title = languages_translate(p, part=0)[0]
        embed = emb(bot, ctx, title=title)
        try:
            name = languages_translate(p, part=1)[lan]
        except IndexError:
            name = languages_translate(p, part=1)[0]
        text = ""
        values = languages_translate(p, part=2)


        for value in values:
            try:
                add = value
            except IndexError:
                add = value
            text += f"\n{add}"
        embed.add_field(name=name, value=text)
        return await ctx.reply(embed=embed)
