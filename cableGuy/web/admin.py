from django.contrib import admin
from advanced_filters.admin import AdminAdvancedFiltersMixin
from .models import *
from import_export.admin import ImportExportModelAdmin


@admin.register(DeviceType)
class DeviceTypeAdmin(ImportExportModelAdmin):
    list_display = ('name', 'code','notes')


class CableAdmin(AdminAdvancedFiltersMixin,admin.ModelAdmin):
     list_display = ('__str__','system', 'from_room','to_room','from_device','to_device')
     list_filter = ('from_room', 'from_device')
     # specify which fields can be selected in the advanced filter
     # creation form
     advanced_filter_fields = ('from_room','to_room','from_device','to_device')

     def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (db_field.name == "from_device") or (db_field.name == "to_device"):
            kwargs["queryset"] = Device.objects.order_by('room')
        return super(CableAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Cable,CableAdmin)

#admin.site.register(System)

class RoomInline(admin.StackedInline):
    model = Room
    extra = 0
    verbose_name = "Rooms"
    fields = ["name","code"]

class DeviceInline(admin.StackedInline):
    model = Device
    extra = 0
    verbose_name = "Sub Devices"
    fields = ["device_type","code"]

class SubDeviceInline(admin.StackedInline):
    model = Device
    extra = 0
    verbose_name = "Sub Devices"
    fields = ["device_type","code"]

class RoomAdmin(admin.ModelAdmin):
     list_display = ('name', 'code','building')
     inlines = [DeviceInline]

admin.site.register(Room,RoomAdmin)

@admin.register(Device)
class DeviceAdmin(ImportExportModelAdmin):
     list_display = ('code','room')
     inlines = [SubDeviceInline]


class BuildingAdmin(admin.ModelAdmin):
     list_display = ('name', 'code','notes')
     inlines = [RoomInline]

admin.site.register(Building,BuildingAdmin)


@admin.register(System)
class ItemImportExportAdmin(ImportExportModelAdmin):
    pass
