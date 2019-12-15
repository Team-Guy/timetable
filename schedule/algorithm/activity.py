class Activity:

    def __init__(self, name=None, activity_type=None, extra=None,
                 dates=None, priority=None, week=None, activity_id=None):
        if week is None or week == '-':
            self._week = None
        else:
            self._week = int(week)
        self._name = name
        self._type = activity_type
        self._extra = extra
        self._dates = dates
        self._priority = priority
        self._ids = [activity_id]

    @property
    def dates(self):
        return self._dates

    def __str__(self):
        msg = "Name: " + self._name + " | Type: " + self._type + " | Week: " + str(self._week) + "\n"
        for i in range(len(self._dates)):
            msg += "\t" + str(self._dates[i])
        msg += 'Priority: ' + self.x_str(self._priority) + "\n"
        return msg

    @staticmethod
    def x_str(s):
        if s is None:
            return ''
        return str(s)

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def extra(self):
        return self._extra

    @property
    def priority(self):
        return self._priority

    @property
    def week(self):
        return self._week

    @property
    def ids(self):
        return self._ids
