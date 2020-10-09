# COVID-19-Actions
COVID-19 Data Reorganization using Github Actions.   
This GitHub Action will re-generate the CSV file and provide a visual graph that is suitable for the Corona Live website and COVID-19 discord bot.   
You can use the data files without any limitation, but Python scripts are protected under the MIT license.

*Read this in other languages: [English](README.md), [한국어](README.ko.md).*

# File and Dataset
### DataUpdate.py
Reorganize COVID-19 Dataset from JHU CSSE and generate the visual graph.   

### Map.py
Generate COVID-19 spread map file in form of HTML.   
This map displays the total confirmed, deaths, recovered, and active cases of COVID-19 by using different sizes of circles with different colors. The circles will appear in each state in the United States individually and in each country in the world.   

## DailyReports
### MM-DD-YYYY
Folders that includes all the data files from April 8th, 2020. The files under each folder might be different based on the modification of the script file.   

## LastUpdated
### Img
Under the Img folder, the following graphs will be included.

| Type | Description |
| --- | --- |
| Global Linear | The linear graph of COVID-19 that includes the number of Confirmed, Recovered, and Death. |
| Global Log | The logarithmic graph of COVID-19 that includes the number of Confirmed, Recovered, and Death. |
| Prediction | The prediction graph of COVID-19 Total Confirmed case based on the time interval. Those predictions are not accurate due to the uncertainty of the situation. |
| Top10 | The bar graphs of ten countries with most Total Confirmed cases. |

All of the images are named under the following rules:
1. Starts with the lower case of the type mentioned above. Replace the blank space with underbar "_".
2. Each of the images has a transparent version and background version. The transparent version of the image will end with "_t" and the background version will end with "_bg" tag.
3. All files are png.

### Original
A folder that includes all original files at that point.

### Reorganized
| File Name | Description |
| --- | --- |
| combined.csv | Dataset that includes all number of Confirmed, Recovered, and Deaths cases on that day. |
| confirmed.csv | Dataset that includes a number of Confirmed cases since January 22nd, 2020. | 
| deaths.csv | Dataset that includes a number of Deaths cases since January 22nd, 2020. | 
| recovered.csv | Dataset that includes a number of Recovered cases since January 22nd, 2020. | 

### data.json
A JSON file that includes the following.
| Name | Variable Type | Description | 
| --- | --- | --- |
| date | String | Current Date. | 
| last_updated | String | Last updated date. |
| total_confirmed | Integer | Worldwide total confirmed case number. |
| total_deaths | Integer | Worldwide total deaths case number. |
| total_recovered | Integer | Worldwide total recovered case number. |
| total_active | Integer | Worldwide total active case number. |
| mortality_rate | Double | Worldwide mortality rate. |
| recovery_rate | Double | Worldwide recovery rate. |

### map.html
HTML map which displays the total confirmed, deaths, recovered, and active cases of COVID-19 by using different sizes of circles with different colors. The circles will appear in each state in the United States individually and in each country in the world.   

### prediction.json
| Name | Variable Type | Description | 
| --- | --- | --- |
| last_updated | String | Last updated date |
| total_confirmed_prediction | Integer | Total predicted number of confirmed cases.  |
| total_confirmed_difference | Integer | A difference between today's confirmed cases and predicted confirmed cases. |
| tomorrow | String | Date of tomorrow. |
| tomorrow_confirmed_prediction | Integer | Predicted number of confirmed cases of tomorrow. |
| tomorrow_confirmed_difference | Integer | A difference between today's confirmed cases and tomorrow's predicted confirmed cases. |
| total_days | Integer | Predicted total days of the pandemic. |
| days_remained | Integer | Number of days left until the predicted end of the pandemic. |

# Source
All of the data files are based on the Data Repository by Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE).   
You can find the data repository [here](https://github.com/CSSEGISandData/COVID-19).

# License
MIT License. Feel free to use this Python script and Data.
