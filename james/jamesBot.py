import os
import time
from random import randint

import discord
from discord import Message
from dotenv import load_dotenv
from googletrans import Translator

from james.thingstodo import thingsToDo
from james.jokes import jokes

from james.messages import messages,Response,PARAM_THINGS,PARAM_FRIENDS,PARAM_MENTION,PARAM_ACTION_RESULT,PARAM_JOKE,listPrint

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

robCommands = ['rob steal', 'rob quote context', 'rob catch', 'rob quote', 'rob random 100', 'rob faction join TheBestFaction', 'rob faction list']
leoCommands = ['?leo steal', '?leo git', '?leo rally', '?leo sally']
rexCommands = ['good rex','bad rex','!witan']


class JamesTheSheep(discord.Client):

    def __init__(self, **options):
        self.translationFrequency = 30
        self.translationEnabled = True
        self.stealAttempts = []
        self.friends = {'<@690257560531763204>', '<@678903558828982274>', '<@689981551534014576>',
                        '<@689751502700675072>'}
        super().__init__(**options)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message: Message):
        if message.author == client.user:
            return

        print(message.author.display_name, message.author.mention)

        if self.translationEnabled and message.author.display_name == 'RoBot':
            print(message.content)
            if message.content == 'Rob catches the ball, and throws it to <@!690154676938866719>':
                f = self.friends.pop()
                await message.channel.send('James catches the ball, and throws it to ' + f)
                self.friends.add(f)
            elif message.content == '<@!690154676938866719> steal':
                await message.channel.send('We already talked about this, you can\'t steal me')
            elif randint(0, 10) == 1:
                time.sleep(1)
                await message.channel.send(robCommands[randint(0, len(robCommands) - 1)])
        elif self.translationEnabled and message.author.display_name == 'Leo the Lion':
            if message.content.startswith('Ro'):
                await message.channel.send('AHHH, Run away from Leo!')
            elif randint(0, 10) == 1:
                time.sleep(1)
                await message.channel.send(leoCommands[randint(0, len(leoCommands) - 1)])
        elif self.translationEnabled and message.author.display_name == 'Rex O\'Saurus':
            if randint(0, 10) == 1:
                time.sleep(1)
                await message.channel.send(rexCommands[randint(0, len(rexCommands) - 1)])
        elif message.mentions and message.mentions[0].name == 'JamesTheSheep':
            m = message.content[22:].strip()
            print(m)
            if len(m) == 0:
                await message.channel.send('Hi, I\'m here. baaaa')
            elif await self.converse(message, m):
                print('was social')
            elif await self.runCommand(message, m):
                print('did as instructed')
            else:
                await message.channel.send('Sorry but I didn\'t quite get that. baaaaaa')
        else:
            await self.translate(message)

    async def translate(self, message: Message):
        if self.translationEnabled and randint(0, self.translationFrequency) == 1:
            if not message.content.startswith('"'):
                try:
                    translator = Translator()
                    result = translator.translate(message.content, dest='cy')
                    await message.channel.send(
                        'Did you know you could say it in welsh like this: ```' + result.text + '```')
                except:
                    print('couldn\'t translate:', message.content)

    async def converse(self, message: Message, m: str):
        m = m.lower()
        for n in messages.keys():
            if m.startswith(n):
                response: Response = messages.get(n)
                response_parameters = response.responseParameters
                action_result = ''
                if response.action is not None:
                    action_result = response.action(self, message)
                for i, j in enumerate(response.responseParameters):
                    if j == PARAM_MENTION:
                        response_parameters[i] = message.author.mention
                    elif j == PARAM_FRIENDS:
                        response_parameters[i] = listPrint(self.friends)
                    elif j == PARAM_THINGS:
                        response_parameters[i] = thingsToDo[randint(0, len(thingsToDo) - 1)]
                    elif j == PARAM_ACTION_RESULT:
                        response_parameters[i] = action_result
                    elif j == PARAM_JOKE:
                        response_parameters[i] = jokes[randint(0, len(jokes) - 1)]

                await message.channel.send(response.responseMessage.format(*response_parameters))
                return True
        return False

    async def runCommand(self, message: Message, m: str):
        """Dispatch method"""
        command = m.lower().split(' ')
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, 'cmd_' + str(command[0]), self.returnFalse)
        # Call the method as we return it
        return await method(message, command)

    async def cmd_say(selfself,message,command):
        m = ''
        for i in command[1:]:
            m = m+ i + ' '
        await message.channel.send(m)
        return True

    async def cmd_setfrequency(self, message, command):
        if len(command) >= 2 and command[1].isnumeric():
            self.translationFrequency = int(command[1])
            await message.channel.send('frequency now 1/' + command[1])
            return True
        else:
            await message.channel.send('Invalid usage of setfrequency')
        return True

    async def returnFalse(self, message, command):
        return False


client = JamesTheSheep()
client.run(TOKEN)
