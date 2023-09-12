""" soteriareitti/utils/utils_geo.py """
import math


class Location:
    """ Location class represents a point location on a map"""

    def __init__(self, longitude: float, latitude: float):
        """ 
        Initialize a location with longitude and latitude 

        Remember that longitude is the x-axis and latitude is the y-axis
        Longitude and latitude are in degrees
        """
        self.longitude = longitude
        self.latitude = latitude

    def __str__(self):
        return f"Location: ({self.longitude}, {self.latitude})"

    def as_tuple(self) -> tuple[float, float]:
        return (self.longitude, self.latitude)

    @property
    def longitude_rad(self) -> float:
        """ Return longitude in radians """
        return math.radians(self.longitude)

    @property
    def latitude_rad(self) -> float:
        """ Return latitude in radians """
        return math.radians(self.latitude)


class Distance:
    """ Distance class represents a distance on the map"""

    def __init__(self, distance_meters: float):
        self.__distance_meters = distance_meters

    @property
    def meters(self) -> float:
        return self.__distance_meters

    @property
    def kilometers(self) -> float:
        return self.__distance_meters/1000


class GeoUtils:
    earth_radius = Distance(6378137)  # Earth radius in meters

    @staticmethod
    def calculate_distance(location_source: Location, location_target: Location) -> Distance:
        """ Calculate distance between two locations """
        difference_longitude = location_target.longitude_rad - location_source.longitude_rad
        difference_latitude = location_target.latitude_rad - location_source.latitude_rad

        # Haversine formula
        # https://www.movable-type.co.uk/scripts/latlong.html

        # pylint: disable-next=invalid-name
        a = math.sin(difference_latitude / 2)**2 + math.cos(location_source.latitude_rad) * \
            math.cos(location_target.latitude_rad) * math.sin(difference_longitude / 2)**2

        # pylint: disable-next=invalid-name
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        # pylint: disable-next=invalid-name
        d = GeoUtils.earth_radius.meters * c

        return Distance(d)
