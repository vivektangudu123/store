from django.core.management.base import BaseCommand
from myapp.models import StoreStatus, StoreTimezone, StoreSchedule
from myapp.utils import generate_csv_for_store
class Command(BaseCommand):
    help = 'Generate CSV file for store'

    def add_arguments(self, parser):
        self.stdout.write(self.style.SUCCESS('For a store.....'))
        # parser.add_argument('store_id', type=str, help='Store ID')


    def handle(self, *args, **kwargs):
        # store_id = kwargs['store_id']
        output_file_path = generate_csv_for_store("7150774588280614833")
        # self.stdout.write(self.style.SUCCESS(f'CSV file generated: {output_file_path}'))

