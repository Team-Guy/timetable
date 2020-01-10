import copy

from dbutils.faculty_activity import FacultyActivity
from dbutils.school_utils import get_faculty_activities, get_all_faculty_activities, get_user_preferences
from dbutils.extra_utils import get_extra_activities
from schedule.algorithm.activity import Activity
from schedule.algorithm.date import Date
#       The output will be 2 schedules:
#       1. First one will put all the high priority activities and try to respect as many
#       filters as possible. Will output the computed schedule and a list of activities that were not introduced and
#       a list of filters that were violated in order to put the high priority activities.
#       2. Second one will put all activities and try to respect as many filters as possible. Same output.
#       The algorithm will take into account the location of activities when building the schedule
from scrapping.serie import Serie


# TODO: 1. Filters
#           - Eg: optional: few pauses between groups of activities
#       2. Take into consideration the location of activities
#       3. Change output to whole object, search in all_activities for the correct id for each activity in schedule
# ASK: 1. Some activities will have their fields changed, what will happen in the DB
# Version 1.0
#       Sort by priority the activities (HIGH -> LOW) and put them on the first available interval
#       The same input will generate the same schedule (Greedy)
# Version 2.0
#       The sorting has been altered to:
#       1. Single exact data AND HIGH priority (Eg: Lab la care nu te lasa cu alte grupe, Dentist)
#       2. Date exacta AND HIGH priority => pusi primii in orar (Eg: Lab) - ACTUAL: HIGH to LOW
#       3. HIGH priority
#       4. Data AND LOW priority
#       5. LOW priority
#       DONE:
#       Filter 1: fara activitati inainte /dupa de ora X per day
#       NOTES:
#       This algorithms sucks because: we will need to keep all ids of the activities that we group together and we will
#       need to pay attention when we make the output to specify the correct


def lock_program_filter_1(program, schedule_filters):
    lock_before = schedule_filters['before_x']
    lock_after = schedule_filters['after_x']
    for p_week in lock_before.keys():
        for p_day in lock_before[p_week].keys():
            for p_interval in range(8, lock_before[p_week][p_day]):
                if program[p_week][p_day][p_interval] is None:
                    program[p_week][p_day][p_interval] = 'blocked'

    for p_week in lock_after.keys():
        for p_day in lock_after[p_week].keys():
            for p_interval in range(lock_after[p_week][p_day], 20):
                if program[p_week][p_day][p_interval] is None:
                    program[p_week][p_day][p_interval] = 'blocked'


def unlock_program_filter_1(program):
    for p_week in program.keys():
        for p_day in program[p_week].keys():
            program[p_week][p_day] = {k: None if program[p_week][p_day][k] == 'blocked' else program[p_week][p_day][k]
                                      for k in program[p_week][p_day].keys()}


def exact_data(dates, ed_week):
    if ed_week is None:
        return False
    for ed_data in dates:
        if ed_data.day is None or ed_data.start_hour is None:
            return False
    return True


def sort_activities(l_activities):
    one_data_high_priority = {}
    exact_data_high_priority = {}
    high_priority = {}
    exact_data_low_priority = {}
    low_priority = {}
    for s_activity in l_activities:
        if len(l_activities[s_activity].dates) == 1 and l_activities[s_activity].priority == 3 and exact_data(
                l_activities[s_activity].dates, l_activities[s_activity].week):
            one_data_high_priority[s_activity] = l_activities[s_activity]
        elif l_activities[s_activity].priority == 3 and exact_data(l_activities[s_activity].dates,
                                                                   l_activities[s_activity].week):
            exact_data_high_priority[s_activity] = l_activities[s_activity]
        elif l_activities[s_activity].priority == 3:
            high_priority[s_activity] = l_activities[s_activity]
        elif l_activities[s_activity].priority == 1 and exact_data(l_activities[s_activity].dates,
                                                                   l_activities[s_activity].week):
            exact_data_low_priority[s_activity] = l_activities[s_activity]
        else:
            low_priority[s_activity] = l_activities[s_activity]
    return_dict = dict(one_data_high_priority)
    return_dict.update(exact_data_high_priority)
    return_dict.update(high_priority)
    return_dict.update(exact_data_low_priority)
    return_dict.update(low_priority)
    return return_dict


