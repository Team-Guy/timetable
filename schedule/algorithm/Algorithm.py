import collections

from schedule.algorithm.Activity import Activity
from schedule.algorithm.Date import Date
import json
import datetime

# Version 1.x
# TODO: 1. What to output
# TODO: 2. Filters
# TODO: 3.  -Single exact data AND HIGH priority (Eg: Lab la care nu te lasa cu alte grupe, Dentist)
# TODO:     -Data exacta AND HIGH priority => pusi primii in orar (Eg: Lab) - ACTUAL: HIGH to LOW
# TODO:     -HIGH priority
# TODO:     -Data AND LOW priority
# TODO:     -LOW priority
# Indici: toate orele in orar VS respectarea filterlor | astea sunt eventual cele 2 orare pe care le putem genera
# Nu o sa se poata genera mai multe orare cu acelasi input.


def put_free(program, duration, msg):
    for p_week in program.keys():
        for p_day in program[p_week].keys():
            for p_hour in program[p_week][p_day].keys():
                empty = True
                for p_interval in range(p_hour, p_hour + duration):
                    if program[p_week][p_day][p_interval] is not None:
                        empty = False
                        break
                if empty:
                    for p_interval in range(p_hour, p_hour + duration):
                        program[p_week][p_day][p_interval] = msg
                    return 1
    return 0


def put_day(program, duration, a_day, msg):
    for p_week in program.keys():
        for p_hour in program[p_week][a_day].keys():
            empty = True
            for p_interval in range(p_hour, p_hour + duration):
                if program[p_week][a_day][p_interval] is not None:
                    empty = False
                    break
            if empty:
                for p_interval in range(p_hour, p_hour + duration):
                    program[p_week][a_day][p_interval] = msg
                return 1
    return 0


def put_day_hour(program, duration, a_day, a_hour, msg):
    for p_week in program.keys():
        empty = True
        for p_interval in range(a_hour, a_hour + duration):
            if program[p_week][a_day][p_interval] is not None:
                empty = False
                break
        if empty:
            for p_interval in range(a_hour, a_hour + duration):
                program[p_week][a_day][p_interval] = msg
            return 1
    return 0


def put_week_day_hour(program, duration, a_week, a_day, a_hour, msg):
    for p_interval in range(a_hour, a_hour + duration):
        if program[a_week][a_day][p_interval] is not None:
            return 0
    for p_interval in range(a_hour, a_hour + duration):
        program[a_week][a_day][p_interval] = msg
    return 1


def output_json(schedule):
    output = {}
    for o_week in schedule.keys():
        output[o_week] = {}
        for o_day in schedule[o_week]:
            output[o_week][o_day] = {}
            for hour in schedule[o_week][o_day]:
                if schedule[o_week][o_day][hour] is not None:
                    output[o_week][o_day] = schedule[o_week][o_day][hour]
    return output


activities = {}
days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

with open('input.txt') as json_file:
    data = json.load(json_file)

for week in data:
    for day in data[week]:
        for activity in data[week][day]:
            name = activity['title']
            a_type = activity['type']
            start_time = datetime.time(int(activity['start_time'].split(":")[0])).hour
            date = Date(day, start_time, activity['duration'], activity['location'])
            if (name, a_type, week) in activities.keys():
                activities[(name, a_type, week)].dates.append(date)
            else:
                priority = activity['priority']
                if priority == "HIGH":
                    priority = 3
                elif priority == "MEDIUM":
                    priority = 2
                elif priority == "LOW":
                    priority = 1
                else:
                    priority = 0
                activities[(name, a_type, week)] = Activity(name=name, activity_type=a_type, dates=[date],
                                                            priority=priority, week=week, activity_id=activity['id'])

intervals = {}
for i in range(8, 20):
    intervals[i] = None

weeks = {1: {'monday': intervals.copy(), 'tuesday': intervals.copy(), 'wednesday': intervals.copy(),
             'thursday': intervals.copy(), 'friday': intervals.copy()},
         2: {'monday': intervals.copy(), 'tuesday': intervals.copy(), 'wednesday': intervals.copy(),
             'thursday': intervals.copy(), 'friday': intervals.copy()}
         }


activities = sorted(activities.items(), key=lambda kv: kv[1].priority, reverse=True)

# noinspection PyTypeChecker
activities = collections.OrderedDict(activities)


for activity in activities:
    for date in activities[activity].dates:
        if activities[activity].week is None:
            if date.day is None:
                if date.start_hour is None:
                    put_free(weeks, date.duration, activities[activity].name + " " + activities[activity].type)
            else:
                if date.startHour is None:
                    put_day(weeks, date.duration, date.day, activities[activity].name + " " + activities[activity].type)
                else:
                    put_day_hour(weeks, date.duration, date.day, date.start_hour,
                                 activities[activity].name + activities[activity].type)

        elif weeks[activities[activity].week][date.day][date.start_hour] is None:
            put_week_day_hour(weeks, date.duration, activities[activity].week, date.day, date.start_hour,
                              str(activities[activity].id) + "|" + str(activities[activity].week))
            break

with open('output.txt', 'w') as outfile:
    json.dump(weeks, outfile)
