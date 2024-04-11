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

def import_store_status(file_path):
    file_path = '/Users/vivek/Downloads/store_status.csv'
    file_path = '/Users/vivek/Downloads/store_status.csv'
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            StoreStatus.objects.create(
                store_id=row['store_id'],
                status=row['status'],
                timestamp_utc=row['timestamp_utc']
            )
    return 1
def import_store_schedule(file_path):
    file_path = '/Users/vivek/Downloads/Menu_hours.csv'
    file_path = '/Users/vivek/Downloads/Menu_hours.csv'
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            StoreSchedule.objects.create(
                store_id=row['store_id'],
                day=row['day'],
                start_time_local=row['start_time_local'],
                end_time_local=row['end_time_local']
            )
    return 1
def import_store_timezone(file_path):
    file_path = '/Users/vivek/Downloads/bq-results-20230125-202210-1674678181880.csv'
    file_path = '/Users/vivek/Downloads/bq-results-20230125-202210-1674678181880.csv'
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            StoreTimezone.objects.create(
                store_id=row['store_id'],
                timezone_str=row['timezone_str']
            )
    return 1

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
    
    report.status = 1
    report.save()
def insert_data(request):
    time_zone_csv=os.getenv('time_zone_csv')
    # print(time_zone_csv)
    menu_hours_csv=os.getenv('menu_hours_csv')
    store_status_csv=os.getenv('store_status_csv')
    # import_store_status(store_status_csv)
    # import_store_schedule(menu_hours_csv)
    # import_store_timezone(time_zone_csv)
    results = []
    t1 = threading.Thread(target=lambda: results.append(import_store_status(store_status_csv)))
    t2 = threading.Thread(target=lambda: results.append(import_store_schedule(menu_hours_csv)))
    t3 = threading.Thread(target=lambda: results.append(import_store_timezone(time_zone_csv)))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    a=0
    for i in range(3):
        a=a+results[i]
    if( a==3):
        return JsonResponse({'Success':True})
    else:
        return JsonResponse({'Success':False})
    
def generate_report(unique_store_ids, reportid):
    report_data = []
    i = 0
    for store in unique_store_ids:
        if i > 150:
            break
        store_id_str = str(store['store_id'])
        report_data.append(generate_csv_for_store(store_id_str))
        i += 1
    generate_report_csv(report_data, reportid)
    report = Report.objects.get(reportid=reportid)
    report.status = 1
    report.save()
    
@api_view(['GET'])
def getRoute(request):
    routes = [
        'GET /insert',
        'GET /trigger_report',
        'GET /get_report'
    ]
    return JsonResponse({'routes': routes})


    # return JsonResponse({'Success':True})


@api_view(['GET'])
def trigger_report(request):
        unique_store_ids = StoreStatus.objects.values('store_id').distinct()
        reportid=secrets.token_urlsafe(16)
        report = Report.objects.create(reportid=reportid, status=0)
        
        report_data=[]
        i=0
        for store in unique_store_ids:
            if(i>150):
                break
            store_id_str = str(store['store_id'])
            print(store_id_str)
            report_data.append(generate_csv_for_store(store_id_str))
            i=i+1
        print(report.reportid)
        generate_report_csv(report_data,report)
        report.status=1
        return JsonResponse({"report_id": report.reportid})


@api_view(['GET'])
def getReport(request, pk):
    try:
        report = Report.objects.get(reportid=str(pk))
        if report.status == 1:
            report_file_path = os.path.join(settings.MEDIA_ROOT, report.report_url.name)
            if os.path.exists(report_file_path):
                with open(report_file_path, 'r', newline='') as csvfile:
                    response = HttpResponse(content_type='text/csv')
                    # response['Content-Disposition'] = 'attachment; filename="data.csv"'

                    csv_reader = csv.reader(csvfile)
                    writer = csv.writer(response)
                    for row in csv_reader:
                        writer.writerow(row)

                # json_data = df.to_json(orient='records')
                return response
            else:
                return Response(status=404, data={"error": "Report file not found"})

        else:
            return Response(status=200, data={"status": "Running"})
    except Report.DoesNotExist:
        return Response(status=404, data={"error": "Report not found"})
    except Exception as e:
        return Response(status=500, data={"error": str(e)})
