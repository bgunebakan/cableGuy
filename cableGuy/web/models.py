from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models.query import QuerySet

class SoftDeleteManager(models.Manager):

    def get_query_set(self):
        return QuerySet(self.model, using=self._db).filter(deleted=False)

    def filter(self, *args, **kwargs):
        return self.get_query_set().filter(*args, **kwargs)

    def all(self, *args, **kwargs):
        return self.get_query_set().filter(*args, **kwargs)

class Building(models.Model):

    name = models.CharField(max_length=30,unique=True,verbose_name = "Name")
    code = models.CharField(max_length=30,unique=True,verbose_name = "Code")

    notes = models.TextField(max_length=100,verbose_name = "Notes",null=True,blank=True)

    created_date = models.DateTimeField(default=timezone.now,verbose_name = "Created date")
    updated_date = models.DateTimeField(auto_now=True,verbose_name = "Updated Date")
    deleted = models.BooleanField(default=False,verbose_name = "Deleted")

    objects = SoftDeleteManager()

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Building')
        verbose_name_plural = _(u'Buildings')

    def __str__(self):
        return self.name

class Room(models.Model):

    name = models.CharField(max_length=30,unique=True,verbose_name = "Name")
    code = models.CharField(max_length=30,unique=True,verbose_name = "Code")

    building = models.ForeignKey(Building,null=False,blank=False,on_delete=models.CASCADE,verbose_name = "Building")
    notes = models.TextField(max_length=100,verbose_name = "Notes",null=True,blank=True)

    created_date = models.DateTimeField(default=timezone.now,verbose_name = "Created date")
    updated_date = models.DateTimeField(auto_now=True,verbose_name = "Updated Date")
    deleted = models.BooleanField(default=False,verbose_name = "Deleted")

    objects = SoftDeleteManager()

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Room')
        verbose_name_plural = _(u'Rooms')

    def __str__(self):
        return str(self.name)

class System(models.Model):

    name = models.CharField(max_length=30,unique=True,verbose_name = "Name")
    code = models.CharField(max_length=30,unique=True,verbose_name = "Code")

    notes = models.TextField(max_length=100,verbose_name = "Notes",null=True,blank=True)

    created_date = models.DateTimeField(default=timezone.now,verbose_name = "Created date")
    updated_date = models.DateTimeField(auto_now=True,verbose_name = "Updated Date")
    deleted = models.BooleanField(default=False,verbose_name = "Deleted")

    objects = SoftDeleteManager()

    class Meta:
        ordering = ['name']
        verbose_name = _(u'System')
        verbose_name_plural = _(u'Systems')

    def __str__(self):
        return self.name

class DeviceType(models.Model):

    name = models.CharField(max_length=30,unique=True,verbose_name = "Name")
    code = models.CharField(max_length=30,unique=True,verbose_name = "Code")

    notes = models.TextField(max_length=100,verbose_name = "Notes",null=True,blank=True)

    created_date = models.DateTimeField(default=timezone.now,verbose_name = "Created date")
    updated_date = models.DateTimeField(auto_now=True,verbose_name = "Updated Date")
    deleted = models.BooleanField(default=False,verbose_name = "Deleted")

    objects = SoftDeleteManager()

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Device Type')
        verbose_name_plural = _(u'Device Types')

    def __str__(self):
        return self.name

class Device(models.Model):

    #name = models.CharField(max_length=30,blank=True,null=True,verbose_name = "Name")
    code = models.CharField(max_length=30,null=True,blank=True,verbose_name = "Code",help_text="Leave empty for auto code generation")
    room = models.ForeignKey(Room,null=False,blank=False,on_delete=models.CASCADE,verbose_name = "Room")
    device_type = models.ForeignKey(DeviceType,null=True,blank=True,on_delete=models.CASCADE,verbose_name = "Device Type")

    top_device = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,verbose_name = "Top Device")

    notes = models.TextField(max_length=100,verbose_name = "Notes",null=True,blank=True)

    created_date = models.DateTimeField(default=timezone.now,verbose_name = "Created date")
    updated_date = models.DateTimeField(auto_now=True,verbose_name = "Updated Date")
    deleted = models.BooleanField(default=False,verbose_name = "Deleted")

    objects = SoftDeleteManager()

    class Meta:
        ordering = ['code']
        verbose_name = _(u'Device')
        verbose_name_plural = _(u'Devices')

    def __str__(self):
        return str(self.room) + " " + str(self.code)

class Cable(models.Model):

    system = models.ForeignKey(System,null=False,blank=False,on_delete=models.CASCADE,verbose_name = "System")

    from_room = models.ForeignKey(Room,related_name="from_room",null=False,blank=False,on_delete=models.CASCADE,verbose_name = "From Room")
    to_room = models.ForeignKey(Room,related_name="to_room",null=False,blank=False,on_delete=models.CASCADE,verbose_name = "To Room")

    from_device = models.ForeignKey(Device,related_name="from_device",null=False,blank=False,on_delete=models.CASCADE,verbose_name = "From Device")
    to_device = models.ForeignKey(Device,related_name="to_device",null=False,blank=False,on_delete=models.CASCADE,verbose_name = "To Device")

    name = models.CharField(max_length=30,null=True,blank=True,verbose_name = "Name")

    notes = models.TextField(max_length=100,verbose_name = "Notes",null=True,blank=True)

    created_date = models.DateTimeField(default=timezone.now,verbose_name = "Created date")
    updated_date = models.DateTimeField(auto_now=True,verbose_name = "Updated Date")
    deleted = models.BooleanField(default=False,verbose_name = "Deleted")

    objects = SoftDeleteManager()

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Cable')
        verbose_name_plural = _(u'Cables')

    def __str__(self):
        if self.from_room != self.to_room:
            return str(self.system.code) + ":" + str(self.from_room.code) + ":" + str(self.from_device.code) + "/" + str(self.to_room.code) + ":" + str(self.to_device.code)
        else:
            return str(self.system.code) + ":" + str(self.from_room.code) + ":" + str(self.from_device.code) + "/" + str(self.to_device.code)
