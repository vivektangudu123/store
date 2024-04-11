from datetime import datetime,timedelta

def parse_timestamp(timestamp):
    return datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

def filter_by_date(observations, desired_date):
    desired_date =parse_timestamp(desired_date).date()
    filtered_observations = []
    for observation in observations:
        observation_date_str = observation[2] 
        observation_date = datetime.strptime(observation_date_str, '%Y-%m-%d %H:%M:%S').date()
        if observation_date == desired_date:
            filtered_observations.append(observation)
            
    return filtered_observations

def calculate_business_uptime_downtime_for_day(observations, business_hours,max_date):
    total_uptime = 0
    total_downtime = 0
    last_observation_time = None
    filtered_observations=filter_by_date(observations,max_date)
    filtered_observations.sort(key=lambda obs: obs["timestamp_utc"])
    max_date_obj = parse_timestamp(max_date)
    weekday = max_date_obj.weekday()
    menu_hours = business_hours[weekday]
    opening_time = datetime.strptime(menu_hours[1], '%H:%M:%S').time()
    closing_time = datetime.strptime(menu_hours[2], '%H:%M:%S').time()
    
    opening_datetime = datetime.combine(max_date_obj.date(), opening_time)
    closing_datetime = datetime.combine(max_date_obj.date(), closing_time)
    
    filtered_observations = [obs for obs in filtered_observations if opening_datetime.time() <= parse_timestamp(obs["timestamp_utc"]).time() < closing_datetime.time()]
    total_obs = len(filtered_observations)
    # print(filtered_observations)

    if total_obs == 0:
        return 0, 0
    
    last_observation_time = parse_timestamp(filtered_observations[0]["timestamp_utc"])
    latest_status = filtered_observations[0]["status"]
    
    for i in range(1, total_obs):
        current_observation_time = parse_timestamp(filtered_observations[i]["timestamp_utc"])
        if latest_status == "active":
            total_uptime += (current_observation_time - last_observation_time).total_seconds()
        else:
            total_downtime += (current_observation_time - last_observation_time).total_seconds()
        last_observation_time = current_observation_time
        latest_status = filtered_observations[i]["status"]

    if latest_status == "active":
        total_uptime += (closing_datetime - last_observation_time).total_seconds()
    else:
        total_downtime += (closing_datetime - last_observation_time).total_seconds()

    return round(total_uptime / 3600, 2), round(total_downtime / 3600, 2)

def calculate_business_uptime_downtime_for_past_hour(observations, business_hours, max_date, current_time):
    total_uptime = 0
    total_downtime = 0
    last_observation_time = None
    filtered_observations=filter_by_date(observations,max_date)
    filtered_observations.sort(key=lambda obs: obs["timestamp_utc"])
    max_date_obj = parse_timestamp(max_date)
    weekday = max_date_obj.weekday()
    menu_hours = business_hours[weekday]
    opening_time = datetime.strptime(menu_hours[1], '%H:%M:%S').time()
    closing_time = datetime.strptime(menu_hours[2], '%H:%M:%S').time()
    
    opening_datetime = datetime.combine(max_date_obj.date(), opening_time)
    closing_datetime = datetime.combine(max_date_obj.date(), closing_time)
    
    # Calculate the start time of the past hour
    past_hour_start = current_time - timedelta(hours=1)
    past_hour_end = current_time
    
    if(past_hour_start.time()>closing_time):
        return 0,0
    # Find the status just before the past hour starts
    status_before_past_hour = None
    for obs in observations:
        obs_time = parse_timestamp(obs["timestamp_utc"])
        if obs_time < past_hour_start:
            status_before_past_hour = obs["status"]
        else:
            break
    
    filtered_observations = [obs for obs in filtered_observations if past_hour_start <= parse_timestamp(obs["timestamp_utc"]) < past_hour_end]
    filtered_observations = [obs for obs in filtered_observations if opening_datetime.time() <= parse_timestamp(obs["timestamp_utc"]).time() < closing_datetime.time()]
    
    total_obs = len(filtered_observations)

    if total_obs == 0:
        if status_before_past_hour == "active":
            return 60, 0  
        else:
            return 0,60
    
    last_observation_time = parse_timestamp(filtered_observations[0]["timestamp_utc"])
    latest_status = filtered_observations[0]["status"]
    
    for i in range(1, total_obs):
        current_observation_time = parse_timestamp(filtered_observations[i]["timestamp_utc"])
        if latest_status == "active":
            total_uptime += (current_observation_time - last_observation_time).total_seconds()
        else:
            total_downtime += (current_observation_time - last_observation_time).total_seconds()
        last_observation_time = current_observation_time
        latest_status = filtered_observations[i]["status"]

    if latest_status == "active":
        total_uptime += (closing_datetime - last_observation_time).total_seconds()
    else:
        total_downtime += (closing_datetime - last_observation_time).total_seconds()

    return round(total_uptime / 60, 2), round(total_downtime / 60, 2)
