import requests


def get_shortened_url(url):
    data = {'original_url': url}
    res = requests.post('http://localhost:4000/shorten', json=data)
    response = res.json()
    shortened_url = response['shortenedUrl']
    if shortened_url == 'Not found!':
        return 'Please enter a valid URL.'
    return shortened_url

def get_google_map_link(location):
    dummy_responses =  {
    "g_link": "Google link response"
    }
    map_link = dummy_responses['g_link']
    return map_link

def get_translation(query):
    dummy_responses =  {
    "translation": "Your translated response"
    }
    translation = dummy_responses['translation']
    return translation

# print(get_shortened_url(URL))