from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="unicarona")

def obter_coordenadas(endereco):
    location = geolocator.geocode(endereco)

    if location:
        return location.latitude, location.longitude
    print(location.address)
    print(location.latitude, location.longitude)

    return None, None


def calcular_distancia(coord1, coord2):
    return geodesic(coord1, coord2).km

