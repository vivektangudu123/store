from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import csv
from myapp.models import StoreStatus, StoreTimezone, StoreSchedule,Report
from django.http import JsonResponse
import threading 
import secrets
from django.conf import settings
from myapp.utils import generate_csv_for_store
from django.http import HttpResponse
from django.http import JsonResponse
import time

def generate_report_csv(report_data, report):
    file_name = f"{report.reportid}.csv"
    file_path = os.path.join(settings.BASE_DIR, 'reports_csv', file_name)
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w+", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["store_id", "last_one_hour uptime(in minutes)", "last_one_hour downtime(in minutes)", "last_one_day uptime(in hours)", "last_one_day downtime(in hours)", "last_one_week uptime(in hours)", "last_one_week downtime(in hours)"])
        for data in report_data:
            csv_writer.writerow(data)
            
    report.report_url.save(file_name, open(file_path, "rb"))

@api_view(['GET'])
def getRoute(request):
    routes = [
        'GET /insert',
        'GET /trigger_report',
        'GET /get_report'
    ]
    return JsonResponse({'routes': routes})




@api_view(['GET'])
def trigger_report(request):
        unique_store_ids = StoreStatus.objects.values('store_id').distinct()
        reportid=secrets.token_urlsafe(16)
        report = Report.objects.create(reportid=reportid, status=0)
        
        report_data=[]
        i=0
        start_time = time.time()
        for store in unique_store_ids:
            if(i>5):
                break
            store_id_str = str(store['store_id'])
            print(store_id_str)
            report_data.append(generate_csv_for_store(store_id_str))
            i=i+1
        print(report.reportid)
        print()
        generate_report_csv(report_data,report)
        report.status=1
        report.save()
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Processing store took {execution_time} seconds")
        return JsonResponse({"report_id": report.reportid})








@api_view(['GET'])
def getReport(request, pk):
    try:
        report = Report.objects.get(reportid=str(pk))
        print(report.status)
        if report.status == 1:
            report_file_path = os.path.join(settings.MEDIA_ROOT, report.report_url.name)
            if os.path.exists(report_file_path):
                with open(report_file_path, 'r', newline='') as csvfile:
                    response = HttpResponse(content_type='text/csv')

                    csv_reader = csv.reader(csvfile)
                    writer = csv.writer(response)
                    for row in csv_reader:
                        writer.writerow(row)
                return response
            
            else:
                return Response(status=404, data={"error": "Report file not found"})

        else:
            return Response(status=200, data={"status": "Running"})
    except Report.DoesNotExist:
        return Response(status=404, data={"error": "Report not found"})
    except Exception as e:
        return Response(status=500, data={"error": str(e)})
