# bot.py
import os
import logging

import discord
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class Bot(commands.Bot):
    """Subclass the bot class"""

    async def process_commands(self, message):
        """Allow commands from Bots"""
        ctx = await self.get_context(message)
        await self.invoke(ctx)

bot = Bot(command_prefix=commands.when_mentioned)

bot.load_extension("mary.cogs.mctour")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You are missing a required argument.')
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Pardon, I didn\'t quite get that.')
    else:
        await ctx.send('something went wrong, please contact the Admin')
        logging.error(error)


@bot.command(aliases=["hello","Hello","Hi"])
async def hi(ctx: Context):
    """says hello"""
    await ctx.send('Hello there!')

@bot.command()
async def git(ctx):
    """link to the bots git"""
    await ctx.send('https://github.com/RamseyTheCyclist/SSAGO-bots')

bot.run(TOKEN)
