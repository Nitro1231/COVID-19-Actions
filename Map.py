import folium
import pandas as pd
import folium.plugins as plugins
dataMap = folium.Map(location=[30,0], zoom_start=2.5, tiles='CartoDBdark_matter')

m_confirmed = folium.FeatureGroup(name='Confirmed').add_to(dataMap)
m_deaths = folium.FeatureGroup(name='Deaths').add_to(dataMap)
m_recovered = folium.FeatureGroup(name='Recovered').add_to(dataMap)
m_active = folium.FeatureGroup(name='Active').add_to(dataMap)

data = pd.read_csv('LastUpdated/Original/daily_reports.csv')
data = data[['Combined_Key', 'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active']].dropna()

print(data)

for item in data.index:
    lat = data.loc[item, 'Lat']
    long = data.loc[item, 'Long_']

    rad = data.loc[item, 'Confirmed']/2500
    name = f"{data.loc[item, 'Combined_Key']}\n[{lat},{long}]\nConfirmed: {data.loc[item, 'Confirmed']}"
    folium.CircleMarker([lat, long], radius=rad, color='#f39c12', popup=name, fill=True).add_to(m_confirmed)

    rad = data.loc[item, 'Deaths']/2500
    name = f"{data.loc[item, 'Combined_Key']}\n[{lat},{long}]\nDeaths: {data.loc[item, 'Deaths']}"
    folium.CircleMarker([lat, long], radius=rad, color='#c0392b', popup=name, fill=True).add_to(m_deaths)

    rad = data.loc[item, 'Recovered']/2500
    name = f"{data.loc[item, 'Combined_Key']}\n[{lat},{long}]\nRecovered: {data.loc[item, 'Recovered']}"
    folium.CircleMarker([lat, long], radius=rad, color='#27ae60', popup=name, fill=True).add_to(m_recovered)

    rad = data.loc[item, 'Active']/2500
    name = f"{data.loc[item, 'Combined_Key']}\n[{lat},{long}]\nActive: {data.loc[item, 'Active']}"
    folium.CircleMarker([lat, long], radius=rad, color='#2980b9', popup=name, fill=True).add_to(m_active)

plugins.Fullscreen( position='topright', title='Fullscreen', title_cancel='Exit Fullscreen', force_separate_button=True ).add_to(dataMap)
folium.LayerControl(collapsed=False).add_to(dataMap)
plugins.LocateControl().add_to(dataMap)
minimap = plugins.MiniMap()
dataMap.add_child(minimap)

dataMap.save('LastUpdated/map.html')