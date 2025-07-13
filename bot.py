# bot.py
import discord
from discord.ext import commands

import stream_monitor  # Import the full module, not just check_streams
from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True  # Needed if you plan to use text commands
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready!")
    stream_monitor.bot = bot  # Inject bot instance into stream_monitor
    stream_monitor.check_streams.start()


bot.run(DISCORD_TOKEN)
