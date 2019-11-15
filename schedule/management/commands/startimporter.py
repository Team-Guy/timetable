from django.core.management import BaseCommand

from scrapping.main import getAll


class Command(BaseCommand):
    help = 'Start the scraper for the ubb timetable'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write('Started importing the subjects...')
        getAll()
        self.stdout.write('Finished importing the subjects...')
