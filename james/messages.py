from discord import Message

def listPrint(l: []):
    m = ''
    for t in l:
        m = m + t + ' '
    return m

class Response:
    def __init__(self, response_message: str, response_parameters: [] = [], action=None):
        self.responseMessage = response_message
        self.responseParameters = response_parameters
        self.action = action


PARAM_MENTION = 'mention'
PARAM_THINGS = 'thingstodo'
PARAM_ACTION_RESULT = 'actionresult'
PARAM_FRIENDS = 'friends'
PARAM_JOKE = 'joke'

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


def cmd_shutup(j, message):
    j.translationEnabled = False


def cmd_resumetalking(j, message):
    j.translationEnabled = True


def cmd_steal(j, message):
    j.stealAttempts.append(message.author.mention)
    if message.author.mention in j.friends:
        j.friends.discard(message.author.mention)
        return 'I thought you were my friend!'
    return 'I\'m a none stealable you fool. -10 points to griffindor.'

messages = {
    'i am good': Response('{0} Well that\'s nice to see, maybe you could try {1} to make your day even better.',
                          [PARAM_MENTION, PARAM_THINGS]),
    'i am not good': Response('{0} oh no, might I suggest that you {1} to cheer you up?',
                              [PARAM_MENTION, PARAM_THINGS]),
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
                     'Hi\n'
                     'Do you have a brain?\n'
                     'I\'m tired\n'
                     'Tell a joke | I want a good laugh | cheer me up\n'
                     'It\'s cold out here.\n'
                     '```'),
    'thanks': Response('You\'re Welcome'),
    'hello': Response('Hello {0}', [PARAM_MENTION]),
    'hi': Response('Hi'),
    'catch': Response('James catches the ball, and throws it to {0}', [PARAM_ACTION_RESULT], action=cmd_catch),
    'resumetalking': Response('Yay :) BAAAA', action=cmd_resumetalking),
    'shutup': Response('Fine :( BAAAA', action=cmd_shutup),
    'shut up': Response('Fine :( BAAAA', action=cmd_shutup),
    'steal': Response('{0}', [PARAM_ACTION_RESULT], action=cmd_steal),
    'say hello to oli': Response('Hi <@678903558828982274>'),
    'do you have a brain': Response('Sort of...: https://github.com/RamseyTheCyclist/SSAGO-bots'),
    'i\'m tired': Response('Well go to sleep {0}', [PARAM_MENTION]),
    'tell a joke': Response('{0}', [PARAM_JOKE]),
    'i want a good laugh': Response('{0}', [PARAM_JOKE]),
    'cheer me up':Response('{0}',[PARAM_JOKE]),
    'greetings':Response('Who? me?'),
    'it\'s cold out here':Response('Brrrrr')
}