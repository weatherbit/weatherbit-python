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
        self.city_name = response.get('city_name')
        self.lat = response.get('lat')
        self.lon = response.get('lon')
        self.country_code = response.get('country_code')
        self.state_code = response.get('state_code')
        self.timezone = response.get('timezone')
        self._load_from_points(response['data'])

    def _load_from_points(self, points):
        for point in points:
            self.points.append(Point(point))
        # Sort by datetime.
        self.points.sort(key=lambda p: p.timestamp_utc)

    def get(self, api_vars=None):
        return self.get_series(api_vars)

    def get_series(self, api_vars=None):
        """""
        Accepts either a list of variables, or a string (single var)
        Returns a list (sorted by datetime) of objects with the variables
        requested, and their corresponding dates.
        """""
        series = []
        exclude_none = False

        if api_vars is not None:
            if type(api_vars) != list:
                raise Exception("Field list must be list. Example: ['temp','slp']. See https://www.weatherbit.io/api for specific fields") 

        if api_vars is None or not api_vars or api_vars == []:
            # If api_vars is None or empty, include all non-None attributes
            api_vars = [attr for attr in dir(self.points[0]) if not callable(getattr(self.points[0], attr)) and not attr.startswith("__")]
            exclude_none = True

        for p in self.points:
            series_point = {}
            for var in api_vars:
                try:
                    val = getattr(p, var)
                    if exclude_none:
                        if val is not None:
                            series_point[var] = val
                        continue
                    series_point[var] = val
                except AttributeError as e:
                    raise e
            series_point['datetime'] = p.datetime
            series_point['timestamp_utc'] = p.timestamp_utc
            series_point['timestamp_local'] = p.timestamp_local
            series.append(series_point)

        # Sort by datetime.
        series.sort(key=lambda p: p['timestamp_utc'])
        return series

class NormalsTimeSeries(UnicodeMixin):
    def __init__(self, data, response, headers):
        self.response = response
        self.http_headers = headers
        self.json = data
        self.points = []
        self._load(self.json)

    def _sorting_key(self, point):
        return (point.month, point.day, point.hour)

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
        self.city_name = response.get('city_name')
        self.lat = response.get('lat')
        self.lon = response.get('lon')
        self.country_code = response.get('country_code')
        self.state_code = response.get('state_code')
        self.timezone = response.get('timezone')
        self._load_from_points(response['data'])

    def _load_from_points(self, points):
        for point in points:
            self.points.append(Point(point))
        # Sort by datetime.
        self.points = sorted(self.points, key=self._sorting_key)

    def get(self, api_vars=None):
        return self.get_series(api_vars)

    def get_series(self, api_vars=None):
        """""
        Accepts either a list of variables, or a string (single var)
        Returns a list (sorted by datetime) of objects with the variables
        requested, and their corresponding dates.
        """""
        series = []
        exclude_none = False

        if api_vars is not None:
            if type(api_vars) != list:
                raise Exception("Field list must be list. Example: ['temp','slp']. See https://www.weatherbit.io/api for specific fields") 

        if api_vars is None or not api_vars:
            # If api_vars is None or empty, include all non-None attributes
            api_vars = [attr for attr in dir(self.points[0]) if not callable(getattr(self.points[0], attr)) and not attr.startswith("__")]
            exclude_none = True


        for p in self.points:
            series_point = {}
            for var in api_vars:
                try:
                    val = getattr(p, var)
                    if exclude_none:
                        if val is not None:
                            series_point[var] = val
                        continue
                    series_point[var] = val
                except AttributeError as e:
                    raise e
            series_point['month'] = p.month
            series_point['day'] = p.month
            series_point['hour'] = p.hour
            series.append(series_point)

        # Sort by datetime.
        series = sorted(series, key=lambda x: (x.get('month', None), x.get('day', None), x.get('hour', None)))
        return series

