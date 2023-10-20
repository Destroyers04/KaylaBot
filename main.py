import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#Shows bot is on
@bot.event
async def on_ready():
    cogs = ["response_cog", "music_cog"]
    bot.remove_command('help')
    for cog in cogs:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"{cog} loaded successfully!")
        except commands.ExtensionError as e:
            print(f"{cog} could not be loaded. [{e}]")
    channel = bot.get_channel(1162443923155865620)
    print(f'{bot.user} is now awake')
    await channel.send("Good morning!")

if __name__ == "__main__":
    bot.run("MTE2MzQ5MTQ2NTcwNDUyMTc3MA.GTo_UV.YIp5AZ__fM_Y8bHiaHT8W1_GU93IKT2LUCvu6M")