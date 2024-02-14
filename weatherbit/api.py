import requests
import threading
import datetime
from weatherbit.models import Forecast, History, Current, Normals, Alert
from weatherbit.utils import is_valid_day_format

class Api(object):
    def __init__(self, key, granularity=None, history_granularity=None, https=True):
        self.key = key
        self.version = 'v2.0'
        self.forecast_granularity = 'daily'
        self.history_granularity = 'hourly'
        self.callback = None
        self.https = https

        if granularity:
            self.forecast_granularity = granularity

        if history_granularity:
            self.history_granularity = history_granularity

        self.api_domain = "api.weatherbit.io"
        return

    def _get_base_url(self):
        if self.https:
            base_url = "https://"
        else:
            base_url = "http://"
        return base_url + self.api_domain + "/" + self.version + "/"

    def _get_forecast_url(self, granularity):
        return self._get_base_url() + "forecast/" + granularity + "?key=" + self.key + "&client=wbitpython"

    def _get_forecast_url_AQ(self):
        return self._get_base_url() + "forecast/airquality?key=" + self.key + "&client=wbitpython"

    def _get_forecast_url_AGW(self):
        return self._get_base_url() + "forecast/agweather?key=" + self.key + "&client=wbitpython"

    def _get_current_url(self):
        return self._get_base_url() + "current?key=" + self.key + "&client=wbitpython"

    def _get_alerts_url(self):
        return self._get_base_url() + "alerts?key=" + self.key + "&client=wbitpython"

    def _get_current_url_AQ(self):
        return self._get_base_url() + "current/airquality?key=" + self.key + "&client=wbitpython"

    def _get_history_url(self, granularity):
        return self._get_base_url() + "history/" + granularity + "?key=" + self.key + "&client=wbitpython"

    def _get_history_url_AQ(self):
        return self._get_base_url() + "history/airquality?key=" + self.key + "&client=wbitpython"

    def _get_history_url_AGW(self):
        return self._get_base_url() + "history/agweather?key=" + self.key + "&client=wbitpython"

    def _get_history_url_normals(self):
        return self._get_base_url() + "normals?key=" + self.key + "&client=wbitpython"

    def get_forecast_url(self, **kwargs):

        granularity = self.forecast_granularity

        if 'granularity' in kwargs:
            granularity = kwargs['granularity']
        elif 'tp' in kwargs:
            granularity = kwargs['tp']

        if granularity not in ['minutely', 'hourly', 'daily']:
            raise Exception('Unsupported granularity')

        base_url = self._get_forecast_url(granularity)

        # Build root geo-lookup.
        if 'lat' in kwargs and 'lon' in kwargs:
            arg_url_str = "&lat=%(lat)s&lon=%(lon)s"
        elif 'city' in kwargs:
            arg_url_str = "&city=%(city)s"
        elif 'city_id' in kwargs:
            arg_url_str = "&city_id=%(city_id)s"
        elif 'station' in kwargs:
            arg_url_str = "&station=%(station)s"
        elif 'postal_code' in kwargs:
            arg_url_str = "&postal_code=%(postal_code)s"

        # Add on additional parameters.
        if 'state' in kwargs:
            arg_url_str = arg_url_str + "&state=%(state)s"
        if 'country' in kwargs:
            arg_url_str = arg_url_str + "&country=%(country)s"
        if 'days' in kwargs:
            if granularity != 'daily':
                print("WARNING: 'days' parameter ignored")
            else:
                arg_url_str = arg_url_str + "&days=%(days)s"
        if 'units' in kwargs:
            arg_url_str = arg_url_str + "&units=%(units)s"
        if 'hours' in kwargs:
            if granularity != 'hourly':
                print("WARNING: 'hours' parameter ignored")
            else:
                arg_url_str = arg_url_str + "&hours=%(hours)s"

        return base_url + (arg_url_str % kwargs)

    def get_forecast_url_AQ(self, **kwargs):
        base_url = self._get_forecast_url_AQ()

        if 'tp' in kwargs:
            tp = kwargs['tp']
        else:
            tp = self.forecast_granularity

        if tp not in ['hourly']:
            print("WARNING: Unsupported granularity supplied. Returning default granularity")

        # Build root geo-lookup.
        if 'lat' in kwargs and 'lon' in kwargs:
            arg_url_str = "&lat=%(lat)s&lon=%(lon)s"
        elif 'city' in kwargs:
            arg_url_str = "&city=%(city)s"
        elif 'city_id' in kwargs:
            arg_url_str = "&city_id=%(city_id)s"
        elif 'station' in kwargs:
            arg_url_str = "&station=%(station)s"
        elif 'postal_code' in kwargs:
            arg_url_str = "&postal_code=%(postal_code)s"

        # Add on additional parameters.
        if 'state' in kwargs:
            arg_url_str = arg_url_str + "&state=%(state)s"
        if 'country' in kwargs:
            arg_url_str = arg_url_str + "&country=%(country)s"
        if 'days' in kwargs:
            arg_url_str = arg_url_str + "&days=%(days)s"
        if 'units' in kwargs:
            arg_url_str = arg_url_str + "&units=%(units)s"
        if 'hours' in kwargs:
            arg_url_str = arg_url_str + "&hours=%(hours)s"

        return base_url + (arg_url_str % kwargs)

    def get_current_url(self, **kwargs):
        base_url = self._get_current_url()

        # Build root geo-lookup.
        if 'lat' in kwargs and 'lon' in kwargs:
            arg_url_str = "&lat=%(lat)s&lon=%(lon)s"
        elif 'city' in kwargs:
            arg_url_str = "&city=%(city)s"
        elif 'city_id' in kwargs:
            arg_url_str = "&city_id=%(city_id)s"
        elif 'station' in kwargs:
            arg_url_str = "&station=%(station)s"
        elif 'postal_code' in kwargs:
            arg_url_str = "&postal_code=%(postal_code)s"

        # Add on additional parameters.
        if 'state' in kwargs:
            arg_url_str = arg_url_str + "&state=%(state)s"
        if 'country' in kwargs:
            arg_url_str = arg_url_str + "&country=%(country)s"
        if 'units' in kwargs:
            arg_url_str = arg_url_str + "&units=%(units)s"
        if 'include' in kwargs:
            arg_url_str = arg_url_str + "&include=%(include)s"

        return base_url + (arg_url_str % kwargs)

    def get_alerts_url(self, **kwargs):
        base_url = self._get_alerts_url()

        # Build root geo-lookup.
        if 'lat' in kwargs and 'lon' in kwargs:
            arg_url_str = "&lat=%(lat)s&lon=%(lon)s"
        elif 'city' in kwargs:
            arg_url_str = "&city=%(city)s"
        elif 'city_id' in kwargs:
            arg_url_str = "&city_id=%(city_id)s"
        elif 'station' in kwargs:
            arg_url_str = "&station=%(station)s"
        elif 'postal_code' in kwargs:
            arg_url_str = "&postal_code=%(postal_code)s"

        # Add on additional parameters.
        if 'state' in kwargs:
            arg_url_str = arg_url_str + "&state=%(state)s"
        if 'country' in kwargs:
            arg_url_str = arg_url_str + "&country=%(country)s"

        return base_url + (arg_url_str % kwargs)

    def get_current_url_AQ(self, **kwargs):
        base_url = self._get_current_url_AQ()

        # Build root geo-lookup.
        if 'lat' in kwargs and 'lon' in kwargs:
            arg_url_str = "&lat=%(lat)s&lon=%(lon)s"
        elif 'city' in kwargs:
            arg_url_str = "&city=%(city)s"
        elif 'city_id' in kwargs:
            arg_url_str = "&city_id=%(city_id)s"
        elif 'postal_code' in kwargs:
            arg_url_str = "&postal_code=%(postal_code)s"

        # Add on additional parameters.
        if 'state' in kwargs:
            arg_url_str = arg_url_str + "&state=%(state)s"
        if 'country' in kwargs:
            arg_url_str = arg_url_str + "&country=%(country)s"
        if 'units' in kwargs:
            arg_url_str = arg_url_str + "&units=%(units)s"

        return base_url + (arg_url_str % kwargs)


    def get_forecast_url_AGW(self, **kwargs):
        base_url = self._get_forecast_url_AGW()

        # Build root geo-lookup.
        if 'lat' in kwargs and 'lon' in kwargs:
            arg_url_str = "&lat=%(lat)s&lon=%(lon)s"
        else:
            raise Exception('Unsupported geolocation type. Lat/Lon only.')

        if 'tp' in kwargs:
            tp = kwargs['tp']
        else:
            tp = self.forecast_granularity

        if tp in ['daily']:
            arg_url_str = arg_url_str + "&tp={}".format(tp)
        else:
            print("WARNING: Unsupported granularity supplied. Returning default granularity")

        return base_url + (arg_url_str % kwargs)

    def get_history_url(self, **kwargs):

        granularity = kwargs['granularity']

        if granularity not in ['subhourly', 'hourly', 'daily']:
            raise Exception('Unsupported granularity')

        base_url = self._get_history_url(kwargs['granularity'])

        # Build root geo-lookup.
        if 'lat' in kwargs and 'lon' in kwargs:
            arg_url_str = "&lat=%(lat)s&lon=%(lon)s"
        elif 'city' in kwargs:
            arg_url_str = "&city=%(city)s"
        elif 'city_id' in kwargs:
            arg_url_str = "&city_id=%(city_id)s"
        elif 'station' in kwargs:
            arg_url_str = "&station=%(station)s"
        elif 'postal_code' in kwargs:
            arg_url_str = "&postal_code=%(postal_code)s"

        # Add on additional parameters.
        if 'start_date' in kwargs:
            arg_url_str = arg_url_str + "&start_date=%(start_date)s"
        if 'end_date' in kwargs:
            arg_url_str = arg_url_str + "&end_date=%(end_date)s"

        if 'state' in kwargs:
            arg_url_str = arg_url_str + "&state=%(state)s"
        if 'country' in kwargs:
            arg_url_str = arg_url_str + "&country=%(country)s"
        if 'units' in kwargs:
            arg_url_str = arg_url_str + "&units=%(units)s"

        return base_url + (arg_url_str % kwargs)

    def get_history_url_AQ(self, **kwargs):
        base_url = self._get_history_url_AQ()

        # Build root geo-lookup.
        if 'lat' in kwargs and 'lon' in kwargs:
            arg_url_str = "&lat=%(lat)s&lon=%(lon)s"
        elif 'city' in kwargs:
            arg_url_str = "&city=%(city)s"
        elif 'city_id' in kwargs:
            arg_url_str = "&city_id=%(city_id)s"
        elif 'station' in kwargs:
            arg_url_str = "&station=%(station)s"

        # Add on additional parameters.
        if 'start_date' in kwargs:
            arg_url_str = arg_url_str + "&start_date=%(start_date)s"
        if 'end_date' in kwargs:
            arg_url_str = arg_url_str + "&end_date=%(end_date)s"

        if 'state' in kwargs:
            arg_url_str = arg_url_str + "&state=%(state)s"
        if 'country' in kwargs:
            arg_url_str = arg_url_str + "&country=%(country)s"
        if 'units' in kwargs:
            arg_url_str = arg_url_str + "&units=%(units)s"

        if 'tp' in kwargs:
            tp = kwargs['tp']
        else:
            tp = self.history_granularity

        if tp in ['hourly']:
            arg_url_str = arg_url_str + "&tp={}".format(tp)
        else:
            print("WARNING: Unsupported granularity supplied. Returning default granularity")

        return base_url + (arg_url_str % kwargs)

    def get_history_url_AGW(self, **kwargs):
        base_url = self._get_history_url_AGW()

        # Build root geo-lookup.
        if 'lat' in kwargs and 'lon' in kwargs:
            arg_url_str = "&lat=%(lat)s&lon=%(lon)s"
        else:
            raise Exception('Unsupported geolocation type. Lat/Lon only.')
        # Add on additional parameters.
        if 'start_date' in kwargs:
            arg_url_str = arg_url_str + "&start_date=%(start_date)s"
        if 'end_date' in kwargs:
            arg_url_str = arg_url_str + "&end_date=%(end_date)s"

        if 'units' in kwargs:
            arg_url_str = arg_url_str + "&units=%(units)s"

        if 'tp' in kwargs:
            tp = kwargs['tp']
        else:
            tp = self.history_granularity

        if tp in ['hourly','daily']:
            arg_url_str = arg_url_str + "&tp={}".format(tp)
        else:
            print("WARNING: Unsupported granularity supplied. Returning default granularity")

        return base_url + (arg_url_str % kwargs)

    def get_normals_url(self, **kwargs):
        base_url = self._get_history_url_normals()

        # Build root geo-lookup.
        if 'lat' in kwargs and 'lon' in kwargs:
            arg_url_str = "&lat=%(lat)s&lon=%(lon)s"
        else:
            raise Exception('Unsupported geolocation type. Lat/Lon only.')
        # Add on additional parameters.
        if 'start_day' in kwargs and 'end_day' in kwargs:
            arg_url_str = arg_url_str + "&start_day=%(start_day)s"
            arg_url_str = arg_url_str + "&end_day=%(end_day)s"
        else:
            raise Exception('start_day and end_day required.')

        if 'units' in kwargs:
            arg_url_str = arg_url_str + "&units=%(units)s"

        if 'series_year' in kwargs:
            arg_url_str = arg_url_str + "&series_year=%(units)s"

        if 'tp' in kwargs:
            tp = kwargs['tp']
        else:
            tp = self.history_granularity

        if tp in ['hourly','daily', 'monthly']:
            arg_url_str = arg_url_str + "&tp={}".format(tp)
        else:
            print("WARNING: Unsupported granularity supplied. Returning default granularity")

        return base_url + (arg_url_str % kwargs)

    def set_key(self, key):
        self.key = key

    def set_version(self, version):
        self.version = version

    def set_https(https = False):
        self.https = https
        return

    def set_forecast_granularity(self, granularity):
        self.forecast_granularity = granularity

    def set_history_granularity(self, granularity):
        self.history_granularity = granularity

    def set_granularity(self, granularity):
        self.history_granularity = granularity
        self.forecast_granularity = granularity

    def get_forecast(self, source = None, **kwargs):
        
        if kwargs is None:
            raise Exception('Arguments Required.')

        if source == 'airquality':
            url = self.get_forecast_url_AQ(**kwargs)
        elif source == 'agweather':
            url = self.get_forecast_url_AGW(**kwargs)
        else:
            if 'tp' not in kwargs and self.forecast_granularity is None:
                raise Exception("Granularity is not set on the Api object, or it has not been supplied via tp parameter.") 
            url = self.get_forecast_url(**kwargs)

        forecast = self._make_request(url, self._parse_forecast)

        return forecast

    def get_current(self, source = None, **kwargs):
        
        if kwargs is None:
            raise Exception('Arguments Required.')

        if source == 'airquality':
            url = self.get_current_url_AQ(**kwargs)
        else:
            url = self.get_current_url(**kwargs)

        return self._make_request(url, self._parse_current)

    def get_alerts(self, source = None, **kwargs):
        
        if kwargs is None:
            raise Exception('Arguments Required.')

        url = self.get_alerts_url(**kwargs)

        return self._make_request(url, self._parse_alerts)

    def get_history(self, source = None, **kwargs):
        
        if kwargs is None:
            raise Exception('Arguments Required.')

        if 'start_date' not in kwargs or 'end_date' not in kwargs:
            raise Exception('start_date, and end_date required.')

        start_date = kwargs['start_date']
        end_date = kwargs['end_date']

        kwargs['granularity'] = self.history_granularity

        # Convert start_date, and end_dates into strings.
        # Assumes all time is in UTC.
        # TODO: Make timezone aware using pytz.
        if type(start_date) is datetime.date:
            if start_date.hour > 0:
                kwargs['start_date'] = start_date.strftime('%Y-%m-%d:%H')
            else:
                kwargs['start_date'] = end_date.strftime('%Y-%m-%d')

        if type(end_date) is datetime.date:
            if end_date.hour > 0:
                kwargs['end_date'] = end_date.strftime('%Y-%m-%d:%H')
            else:
                kwargs['end_date'] = end_date.strftime('%Y-%m-%d')

        if source == 'airquality':
            url = self.get_history_url_AQ(**kwargs)
        elif source == 'agweather':
            url = self.get_history_url_AGW(**kwargs)
        else:
            url = self.get_history_url(**kwargs)

        return self._make_request(url, self._parse_history)

    def get_normals(self, **kwargs):
        
        if kwargs is None:
            raise Exception('Arguments Required.')

        if 'start_day' not in kwargs or 'end_day' not in kwargs:
            raise Exception('start_day, and end_day required.')

        if not is_valid_day_format(kwargs['start_day']) or not is_valid_day_format(kwargs['end_day']):
            raise Exception('Invalid start_day, and end_day supplied. Expected format MM-DD')
        start_day = kwargs['start_day']
        end_day = kwargs['end_day']

        kwargs['granularity'] = self.history_granularity

        url = self.get_normals_url(**kwargs)

        return self._make_request(url, self._parse_normals)

    def _parse_forecast(self, request_url):
        weatherbitio_reponse = requests.get(request_url)
        if weatherbitio_reponse.status_code != 200:
            raise Exception(weatherbitio_reponse.json())
        json = weatherbitio_reponse.json()
        headers = weatherbitio_reponse.headers

        return Forecast(json, weatherbitio_reponse, headers)

    def _parse_history(self, request_url):
        weatherbitio_reponse = requests.get(request_url)
        if weatherbitio_reponse.status_code != 200:
            raise Exception(weatherbitio_reponse.json())
        json = weatherbitio_reponse.json()
        headers = weatherbitio_reponse.headers

        return History(json, weatherbitio_reponse, headers)

    def _parse_normals(self, request_url):
        weatherbitio_reponse = requests.get(request_url)
        if weatherbitio_reponse.status_code != 200:
            raise Exception(weatherbitio_reponse.json())
        json = weatherbitio_reponse.json()
        headers = weatherbitio_reponse.headers

        return Normals(json, weatherbitio_reponse, headers)

    def _parse_current(self, request_url):
        weatherbitio_reponse = requests.get(request_url)
        if weatherbitio_reponse.status_code != 200:
            raise Exception(weatherbitio_reponse.json())
        json = weatherbitio_reponse.json()
        headers = weatherbitio_reponse.headers

        return Current(json, weatherbitio_reponse, headers)

    def _parse_alerts(self, request_url):
        weatherbitio_reponse = requests.get(request_url)
        if weatherbitio_reponse.status_code != 200:
            raise Exception(weatherbitio_reponse.json())
        json = weatherbitio_reponse.json()
        headers = weatherbitio_reponse.headers

        return Alert(json, weatherbitio_reponse, headers)

    def _make_request(self, request_url, callback=None):
        """
            This function is used by load_forecast OR by users to manually
            construct the URL for an API call.
        """
        return callback(request_url)

    def __load_async(self, url, callback):
        callback(url)