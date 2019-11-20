class Date:
    """
    The class Date is used to store all the information about an activity
    """

    def __init__(self, day=None, start_hour=None, duration=None, location=None):
        """
        The only constructor for Date class
        :param day: Day of the activity. Expected values: {monday, tuesday, wednesday, thursday, friday} - String
        :param start_hour: The hour that the activity begins. Expected values: {from 8 to 19} - Integer
        :param duration: The duration of an activity. Minimum 1. - Integer
        :param location: The location where the activity unfolds. - String
        """
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
        """
        Used if one or more information about the activity is missing.
        :param s: The string
        :return: '-' if the string is None, else str(string)
        """
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
