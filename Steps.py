import datetime


class Pause:
    def __init__(self, msg):
        self.msg = msg
        self.tag = 'PAUSE'

    def __str__(self):
        return 'Pause ({msg})'.format(**self)


class Done:
    def __init__(self):
        self.tag = 'DONE'

    def __str__(self):
        return 'Done!'.format(**self)


class Target:
    def __init__(self):
        self.tag = 'TARGET'

    def __str__(self):
        return 'Use settings file for target'.format(**self)


class Heat:
    def __init__(self, temp):
        self.tag = 'HEAT'
        self.temp = temp

    def __str__(self):
        return 'Heat to {tmp}°'.format(**self)


class Cook:
    def __init__(self, temp, time):
        self.tag = 'COOK'
        self.temp = temp
        self.time = time
        self.timestring = datetime.timedelta(seconds=time)

    def __str__(self):
        return 'Cook at {tmp}° for {timestring}'.format(**self)


def parse(command):
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
