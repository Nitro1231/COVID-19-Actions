import os, sys
import ntplib
import json
import shutil
import pandas as pd
import urllib.request
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
from datetime import datetime, timezone, timedelta
from collections import OrderedDict

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

def overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)

def dataUpdate(time):
    targetTime = time.strftime('%m-%d-%Y')
    lastUpdated = time.strftime(f'%Y-%m-%dT%H:%M:%SUTC')
    jsonData = OrderedDict()
    jsonData['date'] = targetTime
    jsonData['last_updated'] = lastUpdated

    mkdir('LastUpdated')
    mkdir('LastUpdated/Original')
    mkdir('LastUpdated/Reorganized')
    mkdir('LastUpdated/Img')

    try:
        daily = time.strftime('%m-%d-%Y')
        URL = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{daily}.csv'
        urllib.request.urlretrieve(URL, f'LastUpdated/Original/daily_reports.csv')
    except:
        daily = (time - timedelta(days=1)).strftime('%m-%d-%Y')
        URL = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{daily}.csv'
        urllib.request.urlretrieve(URL, f'LastUpdated/Original/daily_reports.csv')

    dataList = ['confirmed', 'deaths', 'recovered']
    for dataType in dataList:
        URL = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_{dataType}_global.csv'
        urllib.request.urlretrieve(URL, f'LastUpdated/Original/{dataType}.csv')
        data = pd.read_csv(f'LastUpdated/Original/{dataType}.csv')
        data = data.drop(columns='Province/State').drop(columns='Lat').drop(columns='Long')
        data = data.groupby('Country/Region').sum()
        jsonData[f'total_{dataType}'] = int(data[data.columns[data.shape[1] - 1]].sum())
        data.to_csv(f'LastUpdated/Reorganized/{dataType}.csv')

    jsonData['total_active'] = jsonData['total_confirmed'] - jsonData['total_deaths'] - jsonData['total_recovered']
    jsonData['mortality_rate'] = jsonData['total_deaths'] / jsonData['total_confirmed']
    jsonData['recovery_rate'] = jsonData['total_recovered'] / jsonData['total_confirmed']

    finalData = json.dumps(jsonData)
    with open('LastUpdated/data.json', 'w') as f:
        f.write(finalData)
    f.close

    dataCombined = pd.read_csv('LastUpdated/Reorganized/confirmed.csv')
    dataCombined = dataCombined[['Country/Region']]
    for dataType in dataList:
        data = pd.read_csv(f'LastUpdated/Reorganized/{dataType}.csv')
        data = data[['Country/Region', data.columns[data.shape[1] - 1]]]
        data.columns = ['Country/Region', dataType]
        dataCombined = pd.merge(dataCombined, data, on='Country/Region')
    dataCombined.to_csv('LastUpdated/Reorganized/combined.csv', index=False)

    return targetTime, lastUpdated

def top10Graph(lastUpdated):
    data = pd.read_csv('LastUpdated/Reorganized/combined.csv')
    data = data[['Country/Region', 'confirmed', 'deaths', 'recovered']].groupby('Country/Region').sum()
    data = data.sort_values(["confirmed"], ascending=[False])
    data = data.head(10)

    plt.style.use(['dark_background'])
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.25)
    ax.yaxis.grid()
    data['confirmed'].plot(kind='bar', color=(241/255, 196/255, 15/255,1.0), label='Confirmed')
    data['recovered'].plot(kind='bar', color=(46/255, 204/255, 113/255,1.0), label='Recovered')
    data['deaths'].plot(kind='bar', color=(231/255, 76/255, 60/255,1.0), label='Deaths')
    ax.yaxis.set_major_formatter(ticker.EngFormatter())
    plt.xticks(rotation=45)
    plt.xlabel('Country')
    plt.ylabel('Number of People')
    plt.legend(fancybox=True)
    plt.title(f'TOP-10 countries with most confirmed cases ({lastUpdated})')
    plt.savefig('LastUpdated/Img/top10_bg.png', aspect='auto')
    plt.savefig('LastUpdated/Img/top10_t.png', aspect='auto', transparent=True)
    plt.cla()
    plt.close('all')
    
def globalGraph(log):
    title = f'Global Cases Linear Graph ({lastUpdated})'
    name = 'global_linear'
    if (log):
        title = f'Global Cases Log Graph ({lastUpdated})'
        name = 'global_log'
        

    confirmedData = pd.DataFrame.from_dict(getData('confirmed'), orient='index', columns=['total'])
    recoveredData = pd.DataFrame.from_dict(getData('recovered'), orient='index', columns=['total'])
    deathsData = pd.DataFrame.from_dict(getData('deaths'), orient='index', columns=['total'])

    plt.style.use(['dark_background'])
    confirmedData['total'].plot(color=(241/255, 196/255, 15/255,1.0), label='Confirmed', logy=log, marker='o', zorder=3)
    recoveredData['total'].plot(color=(46/255, 204/255, 113/255,1.0), label='Recovered', logy=log, marker='o', zorder=2)
    deathsData['total'].plot(color=(231/255, 76/255, 60/255,1.0), label='Deaths', logy=log, marker='o', zorder=1)
    
    plt.gca().yaxis.set_major_formatter(ticker.EngFormatter())
    plt.minorticks_off()
    plt.xlabel('Date')
    plt.ylabel('Number of People')
    plt.legend(['Confirmed', 'Recovered', 'Deaths'], fancybox=True)
    plt.title(title)
    plt.savefig(f'LastUpdated/Img/{name}_bg.png', aspect='auto')
    plt.savefig(f'LastUpdated/Img/{name}_t.png', aspect='auto', transparent=True)
    plt.cla()
    plt.close('all')

def getData(dataType):
    data = pd.read_csv(f'LastUpdated/Reorganized/{dataType}.csv')
    arr = data.columns.tolist()
    arr.pop(0)
    newData = OrderedDict()
    for date in arr:
        newData[str(date)] = int(data[date].sum())
    return newData

targetTime, lastUpdated = dataUpdate(getUTC())
top10Graph(lastUpdated)
globalGraph(True)
globalGraph(False)

overwrite('LastUpdated', f'DailyReports/{targetTime}')