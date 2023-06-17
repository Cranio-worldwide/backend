from http import HTTPStatus

import requests


def get_user_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip_address = user_ip_address.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    return ip_address


def get_geodata(ip_address):
    if ip_address == '127.0.0.1' or ip_address.startswith('172'):
        endpoints = (
            # temporary solution for development process
            'https://ipapi.co/json/',
            'https://api.ipgeolocation.io/ipgeo?'
            'apiKey=2b3f60044ccf4af3b5b67882e3c2172f',
        )
    else:
        endpoints = (
            # these endpoints provide 1000 free requests/day, more to be added
            f'https://ipapi.co/{ip_address}/json/',
            'https://api.ipgeolocation.io/ipgeo?'
            f'apiKey=2b3f60044ccf4af3b5b67882e3c2172f&ip={ip_address}',
        )
    for endpoint in endpoints:
        response = requests.get(endpoint)
        if response.status_code == HTTPStatus.OK:
            return response.json()
    return None


def parse_coordinates(geodata):
    return f"{geodata.get('latitude')}, {geodata.get('longitude')}"
