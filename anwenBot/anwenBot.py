#Anwen Bot
#Made by Aaron Ramsey (aaronramsey2000@gmail.com)

import os, random

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!') ##red is okay just pycharm doesnt like it


@bot.event
async def on_ready():
    print(
        f'{bot.user.name} has connected to Discord!'
    )

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise discord.DiscordException

@bot.command(name='hi', help='Says hi to you')
async def sayHello(ctx):
    sayingHello = [
        "Hi, I'm Anwen, lol",
        "Hey, I'm the Quartermaster's mascot for MSAGM Aber SSAGO",
        "Sup, its ya boy Anwen",
    ]
    response = random.choice(sayingHello)
    await ctx.send(response)

@bot.command(name='randomAberKit', help='Tells you a random pice of kit Aber SSAGO own')
async def randKit(ctx):
    items = ["Vango Beta 450 XL",
    "DECOMMISSIONED - Vango Beta 450",
    "Wynnster Europa 3XV",
    "Wynnster Cairn 2",
    "Eurohike 3 Man",
    "Icelandic",
    "Gas Lamp",
    "Coleman Electric Lamps",
    "Tent Repair Kit",
    "Head Torch",
    "Mallet",
    "Large Bag of Wooden Tent Pegs",
    "Grey Tarpaulin",
    "Vango Sleeping Bag",
    "Cheap Sleeping Bag",
    "Spare Pole",
    "230g Butane Canister",
    "Camp Table",
    "White Bucket",
    "Jamie Oliver Apron",
    "Tea Towel",
    "Plastic Cup",
    "Bowl",
    "Open Fire Kettle",
    "Hand Soap",
    "Billy Pans",
    "Colander",
    "Frying Pan",
    "Trangia",
    "Disposable Plates",
    "Disposable Cutlery",
    "Disposable Cups",
    "Washing Up Liquid",
    "Water Carrier",
    "Firelighters",
    "Cooking Utensils",
    "Matches and Lighter",
    "Cool Pack",
    "Jug",
    "Cooking Knives",
    "Chopping Boards",
    "First Aid Kit",
    "First Aid Kit Contents",
    "Burns Kit",
    "Space Hopper",
    "Frisbee",
    "Tennis Ball",
    "Board Games",
    "SSAGO Flag + Pole",
    "Welsh Flag",
    "Union Flag",
    "Red Box",
    "Green Box",
    "Carboard Box",
    "Blue Box",
    "Tool Box",
    "Presidents Box",
    "Craft Stars",
    "Craft Stuff",
    "Bags 4-9",
    "Raft/Flippers/Paddles",
    "SSAGO Files",
    "SSAGO Mascots",
    "Event Shelter + 3 Sides + Door Side"]
    response = "A random piece of kit aber has is: " + random.choice(items)
    await ctx.send(response)

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#
#     if message.content == 'lost':
#         response = "Phil lost me"
#         await message.channel.send(response)
#     elif message.content == 'raise-exception':
#         raise discord.DiscordException

bot.run(TOKEN)
