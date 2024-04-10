from myapp.models import StoreStatus, StoreTimezone, StoreSchedule
import pandas as pd
import pytz 
from .timezone import get_timezone
import datetime
def avg_time(timestamps):
    timestamps = [datetime.datetime.strptime(timestamp, '%H:%M:%S').time() for timestamp in timestamps]
    
    total_seconds = sum(timestamp.hour * 3600 + timestamp.minute * 60 + timestamp.second for timestamp in timestamps)
    
    average_seconds = total_seconds / len(timestamps)
    
    average_time = datetime.time(int(average_seconds / 3600), int((average_seconds % 3600) / 60), int(average_seconds % 60))
    
    average_time_str = average_time.strftime('%H:%M:%S')
    
    return average_time_str

def process_timetable(df):
    list_1=[]
    if(len(df)==0):
        for i in range(7):
            list_1.append((i,'00:00:00', '23:59:59'))
        return list_1
    list_1=[]
    hashmap = {}
    start_timestamps = []
    end_timestamps=[]
    co=0
    for i in range(7):
        hashmap[i]=False
    if(len(df)):
        for i in range(7):
            if(str(i) in df['day'].values):
                    ha = df[df['day'] == str(i)]
                    start_time = ha["start_time_local"].iloc[0]  
                    end_time = ha["end_time_local"].iloc[0]  
                    start_timestamps.append(start_time)
                    end_timestamps.append(end_time)
                    hashmap[i] = True
                    co=co+1
                    list_1.append((i, start_time, end_time))
    if(co!=7):
        average_start_timestamps = avg_time(start_timestamps)
        average_end_timestamps = avg_time(end_timestamps)
        for i in range(7):
            if (hashmap[i]==False):
                list_1.append((i, average_start_timestamps, average_start_timestamps))

    return list_1

def get_schedule(store_id):
    store_schedule_data = StoreSchedule.objects.filter(store_id=store_id)
    dff = list(store_schedule_data.values())
    df = pd.DataFrame(dff)
    lis=process_timetable(df)
    return lis