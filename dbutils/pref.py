from authentication.models import Preference
from dbutils.to_string import auto_str


@auto_str
class Pref:

    def __init__(self, pref: Preference):
        self.id = id
        self.mondayStart = pref.mondayStart
        self.mondayEnd = pref.mondayEnd
        self.tuesdayStart = pref.tuesdayStart
        self.tuesdayEnd = pref.thursdayEnd
        self.wednesdayStart=pref.wednesdayStart
        self.wednesdayEnd=pref.wednesdayEnd
        self.thursdayStart=pref.thursdayStart
        self.thursdayEnd=pref.thursdayEnd
        self.fridayStart=pref.fridayStart
        self.fridayEnd=pref.fridayEnd