class SingleTime(UnicodeMixin):
    def __init__(self, data, response, headers):
        self.response = response
        self.http_headers = headers
        self.json = data
        self.points = []
        self.points_minutely = []
        self.points_alerts = []
        self._load(self.json)

            
    def update(self):
        """""
        Call update() to refresh the object state, and any stale data from the API.
        """""
        r = requests.get(self.response.url)
        self.json = r.json()
        self.response = r
        self.points = []
        self.points_minutely = None
        self.points_alerts = None
        self._load(self.json)

    def _load(self, response):
        if 'count' in response:
            self.count = int(response['count'])
        if 'data' in response:
            self._load_from_points(response['data'])
        if 'minutely' in response:
            self._load_from_points_minutely(response['minutely'])
        if 'alerts' in response:
            self._load_from_points_alerts(response['alerts'])

    def _load_from_points(self, points):
        for point in points:
            self.points.append(SingleTimePoint(point))
        # Sort by datetime.
        self.points.sort(key=lambda p: p.datetime)

    def _load_from_points_minutely(self, points):
        self.points_minutely = []
        for point in points:
            self.points_minutely.append(Point(point))
        # Sort by datetime.
        self.points_minutely.sort(key=lambda p: p.timestamp_utc)

    def _load_from_points_alerts(self, points):
        self.points_alerts = []
        for point in points:
            self.points_alerts.append(SingleTimePoint(point))
        # Sort by datetime.
        self.points_alerts.sort(key=lambda p: p.effective_utc)

    def get(self, api_vars=None):
        """""
        Accepts either a list of variables, or a string (single var)
        Returns a list (sorted by datetime) of objects with the variables
        requested, and their corresponding dates.
        """""
        series = []
        exclude_none = False

        if api_vars is not None:
            if type(api_vars) != list:
                raise Exception("Field list must be list. Example: ['temp','slp']. See https://www.weatherbit.io/api for specific fields") 

        if len(self.points) > 0:
            if api_vars is None or not api_vars:
                # If api_vars is None or empty, include all non-None attributes
                api_vars = [attr for attr in dir(self.points[0]) if not callable(getattr(self.points[0], attr)) and not attr.startswith("__")]
                exclude_none = True

            for p in self.points:
                series_point = {}
                for var in api_vars:
                    try:
                        val = getattr(p, var)
                        if exclude_none:
                            if val is not None:
                                series_point[var] = val
                            continue
                        series_point[var] = val
                    except AttributeError as e:
                        raise e
                series_point['datetime'] = p.datetime
                series_point['timestamp_utc'] = p.timestamp_utc
                series_point['timestamp_local'] = p.timestamp_local
                if self.points_minutely is not None:
                    series_point['minutely'] = []
                    for pt in self.points_minutely:
                        series_point['minutely'].append({key: value for key, value in vars(pt).items() if not callable(value) and value is not None})

                if self.points_alerts is not None:
                    series_point['alerts'] = []
                    for pt in self.points_alerts:
                        series_point['alerts'].append({key: value for key, value in vars(pt).items() if not callable(value) and value is not None})

                series.append(series_point)
            series.sort(key=lambda p: p['datetime'])
        elif self.points_alerts is not None:
            # If api_vars is None or empty, include all non-None attributes
            if len(self.points_alerts) > 0:
                api_vars = [attr for attr in dir(self.points_alerts[0]) if not callable(getattr(self.points_alerts[0], attr)) and not attr.startswith("__")]
            exclude_none = True

            for p in self.points_alerts:
                series_point = {}
                for var in api_vars:
                    try:
                        val = getattr(p, var)
                        if val is not None:
                            series_point[var] = val
                    except AttributeError as e:
                        raise e
                series_point['effective_utc'] = p.effective_utc
                series_point['effective_local'] = p.effective_local
                series.append(series_point)
            series.sort(key=lambda p: p['effective_utc'])
        return series

