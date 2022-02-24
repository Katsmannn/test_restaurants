from django.db import models


class Company(models.Model):

    name = models.CharField(
        max_length=50,
        verbose_name='name',
        unique=True
    )

    class Meta:
        verbose_name = 'Company'
        ordering = ['name']

    def __str__(self):
        return self.name


class Restaurant(models.Model):

    name = models.CharField(
        max_length=50,
        verbose_name='name',
    )
    city = models.CharField(
        max_length=50,
        verbose_name='city',
        blank=True,
        null=True
    )
    latitude = models.FloatField(
        max_length=15,
        verbose_name='latitude'
    )
    longitude = models.FloatField(
        max_length=15,
        verbose_name='longitude'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='company',
        verbose_name='company'
    )

    class Meta:
        verbose_name = 'Restaurant'
        ordering = ['name']

    def __str__(self):
        return self.name
