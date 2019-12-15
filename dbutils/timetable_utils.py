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


def get_moved_location(generated_timetable, title, act_type):
    if act_type:
        for week in generated_timetable['faculty'].keys():
            for day in generated_timetable['faculty'][week].keys():
                for hour in generated_timetable['faculty'][week][day].keys():
                    if generated_timetable['faculty'][week][day][hour]['title'] == title \
                            and generated_timetable['faculty'][week][day][hour]['type'] == act_type:
                        return week, day, hour


def get_differences(last_timetable: dict, generated_timetable: dict):
    # last_timetable[--extra--][week][day][hour] == generated_timetable
    differences = list()
    # for extra in last_timetable.keys():
    #     for week in last_timetable[extra].keys():
    #         for day in last_timetable[extra][week].keys():
    #             for hour in last_timetable[extra][week][day].keys():
    #                 print(generated_timetable[extra][int(week)][day][int(hour)])
    #                 if last_timetable[extra][week][day][hour]['id'] != \
    #                         generated_timetable[extra][int(week)][day][int(hour)]['id']:
    #                     week, day, hour = get_moved_location(generated_timetable,
    #                                                          generated_timetable[extra][int(week)][day][int(hour)][
    #                                                              'title'],
    #                                                          generated_timetable[extra][int(week)][day][int(hour)].get(
    #                                                              'type'))
    #                     differences.append((generated_timetable[extra][int(week)][day][int(hour)]['title'], generated_timetable[extra][int(week)][day][int(hour)].get('type'), hour, day, week))
    # print(differences)