from authentication.models import Preference
from dbutils.to_string import auto_str


@auto_str
class Pref:

    def __init__(self, pref: Preference):
        self.id = pref.user.id
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
        self.mondayMax=pref.mondayMax
        self.tuesdayMax=pref.tuesdayMax
        self.wednesdayMax=pref.wednesdayMax
        self.thursdayMax=pref.thursdayMax
        self.fridayMax=pref.fridayMax


    def to_dict(self):
        return {
            "id":self.id,
            "mondayStart":str(self.mondayStart.hour)+':'+str(self.mondayStart.minute)+':'+str(self.mondayStart.second),
            "mondayEnd":str(self.mondayEnd.hour)+':'+str(self.mondayEnd.minute)+':'+str(self.mondayEnd.second),
            "tuesdayStart":str(self.tuesdayStart.hour)+':'+str(self.tuesdayStart.minute)+':'+str(self.tuesdayStart.second),
            "tuesdayEnd":str(self.tuesdayEnd.hour)+':'+str(self.tuesdayEnd.minute)+':'+str(self.tuesdayEnd.second),
            "wednesdayStart":str(self.wednesdayStart.hour)+':'+str(self.wednesdayStart.minute)+':'+str(self.wednesdayStart.second),
            "wednesdayEnd":str(self.wednesdayEnd.hour)+':'+str(self.wednesdayEnd.minute)+':'+str(self.wednesdayEnd.second),
            "thursdayStart":str(self.thursdayStart.hour)+':'+str(self.thursdayStart.minute)+':'+str(self.thursdayStart.second),
            "thursdayEnd":str(self.thursdayEnd.hour)+':'+str(self.thursdayEnd.minute)+':'+str(self.thursdayEnd.second),
            "fridayStart":str(self.fridayStart.hour)+':'+str(self.fridayStart.minute)+':'+str(self.fridayStart.second),
            "fridayEnd":str(self.fridayEnd.hour)+':'+str(self.fridayEnd.minute)+':'+str(self.fridayEnd.second),
            "mondayMax":self.mondayMax,
            "tuesdayMax":self.tuesdayMax,
            "wednesdayMax":self.wednesdayMax,
            "thursdayMax":self.thursdayMax,
            "fridayMax":self.fridayMax
        }