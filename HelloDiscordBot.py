import discord
from discord.ext import commands
from matcher import *

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
    target_phrase = "I'm crying"
    user_input = message.content.lower()

    # Check similarity using Levenshtein distance
    similarity = default_similarity(user_input, target_phrase)

    # Define a threshold for considering a match
    similarity_threshold = 0.8

    if similarity >= similarity_threshold:
        user_id = str(message.author.id)

        # Increment the count for the user or set it to 1 if it doesn't exist
        my_hashmap[user_id] = my_hashmap.get(user_id, 0) + 1


@client.command()
async def print_count(ctx):
    user_id = str(ctx.author.id)
    count = my_hashmap.get(user_id, 0)
    await ctx.send(f'This user {ctx.author.name} said Im crying {count} times')




# Run the bot
client.run('token')