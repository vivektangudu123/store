# Store Monitoring

[](https://github.com/vivektangudu123/store)

 Deployed link:    [https://store-xnss.onrender.com/trigger_report/](https://store-xnss.onrender.com/trigger_report/)

Video link: 

[https://www.loom.com/share/5c8e80e0dca549e2964bd17da744244f?sid=be6cc7e1-7cca-4d33-8d29-2a27cd9f8d3a](https://www.loom.com/share/5c8e80e0dca549e2964bd17da744244f?sid=be6cc7e1-7cca-4d33-8d29-2a27cd9f8d3a)

Vivek Tangudu\
**Email:** vivektangudu@outlook.com\
**Phone**: +91 9441354555\
**LinkedIn**: [linkedin.com/in/vivektangudu](http://linkedin.com/in/vivektangudu)\
Resume: https://drive.google.com/file/d/1gATYbPiR1fEuOw77wdH_nuVlmsWGePLy/view?usp=share_link

## About Me

Hi! I'm Vivek from the International Institute of Information Technology in Bangalore. I'm currently in my 4th year, pursuing an integrated M.Tech degree in Computer Science and Engineering.

[GitHub - vivektangudu123/BookHive-Manager](https://github.com/vivektangudu123/BookHive-Manager)
One of my notable projects is the development of a robust Library Management System using the MERN stack. Leveraging MongoDB, Express.js, React, and Node.js, I implemented features such as book addition, issuance management, and issue editing. I emphasized deployment efficiency by utilizing Docker for containerization and Kubernetes for orchestration, showcasing my proficiency in full-stack programming and containerization technologies

In another project, "Why So Harsh," I devised an advanced model for comment categorization through tone detection. Achieving a remarkable accuracy rate of 97% through systematic tuning and experimentation with diverse models, I demonstrated my proficiency in machine learning, natural language processing, and data science.

My technical skill set encompasses a wide range of languages and technologies, including Python, Java, JavaScript, C++, and various databases such as MySQL, MongoDB, and PostgreSQL. I am well-versed in DevOps practices, Linux, Jenkins, Kubernetes, Docker, and have experience with the MERN stack.

## Availability

I am available from May 15, 2024, until my graduation on June 30, 2025. I can obtain a No Objection Certificate (NOC) from my college, as they permit me to complete an internship during this period.

## Architecture

**importing data:**

All the given csv files were downloaded using the python package gdown. And then stored the data in sqlite(locally) or in PostgreSQL(deployed application: AWS ). Each line was read and stored accordingly.

**trigger_report**:

 All the unique values of “store_id” were read from store_status table. For each store_id we calculated the required values using 3 functions.

- [calculate_business_uptime_downtime_for_day](https://www.notion.so/Store-Monitoring-62920705299f4d4899e72b1684342360?pvs=21)
- [calculate_business_uptime_downtime_for_past_hour](https://www.notion.so/Store-Monitoring-62920705299f4d4899e72b1684342360?pvs=21)
- for week: Used the day function.

All the values were calculated and written in CSV file with their report_id as the name of the file.

Before using the above functions, Pulled the required data from the tables by filtering with store_id.

To calculate_business_uptime_downtime_for_day, Found the latest date at which the store status was updated and calculated for that particular date.

Similarly, implemented to retrieve the time_zone, business hours using the store_id.

## calculate_business_uptime_downtime_for_day

1. **Input Parameters**: The function takes three inputs:
- **`observations`**: A list of observations made throughout the day, each containing a timestamp and a status (like "active" or "inactive").
- **`business_hours`**: A dictionary containing the opening and closing hours for each day of the week.
- **`max_date`**: The date for which you want to calculate the uptime and downtime.
1. **Filter Observations**: Filter the observations to include only those that occurred on or before the **`max_date`**.
2. **Determine Business Hours**: Get the business hours for the day corresponding to **`max_date`** and convert them into datetime objects.
3. **Filter Observations Within Business Hours**: Keep only those observations that fall within the business hours of the day.
4. **Calculate Uptime and Downtime**: Iterate through the filtered observations. For each observation:
    - If the status is "active" (meaning the business is up), add the time difference between this observation and the last one to the total uptime.
    - If the status is "inactive" (meaning the business is down), add the time difference between this observation and the last one to the total downtime.
    - Update the last observation time and status for the next iteration.
5. **Handle the Last Observation**: If the last status is "active" (meaning the business was up until closing time), calculate the uptime until closing time. Otherwise, calculate the downtime until closing time.

## calculate_business_uptime_downtime_for_past_hour

1. **Input Parameters**: The function takes the same inputs as before: **`observations`**, **`business_hours`**, **`max_date`**, and **`current_time`**. Additionally, it calculates the start and end times of the past hour.
2. **Filter Observations**: Filter the observations to include only those that occurred on or before the **`max_date`**.
3. **Determine Business Hours**: Get the business hours for the day corresponding to **`max_date`** and convert them into datetime objects.
4. **Calculate Past Hour**: Calculate the start and end times of the past hour relative to the **`current_time`**.
5. **Find Status Before Past Hour**: Iterate through all observations to find the status just before the past hour starts.
6. **Filter Observations Within Past Hour**: Keep only those observations that fall within the past hour and also within the business hours.
7. **Handle Empty Observation Set**: If there are no observations within the past hour, use the status before the past hour to determine the uptime and downtime for the entire past hour.
8. **Calculate Uptime and Downtime**: Iterate through the filtered observations within the past hour. For each observation:
    - If the status is "active" (meaning the business is up), add the time difference between this observation and the last one to the total uptime.
    - If the status is "inactive" (meaning the business is down), add the time difference between this observation and the last one to the total downtime.
    - Update the last observation time and status for the next iteration.
9. **Handle the Last Observation**: If the last status within the past hour is "active" (meaning the business was up until the closing time), calculate the uptime until the end of the past hour. Otherwise, calculate the downtime until the end of the past hour.

# Future Scope

- We can create a realtime ETL pipeline to update the database for every hour.
- Adding asynchronous functions to run in the background. (Threading)

**React JS deployment**

A react app: [https://library-odfb.onrender.com/](https://library-odfb.onrender.com/) 

login details ( vivektangudu@gmail.com, vivek)