def put_free(program, duration, msg):
    """
    Finds the first interval with the length equal to duration and puts the activity there.
    :param program: The schedule that is the output of the algorithm - Dictionary
    :param duration: The duration of the activity - Integer
    :param msg: The activity to be put on the program  containing the name of the activity and the type - String
    :return: 1 if the such an interval is found, else 0
    """
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
    """
    Finds the first free interval (equal to the duration) in a specific day.
    :param program: The schedule that is the output of the algorithm - Dictionary
    :param duration: The duration of the activity - Integer
    :param a_day: The day that the activity takes place - Expected value: {monday-friday} - String
    :param msg: The activity to be put on the program  containing the name of the activity and the type - String
    :return: 1 if the such an interval is found, else 0
    """
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
    """
    Finds the week (1 or 2) that has a free interval for the activity
    :param program: The schedule that is the output of the algorithm - Dictionary
    :param duration: The duration of the activity - Integer
    :param a_day: The day that the activity takes place - Expected value: {monday-friday} - String
    :param a_hour: The start hour of the activity - Expected value: {8-19} - Integer
    :param msg: The activity to be put on the program  containing the name of the activity and the type - String
    :return: 1 if the such an interval is found, else 0
    """
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


def put_week_day_hour(program, duration, a_week, a_day, a_hour, tuple_msg, a_filters):
    """
    Tries to put the activity at a specific week, day, hour
    :param program: The schedule that is the output of the algorithm - Dictionary
    :param duration: The duration of the activity - Integer
    :param a_week: The week that the activity takes place - Expected value: {1, 2} - Integer
    :param a_day: The day that the activity takes place - Expected value: {monday-friday} - String
    :param a_hour: The start hour of the activity - Expected value: {8-19} - Integer
    :param msg: The activity to be put on the program  containing the name of the activity and the type - String
    :param a_filters: The filters that we use to optimize the algorithm for the user
    :return: 1 if the such an interval is found, else 0
    """
    activity = tuple_msg[0]
    if a_filters[2]['active']:
        if a_day + '-max' in a_filters[2]['max-per-day'][a_week].keys():
            # print(msg)
            # print(a_day + '-current: ' + str(a_filters[2]['max-per-day'][a_week][a_day + '-current']))
            # print(a_day + '-max: ' + str(a_filters[2]['max-per-day'][a_week][a_day + '-max']))
            if a_filters[2]['max-per-day'][a_week][a_day + '-max'] <= a_filters[2]['max-per-day'][a_week][a_day +
                                                                                                          '-current']:
                return 0
            elif a_filters[2]['max-per-day'][a_week][a_day + '-current'] + duration > \
                    a_filters[2]['max-per-day'][a_week][a_day + '-max']:
                return 0

            # print(a_day + '-current: ' + str(a_filters[2]['max-per-day'][a_week][a_day + '-current']))
            # print("\n\n")

    for p_interval in range(a_hour, a_hour + duration):
        if program[a_week][a_day][p_interval] is not None:
            return 0
    for p_interval in range(a_hour, a_hour + duration):
        program[a_week][a_day][p_interval] = (activity.__dict__, tuple_msg[1])

    a_filters[2]['max-per-day'][a_week][a_day + '-current'] += duration
    return activity.id


def put_week_day(program, duration, a_week, a_day, msg):
    for p_hour in program[a_week][a_day].keys():
        empty = True
        for p_interval in range(p_hour, p_hour + duration):
            if program[a_week][a_day][p_interval] is not None:
                empty = False
                break
        if empty:
            for p_interval in range(p_hour, p_hour + duration):
                program[a_week][a_day][p_interval] = msg
            return 1
    return 0


def put_week(program, duration, a_week, msg):
    for p_day in program[a_week].keys():
        for p_hour in program[a_week][p_day].keys():
            empty = True
            for p_interval in range(p_hour, p_hour + duration):
                if program[a_week][p_day][p_interval] is not None:
                    empty = False
                    break
            if empty:
                for p_interval in range(p_hour, p_hour + duration):
                    program[a_week][p_day][p_interval] = msg
                return 1
    return 0


def get_object(activity_id, all_activities):
    for activity in all_activities:
        if activity.id == activity_id:
            return activity


