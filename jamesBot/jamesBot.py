import os
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

        if message.mentions and message.mentions[0].name == 'JamesTheSheep':
            m = message.content[22:].strip()
            if len(m) == 0:
                await message.channel.send('Hi, I\'m here. baaaa')
            elif await self.converse(message,m):
                print('was social')
            elif await self.commands(message,m):
                print('did as instructed')
            else:
                await message.channel.send('Sorry but I didn\'t quite get that. baaaaaa')


    async def translate(self,message:Message):
        if self.translationEnabled and randint(0, self.translationFrequency) == 1:
            translator = Translator()

            result = translator.translate(message.content, dest='cy')
            await message.channel.send('Did you know you could say it in welsh like this: ```' + result.text + '```')

    async def commands(self, message:Message,m:str):
        command = m.lower().split(' ')
        if command[0] == 'steal':
            self.stealAttempts.append(message.author.name)
            await message.channel.send('I\'m a none stealable you fool. -10 points to griffindor.')
            return True
        elif command[0] == 'setfrequency':
            if len(command) >= 3 and command[1].isnumeric():
                self.translationFrequency = int(command[1])
                await message.channel.send('frequency now 1/' + command[1])
                return True
            else:
                await message.channel.send('Invalid usage')
                return True
        elif command[0] == 'shutup':
            self.translationEnabled = False
            await  message.channel.send('Fine :( BAAAA')
            return True
        elif command[0] == 'resumetalking':
            self.translationEnabled = True
            await  message.channel.send('Yay :) BAAAA')
            return True
        elif command[0] == 'help':
            await message.channel.send('shutup - tells James to shutup \n resumeTalking - tell james he can '
                                       'talk.\n HowAreYou? -  asks him how he is '
                                       '\n setfrequency X -  set frequency of his translation attempts.')
            return True
        return False

    async def converse(self,message:Message,m:str):
        if m.lower() == 'How are you?':
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

client = JamesTheSheep()
client.run(TOKEN)
