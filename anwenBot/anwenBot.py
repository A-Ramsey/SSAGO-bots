#Anwen Bot
#Made by Aaron Ramsey (aaronramsey2000@gmail.com)
#bot id: 690257560531763204

import os, random

import discord
import psycopg2 as psycopg2
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PORT = os.getenv('DATABASE_PORT')

bot = commands.Bot(command_prefix=commands.when_mentioned) ##red is okay just pycharm doesnt like it

atPhil = 0
phil = ["<@353993682841763840>", "Phil"]


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
        "Hi, I'm Anwen",
        "Hey, I'm the Quartermaster's mascot for MSAGM Aber SSAGO",
        "Sup, its ya boy Anwen",
    ]
    response = random.choice(sayingHello)
    await ctx.send(response)

def addToDB(id, scoreAdj):
    print("in add to db")
    conn = psycopg2.connect(host=DATABASE_HOST, database=DATABASE_NAME, user=DATABASE_USERNAME, password=DATABASE_PASSWORD, port=int(DATABASE_PORT))
    curr = conn.cursor()
    print(curr.execute("SELECT * WHERE id = %s", str(id)))


def personWin(perGuess, botGuess):
    if (perGuess == "r" and botGuess == "s") or (perGuess == "s" and botGuess == "p") or (perGuess == "p" and botGuess == "r"):
        return 1
    elif (perGuess == "s" and botGuess == "r") or (perGuess == "p" and botGuess == "s") or (perGuess == "r" and botGuess == "p"):
        return -1
    elif (perGuess == "s" and botGuess == "s") or (perGuess == "p" and botGuess == "p") or (perGuess == "r" and botGuess == "r"):
        return 0
    else:
        return -99

def addGuess(guess, bot, uid):
    response = ""
    if bot:
        response += "I"
    else:
        response += "<@" + str(uid) +">"
    response += " guessed "
    if guess == "r":
        response += "rock"
    elif guess == "p":
        response += "paper"
    elif guess == "s":
        response += "scissors"
    else:
        response += "an invalid guess"
    response += ". "
    return response

def rps(ctx, guess: str):
    print (ctx.author.id)
    rpsGuesses = ["r", "p", "s"]
    guess = guess.lower()
    botGuess = random.choice(rpsGuesses)
    response = ""
    if guess == "rock":
        guess = "r"
    elif guess == "paper":
        guess = "p"
    elif guess == "scissors":
        guess = "s"
    else:
        guess = "err"

    winner = personWin(guess, botGuess)
    response += addGuess(guess, False, ctx.author.id)
    if winner != -99:
        response += addGuess(botGuess, True, 0)

    if winner == 1:
        response += "You Win!"
    elif winner == 0:
        response += "Draw!"
    elif winner == -1:
        response += "I win!"
    elif winner == -99:
        response += "Try a valid guess next time!"

    #addToDB(ctx.author.id, 1)

    return response

@bot.command(name='rockPaperScissors', help='Plays rock paper scissors with you')
async def rockPS(ctx, guess):
    await ctx.send(rps(ctx, guess))

@bot.command(name='rps', help='Plays rock paper scissors with you')
async def rockPS(ctx, guess):
    await ctx.send(rps(ctx, guess))

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

@bot.command(name='atPhil', help='Gets the bot to @ Phil when you ask who lost him')
async def atPhilOnMessage(ctx):
    global atPhil
    atPhil = 0
    response = "I will now @ Phil every time you ask who lost him"
    await ctx.send(response)

@bot.command(name='dontAtPhil', help='Gets the bot to not @ Phil when you ask who lost him')
async def dontAtPhilOnMessage(ctx):
    global atPhil
    atPhil = 1
    response = "I will not @ Phil every time you ask who lost him"
    await ctx.send(response)

@bot.command(name='lost', help='Tells you who lost him')
async def lost(ctx):
    global atPhil
    response = phil[atPhil] + " lost me"
    await ctx.message.channel.send(response)


# async def on_message(message):
#     await bot.process_commands(message)
#     print("I'mk running")
#     await message.add_reaction(':mainlogo:')

bot.run(TOKEN)