def put_in_program(a_activity, a_activities, a_weeks, a_filters_dict, a_all_activities):
    result = 0
    for p_date in a_activities[a_activity].dates:
        if a_activities[a_activity].week is None:
            if p_date.day is None:
                if p_date.start_hour is None:
                    result = put_free(a_weeks, p_date.duration,
                                      # Bafta coae
                                      # str(a_activities[a_activity].ids[a_activities[a_activity].dates.index(p_date)]))
                                      a_activities[a_activity].name + ' ' + a_activities[a_activity].type)
            else:
                if p_date.startHour is None:
                    result = put_day(a_weeks, p_date.duration, p_date.day,
                                     a_activities[a_activity].name + ' ' + a_activities[a_activity].type)

                else:
                    result = put_day_hour(a_weeks, p_date.duration, p_date.day, p_date.start_hour,
                                          a_activities[a_activity].name + ' ' + a_activities[a_activity].type)

        elif a_activities[a_activity].week is not None:
            if p_date.day is None:
                if p_date.start_hour is None:
                    result = put_week(a_weeks, p_date.duration, a_activities[a_activity].week,
                                      str(a_activities[a_activity].ids[a_activities[a_activity].dates.index(p_date)]))
            else:
                if p_date.start_hour is not None:
                    obj = get_object(a_activities[a_activity].ids[a_activities[a_activity].dates.index(p_date)],
                                     a_all_activities)
                    result += put_week_day_hour(a_weeks, p_date.duration, a_activities[a_activity].week, p_date.day,
                                                p_date.start_hour,
                                                (obj, str(a_activities[a_activity].extra)), a_filters_dict)
                    # str(a_activities[a_activity].name) + " " + a_activities[
                    #     a_activity].type + '|' + str(a_activities[a_activity].extra),
                    # a_filters_dict)

                else:
                    result = put_week_day(a_weeks, p_date.duration, a_activities[a_activity].week, p_date.day,
                                          a_activities[a_activity].name + ' ' + a_activities[a_activity].type)

        if result != 0:
            return result
    return result


def are_filters_bypassed(activity_id, bypass_list):
    filters = []
    for a_id, a_filter in bypass_list:
        if a_id == activity_id:
            filters.append(a_filter)
    return filters


