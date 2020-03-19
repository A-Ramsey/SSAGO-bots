import os
import time
from random import randint

import discord
from discord import Message
from dotenv import load_dotenv
from googletrans import Translator

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class JamesTheSheep(discord.Client):

    def __init__(self, **options):
        self.translationFrequency = 30
        self.translationEnabled = True
        self.stealAttempts = []
        super().__init__(**options)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message:Message):
        if message.author == client.user:
            return

        await self.translate(message)
        print(message.author.display_name)

        if message.mentions and message.mentions[0].name == 'JamesTheSheep':
            m = message.content[22:].strip()
            print(m)
            if len(m) == 0:
                await message.channel.send('Hi, I\'m here. baaaa')
            elif await self.converse(message,m):
                print('was social')
            elif await self.runCommand(message,m):
                print('did as instructed')
            else:
                await message.channel.send('Sorry but I didn\'t quite get that. baaaaaa')
        elif self.translationEnabled and message.author.display_name == 'RoBot' and randint(0, 1) == 1:
            await message.channel.send('rob steal')

    async def translate(self,message:Message):
        if self.translationEnabled and randint(0, self.translationFrequency) == 1:
            translator = Translator()

            result = translator.translate(message.content, dest='cy')
            await message.channel.send('Did you know you could say it in welsh like this: ```' + result.text + '```')

    async def converse(self,message:Message,m:str):
        if m.lower() == 'how are you?':
            result = 'Alive and well :) Baaaa\n'
            if self.translationEnabled:
                result = result + 'I will translate every 1/' + str(self.translationFrequency) + ' messages.\n'
            else:
                result = result + 'I was told to shutup :( baaa please re-enable me... baaaa\n'
            if len(self.stealAttempts) > 0:
                result = result + 'And these people have recently tried to steal me: ' + str(self.stealAttempts)
            await message.channel.send(result)
            return True
        return False

    async def runCommand(self, message: Message, m: str):
        """Dispatch method"""
        command = m.lower().split(' ')
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, 'cmd_' + str(command[0]), self.cmd_returnFalse)
        # Call the method as we return it
        return await method(message, command)

    async def cmd_steal(self, message,command):
        self.stealAttempts.append(message.author.display_name)
        await message.channel.send('I\'m a none stealable you fool. -10 points to griffindor.')
        return True

    async def cmd_setfrequency(self,message,command):
        if len(command) >= 2 and command[1].isnumeric():
            self.translationFrequency = int(command[1])
            await message.channel.send('frequency now 1/' + command[1])
        else:
            await message.channel.send('Invalid usage of setfrequency')
        return True

    async def cmd_(self,message,command):
        self.translationEnabled = False
        await  message.channel.send('Fine :( BAAAA')
        return True

    async def cmd_resumetalking(self,message,command):
        self.translationEnabled = True
        await  message.channel.send('Yay :) BAAAA')
        return True

    async def cmd_help(self,message,command):
        await message.channel.send('shutup - tells James to shutup \n resumeTalking - tell james he can '
                                   'talk.\n HowAreYou? -  asks him how he is '
                                   '\n setfrequency X -  set frequency of his translation attempts.')
        return True

    async def cmd_returnFalse(self,message,command):
        return False




client = JamesTheSheep()
client.run(TOKEN)
