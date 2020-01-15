import json

from authentication.models import LastTimetable
from schedule.models import User


def save_last_timetable(timetable: str, username: str):
    gmail_user = username + '@gmail.com'
    db_user = User.objects.get(email=gmail_user)
    LastTimetable(user=db_user, lastTimetable=timetable).save()


def get_last_timetable(username):
    username = username + '@gmail.com'
    user = User.objects.get(email=username)
    last = LastTimetable.objects.get(user=user).lastTimetable
    return json.loads(LastTimetable.objects.get(user=user).lastTimetable)


def get_moved_location(new_timetable, last_activity):
    for a_type in ("school", "extra"):  # All keys are str
        for week in new_timetable[a_type]:
            for day in new_timetable[a_type][week]:
                for hour in new_timetable[a_type][week][day]:
                    if isinstance(new_timetable[a_type][week][day][hour], dict):  # If it is an activity
                        if new_timetable[a_type][week][day][hour]['title'] == last_activity['title']:
                            if 'type' in last_activity.keys():
                                if new_timetable[a_type][week][day][hour]['type'] == last_activity['type']:
                                    return week, day, hour
                            else:
                                return week, day, hour


def add_difference(differences, before_location, moved_location, last_activity):
    if moved_location is None:
        moved_location = ("null", "null", "null")
    if 'type' in last_activity.keys():
        differences.append(
            {"i_week": int(before_location[0]), "i_day": before_location[1], "i_hour": int(before_location[2]),
             "n_week": moved_location[0], "n_day": moved_location[1], "n_hour": moved_location[2],
             "title": last_activity['title'], "type": last_activity['type']})
    else:
        differences.append({"i_week": before_location[0], "i_day": before_location[1], "i_hour": before_location[2],
                            "n_week": moved_location[0], "n_day": moved_location[1], "n_hour": moved_location[2],
                            "title": last_activity['title']})


def same_activity(last_activity, new_activity):
    return last_activity['title'] == new_activity['title'] and last_activity['type'] == new_activity['type'] and \
           last_activity['day'] == new_activity['day'] and last_activity['start_time'] == new_activity['start_time'] and \
           last_activity['frequency'] == new_activity['frequency']


def dup_diff(diff):
    return diff['i_week'] == diff['n_week'] and diff['i_day'] == diff['n_day'] and (
                diff['i_hour'] == diff['n_hour'] or diff['i_hour'] - 1 == diff['n_hour'])


def get_differences(last_timetable: dict, generated_timetable: dict):
    differences = []
    for a_type in ("school", "extra"):  # All keys are str
        for week in last_timetable[a_type]:
            for day in last_timetable[a_type][week]:
                for hour in last_timetable[a_type][week][day]:
                    last_activity = last_timetable[a_type][week][day][hour]
                    if isinstance(last_activity, dict):  # Means that is an activity
                        new_activity = generated_timetable[a_type][int(week)][day][int(hour)]  # Has some keys int
                        if isinstance(new_activity, dict):  # If it is an activity
                            if new_activity['id'] == last_activity['id'] or same_activity(last_activity,
                                                                                          new_activity):  # If they are the same exact activity
                                continue
                            else:  # If they are not
                                moved_location = get_moved_location(generated_timetable,
                                                                    last_activity)  # Find where it moved
                                before_location = (week, day, hour)
                                add_difference(differences, before_location, moved_location, last_activity)
                        else:  # Is either blocked or null | Either case it moved
                            moved_location = get_moved_location(generated_timetable,
                                                                last_activity)  # Find where it moved
                            before_location = (week, day, hour)
                            add_difference(differences, before_location, moved_location, last_activity)
    diffs = []
    for diff in differences:
        if not dup_diff(diff) and diff['i_hour'] % 2 == 0 and (diff['i_week'] == diff['n_week'] or diff['n_week']=='null'):
            diffs.append(diff)
    return diffs
