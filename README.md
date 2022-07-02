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

	### FORECASTS

	# Set the granularity of the API - Options: ['daily','hourly','subhourly']
	# Depends on supported granularity of API - please see https://www.weatherbit.io/api
	# Currently supported:
	# History: daily, hourly, subhourly
	# Forecast: daily, hourly
	# Air quality: hourly
	# Will only affect forecast requests.
	api.set_granularity('daily')
	

	### Forecasts (daily)

	# Query by lat/lon - get extended forecast out to 240 hours (default 48 hours)
	forecast = api.get_forecast(lat=lat, lon=lon, hours=240)

	# You can also query by city:
	forecast = api.get_forecast(city="Raleigh,NC", hours=240)

	# Or City, state, and country:
	forecast = api.get_forecast(city="Raleigh", state="North Carolina", country="US", hours=240)

	# Or Postal code:
	forecast = api.get_forecast(postal_code="27601", country="US", hours=240)

	# get_series requires a list of fields to return in a time series (list).
	# See documentation for field names: https://www.weatherbit.io/api
	print(forecast.get_series(['high_temp','low_temp','precip','weather']))


	### Forecasts (hourly)
	api.set_granularity('hourly')


	# Query by lat/lon - get extended forecast out to 240 hours (default 48 hours)
	forecast = api.get_forecast(lat=lat, lon=lon, hours=240)

	# Or Postal code:
	forecast = api.get_forecast(postal_code="27601", country="US", hours=240)

	# get an hourly forecast:
	print(forecast.get_series(['temp','precip','weather', 'solar_rad']))


	### Forecasts (hourly - Air quality)
	# Get an hourly air quality forecast for a lat/lon
	forecast_AQ = api.get_forecast(source='airquality', lat=lat, lon=lon)
	print(forecast_AQ.get_series(['aqi','pm10','no2']))


	### HISTORY

	# Get sub-hourly history by lat/lon:
	api.set_granularity('subhourly')
	history = api.get_history(lat=lat, lon=lon, start_date='2018-02-01',end_date='2018-02-02')

	# To get a daily time series of temperature, precipitation, and rh:
	print history.get_series(['precip','temp','rh'])

	# Get hourly history by lat/lon
	api.set_granularity('hourly')
	history = api.get_history(lat=lat, lon=lon, start_date='2018-02-01',end_date='2018-02-02')
	
	# To get an hourly time series for these fields:
	print(history.get_series(['precip','temp','rh','solar_rad']))

	# Get historical air quality data
	history_AQ = api.get_history(source='airquality', lat=lat, lon=lon, start_date='2018-02-01',end_date='2018-02-02')
	print(history_AQ.get_series(['aqi','pm10','no2']))


	### Current Conditions

	# Get current air quality
	AQ = api.get_current(source='airquality', city="Raleigh", state="North Carolina", country="US")
	print(AQ.get(['aqi','pm10','pm25']))

	# Get current conditions
	current_weather = api.get_current(city="Raleigh", state="North Carolina", country="US")
	print(current_weather.get(['weather','temp','precip']))

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
- **source** - (optional) "airquality" - to return airquality data instead.  

#### *function* weatherbit.Api.get_forecast(city=..., state=..., country=...)
---------------------------------------------------

This makes an API request and returns a **Forecast** object (see below).

Parameters:
- **key** - Your API key from https://www.weatherbit.io.  
- **city** - The City to search by. This can be appended with a state like -> "City,ST".  
- **state** - (optional) State of location.  
- **country** - (optional) Country of location  
- **source** - (optional) "airquality" - to return airquality data instead.  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.  

#### *function* weatherbit.Api.get_forecast(postal_code=..., country=...)
---------------------------------------------------

This makes an API request and returns a **Forecast** object (see below).

Parameters:
- **key** - Your API key from https://www.weatherbit.io.  
- **postal_code** - postal code.  
- **country** - (recommended) Country of location  
- **source** - (optional) "airquality" - to return airquality data instead.  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.  
  
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
- **source** - (optional) "airquality" - to return airquality data instead.  

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
- **source** - (optional) "airquality" - to return airquality data instead.  

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
- **source** - (optional) "airquality" - to return airquality data instead.  

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

----------------------------------------------------

