import discord
from discord.ext import commands
import os
from database import get_prefix_for_guild
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')


intents = discord.Intents.default()
intents.message_content = True


async def dynamic_prefix(bot, message):
return get_prefix_for_guild(str(message.guild.id))


bot = commands.Bot(command_prefix=dynamic_prefix, intents=intents)


@bot.event
async def on_ready():
print(f"Bot online: {bot.user}")


@bot.command()
async def ping(ctx):
await ctx.send("Pong!")


bot.run(BOT_TOKEN)
