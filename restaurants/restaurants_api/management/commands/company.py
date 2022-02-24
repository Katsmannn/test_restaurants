from django.core.management.base import BaseCommand


from restaurants_api.models import Company


class Command(BaseCommand):
    """
    Создание компаний в базе данных.
    """
    help = 'Create company'

    def handle(self, *args, **options):

        COMPANY_LIST = [
            'McDonalds',
            'KFC',
            'Burger King',
        ]

        for company_name in COMPANY_LIST:
            Company.objects.get_or_create(
                name=company_name
            )
