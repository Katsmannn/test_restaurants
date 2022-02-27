import requests

from .exceptions import NoRestaurantData


def get_restaurant_list(url):
    '''
    Получение списка ресторанов с ресурса url.
    '''
    try:
        restaurant_list = requests.get(url)
    except requests.exceptions.RequestException:
        return
    return restaurant_list.json()


def parse_kfc(restaurant_list):
    '''
    Парсер ответа с сайта KFC.

    Возвращает список ресторанов.
    Каждый ресторан выводится в виде словаря, содержащего ключи:
    'name' - название ресторана,
    'latitude', 'longitude' - географические координаты ресторана,
    'city' - город, в котором находится ресторан.
    '''

    result = []
    kfc = restaurant_list.get('searchResults')
    if kfc is None:
        raise NoRestaurantData(
            'Отсутствует информация о ресторанах KFC'
        )
    for restaurant in kfc:
        restaurant_data = restaurant['storePublic']
        restaurant_contacts = restaurant_data['contacts']
        name = restaurant_data['title']['ru']
        city = restaurant_contacts['city']['ru']
        coordinates = (
            restaurant_contacts['coordinates']['geometry']['coordinates']
        )
        latitude, longitude = coordinates[0], coordinates[1]
        if latitude is not None:
            result.append(
                {
                    'name': name,
                    'latitude': float(latitude),
                    'longitude': float(longitude),
                    'city': city
                }
            )
    return result


def parse_mcdolalds(restaurant_list):
    '''
    Парсер ответа с сайта McDonalds.

    Возвращает список ресторанов.
    Каждый ресторан выводится в виде словаря, содержащего ключи:
    'name' - название ресторана,
    'latitude', 'longitude' - географические координаты ресторана,
    'city' - город, в котором находится ресторан.
    '''

    result = []
    md = restaurant_list.get('restaurants')
    if md is None:
        raise NoRestaurantData(
            'Отсутствует информация о ресторанах McDonalds'
        )
    for restaurant in md:
        restaurant_location = restaurant['location']
        name = restaurant_location['code']
        city = restaurant_location['name']
        latitude = restaurant['latitude']
        longitude = restaurant['longitude']
        if latitude is not None:
            result.append(
                {
                    'name': name,
                    'latitude': float(latitude),
                    'longitude': float(longitude),
                    'city': city
                }
            )
    return result


def parse_burger_king(restaurant_list):
    '''
    Парсер ответа с сайта Burger King.

    Возвращает список ресторанов.
    Каждый ресторан выводится в виде словаря, содержащего ключи:
    'name' - название ресторана,
    'latitude', 'longitude' - географические координаты ресторана.
    '''

    result = []
    bk = restaurant_list.get('items')
    if bk is None:
        raise NoRestaurantData(
            'Отсутствует информация о ресторанах Burger King'
        )
    for restaurant in bk:
        name = restaurant['name']
        latitude = restaurant['latitude']
        longitude = restaurant['longitude']
        if latitude is not None:
            result.append(
                {
                    'name': name,
                    'latitude': float(latitude),
                    'longitude': float(longitude)
                }
            )
    return result


def increase_longitude(longitude, delta):
    '''
    Увеличение географической широты.
    Учитывает изменение знака при переходе через 180 меридиан.
    '''

    result = longitude + delta
    return result if result <= 180 else 360 - result


def decrease_longitude(longitude, delta):
    '''
    Увеличение географической широты.
    Учитывает изменение знака при переходе через 180 меридиан.
    '''

    result = longitude - delta
    return result if result >= -180.0 else 360 + result
