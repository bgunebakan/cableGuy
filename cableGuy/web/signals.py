# -*- coding: utf-8 -*-
from .models import Device,DeviceType,Cable
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save,post_delete



@receiver(pre_save, sender=Device)
def sub_device_room(sender, instance, **kwargs):

    if instance.top_device:
        instance.room = instance.top_device.room


@receiver(post_save, sender=Device)
def last_device_no(sender, created, instance, **kwargs):

    if created:
        print("Generate new device code")
        if instance.top_device:
            return
        devices = Device.objects.filter(room=instance.room,device_type=instance.device_type)
        device_no_list = []

        if devices:
            for device in devices:
                if device.code:
                    print(device.code)
                    code = str(device.code)
                    number = code.replace(device.device_type.code, "")
                    print("device number: " + number)
                    device_no_list.append(int(number))

        if device_no_list:
            last_device_no = max(device_no_list) + 1
        else:
            last_device_no = 1

        device_no = str(instance.device_type.code) + str(last_device_no)
        print(device_no)
        instance.code = device_no
        instance.save()

@receiver(post_save, sender=Device)
def last_subdevice_no(sender, created, instance, **kwargs):

    if created:
        print("Generate new sub device code")
        if not instance.top_device:
            return
        devices = Device.objects.filter(room=instance.room,device_type=instance.device_type,top_device=instance.top_device)
        device_no_list = []

        if devices:
            for device in devices:
                if device.code:
                    print(device.code)
                    code = str(device.code)
                    number = code.replace(device.device_type.code, "")
                    print("device number: " + number)
                    device_no_list.append(int(number))

        if device_no_list:
            last_device_no = max(device_no_list) + 1
        else:
            last_device_no = 1

        device_no = str(instance.device_type.code) + str(last_device_no)
        print(device_no)
        instance.code = device_no
        instance.save()
