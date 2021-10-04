import pycep_correios
from services.getLocation import getLocationByCEP
from googleplaces import GooglePlaces, types, lang

def GetNearHospital(cep):

    API_KEY = open('services/apiKeyGoogle.txt').read()

    endereco = pycep_correios.get_address_from_cep(cep)
    print(endereco)
    location = getLocationByCEP(API_KEY, endereco['cep'])
    if not location:
        return None

    google_places = GooglePlaces(API_KEY)

    query_result = google_places.nearby_search(
        lat_lng={'lat': location['lat'], 'lng': location['lng']},
        radius=5000,
        types=[types.TYPE_HOSPITAL],
        rankby='distance')

    print('Locais encontrados:')
    if query_result.has_attributions:
        print(query_result.html_attributions)
    for place in query_result.places:
        print(place.name)
        if 'UBS' in place.name or 'Hospital' in place.name or 'Unidade de Saúde' in place.name or 'Unidade de Saude' in place.name:
            return place

    return None
