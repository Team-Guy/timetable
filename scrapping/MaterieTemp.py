import json

class MaterieTemp:

    def __init__(self,grupe,startHour,duration,text,frequency,day,classType):
        text = text.split(':')[-1].replace('(facultativ)', '')
        self.text = text.split('(')[0].strip()
        self.profesor = text.split('(')[1].split(')')[0].strip()
        self.locatie = text.split(')')[1][1:].split('(')[0].strip()
        self.grupe=grupe
        self.startHour=startHour
        self.duration=duration
        self.frequency=frequency
        self.day=day
        self.tip=classType



    def __str__(self):
        return json.dumps(self,default= lambda item: item.__dict__, indent=4)

