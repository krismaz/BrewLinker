import datetime


class Pause:
    def __init__(self, msg):
        self.msg = msg.strip()
        self.tag = 'PAUSE'

    def __str__(self):
        return 'Pause ({msg})'.format(**self.__dict__)


class Done:
    def __init__(self):
        self.tag = 'DONE'

    def __str__(self):
        return 'Done!'.format(**self.__dict__)


class Target:
    def __init__(self):
        self.tag = 'TARGET'

    def __str__(self):
        return 'Use settings file for target'.format(**self.__dict__)


class Heat:
    def __init__(self, temp):
        self.tag = 'HEAT'
        self.temp = temp

    def __str__(self):
        return 'Heat to {temp}°'.format(**self.__dict__)


class Cook:
    def __init__(self, temp, time):
        self.tag = 'COOK'
        self.temp = temp
        self.time = time
        self.timestring = datetime.timedelta(seconds=time)

    def __str__(self):
        return 'Cook at {temp}° for {timestring}'.format(**self.__dict__)


def parse(command):
    if not command or command[0] == '#':
        return None
    op, *args = command.split(' ')
    if op == 'PAUSE':
        return Pause(' '.join(args))
    elif op == 'DONE':
        return Done()
    elif op == 'TARGET':
        return Target()
    elif op == 'HEAT':
        return Heat(float(args[0]))
    elif op == 'COOK':
        return Cook(float(args[0]), float(args[1]) * 60.)
    return None
