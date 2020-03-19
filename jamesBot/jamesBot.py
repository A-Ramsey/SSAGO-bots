import os
from random import randint

import discord
from dotenv import load_dotenv
from googletrans import Translator


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class CustomClient(discord.Client):

    def __init__(self, **options):
        self.translationFrequency = 30
        self.translationEnabled = True
        super().__init__(**options)



    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self,message):
        if message.author == client.user:
            return
        if self.translationEnabled and randint(0, self.translationFrequency) == 1:
            translator = Translator()

            result = translator.translate(message.content,dest='cy')
            await message.channel.send('Did you know you could say it in welsh like this: ```' + result.text + '```')

        if message.content.lower().startswith('!jamesthesheep'):
            command = message.content.lower().split(' ')
            if command[1] == 'setfrequency':
                self.translationFrequency = int(command[2])
                await message.channel.send('frequency now 1/' + command[2])
            elif command[1] == 'shutup':
                self.translationEnabled = False
                await  message.channel.send('Fine :( BAAAA')
            elif command[1] == 'resumetalking':
                self.translationEnabled = True
                await  message.channel.send('Yay :) BAAAA')
            elif command[1] == 'help':
                await message.channel.send(' shutup - tells James to shutup \n resumetalking - tell james he can talk '
                                           '\n setfrequency X -  set frequency of his translation attempts.')




client = CustomClient()
client.run(TOKEN)