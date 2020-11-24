from bs4 import BeautifulSoup
import requests
from datetime import date,timedelta
dict1 = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}


def allsundays(year):
    dates = []
    d = date(year, 1, 1)                    # January 1st
    d += timedelta(days = 6 - d.weekday())  # First Sunday
    while d.year == year:
        dates.append(str(d))
        d += timedelta(days = 7)
    return dates
    


def getHolidays(year,dates):
    url="https://www.officeholidays.com/countries/india/karnataka/"+year
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text
    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    #print(soup.prettify()) # print the parsed data of html
    #print(soup.title)
    date_table = soup.find("table", attrs={"class": "country-table"})
    date_table_data = date_table.tbody.find_all("tr")  # contains 2 rows
    d = set(allsundays(int(year)))
    holidays = list(set(list(map(lambda x: year+'-'+dict1[x[0]]+"-"+x[1],list(map(lambda x: x.text.split(), list(map(lambda y: y.find("td",attrs={"style":"white-space:nowrap;"}),date_table_data))))))).union(d))
    holidays.sort()
    return holidays