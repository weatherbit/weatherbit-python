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
	lat = 38.00
	lon = -125.75

	api = Api(api_key)

	# Set the granularity of the API - Options: ['daily','hourly','3hourly']
	# Will only affect forecast requests.
	api.set_granularity('daily')

	# Query by lat/lon
	forecast = api.get_forecast(lat=lat, lon=long)

	# You can also query by city:
	forecast = api.get_forecast(city="Raleigh,NC")

	# Or City, state, and country:
	forecast = api.get_forecast(city="Raleigh", state="North Carolina", country="US")

	# To get a daily forecast of temperature, and precipitation:
	print forecast.get_series(['temp','precipitation'])

	# Get hourly history by lat/lon:
    api.set_granularity('daily')
	history = api.get_history(lat=lat, lon=lon, start_date='2018-02-01',end_date='2018-02-02')

	# To get a daily time series of temperature, precipitation, and rh:
	print forecast.get_series(['precip','temp','rh'])

	# Get hourly history by lat/lon
	api.set_granularity('hourly')
    history = api.get_history(lat=lat, lon=lon, start_date='2018-02-01',end_date='2018-02-02')
	
	# To get an hourly time series of temperature, precipitation, and rh:
	print forecast.get_series(['precip','temp','rh'])

	...
```

The ``get_forecast()`` method requires named parameters. The current choices are either (lat=..., lon=...), (city="City,ST"), or (city=..., state=..., country=...)


### Advanced

#### *function* weatherbit.Api.get_forecast(lat=..., lon=...)
---------------------------------------------------

This makes an API request and returns a **Forecast** object (see below).

Parameters:  
- **key** - Your API key from https://www.weatherbit.io.  
- **lat** - The latitude of the location for the forecast  
- **lon** - The longitude of the location for the forecast  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.  

#### *function* weatherbit.Api.get_forecast(city=..., state=..., country=...)
---------------------------------------------------

This makes an API request and returns a **Forecast** object (see below).

Parameters:
- **key** - Your API key from https://www.weatherbit.io.  
- **city** - The City to search by. This can be appended with a state like -> "City,ST".  
- **state** - (optional) State of location.  
- **country** - (optional) Country of location  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.  
  
#### *function* weatherbit.Api.get_history(lat=..., lon=...)  
---------------------------------------------------
  
This makes an API request and returns a **History** object (see below).  
  
Parameters:  
- **key** - Your API key from https://www.weatherbit.io.  
- **lat** - The latitude of the location for the forecast  
- **lon** - The longitude of the location for the forecast  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.  

#### *function* weatherbit.Api.get_history(city=..., state=..., country=...)  
---------------------------------------------------  
  
This makes an API request and returns a **History** object (see below).   
  
Parameters:  
- **key** - Your API key from https://www.weatherbit.io.  
- **city** - The City to search by. This can be appended with a state like -> "City,ST".  
- **state** - (optional) State of location.  
- **country** - (optional) Country of location  
- **units** - (optional) A string of the preferred units of measurement. Choices are currently 'S' for scientific, 'M' for Metric, or 'I' for imperial units.  

----------------------------------------------------



#### *class* forecastio.models.Forecast  
------------------------------------  

The **Forecast** object, it contains both weather data and the HTTP response from Weatherbit  

**Attributes**  
- **http_headers**  
		-  A dictionary of response headers.   
- **json**
		-  A dictionary containing the json data returned from the API call.  
- **city_name**  
    	-  City Name of the forecast points.  
- **country_code**
    	-  Country Code of the forecast points  
- **state_code**
    	-  State Code of the forecast points  
- **lat**  
    	-  Latitude of the forecast points  
- **lon**  
    	-  Longitude of the forecast points  
- **points**  
	-  Array of forecast data Point objects.  

**Methods**  
- **get_series([var1, var2, ... , varn])**  
		-  Returns list of dicts sorted by datetime, containing the desired variables in a time series.  
- **update()**  
		-  Refreshes the forecast data by making a new request.  

----------------------------------------------------

#### *class* forecastio.models.History  
------------------------------------

The **History** object, it contains both weather data and the HTTP response from Weatherbit  
  
**Attributes**  
- **response**  
		-  The Response object returned from requests request.get() method.  
- **http_headers**  
		-  A dictionary of response headers.   
- **json**  
		-  A dictionary containing the json data returned from the API call.  
- **city_name**  
    	-  City Name of the historical points.  
- **country_code**  
    	-  Country Code of the historical points  
- **state_code**  
    	-  State Code of the historical points  
- **lat**  
    	-  Latitude of the historical points  
- **lon**  
    	-  Longitude of the historical points  
- **points**  
	-  Array of historical data Point objects.  
  
**Methods**  
- **get_series([var1, var2, ... , varn])**  
		-  Returns list of dicts sorted by datetime, containing the desired variables in a time series.  
- **update()**   
		-  Refreshes the forecast data by making a new request.  

----------------------------------------------------

#### *class* weatherbit.models.Point
---------------------------------------------

Contains data about a history or forecast over time.  

**Attributes**  
- **snow**  
		-  Total Snowfall.  
- **precip**
		-  Total Liquid equivalent precipitation.  
- **snow6h**  
		-  6h Total Snowfall.  
- **precip6h**  
		-  6h Total Liquid equivalent precipitation.  
- **datetime**  
		-  Datetime object - Datetime  (UTC).  
- **wind_dir**  
		-  Average Wind direction in degrees (0-360).  
- **wind_spd**  
		-  Average Wind speed.   
- **rh**  
		-  Average Relative Humidity (%).  
- **clouds**  
		-  Average Cloud cover (%).  
- **slp**  
		-  Average Sea level pressure in millibars.  
- **temp**  
		-  Average Temperature.  
- **max_temp**  
		-  Maximum Temperature. (daily only)  
- **min_temp**  
		-  Minimum Temperature. (daily only)  
- **weather**  
	    -  Dict containing day/night weather icon, description, and code.  

----------------------------------------------------


#### *class* weatherbit.models.SingleTimePoint  
---------------------------------------------

Contains data about a single point in time - Current weather data.  

**Attributes**  
- **snow**  
		-  Total Snowfall.  
- **precip**
		-  Total Liquid equivalent precipitation.  
- **snow3h**  
		-  Total 3h Snowfall.  
- **precip3h**  
		-  Total 3h  Liquid equivalent precipitation.  
- **datetime**  
		-  Datetime object - Datetime  (UTC).  
- **sunrise**  
		-  Datetime object - Sunrise time (UTC).  
- **sunset**  
		-  Datetime object - Sunset time  (UTC).  
- **wind_dir**  
		-  Wind direction in degrees (0-360).  
- **wind_spd**  
		-  Wind speed.   
- **rh**  
		-  Relative Humidity (%).  
- **slp**  
		-  Sea level pressure in millibars.  
- **temp**  
		-  Temperature.  
- **clouds**  
		-  Cloud cover (%).  
- **visibility**  
		-  Visibility text (for METAR observations only).  
- **station**  
		-  Station ID.  
- **weather**  
	    -  Dict containing day/night weather icon, description, and code.  
  
----------------------------------------------------
