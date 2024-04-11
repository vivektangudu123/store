from myapp.models import StoreStatus, StoreTimezone, StoreSchedule
import pandas as pd
import pytz
from datetime import datetime
from .schedule import get_schedule
from .timezone import get_timezone
from .change_time import change_time
from .cal import *

def generate_csv_for_store(store_id):
    # print(store_id)
    store_status_data = StoreStatus.objects.filter(store_id=store_id)
    dff = list(store_status_data.values())
    df = pd.DataFrame(dff)
    zone=get_timezone(store_id)
    # print(zone)
    # print(df)
    status=change_time(df,zone)
    sche=get_schedule(store_id)
    # here we can change the code to find todays date and change to todays date.
    # max_date= datetime.now().date()
    # max_date = max_date - timedelta(days=1)
    max_date=max_date = max(obs['timestamp_utc'] for obs in status)
    uptime_last_day, downtime_last_day = calculate_business_uptime_downtime_for_day(status, sche,max_date)
    # print(uptime_last_day, downtime_last_day)
    current_time = datetime.now(tz=pytz.utc)
    desired_timezone_obj = pytz.timezone(zone)
    current_time = current_time.astimezone(desired_timezone_obj)
    current_time = current_time.replace(tzinfo=None)
    # print(current_time)
    uptime_last_hour, downtime_last_hour=calculate_business_uptime_downtime_for_past_hour(status,sche,max_date,current_time)
    # print(uptime_last_hour, downtime_last_hour)
    uptime_week=uptime_last_day
    downtime_week=downtime_last_day
    for i in range(1,7):
        max_date_datetime = datetime.strptime(max_date, '%Y-%m-%d %H:%M:%S')
        cal_date = max_date_datetime - timedelta(days=i)
        cal_date_str = cal_date.strftime('%Y-%m-%d %H:%M:%S')
        # print(cal_date_str)
        a,b=calculate_business_uptime_downtime_for_day(status, sche,cal_date_str)
        uptime_week+=a
        downtime_week+=b
        # print(a,b)
        # print("\n")
    uptime_week=round(uptime_week, 2)
    downtime_week=round( downtime_week, 2)

    # print(uptime_week,downtime_week)
    results=[]
    results.append(store_id)
    results.append(uptime_last_hour)
    results.append(uptime_last_day)
    results.append(uptime_week)
    results.append(downtime_last_hour)
    results.append(downtime_last_day)
    results.append(downtime_week)
    print(sche)
    return results