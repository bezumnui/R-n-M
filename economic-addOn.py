import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Context
from emb import emb
import config

def get_prefix(bot, ctx: Context):
    return config.getprefix(ctx.guild.id)


Intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=Intents, help_command=None)

@bot.command()
async def pay(ctx: Context, pay_to=None, money="0"):
    from economy import main as eco
    await eco.pay(bot, ctx, pay_to, money)

@bot.command()
async def money(ctx: Context):
    from economy import main as eco
    await eco.money(bot, ctx)

@bot.command()
async def job(ctx: Context, *command):
    from economy import main as eco
    await eco.job(bot,ctx)


@bot.event
async def on_ready():
    print("connected addOn as: ", bot.user)
    game = nextcord.Game("Eco addOn R'n'M")
    await bot.change_presence(status=nextcord.Status.idle, activity=game)

bot.run(token=config.config["eco"])
