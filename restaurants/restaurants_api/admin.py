from django.contrib import admin

from .models import Company, Restaurant


class RestaurantAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name', 'company')


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Company)
