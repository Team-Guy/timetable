from authentication.models import Preference
from dbutils.to_string import auto_str


@auto_str
class Pref:

    def __init__(self, pref: Preference):
        self.id = id
        self.pref1 = pref.preference1
        self.pref2 = pref.preference2
        self.pref3 = pref.preference3
        self.pref1_prio = pref.preference1_prio
        self.pref2_prio = pref.preference2_prio
        self.pref3_prio = pref.preference3_prio
