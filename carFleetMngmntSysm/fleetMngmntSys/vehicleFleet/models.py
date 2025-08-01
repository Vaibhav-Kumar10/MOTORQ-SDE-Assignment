from django.db import models


class Vehicle(models.Model):
    vin = models.CharField(max_length=10, primary_key=True)
    vManufacturer = models.CharField(max_length=50, null=False)
    vModel = models.CharField(max_length=50, null=False)
    fleetID = models.CharField(max_length=50, null=False)
    ownerInfo = models.TextField(max_length=200, null=False)
    regStatus = models.CharField(max_length=10, null=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vin} - {self.vManufacturer} - {self.vModel}"
