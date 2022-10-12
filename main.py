import discord
from discord.ext import commands

intent_used = discord.Intents.all()

prefixes = ["!", "/"]
bot = commands.Bot(command_prefix=prefixes, intents=intent_used)

TOKEN = "MTAyOTY2NjkwNTU0NTUwNjgzNg.GmdQ8e.00OmcdE-SeHYR2pjYkBxO4zomjqyM5_cyDERHU"

@bot.event
async def on_ready():
    print(f'Logged In')
    await bot.change_presence(activity=discord.Game('who knows what!'))
    print(f'Bot Id {bot.user.id}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() == 'how are you':
        await message.channel.send(f"I am doing great, {message.author}!")
    await bot.process_commands(message)

@bot.command()
async def say(ctx, message):
    await ctx.send(message)

bot.run(TOKEN)
