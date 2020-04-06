import os, sys
import ntplib
import pandas as pd
import urllib.request
import pytest
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timezone, timedelta

def test_DataUpdate():
    try:
        if not(os.path.isdir('DailyReports')):
            os.makedirs(os.path.join('DailyReports'))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory.")
            raise

    # Get current time in UTC.
    c = ntplib.NTPClient()
    # NTP server ip
    response = c.request('time.google.com', version=3)
    response.offset 
    # Get time based on UTC timezone.
    time = datetime.fromtimestamp(response.tx_time, timezone.utc)

    targetTime = ""
    try:
        targetTime = time.strftime('%m-%d-%Y')
        lastUpdate = time.strftime(f'%m-%d-%Y (%H:%M:%S)')
        URL = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{targetTime}.csv'
        urllib.request.urlretrieve(URL, f'DailyReports\\{targetTime}.csv')
    except:
        targetTime = (time - timedelta(days=1)).strftime('%m-%d-%Y')
        lastUpdate = time.strftime(f'%m-%d-%Y (%H:%M:%S)')
        URL = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{targetTime}.csv'
        urllib.request.urlretrieve(URL, f'DailyReports\\{targetTime}.csv')

    originalData = pd.read_csv(f'DailyReports\\{targetTime}.csv')
    data = originalData[['Country_Region', 'Confirmed', 'Deaths', 'Recovered', 'Active']].groupby('Country_Region').sum()
    Confirmed = data['Confirmed'].sum()
    Deaths = data['Deaths'].sum()
    Recovered = data['Recovered'].sum()

    data.to_csv(f'DailyReports\\{targetTime}-Re.csv')
    data = data.sort_values(["Confirmed"], ascending=[False])
    data = data.head(10)

    plt.style.use(['dark_background'])
    fig = plt.figure()
    fig.patch.set_facecolor(color=(30/255, 30/255, 30/255,1.0))
    ax = data['Confirmed'].plot(kind='bar', color=(241/255, 196/255, 15/255,1.0))
    ax = data['Recovered'].plot(kind='bar', color=(46/255, 204/255, 113/255,1.0))
    ax = data['Deaths'].plot(kind='bar', color=(231/255, 76/255, 60/255,1.0))
    plt.xlabel('Country_Region')
    plt.ylabel('Number of People')
    plt.title(f'TOP-10 countries with most confirmed cases ({targetTime})')
    plt.legend()
    plt.savefig(f'DailyReports\\{targetTime}.png')
    #plt.show()
    print(data)

test_DataUpdate()