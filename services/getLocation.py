import requests

def getLocationByCEP(API_KEY, cep):

    session = requests.session()
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={cep}&key={api_key}'.format(cep=cep, api_key=API_KEY)

    response = session.get(url)
    content = response.json()
    
    if content['status'] == 'ZERO_RESULTS':
        return None
        
    print(content['results'][0]['geometry']['location'])
    return content['results'][0]['geometry']['location']