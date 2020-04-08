import folium
import pandas as pd
dataMap = folium.Map(location=[30,0], zoom_start=2.5, tiles='CartoDBdark_matter')
data = pd.read_csv('LastUpdated/Original/daily_reports.csv')
data = data[['Combined_Key', 'Lat', 'Long_', 'Confirmed']].dropna()

print(data)

for item in data.index:
    name = data.loc[item, 'Combined_Key']
    lat = data.loc[item, 'Lat']
    long = data.loc[item, 'Long_']
    rad = data.loc[item, 'Confirmed']/2500
    folium.CircleMarker([lat, long], radius=rad, color='#f39c12', popup=name, fill=True).add_to(dataMap)

dataMap.save('LastUpdated/map.html')