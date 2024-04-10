import csv
from django.core.management.base import BaseCommand
from myapp.models import StoreStatus, StoreTimezone, StoreSchedule
import pandas as pd
import requests
from io import StringIO
import gdown

class Command(BaseCommand):
    help = 'Import data from CSV files to SQLite'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Importing StoreStatus data...'))
        self.import_store_status()

        self.stdout.write(self.style.SUCCESS('Importing StoreTimezone data...'))
        self.import_store_timezone()

        self.stdout.write(self.style.SUCCESS('Importing StoreSchedule data...'))
        self.import_store_schedule()

    def import_store_status(self):
        url = 'https://drive.google.com/uc?export=download&id=1UIx1hVJ7qt_6oQoGZgb8B3P2vd1FD025'
        output_path = 'store_status.csv'

        gdown.download(url, output_path, quiet=False)

        df = pd.read_csv(output_path)

        for _, row in df.iterrows():
            StoreStatus.objects.create(
                store_id=row['store_id'],
                status=row['status'],
                timestamp_utc=row['timestamp_utc']
            )

        self.stdout.write(self.style.SUCCESS('StoreStatus data imported successfully.'))

    def import_store_timezone(self):
        
        url = 'https://drive.google.com/uc?export=download&id=101P9quxHoMZMZCVWQ5o-shonk2lgK1-o'
        output_path = 'time_zone.csv'
        gdown.download(url, output_path, quiet=False)
        df = pd.read_csv(output_path)

            
        for _, row in df.iterrows():
            StoreTimezone.objects.create(
                store_id=row['store_id'],
                timezone_str=row['timezone_str']
            )
        self.stdout.write(self.style.SUCCESS('Time_zone data imported successfully.'))

    def import_store_schedule(self):
        
        url = 'https://drive.google.com/uc?export=download&id=1va1X3ydSh-0Rt1hsy2QSnHRA4w57PcXg'
        output_path = 'schedule.csv'
        gdown.download(url, output_path, quiet=False)
        df = pd.read_csv(output_path)

        for  _,row in df.iterrows():
            StoreSchedule.objects.create(
                store_id=row['store_id'],
                day=row['day'],
                start_time_local=row['start_time_local'],
                end_time_local=row['end_time_local']
            )
        self.stdout.write(self.style.SUCCESS('Schedule data imported successfully.'))
        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))
