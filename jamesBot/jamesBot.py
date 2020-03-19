import os
import time
from random import randint

import discord
from discord import Message
from dotenv import load_dotenv
from googletrans import Translator

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

robCommands = ['rob steal','rob quote context','rob catch']

def listPrint(l:[]):
    m = ''
    for t in l:
        m = m + t + ' '
    return m


class JamesTheSheep(discord.Client):

    def __init__(self, **options):
        self.translationFrequency = 30
        self.translationEnabled = True
        self.stealAttempts = []
        self.friends = {'<@690257560531763204>', '<@678903558828982274>', '<@689981551534014576>'}
        self.known = {'Oli':'<@678903558828982274>'}
        super().__init__(**options)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message:Message):
        if message.author == client.user:
            return

        self.known[message.author.display_name] = message.author.mention

        if self.translationEnabled and message.author.display_name == 'RoBot':
            print(message.content)
            if message.content == 'Rob catches the ball, and throws it to <@!690154676938866719>':
                f = self.friends.pop()
                await message.channel.send('James catches the ball, and throws it to ' + f)
                self.friends.add(f)
            elif randint(0, 2) == 1:
                time.sleep(1)
                await message.channel.send(robCommands[randint(0,2)])
        elif message.mentions and message.mentions[0].name == 'JamesTheSheep':
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
        else:
            await self.translate(message)


    async def translate(self,message:Message):
        if self.translationEnabled and randint(0, self.translationFrequency) == 1:
            if not message.content.startswith('"'):
                translator = Translator()
                result = translator.translate(message.content, dest='cy')
                await message.channel.send('Did you know you could say it in welsh like this: ```' + result.text + '```')

    async def converse(self,message:Message,m:str):
        m = m.lower()
        if m.startswith('how are you'):
            result = 'Alive and well :) Baaaa\n'
            if self.translationEnabled:
                result = result + 'I will translate every 1/' + str(self.translationFrequency) + ' messages.\n'
            else:
                result = result + 'I was told to shutup :( baaa please re-enable me... baaaa\n'
            if len(self.stealAttempts) > 0:
                result = result + 'And these people have recently tried to steal me: ' + listPrint(self.stealAttempts) + '\n'
            result = result + 'and how are you?'
            await message.channel.send(result)
            return True
        elif m.startswith( 'who are you?'):
            result = 'I am one of MSAGM Aber SSAGO\'s mascots, I normally reside with the Secretary.\n'
            result = result + 'I am friends with' + listPrint(self.friends)
            await message.channel.send(result)
            return True
        elif m.startswith('can i be your friend'):
            if message.author.mention in self.friends:
                await message.channel.send('I am already your friend! baaaa')
            else:
                self.friends.add(message.author.mention)
                await message.channel.send('sure you can! baaaaa')
            return True
        elif m.startswith('who are your friends'):
            await message.channel.send('I am friends with: ' + listPrint(self.friends))
            return True
        return False

    async def runCommand(self, message: Message, m: str):
        """Dispatch method"""
        command = m.lower().split(' ')
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, 'cmd_' + str(command[0]), self.returnFalse)
        # Call the method as we return it
        return await method(message, command)

    async def cmd_steal(self, message,command):
        self.stealAttempts.append(message.author.mention)
        if message.author.mention in self.friends:
            self.friends.discard(message.author.mention)
            await message.channel.send('I thought you were my friend!')
        await message.channel.send('I\'m a none stealable you fool. -10 points to griffindor.')
        return True

    async def cmd_setfrequency(self,message,command):
        if len(command) >= 2 and command[1].isnumeric():
            self.translationFrequency = int(command[1])
            await message.channel.send('frequency now 1/' + command[1])
        else:
            await message.channel.send('Invalid usage of setfrequency')
        return True

    async def cmd_contact(self,message,command):
        if len(command) >= 2 and command[1] in self.known.keys():
            await message.channel.send('mention Id of '+command[1] + ' is ' + self.known.get(command[1]))
            return True

    async def cmd_catch(self,message,command):
        f = self.friends.pop()
        await message.channel.send('James catches the ball, and throws it to ' + f)
        self.friends.add(f)
        return True

    async def cmd_(self,message,command):
        self.translationEnabled = False
        await  message.channel.send('Fine :( BAAAA')
        return True

    async def cmd_resumetalking(self,message,command):
        self.translationEnabled = True
        await  message.channel.send('Yay :) BAAAA')
        return True

    async def cmd_thanks(self,message,command):
        await message.channel.send('You are Welcome :)')
        return True

    async def cmd_help(self,message,command):
        await message.channel.send('```'
                                   'Command\n'
                                   'shutup - tells James to shutup \n'
                                   'catch -  catches the ball and throws it to a friend'
                                   'resumeTalking - tell james he can talk.\n'
                                   'setfrequency X -  set frequency of his translation attempts.\n'
                                   'contact display_name - try\'s to return the mention id for the display_name provided'
                                   'help - displays this\n'
                                   '\nConverse\n'
                                   'How Are You?\n'
                                   'Who are you?\n'
                                   'Can I be your friend?\n'
                                   'Who are your friends?\n'
                                   '```')
        return True

    async def returnFalse(self,message,command):
        return False




client = JamesTheSheep()
client.run(TOKEN)
