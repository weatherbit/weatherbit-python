from weatherbit.utils import UnicodeMixin, PropertyUnavailable
import datetime
import requests

class TimeSeries(UnicodeMixin):
    def __init__(self, data, response, headers):
        self.response = response
        self.http_headers = headers
        self.json = data
        self.points = []
        self._load(self.json)

            
    def update(self):
        """""
        Call update() to refresh the object state, and any stale data from the API.
        """""
        r = requests.get(self.response.url)
        self.json = r.json()
        self.response = r
        self.points = []
        self._load(self.json)

    def _load(self, response):
        self.city_name = response['city_name']
        self.lat = response['lat']
        self.lon = response['lon']
        self.country_code = response['country_code']
        self.state_code = response['state_code']
        self._load_from_points(response['data'])

    def _load_from_points(self, points):
        for point in points:
            self.points.append(Point(point))
        # Sort by datetime.
        self.points.sort(key=lambda p: p.datetime)

    def get_series(self, api_vars):
        """""
        Accepts either a list of variables, or a string (single var)
        Returns a list (sorted by datetime) of objects with the variables
        requested, and their corresponding dates.
        """""
        series = []

        if type(api_vars) == str:
            api_vars = [api_vars]

        for p in self.points:
            series_point = {}
            for var in api_vars:
                try:
                    series_point[var] = getattr(p, var)
                except AttributeError as e:
                    raise e
            series_point['datetime'] = p.datetime
            series.append(series_point)

        # Sort by datetime.
        series.sort(key=lambda p: p['datetime'])
        return series

class SingleTime(UnicodeMixin):
    def __init__(self, data, response, headers):
        self.response = response
        self.http_headers = headers
        self.json = data
        self.points = []
        self._load(self.json)

            
    def update(self):
        """""
        Call update() to refresh the object state, and any stale data from the API.
        """""
        r = requests.get(self.response.url)
        self.json = r.json()
        self.response = r
        self.points = []
        self._load(self.json)

    def _load(self, response):
        self.count = int(response['count'])
        self._load_from_points(response['data'])

    def _load_from_points(self, points):
        for point in points:
            self.points.append(SingleTimePoint(point))
        # Sort by datetime.
        self.points.sort(key=lambda p: p.datetime)


class Point(UnicodeMixin):
    def __init__(self, point):
        self.snow = point.get('snow')
        self.wind_dir = point.get('wind_dir')
        self.weather = point.get('weather')
        self.wind_spd = point.get('wind_spd')
        self.rh = point.get('rh')
        self.slp = point.get('slp')
        self.temp = point.get('temp')
        self.max_temp = point.get('max_temp')
        self.min_temp = point.get('min_temp')
        self.precip = point.get('precip')
        self.datetime = self._get_date_from_timestamp(point.get('datetime'))
        self.clouds = point.get('clouds')

        if 'precip6h' in point:
            self.precip6h = point.get('precip6h')
        else:
            self.precip6h = None
        if 'snow6h' in point:
            self.snow6h = point.get('snow6h')
        else:
            self.snow6h = None
    def _get_date_from_timestamp(self, datestamp):
        if ':' in datestamp:
            date = datetime.datetime.strptime(datestamp, '%Y-%m-%d:%H')
        else:
            date = datetime.datetime.strptime(datestamp, '%Y-%m-%d')
        return date

class SingleTimePoint(UnicodeMixin):
    def __init__(self, point):
        self.city_name = point.get('city_name')
        self.lat = point.get('lat')
        self.lon = point.get('lon')
        self.country_code = point.get('country_code')
        self.state_code = point.get('state_code')

        self.snow = point.get('snow')
        self.wind_dir = point.get('wind_dir')
        self.weather = point.get('weather')
        self.wind_spd = point.get('wind_spd')
        self.rh = point.get('rh')
        self.slp = point.get('slp')
        self.temp = point.get('temp')
        self.precip = point.get('precip')
        self.visibility = point.get('visibility')
        self.station = point.get('station')
        self.datetime = self._get_date_from_timestamp(point.get('datetime'))
        self.sunrise = self._get_date_from_timestamp(point.get('sunrise'), True)
        self.sunset = self._get_date_from_timestamp(point.get('sunset'), True)
        self.clouds = point.get('clouds')
        if 'precip3h' in point:
            self.precip3h = point.get('precip3h')
        else:
            self.precip3h = None
        if 'snow3h' in point:
            self.snow3h = point.get('snow3h')
        else:
            self.snow3h = None
    def _get_date_from_timestamp(self, datestamp, min_sec=False):
        
        if min_sec:
            date_format = "%H:%M:%S"
        else:
            date_format = "%Y-%m-%d:%H"

        return datetime.datetime.strptime(datestamp, date_format)


class Forecast(TimeSeries):
    """""
    The Forecast API Response class, extends TimeSeries.
    """""
    pass

class History(TimeSeries):
    """""
    The History API Response class, extends TimeSeries.
    """""
    pass

class Current(SingleTime):
    """""
    The Current API Response class, extends SingleTime.
    """""
    pass