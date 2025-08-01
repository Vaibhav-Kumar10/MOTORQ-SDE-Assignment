from django.db import models
from vehicleFleet.models import Vehicle

# To store telemetry data recieved in every 30 seconds
class Telemetry(models.Model):
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField()
    speed = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    fuel_level = models.FloatField()
    odometer = models.FloatField()
    diagnostics_codes = models.TextField(blank=True, null=True)
    engine_status = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ('vehicle', 'timestamp')  # Avoid duplicate entries

    def __str__(self):
        return f"{self.timestamp} - {self.fuel} - {self.speed} - ({self.latitude}, {self.longitude}) - "


# To store alerts
class Alert(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    alert_type = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
