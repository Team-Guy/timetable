from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Start the scraper for the ubb timetable'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write('Importing ...')
