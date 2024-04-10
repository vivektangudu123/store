from django.db import models

class StoreStatus(models.Model):
    store_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    timestamp_utc = models.CharField(max_length=50) 

class StoreTimezone(models.Model):
    store_id = models.CharField(max_length=100)
    timezone_str = models.CharField(max_length=100)

class StoreSchedule(models.Model):
    store_id = models.CharField(max_length=100)
    day = models.CharField(max_length=100)
    start_time_local = models.CharField(max_length=50)  
    end_time_local = models.CharField(max_length=50)    

class Report(models.Model):
    reportid = models.CharField(max_length=50, primary_key=True)
    status = models.IntegerField()
    report_url = models.FileField(upload_to="reports",null=True,blank=True)