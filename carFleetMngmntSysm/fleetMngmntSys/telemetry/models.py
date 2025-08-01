from django.db import models
from vehicleFleet.models import Vehicle


# To store telemetry data recieved in every 30 seconds
class Telemetry(models.Model):
    timestamp = models.DateTimeField(db_index=True)
    vehicle = models.ForeignKey(
        "vehicleFleet.Vehicle", on_delete=models.SET_NULL, null=True, db_index=True
    )

    speed = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    fuel_level = models.FloatField()
    odometer = models.FloatField()

    diagnostics_codes = models.TextField(blank=True, null=True)
    engine_status = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ("vehicle", "timestamp")  # Prevents duplicate telemetry
        indexes = [
            models.Index(fields=["vehicle", "timestamp"]),  # Composite index
            models.Index(fields=["speed"]),
            models.Index(fields=["fuel_level"]),
        ]

    def __str__(self):
        return f"{self.timestamp} - {self.vehicle} - {self.speed}kmph"


# To store alerts
class Alert(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    alert_type = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["vehicle", "created_at"]),
            models.Index(fields=["alert_type", "created_at"]),
        ]
