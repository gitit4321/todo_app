import requests
import pyperclip as pc
from validators import url as valid_url
from validators import between


def get_shortened_url(url):
    if valid_url(url):
        data = {'original_url': url}
        res = requests.post('http://localhost:4000/shorten', json=data)
        response = res.json()
        shortened_url = response['shortenedUrl']
        return shortened_url
    return 'not_valid'

def get_map_info(origin_zip, destination_zip):
    if between(int(origin_zip), min=1000, max=99999) and between(int(destination_zip), min=1000, max=99999):
        payload = {'Origin': origin_zip,
                'Destination': destination_zip}
        res = requests.get('https://marsican.app/maps/distance', params=payload)
        response = res.json()
        print(response['rows'][0]['elements'][0])
        time_to_dest = response['rows'][0]['elements'][0]['duration']['text']
        dist_to_dest = response['rows'][0]['elements'][0]['distance']['text']
        origin_city = response['origin_addresses'][0][:-11]
        dest_city = response['destination_addresses'][0][:-11]
        output = f'It will take roughly {time_to_dest} to drive the {dist_to_dest} from {origin_city} to {dest_city}.'
        return output
    return 'not_valid'

def get_translation(query):
    dummy_responses =  {
    "translation": "Your translated response"
    }
    translation = dummy_responses['translation']
    return translation