class Point(UnicodeMixin):
    def __init__(self, point):
        self.revision_status = point.get('revision_status')

        self.pres = point.get('pres')
        self.slp = point.get('slp')
        self.weather = point.get('weather')
        self.rh = point.get('rh')
        self.dewpt = point.get('dewpt')
        self.temp = point.get('temp')
        self.app_temp = point.get('app_temp')
        self.app_max_temp = point.get('app_max_temp')
        self.app_min_temp = point.get('app_min_temp')
        self.max_temp = point.get('max_temp')
        self.high_temp = point.get('high_temp')
        self.min_temp = point.get('min_temp')
        self.low_temp = point.get('low_temp')
        self.precip = point.get('precip')
        self.precip_rate = point.get('precip_rate')
        self.pop = point.get('pop')
        self.snow = point.get('snow')
        self.snow_depth = point.get('snow_depth')
        self.ghi = point.get('ghi')
        self.dni = point.get('dni')
        self.dhi = point.get('dhi')
        self.pod = point.get('pod')
        self.uv  = point.get('uv')
        self.max_uv = point.get('max_uv')
        self.ghi  = point.get('ghi')
        self.t_ghi  = point.get('t_ghi')
        self.max_ghi  = point.get('max_ghi')
        self.dni  = point.get('dni')
        self.t_dni  = point.get('t_dni')
        self.max_dni  = point.get('max_dni')
        self.dhi  = point.get('dhi')
        self.t_dhi  = point.get('t_dhi')
        self.max_dhi  = point.get('max_dhi')
        self.solar_rad  = point.get('solar_rad')
        self.t_solar_rad  = point.get('t_solar_rad')
        self.elev_angle  = point.get('elev_angle')
        self.azimuth  = point.get('azimuth')        
        self.wind_gust_spd = point.get('wind_gust_spd')
        self.max_wind_ts = point.get('max_wind_ts')
        self.wind_spd = point.get('wind_spd')
        self.wind_dir = point.get('wind_dir')
        self.max_wind_spd = point.get('max_wind_spd')
        self.max_wind_dir = point.get('max_wind_dir')
        self.vis = point.get('vis')
        self.ozone = point.get('ozone')
        self.moon_phase = point.get('moon_phase')
        self.moon_phase_lunation = point.get('moon_phase_lunation')
        self.moonrise_ts = point.get('moonrise_ts')
        self.moonset_ts = point.get('moonset_ts')
        self.sunrise_ts = point.get('sunrise_ts')
        self.sunset_ts = point.get('sunset_ts')

        # AQ Vars:
        self.aqi = point.get('aqi')
        self.pm25 = point.get('pm25')
        self.pm10 = point.get('pm10')
        self.o3 = point.get('o3')
        self.no2 = point.get('no2')
        self.so2 = point.get('so2')
        self.co = point.get('co')

        if point.get('valid_date'):
            self.datetime = self._get_date_from_timestamp(point.get('valid_date'), True)
        elif point.get('datetime'):
            self.datetime = self._get_date_from_timestamp(point.get('datetime'), True)
        else:
            self.datetime = None
        if point.get('timestamp_utc') and point.get('timestamp_local'):
            self.timestamp_local = self._get_date_from_timestamp(point.get('timestamp_local'))
            self.timestamp_utc = self._get_date_from_timestamp(point.get('timestamp_utc'))
        else:
            # Set these to the datetime field - it is a date.
            self.timestamp_local = self.datetime
            self.timestamp_utc = self.datetime

        self.clouds = point.get('clouds')
        self.clouds_hi = point.get('clouds_hi')
        self.clouds_mid = point.get('clouds_mid')
        self.clouds_low = point.get('clouds_low')

        # AGW vars
        self.bulk_soil_density = point.get('bulk_soil_density')
        self.skin_temp_max = point.get('skin_temp_max')
        self.skin_temp_avg = point.get('skin_temp_avg')
        self.skin_temp_min = point.get('skin_temp_min')
        self.temp_2m_avg = point.get('temp_2m_avg')
        self.precip = point.get('precip')
        self.specific_humidity = point.get('specific_humidity')
        self.evapotranspiration = point.get('evapotranspiration')
        self.pres_avg = point.get('pres_avg')
        self.wind_10m_spd_avg = point.get('wind_10m_spd_avg')
        self.dlwrf_avg = point.get('dlwrf_avg')
        self.dlwrf_max = point.get('dlwrf_max')
        self.dswrf_avg = point.get('dswrf_avg')
        self.dswrf_max = point.get('dswrf_max')
        self.dswrf_net = point.get('dswrf_net')
        self.dlwrf_net = point.get('dlwrf_net')
        self.soilm_0_10cm = point.get('soilm_0_10cm')
        self.soilm_10_40cm = point.get('soilm_10_40cm')
        self.soilm_40_100cm = point.get('soilm_40_100cm')
        self.soilm_100_200cm = point.get('soilm_100_200cm')
        self.v_soilm_0_10cm = point.get('v_soilm_0_10cm')
        self.v_soilm_10_40cm = point.get('v_soilm_10_40cm')
        self.v_soilm_40_100cm = point.get('v_soilm_40_100cm')
        self.v_soilm_100_200cm = point.get('v_soilm_100_200cm')
        self.soilt_0_10cm = point.get('soilt_0_10cm')
        self.soilt_10_40cm = point.get('soilt_10_40cm')
        self.soilt_40_100cm = point.get('soilt_40_100cm')
        self.soilt_100_200cm = point.get('soilt_100_200cm')

        # Normals vars
        self.month = point.get('month')
        self.day = point.get('day')
        self.hour = point.get('hour')
        self.temp = point.get('temp')
        self.max_temp = point.get('max_temp')
        self.min_temp = point.get('min_temp')
        self.dewpt = point.get('dewpt')
        self.wind_spd = point.get('wind_spd')
        self.max_wind_spd = point.get('max_wind_spd')
        self.min_wind_spd = point.get('min_wind_spd')
        self.wind_dir = point.get('wind_dir')
        self.precip = point.get('precip')
        self.snow = point.get('snow')

    def _get_date_from_timestamp(self, datestamp, is_date=False):
        date_format = "%Y-%m-%dT%H:%M:%S"
        if is_date:
            if ':' in datestamp:
                date_format = '%Y-%m-%d:%H'
            else:
                date_format = '%Y-%m-%d'

        return datetime.datetime.strptime(datestamp, date_format)

