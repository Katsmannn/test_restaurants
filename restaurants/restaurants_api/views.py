from rest_framework.decorators import api_view
from rest_framework.response import Response
from geopy import distance

from data.parameters import KFC_URL, BK_URL, MD_URL, DISTANCE
from .utils import (
    get_restaurant_list,
    parse_burger_king,
    parse_kfc,
    parse_mcdolalds,
    decrease_longitude,
    increase_longitude,
)
from .models import Restaurant, Company
from .exceptions import NoRestaurantData


@api_view(['POST'])
def database_update(request):
    '''
    Получение данных о ресторанах с соответствущих URL,
    запись информации в базу данных.
    '''

    COMPANY_LIST = [
      {'url': BK_URL, 'name': 'Burger King', 'parser': parse_burger_king},
      {'url': KFC_URL, 'name': 'KFC', 'parser': parse_kfc},
      {'url': MD_URL, 'name': 'McDonalds', 'parser': parse_mcdolalds},
    ]

    errors = []
    for company in COMPANY_LIST:
        try:
            company_name = company.get('name')
            restaurant_list = get_restaurant_list(company.get('url'))
            if restaurant_list is None:
                errors.append(
                    {
                        'error': f'Сайт {company_name} не доступен.'
                    }
                )
                continue
            company_object = Company.objects.get(name=company_name)
            for restaurant in company['parser'](restaurant_list):
                Restaurant.objects.get_or_create(
                    **restaurant,
                    company=company_object
                )
        except NoRestaurantData as err:
            errors.append(
                {
                    'error': f'{err}'
                }
            )
            continue
        except Exception as e:
            errors.append(
                {
                    'error': f'{e}'
                }
            )
            continue
    return Response(
        {
            'status': 'Информация в базе данных обновлена.',
            'errors': errors
        }
    )


@api_view(['GET'])
def get_restaurants_list(request):
    '''
    Вывод списка ресторанов Burger King.

    Для каждого ресторана выводится количество ресторанов конкурентов,
    находящихся на расстоянии не далее DISTANCE км.
    Выборка ресторанов по расстоянию производится в два этапа:
    - предварительный отбор конкурентов, расположенных в пределах
    DELTA_LATITUDE и DELTA_LONGITUDE от ресторана. DELTA_LATITUDE
    и DELTA_LONGITUDE гарантированно перекрывают DISTANCE во всём диапазоне
    возможных координат;
    - уточнение расстояния до объектов, отобранных на предыдущем этапе.
    Для упрощения рассчётов принимаем, что все рестораны находятся
    исключительно в восточном полушарии.
    '''

    DELTA_LATITUDE = 0.0224
    DELTA_LONGITUDE = 0.125

    result = []
    try:
        bk_list = Restaurant.objects.filter(company__name='Burger King')
        for restaurant in bk_list:
            restaurant_latitude = restaurant.latitude
            restaurant_longitude = restaurant.longitude
            north_border = restaurant_latitude + DELTA_LATITUDE
            south_border = restaurant_latitude - DELTA_LATITUDE
            west_border = decrease_longitude(
                restaurant_longitude,
                DELTA_LONGITUDE
            )
            east_border = increase_longitude(
                restaurant_longitude,
                DELTA_LONGITUDE
            )
            neighbors = Restaurant.objects.filter(
                company__name__in=['McDonalds', 'KFC'],
                latitude__range=(south_border, north_border),
                longitude__range=(west_border, east_border)
            )
            count_neighbor = 0
            for neighbor in neighbors:
                if distance.geodesic(
                    (restaurant_latitude, restaurant_longitude),
                    (neighbor.latitude, neighbor.longitude)
                ).km <= DISTANCE:
                    count_neighbor += 1
            result.append(
                {
                    'name': restaurant.name,
                    'competitors': count_neighbor
                }
            )
    except Exception as e:
        return Response({'error': f'{e}'})
    return Response(result)
