import os
import time
from random import randint

import discord
from discord import Message
from dotenv import load_dotenv
from googletrans import Translator

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class Response:
    def __init__(self, response_message: str, response_parameters: []=[], action=None):
        self.responseMessage = response_message
        self.responseParameters = response_parameters
        self.action = action


robCommands = ['rob steal', 'rob quote context', 'rob catch']
leoCommands = ['?leo steal','?leo git','?leo rally', '?leo sally']
thingsToDo = ['hopping over to minecraft.ssago.org',
              'joining in on or run a virtual event',
              'playing Cards Humanity with rob and some friends.',
              'chat with some friends',
              'try to steal other mascots',
              'play skribbl',
              'hop into a voice channel with your friends',
              'go outside for some fresh air',
              'have a nice bite to eat',
              'cooking a chocolate brownie',
              'cooking a homemade pizza',
              'have a nice drink of water',
              'checkout some photos on the photo channel',
              'checkout some memes on the memes channel',
              'discuss some tv on the tv channel',
              'develop a mascotBot to talk to be my friend',
              ]


def how_am_i(j, message: Message):
    if j.translationEnabled:
        result = 'I will translate every 1/' + str(j.translationFrequency) + ' messages.\n'
    else:
        result = 'I was told to shutup :( baaa please re-enable me... baaaa\n'
    if len(j.stealAttempts) > 0:
        result = result + 'And these people have recently tried to steal me: ' + listPrint(j.stealAttempts)
    return result


def friend(j, message: Message):
    if message.author.mention in j.friends:
        return 'I am already your friend! baaaa'
    else:
        j.friends.add(message.author.mention)
        return 'sure you can! baaaaa'

def cmd_catch(j, message):
        f = j.friends.pop()
        j.friends.add(f)
        return f


def cmd_shutup(self, message):
        self.translationEnabled = False


def cmd_resumetalking(self, message):
        self.translationEnabled = True


def cmd_steal(j, message):
        j.stealAttempts.append(message.author.mention)
        if message.author.mention in j.friends:
            j.friends.discard(message.author.mention)
            return 'I thought you were my friend!'
        return 'I\'m a none stealable you fool. -10 points to griffindor.'

PARAM_MENTION = 'mention'
PARAM_THINGS = 'thingstodo'
PARAM_ACTION_RESULT = 'actionresult'
PARAM_FRIENDS = 'friends'

messages = {
    'i am good': Response('{0} Well that\'s nice to see, maybe you could try {1} to make your day even better.',
                          [PARAM_MENTION, PARAM_THINGS]),
    'i am not good': Response('{0} oh no, might I suggest that you {1} to cheer you up?', [PARAM_MENTION, PARAM_THINGS]),
    'i am excellent': Response('{0} Awesome, maybe you can spread your joy by {1}.', [PARAM_MENTION, PARAM_THINGS]),
    'what can i do around here?': Response('{0} You could {1}.', [PARAM_MENTION, PARAM_THINGS]),
    'who are your friends': Response('I am friends with: {0}', [PARAM_FRIENDS]),
    'who are you?': Response(
        'I am one of MSAGM Aber SSAGO\'s mascots, I normally reside with the Secretary.\nI am friends with {0}',
        [PARAM_FRIENDS]),
    'how are you': Response('Alive and well :) Baaaa.\n{0} and how are you?', [PARAM_ACTION_RESULT], action=how_am_i),
    'can i be your friend': Response('{0}', [PARAM_ACTION_RESULT], action=friend),
    'help': Response('```\n'
                     'Command\n'
                     'shutup - tells James to shutup \n'
                     'catch -  catches the ball and throws it to a friend\n'
                     'resumeTalking - tell james he can talk.\n'
                     'setfrequency X -  set frequency of his translation attempts.\n'
                     'help - displays this\n'
                     '\nConverse\n'
                     'How Are You?\n'
                     'I am good | I am bad | I am excellent.\n'
                     'Who are you?\n'
                     'Can I be your friend?\n'
                     'Who are your friends?\n'
                     'What can I do around here?\n'
                     'Say hello to Oli\n'
                     'Hi'
                     '```'),
    'thanks':Response('You\'re Welcome'),
    'hello':Response('Hello {0}',[PARAM_MENTION]),
    'hi':Response('Hi'),
    'catch':Response('James catches the ball, and throws it to {0}',[PARAM_ACTION_RESULT],action=cmd_catch),
    'resumetalking':Response('Yay :) BAAAA',action=cmd_resumetalking),
    'shutup':Response('Fine :( BAAAA',action=cmd_shutup),
    'shut up':Response('Fine :( BAAAA',action=cmd_shutup),
    'steal':Response('{0}',[PARAM_ACTION_RESULT],action=cmd_steal),
    'say hello to oli':Response('Hi <@678903558828982274>'),
    'do you have a brain':Response('Sort of...: https://github.com/RamseyTheCyclist/SSAGO-bots')
}



def listPrint(l: []):
    m = ''
    for t in l:
        m = m + t + ' '
    return m


class JamesTheSheep(discord.Client):

    def __init__(self, **options):
        self.translationFrequency = 30
        self.translationEnabled = True
        self.stealAttempts = []
        self.friends = {'<@690257560531763204>', '<@678903558828982274>', '<@689981551534014576>', '<@689751502700675072>'}
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
            elif randint(0, 10) == 1:
                time.sleep(1)
                await message.channel.send(robCommands[randint(0, len(robCommands)-1)])
        elif self.translationEnabled and message.author.display_name == 'Leo the Lion':
            if message.content.startswith('Ro'):
                await message.channel.send('AHHH, Run away from Leo!')
            elif randint(0,10) ==1:
                time.sleep(1)
                await message.channel.send(leoCommands[randint(0, len(leoCommands)-1)])
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