class SingleTimePoint(UnicodeMixin):
    def __init__(self, point):
        self.city_name = point.get('city_name')
        self.lat = point.get('lat')
        self.lon = point.get('lon')
        self.country_code = point.get('country_code')
        self.state_code = point.get('state_code')
        self.timezone = point.get('timezone')

        self.snow = point.get('snow')
        self.wind_dir = point.get('wind_dir')
        self.weather = point.get('weather')
        self.pod = point.get('pod')
        self.wind_spd = point.get('wind_spd')
        self.rh = point.get('rh')
        self.pres = point.get('pres')
        self.slp = point.get('slp')
        self.temp = point.get('temp')
        self.app_temp = point.get('app_temp')
        self.precip = point.get('precip')
        self.visibility = point.get('visibility')
        self.vis = point.get('vis')
        self.station = point.get('station')
        if point.get('datetime'):
            self.datetime = self._get_date_from_timestamp(point.get('datetime'), False, True)
        else:
            self.datetime = None
        if point.get('timestamp_utc') and point.get('timestamp_local'):
            self.timestamp_local = self._get_date_from_timestamp(point.get('timestamp_local'))
            self.timestamp_utc = self._get_date_from_timestamp(point.get('timestamp_utc'))
        else:
            self.timestamp_local = None
            self.timestamp_utc = self.datetime
        if point.get('sunrise') and point.get('sunset'):
            self.sunrise = self._get_date_from_timestamp(point.get('sunrise'), True)
            self.sunset = self._get_date_from_timestamp(point.get('sunset'), True)
        self.ghi = point.get('ghi')
        self.dni = point.get('dni')
        self.dhi = point.get('dhi')
        self.solar_rad = point.get('solar_rad')
        self.elev_angle = point.get('elev_angle')
        self.uv  = point.get('uv')
        self.aqi = point.get('aqi')
        self.clouds = point.get('clouds')

        # AQ Vars:
        self.pm25 = point.get('pm25')
        self.pm10 = point.get('pm10')
        self.o3 = point.get('o3')
        self.no2 = point.get('no2')
        self.so2 = point.get('so2')
        self.co = point.get('co')
        self.pollen_level_tree = point.get('pollen_level_tree')
        self.pollen_level_grass = point.get('pollen_level_grass')
        self.pollen_level_weed = point.get('pollen_level_weed')
        self.mold_level = point.get('mold_level')
        self.predominant_pollen_type = point.get('predominant_pollen_type')

        # Alert Vars:
        self.title = point.get('title')
        self.description = point.get('description')
        self.severity = point.get('severity')
        self.effective_utc = point.get('effective_utc')
        self.effective_local = point.get('effective_local')
        self.expires_utc = point.get('expires_utc')
        self.expires_local = point.get('expires_local')
        self.onset_utc = point.get('onset_utc')
        self.onset_local = point.get('onset_local')
        self.ends_utc = point.get('ends_utc')
        self.ends_local = point.get('ends_local')
        self.uri = point.get('uri')
        self.regions = point.get('regions')

    def _get_date_from_timestamp(self, datestamp, hr_min=False, is_date=False):
        date_format = "%Y-%m-%dT%H:%M:%S"
        
        if hr_min:
            date_format = "%H:%M"
        elif is_date:
            date_format = "%Y-%m-%d:%H"
        else:
            date_format = "%Y-%m-%dT%H:%M:%S"

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

class Normals(NormalsTimeSeries):
    """""
    The Normals API Response class, extends NormalsTimeSeries.
    """""
    pass

class Current(SingleTime):
    """""
    The Current API Response class, extends SingleTime.
    """""
    pass

class Alert(SingleTime):
    """""
    The Alert API Response class, extends SingleTime.
    """""
    pass