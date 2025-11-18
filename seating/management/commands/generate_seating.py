from django.core.management.base import BaseCommand
from seating.services.seating_generator import generate_seating_for_date
import datetime

class Command(BaseCommand):
    help = "Generate seating for a date: python manage.py generate_seating 2025-11-20 --capacity 90 --rooms 3"

    def add_arguments(self, parser):
        parser.add_argument('date', type=str, help='Exam date YYYY-MM-DD')
        parser.add_argument('--capacity', type=int, default=90)
        parser.add_argument('--rooms', type=int, default=0)
        parser.add_argument('--start', type=str, default='MC101')

    def handle(self, *args, **options):
        date = datetime.date.fromisoformat(options['date'])
        capacity = options['capacity']
        rooms = options['rooms']
        created = generate_seating_for_date(date, capacity, rooms or 999, start_room_code=options['start'])
        self.stdout.write(self.style.SUCCESS(f"Created {len(created)} seating entries"))
