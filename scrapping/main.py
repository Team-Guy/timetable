import datetime

import requests
from bs4 import BeautifulSoup

from schedule.models import *
from scrapping.day import Day
from scrapping.link import Link
from scrapping.processor import *


def convertToModel(ora):
    for grupa in ora.grupe:
        a = SchoolActivity(
            title=ora.text,
            professor=ora.profesor,
            location=ora.locatie,
            group=grupa,
            duration=ora.duration,
            frequency=ora.frequency,
            start_time=datetime.time(ora.startHour, 0, 0),
            type=ora.tip,
            priority=ora.priority,
            day=ora.day
        )
        a.save()


def convertToModels(toate):
    for zi in toate:
        for ora in zi:
            convertToModel(ora)


def getInfo(link):
    result = requests.get(link)

    soup = BeautifulSoup(result.content, 'lxml')

    rows = soup.find_all('tr')
    rows.pop(0)
    rows.pop(0)
    toate = []
    groups = getGroups(rows.pop(0))
    for day in Day.days.values():
        toate.append(processDay(rows[:12], day, groups))
        rows.pop(0)
        rows = rows[12:]
    convertToModels(toate)


def getAll():
    SchoolActivity.objects.all().delete()
    for link in Link.LINKS:
        getInfo(link)
