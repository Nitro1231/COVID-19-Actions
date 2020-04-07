import os, sys
import ntplib
import json
import pandas as pd
import urllib.request
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timezone, timedelta
from collections import OrderedDict

targetTime = ""
def getUTC():
    # Get current time in UTC.
    c = ntplib.NTPClient()
    # NTP server ip
    response = c.request('time.google.com', version=3)
    response.offset 
    # Get time based on UTC timezone.
    time = datetime.fromtimestamp(response.tx_time, timezone.utc)
    return time

def mkdir(newPath):
    if not(os.path.isdir(newPath)):
        os.makedirs(os.path.join(newPath))

def dataUpdate():
    time = getUTC()
    global targetTime
    global lastUpdated
    targetTime = time.strftime('%m-%d-%Y')
    lastUpdated = time.strftime(f'%m-%d-%Y (%H:%M:%S)')

    jsonData = OrderedDict()
    jsonData['date'] = targetTime
    jsonData['last_updated'] = lastUpdated

    mkdir('LastUpdated')
    mkdir(f'DailyReports/{targetTime}')
    dataList = ['confirmed', 'deaths', 'recovered']
    for dataType in dataList:
        URL = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_{dataType}_global.csv'
        urllib.request.urlretrieve(URL, f'DailyReports/{targetTime}/{dataType}_original.csv')
        data = pd.read_csv(f'DailyReports/{targetTime}/{dataType}_original.csv')
        data = data.drop(columns='Province/State').drop(columns='Lat').drop(columns='Long')
        data = data.groupby('Country/Region').sum()
        jsonData[f'total_{dataType}'] = int(data[data.columns[data.shape[1] - 1]].sum())
        data.to_csv(f'DailyReports/{targetTime}/{dataType}_re.csv')
        data.to_csv(f'LastUpdated/{dataType}.csv')

    jsonData['total_active'] = jsonData['total_confirmed'] - jsonData['total_deaths'] - jsonData['total_recovered']
    jsonData['mortality_rate'] = jsonData['total_deaths'] / jsonData['total_confirmed']
    jsonData['recovery_rate'] = jsonData['total_recovered'] / jsonData['total_confirmed']

    finalData = json.dumps(jsonData)
    with open('LastUpdated/Data.json', 'w') as f:
        f.write(finalData)
    f.close

    dataConfirmed = pd.read_csv('LastUpdated/confirmed.csv')
    colum = dataConfirmed.columns[dataConfirmed.shape[1] - 1]
    dataConfirmed = dataConfirmed[['Country/Region', colum]]
    dataConfirmed.columns = ['Country/Region', 'Confirmed']

    dataDeaths = pd.read_csv('LastUpdated/deaths.csv')
    dataDeaths = dataDeaths[['Country/Region', colum]]
    dataDeaths.columns = ['Country/Region', 'Deaths']

    dataRecovered = pd.read_csv('LastUpdated/recovered.csv')
    dataRecovered = dataRecovered[['Country/Region', colum]]
    dataRecovered.columns = ['Country/Region', 'Recovered']

    dataCombined = pd.merge(dataConfirmed, dataDeaths, on='Country/Region')
    dataCombined = pd.merge(dataCombined, dataRecovered, on='Country/Region')
    dataCombined.to_csv('LastUpdated/combined.csv', index=False)

def top10Graph():
    data = pd.read_csv('LastUpdated/combined.csv')
    data = data[['Country/Region', 'Confirmed', 'Deaths', 'Recovered']].groupby('Country/Region').sum()
    data = data.sort_values(["Confirmed"], ascending=[False])
    data = data.head(10)

    plt.style.use(['dark_background'])
    fig = plt.figure()
    fig.patch.set_facecolor(color=(30/255, 30/255, 30/255,1.0))
    data['Confirmed'].plot(kind='bar', color=(241/255, 196/255, 15/255,1.0))
    data['Recovered'].plot(kind='bar', color=(46/255, 204/255, 113/255,1.0))
    data['Deaths'].plot(kind='bar', color=(231/255, 76/255, 60/255,1.0))
    plt.xlabel('Country')
    plt.ylabel('Number of People')
    plt.legend()
    plt.title(f'TOP-10 countries with most confirmed cases ({lastUpdated})')
    plt.savefig(f'DailyReports/{targetTime}/top10.png', aspect='auto')
    plt.savefig(f'LastUpdated/top10.png', aspect='auto')

dataUpdate()
top10Graph()