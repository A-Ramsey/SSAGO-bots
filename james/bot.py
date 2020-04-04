from random import randint


class Bot:

    def __init__(self, display_name: str, commands: [], mention: str = None, catchCMD: str = None):
        self.display_name: str = display_name
        self.mention: str = mention
        self.commands: [] = commands
        self.catchCMD: str = catchCMD

    def getRandomCommand(self):
        return self.commands[randint(0, len(self.commands) - 1)]

bots = [
    Bot('RoBot', ['rob steal', 'rob quote context', 'rob catch', 'rob quote', 'rob random 100',
                  'rob faction join TheBestFaction', 'rob faction list'], '<@689981551534014576>', 'rob catch'),
    Bot('Leo the Lion', ['?leo steal', '?leo git', '?leo rally', '?leo sally', '?leo translate'],
        '<@689751502700675072>', '<@689751502700675072> catch'),
    Bot('Pablo the Pug', ['pablo.fetch', 'pablo.catch'], '<@690960331584831579>', 'pablo.catch'),
    Bot('Rex O\'Saurus', ['good rex', 'bad rex', '!witan'], '<@689409878162145280>', 'rex catch'),
    Bot('Youlbury', ['y;catch'], '<@690594174365335568>', 'y;catch'),
    Bot('Morrissey (Yellow Rally', ['<@690576065743159308> catch'], '<@690576065743159308>',
        '<@690576065743159308> catch'),
    Bot('Freddo (Green Rally)', ['<@690934924756385804> catch'], '<@690934924756385804>',
        '<@690934924756385804> catch'),
]