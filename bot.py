import discord
import json
from discord.ext import commands
from cogs.chat_cog import ChatCog

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.config = config  # Make config available to cogs

# Load cogs
async def setup_hook():
    await bot.add_cog(ChatCog(bot))

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(config['DISCORD_TOKEN'])
