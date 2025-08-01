from celery import shared_task
from .models import Vehicle, Telemetry, Alert
from django.utils.timezone import now, timedelta


@shared_task
def process_alerts(vehicle_id, speed, fuel_level):
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        alert_window = now() - timedelta(minutes=3)

        # Speed Alert
        if speed > 100:
            recent_speeds = Telemetry.objects.filter(
                vehicle=vehicle, speed__gt=100
            ).order_by("-timestamp")[:5]

            if len(recent_speeds) >= 3:
                if not Alert.objects.filter(
                    vehicle=vehicle, alert_type="Speed", created_at__gte=alert_window
                ).exists():
                    Alert.objects.create(
                        vehicle=vehicle,
                        alert_type="Speed",
                        message=f"Speed exceeded repeatedly: {speed} kmph",
                    )

        # Low Fuel Alert
        if fuel_level < 15:
            if not Alert.objects.filter(
                vehicle=vehicle, alert_type="LowFuel", created_at__gte=alert_window
            ).exists():
                Alert.objects.create(
                    vehicle=vehicle,
                    alert_type="LowFuel",
                    message=f"Low fuel: {fuel_level}% — Please refuel",
                )

    except Exception as e:
        # Log this in production
        print(f"Error in process_alerts: {str(e)}")
