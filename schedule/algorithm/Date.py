class Date:

    def __init__(self, day=None, start_hour=None, duration=None, location=None):
        if day is None or day == '-':
            self._day = None
        else:
            self._day = day
        self._duration = int(duration)
        if start_hour is None or start_hour == '-':
            self._startHour = None
        else:
            self._startHour = start_hour
        if location is None or location == '-':
            self._location = None
        else:
            self._location = location

    def __str__(self):
        return "Day: " + self.x_str(self._day) + " | Duration: " + self.x_str(self._duration) +\
               " | Start Hour: " + self.x_str(self._startHour) + " | Location: " + self.x_str(self._location) + "\n"

    @staticmethod
    def x_str(s):
        if s is None:
            return '-'
        return str(s)

    @property
    def day(self):
        return self._day

    @property
    def duration(self):
        return self._duration

    @property
    def start_hour(self):
        return self._startHour
