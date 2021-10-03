import pycep_correios
from geopy.geocoders import Nominatim
from googleplaces import GooglePlaces, types, lang
import requests
import json

def GetNearHospital(cep):
    endereco = pycep_correios.get_address_from_cep(cep)
    print(endereco)
    geolocator = Nominatim(user_agent="teste123")
    location = geolocator.geocode(endereco['logradouro'] + ", " + endereco['cidade'] + " - " + endereco['bairro'])
    if not location:
        return None

    API_KEY = open('services/apiKeyGoogle.txt').read()

    google_places = GooglePlaces(API_KEY)

    query_result = google_places.nearby_search(
        lat_lng={'lat': location.latitude, 'lng': location.longitude},
        radius=5000,
        types=[types.TYPE_HOSPITAL])


    if query_result.has_attributions:
        print(query_result.html_attributions)
    for place in query_result.places:
        if 'UBS' in place.name or 'Hospital' in place.name or 'Unidade de Saúde' in place.name or 'Unidade de Saude' in place.name:
            return place

    return None
