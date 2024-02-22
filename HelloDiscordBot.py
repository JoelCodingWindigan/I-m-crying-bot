import discord
from discord.ext import commands

import sqlite3

from matcher import is_similar
from db.database import Database
from settings import BOT_TOKEN

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

# hashmap used to keep track of how often a user says hello world
my_hashmap = {}


@client.event
async def on_ready():
    print("The Bot is now ready for use! Booyah")

    #this is in the event the bot crashed and we wanna recopy values from our database into our hashmap
    try:
        with Database('db/counts.sqlite3') as db:
            
            db.execute("SELECT * FROM Crying")
            queries = db.fetchall()
        
            for row in queries:
                user_id = row[0]
                count = row[1]
                my_hashmap[user_id] = count
                #print(row)
    except sqlite3.Error as err:
        print("Error retrieving values from the database", err)


@client.event
async def on_message(message):
    #print(f"Message receoved: {message.content}")
    await count_message(message)
    await client.process_commands(message)


async def count_message(message):
    if not is_similar(message.content.lower(), ["im crying", "i am crying"]):
        return
        
    user_id = message.author.id
    my_hashmap[user_id] = my_hashmap.get(user_id, 0) + 1
    #call database function for increment_count
    try:
        with Database('db/counts.sqlite3') as db:
            db.increment_count(user_id, my_hashmap[user_id])
            db.execute("SELECT * FROM Crying")
            queries = db.fetchall()
        
            for row in queries:
                print(row)
            
    except sqlite3.Error as err:
        print("Error incrementing count", err)
    


        


@client.command()
#not sure if we wanna print from the database i imagine query time will take longer, but ask Justin or Ethan
async def print_count(ctx, user: discord.User = None):
    #basically just prints the author's count if they forgot to give a user
    if user is None:
        user = ctx.author
    count = my_hashmap.get(user.id, 0)
    await ctx.send(f'This user {user.name} said Im crying {count} times')




# Run the bot
client.run(BOT_TOKEN)