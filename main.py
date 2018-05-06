from flask import Flask
from flask_ask import Ask, statement, question, session
from MITsailing import getLaunch,getWind,getSunset,getTemp,getAllConditions,getForecast,getRain

app = Flask(__name__)
ask = Ask(app, '/')


@ask.launch
def start_skill():
	launch = getLaunch()
	launch_msg = "The current wind speed is "+launch['current wind']+" miles per hour, and the temperature is "+str(launch['temperature'])+" degrees celsius. Would you like to hear the full report?"
	launch_msg = (launch['warning']+" "+launch_msg).strip()
	return question(launch_msg)	

@ask.intent('getWind')
def askWind():
	wind = getWind()
	wind_msg = "The current wind speed is "+wind['current wind']+" miles per hour... The average is "+wind['avg wind']+" miles per hour, and the maximum is "+wind['max wind']+" miles per hour."
	wind_msg = (wind['warning']+" "+wind_msg).strip()
	return statement(wind_msg)

@ask.intent('getTemperature')
def askTemperature():
	temp = getTemp()
	temp_msg = "The temperature is "+str(temp['temperature'])+" degrees Celsius, and the water temperature is "+str(temp['water temperature'])+" degrees."
	if temp['heat index']!=temp['temperature']:
		temp_msg+=" The heat index is "+str(temp['heat index'])+" degrees."
	if temp['wind chill']!=temp['temperature']:
		temp_msg+=" The wind chill is "+str(temp['wind chill'])+" degrees."
	temp_msg = (temp['warning']+" "+temp_msg).strip()
	return statement(temp_msg)

@ask.intent('getSunset')
def askSunset():
	sunset = getSunset()
	sunset_msg = "The sunset today will be at "+sunset['sunset']+', '
	if sunset['time to sunset']!=0:
		sunset_msg = "The sunset today will be at "+sunset['sunset']+', '
		if sunset['time to sunset'] > 60:
			hh = int(sunset['time to sunset']/60)
			mm = int((sunset['time to sunset']/60.-int(sunset['time to sunset']/60))*60)
			if hh==1:
				sunset_msg+= 'you have 1 hour and '+str(mm)+' minutes of sun left.'
			else:
				sunset_msg+= 'you have '+str(hh)+' hours and '+str(mm)+' minutes of sun left.'
		else:
			sunset_msg+= 'you have '+str(sunset['time to sunset'])+' minutes of sun left.'
	else:
		sunset_msg = "Sunset already happened today, wait until tomorrow to go sailing again."
	sunset_msg = (sunset['warning']+" "+sunset_msg).strip()
	return statement(sunset_msg)

@ask.intent('getForecast')
def askForecast():	
	forecast = getForecast()
	fore_msg = "The forecast is: "+forecast['forecast'].lower() +'.'
	return statement(fore_msg)

@ask.intent('getRain')
def askRain():
	rain = getRain()
	if float(rain['rain'])==0:
		rain_msg = "No rain has been recorded in the last hour."
	else:
		rain_msg = "There have been "+str(rain['rain'])+' inches of rainfall in the last hour...'
	return statement(rain_msg)

@ask.intent('getAllConditions') 
def askAllConditions():	
	allC = getAllConditions()
	allC_msg = "The current wind speed is "+allC['current wind']+" miles per hour... The average is "+allC['avg wind']+" miles per hour, and the maximum is "+allC['max wind']+" miles per hour."
	allC_msg+= " The temperature is "+str(allC['temperature'])+" degrees Celsius, and the water temperature is "+str(allC['water temperature'])+" degrees."
	if allC['heat index']!=allC['temperature']:
		allC_msg+=" The heat index is "+str(allC['heat index'])+" degrees."
	if allC['wind chill']!=allC['temperature']:
		allC_msg+=" The wind chill is "+str(allC['wind chill'])+" degrees."
	if allC['time to sunset']!=0:
		allC_msg+= " The sunset today will be at "+allC['sunset']+', '
		if allC['time to sunset'] > 60:
			hh = int(allC['time to sunset']/60)
			mm = int((allC['time to sunset']/60.-int(allC['time to sunset']/60))*60)
			if hh==1:
				allC_msg+= 'you have 1 hour and '+str(mm)+' minutes of sun left.'
			else:
				allC_msg+= 'you have '+str(hh)+' hours and '+str(mm)+' minutes of sun left.'
		else:
			allC_msg+= 'you have '+str(allC['time to sunset'])+' minutes of sun left.'
	else:
		allC_msg+= " Sunset already happened, wait until tomorrow to go sailing again."
	allC_msg+= " The forecast is: "+allC['forecast'].lower() +'.'
	if allC['rain']==0:
		allC_msg+= " No rain has been recorded in the last hour."
	allC_msg = (allC['warning']+" "+allC_msg).strip()
	return statement(allC_msg)

@ask.intent('noConditions')
def askExit():
	return statement("Enjoy your sailing.")

if __name__ == '__main__':
    app.run(debug=False)

