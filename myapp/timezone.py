from myapp.models import StoreStatus, StoreTimezone, StoreSchedule
import pandas as pd
def get_timezone(store_id):
    store_timezone_data = StoreTimezone.objects.filter(store_id=store_id)
    dff = list(store_timezone_data.values())
    df = pd.DataFrame(dff)
    if(len(df)==0):
        return "America/Chicago"
    else:
        return df.iloc[0]['timezone_str']
