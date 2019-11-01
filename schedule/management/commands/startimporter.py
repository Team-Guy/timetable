from django.core.management import BaseCommand

from scrapping.Link import Link
from scrapping.main import getInfo


class Command(BaseCommand):
    help = 'Start the scraper for the ubb timetable'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for data in Link.all:
            getInfo(data)
