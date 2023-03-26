from django.contrib import admin

from .models import Address, Service


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'loc_latitude', 'loc_longitude')
    search_fields = ('id', 'loc_latitude', 'loc_longitude')
    empty_value_display = '-пусто-'


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('specialists_id', 'name_service', 'price', 'currency')
    search_fields = ('specialists_id', 'name_service', 'price', 'currency')
    empty_value_display = '-пусто-'


admin.site.register(Address, AddressAdmin)
admin.site.register(Service, ServiceAdmin)
