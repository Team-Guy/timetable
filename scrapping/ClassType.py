
class ClassType:

    LABORATOR='tipL'
    CURS='tipC'
    SEMINAR='tipS'

    @staticmethod
    def getClassType(type):
        if type==ClassType.LABORATOR:
            return 'Laborator'
        elif type==ClassType.CURS:
            return 'Curs'
        elif type==ClassType.SEMINAR:
            return 'Seminar'
        else:
            return None