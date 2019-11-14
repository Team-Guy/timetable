from schedule.models import SchoolActivity


class FacultyActivity:

    def __init__(self, activity: SchoolActivity):
        self.id = activity.id
        self.title = activity.title
        self.type = activity.type
        self.priority = activity.priority
        self.day = activity.day
        self.frequency = activity.frequency
        self.duration = activity.duration
        self.professor = activity.professor
        self.group = activity.group
        self.location = activity.location
        self.start_time = activity.start_time
