from django.contrib import admin

from .models import *

class BuildingAdmin(admin.ModelAdmin):
     list_display = ('name', 'code','notes')

admin.site.register(Building,BuildingAdmin)

class DeviceTypeAdmin(admin.ModelAdmin):
     list_display = ('name', 'code','notes')

admin.site.register(DeviceType,DeviceTypeAdmin)

class CableAdmin(admin.ModelAdmin):
     list_display = ('system', 'from_room','to_room','from_device','to_device')

admin.site.register(Cable,CableAdmin)

admin.site.register(Room)
admin.site.register(System)

class SubDeviceInline(admin.StackedInline):
    model = Device
    extra = 0
    verbose_name = "Sub Devices"
    fields = ["device_type"]

class DeviceAdmin(admin.ModelAdmin):
     list_display = ('name', 'code','room')
     inlines = [SubDeviceInline]

admin.site.register(Device,DeviceAdmin)
