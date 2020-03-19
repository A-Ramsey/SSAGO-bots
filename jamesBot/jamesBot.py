import os
from random import randint

import discord
from dotenv import load_dotenv
from googletrans import Translator


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self,message):
        if message.author == client.user:
            return
        if randint(0, 30) == 1:
            translator = Translator()

            result = translator.translate(message.content,dest='cy')
            await message.channel.send('Did you know you could say it in welsh like this: ```' + result.text + '```')


client = CustomClient()
client.run(TOKEN)