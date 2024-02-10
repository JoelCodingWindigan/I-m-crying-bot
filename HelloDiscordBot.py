import discord
from discord.ext import commands

from matcher import *
from settings import BOT_TOKEN
from database import Database

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

# hashmap used to keep track of how often a user says hello world
my_hashmap = {}


@client.event
async def on_ready():
    print("The Bot is now ready for use! Booyah")
    


@client.event
async def on_message(message):
    #print(f"Message receoved: {message.content}")
    await count_message(message)
    await client.process_commands(message)


async def count_message(message):
    boolean = is_similar(message.content.lower(), ["im crying", "i am crying"])
    user_id = str(message.author.id)
    if boolean == True:
        my_hashmap[user_id] = my_hashmap.get(user_id, 0) + 1

        


@client.command()
async def print_count(ctx):
    user_id = str(ctx.author.id)
    count = my_hashmap.get(user_id, 0)
    await ctx.send(f'This user {ctx.author.name} said Im crying {count} times')




# Run the bot
client.run('MTE5OTc5MTM5OTk1Mjk3ODA2MA.GvrI0L.pwmEdvIVDauuCCTDnLDp_wQTq093ONbd0zrCAc')