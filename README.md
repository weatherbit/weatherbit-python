*******************
# Python Weather API - Pyweatherbit
*******************

This is a wrapper for the Weatherbit API.

The Weatherbit IO allows you to access forecasts, current data, and historical data. This library wraps this functionality, and makes it accessible with Python.


## Installation

You should use pip to install pyweatherbit.

* To install: pip install pyweatherbit
* To remove:  pip uninstall pyweatherbit

## Requirements


- You need an API key to use it. Sign up for the free api [key](https://www.weatherbit.io/pricing "Free API Key") to get started.


## Basic Use


For additional information, refer to the Weatherbit.io API [documentation](https://www.weatherbit.io/api "Api Documentation") .

To use the wrapper:

```python

	from weatherbit.api import Api
	api_key = "YOUR API KEY"
	lat = 35.50
	lon = -78.50

	api = Api(api_key)

	# Currently supported tp options (time period):
	# History: daily, hourly, subhourly
	# AGWeather History: daily, hourly
	# Forecast: daily, hourly, minutely
	# Air quality: hourly
	# Will only affect forecast requests.

	### Forecasts (daily)

	# Query by lat/lon - get extended forecast out to 240 hours (default 48 hours)
	api.get_forecast(lat=lat, lon=lon, days=10, tp='daily').get()

	# You can also query by city:
	api.get_forecast(city="Raleigh,NC", days=10, tp='daily').get()

	# Or City, state, and country:
	api.get_forecast(city="Raleigh", state="North Carolina", country="US", days=10, tp='daily').get()

	# Or Postal code:
	# See documentation for field names: https://www.weatherbit.io/api
	api.get_forecast(postal_code="27601", country="US", days=10, tp='daily').get(['high_temp','low_temp','precip','weather'])

	### Forecasts (hourly)

	# Query by lat/lon - get extended forecast out to 240 hours (default 48 hours)
	api.get_forecast(lat=lat, lon=lon, hours=240, tp='hourly').get()

	# Or Postal code:
	api.get_forecast(postal_code="27601", country="US", hours=240, tp='hourly').get()


	### Forecasts (hourly - Air quality)
	# Get an hourly air quality forecast for a lat/lon
	api.get_forecast(source='airquality', lat=lat, lon=lon, tp='hourly').get()

	### Forecasts (minutely / Nowcast)

	# Query by lat/lon - get 60 minute precip nowcast.
	api.get_forecast(lat=lat, lon=lon, tp='minutely').get()

	### HISTORY

	# Get sub-hourly history by lat/lon, with imperial units.
	# get time series of temperature, precipitation, and rh:
	api.get_history(lat=lat, lon=lon, start_date='2024-02-01',end_date='2024-02-02', tp='subhourly', units="I").get(['precip','temp','rh'])
	# Or get all values. This time with metric units.
	api.get_history(lat=lat, lon=lon, start_date='2024-02-01',end_date='2024-02-02', tp='subhourly', units="M").get()

	# Get daily history by lat/lon
	api.get_history(lat=lat, lon=lon, start_date='2024-02-01',end_date='2024-02-02', tp='daily').get()

	# Get historical air quality data
	api.get_history(source='airquality', lat=lat, lon=lon, start_date='2024-02-01',end_date='2024-02-02', tp='hourly').get()

	# Get daily climate normals for March for location:
	api.get_normals(lat=lat, lon=lon, start_day='03-01',end_day='04-01', tp='daily').get()

	# Get daily climate normals for September - December for location:
	# Select a few fields.
	api.get_normals(lat=lat, lon=lon, start_day='09-01',end_day='01-01', tp='monthly').get(['max_temp', 'min_temp', 'precip'])

	# Get daily historical AGWeather data. Select a few fields.
	api.get_history(source='agweather', lat=lat, lon=lon, start_date='2024-02-01',end_date='2024-02-10', tp='daily').get(['evapotranspiration', 'soilt_0_10cm', 'v_soilm_0_10cm'])

	# Get hourly historical AGWeather data. This time, get all fields.
	api.get_history(source='agweather', lat=lat, lon=lon, start_date='2024-02-01',end_date='2024-02-10', tp='hourly').get()


	### Current Conditions

	# Get current air quality. Select a few fields.
	api.get_current(source='airquality', lat=lat, lon=lon).get(['aqi','pm10','pm25'])

	# Get current conditions for select fields.
	api.get_current(lat=lat, lon=lon).get(['weather','temp','precip'])

	# Or simply get() for all values. This time with imperial units.
	api.get_current(lat=lat, lon=lon, units="I").get()

	# Get weather alerts for a location
	api.get_alerts(lat=lat, lon=lon).get()

	# Get current conditions with alerts, and a minutely forecast for a location
	api.get_current(lat=lat, lon=lon, include="alerts,minutely").get()

	...
```


### Advanced

#### *function* weatherbit.Api.get_forecast(lat=..., lon=...)
---------------------------------------------------

This makes an API request and returns a **Forecast** object (see below).

Parameters:  
- **key** - Your API key from https://www.weatherbit.io.  
- **lat** - The latitude of the location for the forecast  
- **lon** - The longitude of the location for the forecast  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.  
- **source** - (optional) "airquality" or "agweather" - to return airquality/agweather data instead.  
- **tp** - (optional) A string denoting the time period of data 'minutely', 'hourly' or 'daily'.  

#### *function* weatherbit.Api.get_forecast(city=..., state=..., country=...)
---------------------------------------------------

This makes an API request and returns a **Forecast** object (see below).

Parameters:
- **key** - Your API key from https://www.weatherbit.io.  
- **city** - The City to search by. This can be appended with a state like -> "City,ST".  
- **state** - (optional) State of location.  
- **country** - (optional) Country of location  
- **source** - (optional) "airquality" or "agweather" - to return airquality/agweather data instead.  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.  
- **tp** - (optional) A string denoting the time period of data 'minutely', 'hourly' or 'daily'.  

#### *function* weatherbit.Api.get_forecast(postal_code=..., country=...)
---------------------------------------------------

This makes an API request and returns a **Forecast** object (see below).

Parameters:
- **key** - Your API key from https://www.weatherbit.io.  
- **postal_code** - postal code.  
- **country** - (recommended) Country of location  
- **source** - (optional) "airquality" or "agweather" - to return airquality/agweather data instead.  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.  
- **tp** - (optional) A string denoting the time period of data 'minutely', 'hourly' or 'daily'.  
  
#### *function* weatherbit.Api.get_history(lat=..., lon=..., start_date=..., end_date=...)  
---------------------------------------------------
  
This makes an API request and returns a **History** object (see below).  
  
Parameters:  
- **key** - Your API key from https://www.weatherbit.io.  
- **start_date** - Start date of data  
- **end_date** - End date of data  
- **lat** - The latitude of the location  
- **lon** - The longitude of the location    
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.  
- **source** - (optional) "airquality" or "agweather" - to return airquality/agweather data instead.  
- **tp** - (optional) A string denoting the time period of data 'hourly' or 'daily' or 'subhourly'.  

#### *function* weatherbit.Api.get_history(city=..., state=..., country=..., start_date=..., end_date=...)  
---------------------------------------------------  
  
This makes an API request and returns a **History** object (see below).   
  
Parameters:  
- **key** - Your API key from https://www.weatherbit.io.  
- **start_date** - Start date of data  
- **end_date** - End date of data  
- **city** - The City to search by. This can be appended with a state like -> "City,ST".  
- **state** - (optional) State of location.  
- **country** - (optional) Country of location  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.   
- **source** - (optional) "airquality" or "agweather" - to return airquality/agweather data instead.  
- **tp** - (optional) A string denoting the time period of data 'hourly' or 'daily' or 'subhourly'. 

#### *function* weatherbit.Api.get_history(postal_code=..., country=..., start_date=..., end_date=...)  
---------------------------------------------------  
  
This makes an API request and returns a **History** object (see below).   
  
Parameters:  
- **key** - Your API key from https://www.weatherbit.io.  
- **start_date** - Start date of data  
- **end_date** - End date of data  
- **postal_code** - postal code.  
- **country** - (recommended) Country of location  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.   
- **source** - (optional) "airquality" or "agweather" - to return airquality/agweather data instead.  
- **tp** - (optional) A string denoting the time period of data 'hourly' or 'daily' or 'subhourly'. 

----------------------------------------------------

#### *function* weatherbit.Api.get_current(postal_code=..., country=..., start_date=..., end_date=...)  
---------------------------------------------------  
  
This makes an API request and returns a **Current Data** object (see below).   
  
Parameters:  
- **key** - Your API key from https://www.weatherbit.io.  
- **postal_code** - postal code.  
- **country** - (recommended) Country of location  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.   
- **source** - (optional) "airquality" - to return airquality data instead.  
- **include** - (optional) comma separated value of extra data responses to include. Ie. "alerts" or "minutely", or both "alerts,minutely". "alerts" being severe weather alerts, and "minutely" being a minutely nowcast.  

----------------------------------------------------

#### *function* weatherbit.Api.get_current(lat=..., lon=..., country=..., start_date=..., end_date=...)  
---------------------------------------------------  
  
This makes an API request and returns a **Current Data** object (see below).   
  
Parameters:  
- **key** - Your API key from https://www.weatherbit.io.  
- **lat** - The latitude of the location  
- **lon** - The longitude of the location  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.   
- **source** - (optional) "airquality" - to return airquality data instead.  
- **include** - (optional) comma separated value of extra data responses to include. Ie. "alerts" or "minutely", or both "alerts,minutely". "alerts" being severe weather alerts, and "minutely" being a minutely nowcast.  

----------------------------------------------------

#### *function* weatherbit.Api.get_current(city=..., state=..., country=...)  
---------------------------------------------------  
  
This makes an API request and returns a **Current Data** object (see below).   
  
Parameters:  
- **key** - Your API key from https://www.weatherbit.io.  
- **city** - The City to search by. This can be appended with a state like -> "City,ST".  
- **state** - (optional) State of location.  
- **country** - (optional) Country of location  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.   
- **source** - (optional) "airquality" - to return airquality data instead.  
- **include** - (optional) comma separated value of extra data responses to include. Ie. "alerts" or "minutely", or both "alerts,minutely". "alerts" being severe weather alerts, and "minutely" being a minutely nowcast.  

----------------------------------------------------

----------------------------------------------------

#### *function* weatherbit.Api.get_alerts(lat=... , lon=...)  
---------------------------------------------------  
  
This makes an API request and returns a **Alert** object (see below).   
  
Parameters:  
- **key** - Your API key from https://www.weatherbit.io.  
- **lat** - The latitude of the location for the forecast  
- **lon** - The longitude of the location for the forecast  

----------------------------------------------------


----------------------------------------------------

#### *function* weatherbit.Models.Current.get(api_vars=[])  
---------------------------------------------------  
  
Gets data from Current Weather API Response (weatherbit.Api.get_current).
  
Parameters:  
- **api_vars** - Optional list of vars to retrieve from API. 

----------------------------------------------------


----------------------------------------------------

#### *function* weatherbit.Models.Alert.get()  
---------------------------------------------------  
  
Gets data from Current Weather API Response (weatherbit.Api.get_current).
 

----------------------------------------------------

----------------------------------------------------

#### *function* weatherbit.Models.Forecast.get(api_vars=[])  
---------------------------------------------------  
  
Gets data from Forecast API Response (weatherbit.Api.get_forecast).  
  
Parameters:  
- **api_vars** - Optional list of vars to retrieve from API. 

----------------------------------------------------

----------------------------------------------------

#### *function* weatherbit.Models.History.get(api_vars=[])  
---------------------------------------------------  
  
Gets data from History Weather API Response (weatherbit.Api.get_history).  
  
Parameters:  
- **api_vars** - Optional list of vars to retrieve from API. 

----------------------------------------------------

----------------------------------------------------

#### *function* weatherbit.Models.Normals.get(api_vars=[])  
---------------------------------------------------  
  
Gets data from Normals API Response (weatherbit.Api.get_normals).  
  
Parameters:  
- **api_vars** - Optional list of vars to retrieve from API. 

----------------------------------------------------


