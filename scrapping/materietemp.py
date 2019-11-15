import json


class MaterieTemp:

    def __init__(self, grupe, start_hour, duration, text, frequency, day, class_type):
        text = text.split(':')[-1].replace('(facultativ)', '')
        self.text = text.split('(')[0].strip()
        self.profesor = text.split('(')[1].split(')')[0].strip()
        self.locatie = text.split(')')[1][1:].split('(')[0].strip()
        self.grupe = grupe
        self.startHour = start_hour
        self.duration = duration
        self.frequency = frequency
        self.day = day
        self.tip = class_type
        if self.tip == 'Laborator' or self.tip == 'Seminar':
            self.priority = 'HIGH'
        else:
            self.priority = 'LOW'

    def __str__(self):
        return json.dumps(self, default=lambda item: item.__dict__, indent=4)
