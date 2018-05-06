from bs4 import BeautifulSoup
import datetime
import requests

def parseWindSpeed(html):
    soup = BeautifulSoup(html, 'html.parser')
    current = soup.find('div',attrs={'class':'current_summary'})
    for t in current.find_all('tr',attrs={'style':'vertical-align:top'}):
        if t.find('td',attrs={'class':'metric_name'}).text == 'Wind':
            break
    wind = t.find('table').find('a',attrs={'class':'popup','href':'daywind.png'}).text
    max_wind = t.find('span',attrs={'class':"metric_value",'title':"maximum wind speed"}).text
    avg_wind = t.find('span',attrs={'class':"metric_value",'title':"average wind speed"}).text
    return {'current wind':wind,'max wind':max_wind,'avg wind':avg_wind}
    return None

def parseTemp(html):
    soup = BeautifulSoup(html, 'html.parser')
    current = soup.find('div',attrs={'class':'current_summary'})
    for t in current.find_all('tr',attrs={'style':'vertical-align:top'}):
        if t.find('td',attrs={'class':'metric_name'}).text == 'Temperature':
            break
    out_temp = int(round((float(t.find('a',attrs={'class':'popup','href':'dayouttemphilo.png'}).text)-32)*5/9.))
    wind_chill = int(round((float(t.find('span',attrs={'class':'windchill'}).text)-32)*5/9.))
    heat_index = int(round((float(t.find('span',attrs={'class':'heatindex'}).text)-32)*5/9.))

    for t in current.find_all('tr',attrs={'style':'vertical-align:top'}):
        if t.find('td',attrs={'class':'metric_name'}).text == 'TemperatureWater':
            break
    water_temp = int(round((float(t.find('a',attrs={'class':'popup','href':'daywatertemphilo.png'}).text)-32)*5/9.))
    return {'temperature':out_temp,'wind chill':wind_chill,'heat index':heat_index,'water temperature':water_temp}

def parseRain(html):
    soup = BeautifulSoup(html, 'html.parser')
    current = soup.find('div',attrs={'class':'current_summary'})
    rain = int(float(current.find('span',attrs={'title':'rain within the past hour'}).find('a',attrs={'href':'dayrain.png'}).text))
    return {'rain':rain}

def parseSunset(html):
    soup = BeautifulSoup(html, 'html.parser')
    fore = soup.find('div',attrs={'class':'forecast_summary'})
    foundSunset = False
    for t in  fore.find_all('td'):
        if foundSunset:
            sunsetTime = t.text
            break
        if t.text=='Sunset':
            foundSunset=True
    time_now = soup.find('div',attrs={'id':'station_info'}).find('span',attrs={'class':'station_time'}).text.split(' ')[-1]
    today = soup.find('div',attrs={'id':'station_info'}).find('span',attrs={'class':'station_time'}).text.split(' ')[0]
    dateSS = datetime.datetime.strptime(today+' '+sunsetTime,'%m.%d.%Y %H:%M')
    dateTN = datetime.datetime.strptime(today+' '+time_now,'%m.%d.%Y %H:%M')
    if dateSS>dateTN:
        delta = (dateSS-dateTN).seconds/60
    else:
        delta = 0
    return {'sunset':sunsetTime,'time to sunset':int(delta)}

def parsLightning(html):
    soup = BeautifulSoup(html, 'html.parser')
    current = soup.find('div',attrs={'class':'current_summary'})
    for t in current.find_all('tr',attrs={'style':'vertical-align:top'}):
        if t.find('td',attrs={'class':'metric_name'}).text == 'Lightning':
            break
    lightnings = int(t.find('a',attrs={'class':'popup','href':'daylightning.png'}).text)
    return {'lightnings in past minutes':lightnings}


def parseForecast(html):
    soup = BeautifulSoup(html, 'html.parser')
    fore = soup.find('div',attrs={'class':'forecast_summary'})
    forecast = fore.find('td',attrs={'class':'zambretti'}).text.strip()
    return {'forecast':forecast}


def parseWarning(html):
    lightnings = parsLightning(html)
    rain = parseRain(html)
    warning = ''
    if lightnings['lightnings in past minutes'] >=10:
        warning+= ' There have been '+str(lightnings['lightnings in past minutes'])+' in the last minutes...'
    if rain['rain'] >=1:
        warning+= ' There have been '+str(rain['rain'])+' inches of rainfall in the last hour...'
    return warning.strip()

########################################################################

def getLaunch():
    url = 'http://sailing.mit.edu/weather/'
    r = requests.get(url)
    launch = {}
    launch['current wind'] = parseWindSpeed(r.text)['current wind']
    launch['temperature'] = parseTemp(r.text)['temperature']
    launch['warning'] = parseWarning(r.text)
    return launch

def getWind():
    url = 'http://sailing.mit.edu/weather/'
    r = requests.get(url)
    wind = parseWindSpeed(r.text)
    wind['warning'] = parseWarning(r.text)
    return wind

def getSunset():
    url = 'http://sailing.mit.edu/weather/'
    r = requests.get(url)
    sunset = parseSunset(r.text)
    sunset['warning'] = parseWarning(r.text)
    return sunset

def getTemp():
    r = requests.get('http://sailing.mit.edu/weather/')
    temp = parseTemp(r.text)
    temp['warning'] = parseWarning(r.text)
    return temp

def getForecast():
    r = requests.get('http://sailing.mit.edu/weather/')
    forecast = parseForecast(r.text)
    return forecast

def getRain():
    r = requests.get('http://sailing.mit.edu/weather/')
    rain = parseRain(r.text)
    return rain

def getAllConditions():
    url = 'http://sailing.mit.edu/weather/'
    r = requests.get(url)
    allC = {}
    allFuncs = [parseWindSpeed,parseTemp,parseSunset,parseForecast,parseRain]
    for func in allFuncs:
        d = func(r.text)
        for key in d.keys():
            allC[key]=d[key]
    allC['warning'] = parseWarning(r.text)
    return allC

if __name__ == "__main__":
    print getLaunch()
    print getWind()
    print getSunset()
    print getTemp()
    print getForecast()
    print getAllConditions()
