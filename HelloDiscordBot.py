import discord
from discord.ext import commands

from matcher import *
from settings import BOT_TOKEN
from database import Database

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

# hashmap used to keep track of how often a user says hello world
#my_hashmap = {}


@client.event
async def on_ready():
    print("The Bot is now ready for use! Booyah")
    my_hashmap = {}

    #this is in the event the bot crashed and we wanna recopy values from our database into our hashmap
    try:
        with Database("filename.sqlite3") as db:
            queries = db.fetchall()
        
        for row in queries:
            user_id = row[0]
            count = row[1]
            my_hashmap[user_id] = count
    except sqlite3.Error:
        print("Error retrieving values from the database")


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
    #call database function for increment_count
    if boolean == True:
        try:
            with Database(filename.sqlite3) as db:
                db.increment_count(user_id, my_hashmap.get(user_id))
        except sqlite3.error:
            pass
    


        


@client.command()
#not sure if we wanna print from the database i imagine query time will take longer, but ask Justin or Ethan
async def print_count(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
        #basically just prints the author's count if they forgot to give a user
    user_id = str(user.id)
    count = my_hashmap.get(user_id, 0)
    await ctx.send(f'This user {user.name} said Im crying {count} times')




# Run the bot
client.run('Token')