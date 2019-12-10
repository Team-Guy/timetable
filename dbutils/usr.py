from dbutils.to_string import auto_str
from schedule.models import User


@auto_str
class Usr:

    def __init__(self, user: User):
        self.id = user.id
        self.name = user.name
        self.sport = user.sport
        self.peda = user.peda
        self.email = user.email
        self.group = user.group
