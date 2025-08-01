from django.db import models
from vehicleFleet.models import Vehicle

# To store telemetry data recieved in every 30 seconds
class Telemetry(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    speed = models.FloatField()
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    fuel_level = models.FloatField()
    engine_status = models.CharField(max_length=50)
    odometer = models.FloatField(default=0)
    diagnostics_codes = models.TextField(null=True)

    def __str__(self):
        return f"{self.timestamp} - {self.fuel} - {self.speed} - ({self.latitude}, {self.longitude}) - "

# To store alerts
class Alert(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    alert_type = models.CharField(max_length=20)
    message = models.TextField()
