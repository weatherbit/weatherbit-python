import requests
import threading
import datetime
from weatherbit.models import Forecast, History, Current

class Api(object):
    def __init__(self, key, granularity=None, https=False):

        self.key = key
        self.version = 'v1.0'
        self.forecast_granularity = None
        self.callback = None
        self.https = False

        if granularity:
            self.forecast_granularity = granularity

        if https:
            self.https = True

        self.api_domain = "api.weatherbit.io"

        return

    def _get_base_url(self):
        if self.https:
            base_url = "https://"
        else:
            base_url = "http://"
        return base_url + self.api_domain + "/" + self.version + "/"

    def _get_forecast_url(self, granularity):
        return self._get_base_url() + "forecast/" + granularity + "?key=" + self.key

    def _get_current_url(self):
        return self._get_base_url() + "current/" + "?key=" + self.key

    def _get_history_url(self, granularity):
        return self._get_base_url() + "history/" + granularity + "?key=" + self.key

    def get_forecast_url(self, **kwargs):
        base_url = self._get_forecast_url(kwargs['granularity'])

        # Build root geo-lookup.
        if 'lat' in kwargs and 'lon' in kwargs:
            arg_url_str = "&lat=%(lat)s&lon=%(lon)s"
        elif 'city' in kwargs:
            arg_url_str = "&city=%(city)s"
        elif 'city_id' in kwargs:
            arg_url_str = "&city_id=%(city_id)s"

        # Add on additional parameters.
        if 'state' in kwargs:
            arg_url_str = arg_url_str + "&state=%(state)s"
        if 'country' in kwargs:
            arg_url_str = arg_url_str + "&country=%(country)s"
        if 'days' in kwargs:
            arg_url_str = arg_url_str + "&days=%(days)s"
        if 'units' in kwargs:
            arg_url_str = arg_url_str + "&units=%(units)s"

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

        # Add on additional parameters.
        if 'state' in kwargs:
            arg_url_str = arg_url_str + "&state=%(state)s"
        if 'country' in kwargs:
            arg_url_str = arg_url_str + "&country=%(country)s"
        if 'units' in kwargs:
            arg_url_str = arg_url_str + "&units=%(units)s"

        return base_url + (arg_url_str % kwargs)

    def get_history_url(self, **kwargs):
        base_url = self._get_history_url(kwargs['granularity'])

        # Build root geo-lookup.
        if 'lat' in kwargs and 'lon' in kwargs:
            arg_url_str = "&lat=%(lat)s&lon=%(lon)s"
        elif 'city' in kwargs:
            arg_url_str = "&city=%(city)s"
        elif 'city_id' in kwargs:
            arg_url_str = "&city_id=%(city_id)s"

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

    def set_key(self, key):
        self.key = key

    def set_version(self, version):
        self.version = version

    def set_https(https = False):
        self.https = https
        return

    def set_forecast_granularity(self, granularity):
        self.forecast_granularity = granularity

    def get_forecast(self, **kwargs):
        
        if kwargs is None:
            raise Exception('Arguments Required.')

        if self.forecast_granularity:
            kwargs['granularity'] = self.forecast_granularity
        else:
            raise Exception('Granularity is not set on the Api object, or it has not been supplied via call.') 

        url = self.get_forecast_url(**kwargs)

        forecast = self._make_request(url, self._parse_forecast)

        return forecast

    def get_current(self, **kwargs):
        
        if kwargs is None:
            raise Exception('Arguments Required.')

        url = self.get_current_url(**kwargs)

        return self._make_request(url, self._parse_current)

    def get_history(self, **kwargs):
        
        if kwargs is None:
            raise Exception('Arguments Required.')

        if 'start_date' not in kwargs or 'end_date' not in kwargs:
            raise Exception('start_date, and end_date required.')

        start_date = kwargs['start_date']
        end_date = kwargs['end_date']

        # Only hourly is supported atm.
        kwargs['granularity'] = 'hourly'

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

        url = self.get_history_url(**kwargs)

        return self._make_request(url, self._parse_history)

    def _parse_forecast(self, request_url):
        weatherbitio_reponse = requests.get(request_url)
        weatherbitio_reponse.raise_for_status()
        json = weatherbitio_reponse.json()
        headers = weatherbitio_reponse.headers

        return Forecast(json, weatherbitio_reponse, headers)

    def _parse_history(self, request_url):
        weatherbitio_reponse = requests.get(request_url)
        weatherbitio_reponse.raise_for_status()
        json = weatherbitio_reponse.json()
        headers = weatherbitio_reponse.headers

        return History(json, weatherbitio_reponse, headers)

    def _parse_current(self, request_url):
        weatherbitio_reponse = requests.get(request_url)
        weatherbitio_reponse.raise_for_status()
        json = weatherbitio_reponse.json()
        headers = weatherbitio_reponse.headers

        return Current(json, weatherbitio_reponse, headers)

    def _make_request(self, request_url, callback=None):
        """
            This function is used by load_forecast OR by users to manually
            construct the URL for an API call.
        """
        return callback(request_url)

    def __load_async(self, url, callback):
        callback(url)