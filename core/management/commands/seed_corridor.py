from django.core.management.base import BaseCommand
import seed_data

class Command(BaseCommand):
    help = "Seeds initial Yamuna Expressway corridor pilot data for EV Share"

    def handle(self, *args, **options):
        self.stdout.write("Running EV Share corridor seed...")
        seed_data.seed_database()
        self.stdout.write(self.style.SUCCESS("Successfully seeded corridor data!"))