def run(username):
    pref = get_user_preferences(username)

    filters_dict = {
        1: {
            'active': True,
            'before_x': {1: {'Monday': pref.mondayStart.hour, 'Tuesday': pref.tuesdayStart.hour,
                             'Wednesday': pref.wednesdayStart.hour,
                             'Thursday': pref.thursdayStart.hour, 'Friday': pref.fridayStart.hour
                             },
                         2: {'Monday': pref.mondayStart.hour, 'Tuesday': pref.tuesdayStart.hour,
                             'Wednesday': pref.wednesdayStart.hour,
                             'Thursday': pref.thursdayStart.hour, 'Friday': pref.fridayStart.hour
                             }
                         },
            'after_x': {
                1: {'Monday': pref.mondayEnd.hour, 'Tuesday': pref.tuesdayEnd.hour, 'Wednesday': pref.wednesdayEnd.hour,
                    'Thursday': pref.thursdayEnd.hour, 'Friday': pref.fridayEnd.hour
                    },
                2: {'Monday': pref.mondayEnd.hour, 'Tuesday': pref.tuesdayEnd.hour, 'Wednesday': pref.wednesdayEnd.hour,
                    'Thursday': pref.thursdayEnd.hour, 'Friday': pref.fridayEnd.hour
                    }
            }
        },
        2: {
            'active': True,
            'max-per-day': {1: {'Monday-max': pref.mondayMax, 'Tuesday-max': pref.tuesdayMax,
                                'Wednesday-max': pref.wednesdayMax, 'Thursday-max': pref.thursdayMax,
                                'Friday-max': pref.fridayMax,
                                'Monday-current': 0, 'Tuesday-current': 0, 'Wednesday-current': 0,
                                'Thursday-current': 0, 'Friday-current': 0
                                },
                            2: {'Monday-max': pref.mondayMax, 'Tuesday-max': pref.tuesdayMax,
                                'Wednesday-max': pref.wednesdayMax, 'Thursday-max': pref.thursdayMax,
                                'Friday-max': pref.fridayMax,
                                'Monday-current': 0, 'Tuesday-current': 0, 'Wednesday-current': 0,
                                'Thursday-current': 0, 'Friday-current': 0
                                }
                            },
        }
    }

    activities = {}
    '''
    From server
    '''
    faculty_activities = get_all_faculty_activities(username)
    extra_activities = get_extra_activities(username)
    all_activities = []
    for activity in faculty_activities:
        all_activities.extend(get_faculty_activities(subject=activity.title, type=activity.type, spec=Serie.IE3))
    for activity in extra_activities:
        all_activities.append(activity)
    for activity in all_activities:
        if isinstance(activity, FacultyActivity):
            a_type = activity.type
            extra = False
        else:
            a_type = ''
            extra = True
        a_name = activity.title
        a_week = []
        if activity.frequency == "full":
            a_week.append(1)
            a_week.append(2)
        elif activity.frequency == "par":
            a_week.append(2)
        else:
            a_week.append(1)

        date = Date(activity.day, activity.start_time.hour, activity.duration, activity.location)

        for week in a_week:
            if (a_name, a_type, week) in activities.keys():
                activities[(a_name, a_type, week)].dates.append(date)
                activities[(a_name, a_type, week)].ids.append(activity.id)
            else:
                priority = activity.priority

                if priority == "HIGH":
                    priority = 3
                elif priority == "MEDIUM":
                    priority = 2
                elif priority == "LOW":
                    priority = 1
                else:
                    priority = 0
                activities[(a_name, a_type, week)] = Activity(name=a_name, activity_type=a_type,
                                                              dates=[date], extra=extra, priority=priority, week=week,
                                                              activity_id=activity.id)

    """
    Building some useful objects
    """

    intervals = {}
    for i in range(8, 20):
        intervals[i] = None
    # intervals['-'] = None

    weeks = {1: {'Monday': intervals.copy(), 'Tuesday': intervals.copy(), 'Wednesday': intervals.copy(),
                 'Thursday': intervals.copy(), 'Friday': intervals.copy()},
             2: {'Monday': intervals.copy(), 'Tuesday': intervals.copy(), 'Wednesday': intervals.copy(),
                 'Thursday': intervals.copy(), 'Friday': intervals.copy()}
             }

    output = {"school": copy.deepcopy(weeks), "extra": copy.deepcopy(weeks)}

    # activities = sorted(activities.items(), key=lambda kv: kv[1].priority, reverse=True)
    activities = sort_activities(activities)
    # activities = collections.OrderedDict(activities)

    """
    Core of the algorithm
    Tries to put an activity in the program. If there is no information about when the activity should take place, the
    algorithm puts the activity on the first free available interval. If a day is specified it will try to
    put the activity in that day either on week 1 or 2 
    """
    if filters_dict[1]['active']:
        lock_program_filter_1(weeks, filters_dict[1])

    bypassed_filters = []
    unable_to_put = []

    for activity in activities:
        found = 0
        found += put_in_program(activity, activities, weeks, filters_dict, all_activities)
        if found == 0 and activities[activity].priority == 3:
            found_inner = 0
            unlock_program_filter_1(weeks)
            found_inner += put_in_program(activity, activities, weeks, filters_dict, all_activities)
            lock_program_filter_1(weeks, filters_dict[1])
            if found_inner != 0:
                bypassed_filters.append((found_inner, 1))
            found += found_inner
        if found == 0 and activities[activity].priority == 3:
            found_inner = 0
            filters_dict[2]['active'] = False
            found_inner += put_in_program(activity, activities, weeks, filters_dict, all_activities)
            filters_dict[2]['active'] = True
            if found_inner != 0:
                bypassed_filters.append((found_inner, 2))
            found += found_inner
        if found == 0 and activities[activity].priority == 3:
            found_inner = 0
            filters_dict[2]['active'] = False
            unlock_program_filter_1(weeks)
            found_inner += put_in_program(activity, activities, weeks, filters_dict, all_activities)
            lock_program_filter_1(weeks, filters_dict[1])
            filters_dict[2]['active'] = True
            if found_inner != 0:
                bypassed_filters.append((found_inner, 1))
                bypassed_filters.append((found_inner, 2))
            found += found_inner
        if found == 0:
            unable_to_put.append(activities[activity].name + ";" + activities[activity].type)

    output_bypass_filters = {'faculty': {}, 'extra': {}}
    for week in weeks:
        for day in weeks[week]:
            for hour in weeks[week][day]:
                if weeks[week][day][hour] == "blocked":
                    # noinspection PyTypeChecker
                    output["extra"][week][day][hour] = "Blocked by filter"
                    # noinspection PyTypeChecker
                    output["school"][week][day][hour] = "Blocked by filter"
                elif weeks[week][day][hour] is None:
                    output["extra"][week][day][hour] = None
                    output["school"][week][day][hour] = None
                else:
                    tuple_msg = weeks[week][day][hour]
                    activity_id = tuple_msg[0]
                    extra = tuple_msg[1]
                    activities_bypassed = are_filters_bypassed(activity_id, bypassed_filters)
                    if extra == 'False':
                        if len(activities_bypassed) > 0:
                            output_bypass_filters["school"][activity_id] = activities_bypassed
                        output["school"][week][day][hour] = activity_id
                        output["extra"][week][day][hour] = None
                    else:
                        if len(activities_bypassed) > 0:
                            output_bypass_filters["extra"][activity_id] = activities_bypassed
                        output["extra"][week][day][hour] = activity_id
                        output["school"][week][day][hour] = None
                # print(output["extra"][week][day][hour] + "\n\n")
    output['bypass'] = output_bypass_filters
    output['unable'] = unable_to_put

    print(output_bypass_filters)

    return output
    # with open('output.txt', 'w') as outfile:
    #     json.dump(weeks, outfile)
