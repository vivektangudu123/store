import pytz 
import pandas as pd

def change_time(df, value):
    target_timezone = pytz.timezone(value)
    if not pd.api.types.is_datetime64_any_dtype(df['timestamp_utc']):
        df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'], format='mixed')
    if df['timestamp_utc'].dt.tz is None:  
        df['timestamp_utc'] = df['timestamp_utc'].dt.tz_localize('UTC')
    df['timestamp_utc'] = df['timestamp_utc'].dt.tz_convert(target_timezone)
    df['timestamp_utc'] = df['timestamp_utc'].dt.strftime('%Y-%m-%d %H:%M:%S')
    observations = df[['id', 'status', 'timestamp_utc']].to_records(index=False)
    observations = list(observations)
    return observations
