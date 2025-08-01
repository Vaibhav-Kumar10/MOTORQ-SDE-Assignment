import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from vehicleFleet.models import Vehicle
from .models import Telemetry, Alert
from django.utils.timezone import now, timedelta, make_aware, is_naive
from django.db import IntegrityError


@csrf_exempt
def receive_telemetry_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            vin = data.get("vin")
            speed = float(data.get("speed"))
            latitude = float(data.get("latitude"))
            longitude = float(data.get("longitude"))
            fuel_level = float(data.get("fuel_level"))
            odometer = float(data.get("odometer"))
            diagnostics_codes = data.get("diagnostics_codes", "")
            engine_status = data.get("engine_status")

            if not vin or not timestamp:
                return JsonResponse({"error": "Missing VIN or timestamp"}, status=400)

            timestamp_str = data.get("timestamp")
            if not timestamp_str:
                return JsonResponse({"error": "Timestamp is required"}, status=400)

            timestamp = parse_datetime(timestamp_str)
            if timestamp is None:
                return JsonResponse({"error": "Invalid timestamp format"}, status=400)
            if is_naive(timestamp):
                timestamp = make_aware(timestamp)

            latest = (
                Telemetry.objects.filter(vehicle=vehicle).order_by("-timestamp").first()
            )
            if latest and timestamp <= latest.timestamp:
                return JsonResponse({"error": "Outdated telemetry ignored"}, status=400)

            # Validate vehicle exists
            vehicle = get_object_or_404(Vehicle, vin=vin)

            # Save telemetry record
            Telemetry.objects.create(
                vehicle=vehicle,
                timestamp=timestamp,
                speed=speed,
                latitude=latitude,
                longitude=longitude,
                fuel_level=fuel_level,
                odometer=odometer,
                diagnostics_codes=diagnostics_codes,
                engine_status=engine_status,
            )

            alert_messages = []
            alert_window = now() - timedelta(minutes=3)

            # --- Speed alert ---
            speed_violations = Telemetry.objects.filter(
                vehicle=vehicle, speed__gt=100
            ).order_by("-timestamp")[:5]

            existing_speed_alert = Alert.objects.filter(
                vehicle=vehicle,
                alert_type="Speed",
                created_at__gte=alert_window,
            ).exists()

            if (
                speed > 100
                and speed_violations.count() >= 3
                and not existing_speed_alert
            ):
                Alert.objects.create(
                    vehicle=vehicle,
                    alert_type="Speed",
                    message=f"Speed exceeded repeatedly: {speed} kmph",
                )
                alert_messages.append(
                    f"Speed limit exceeded repeatedly: {speed} kmph! Crossed 100 kmph {speed_violations.count()} times."
                )

            # --- Low fuel alert ---
            existing_fuel_alert = Alert.objects.filter(
                vehicle=vehicle, alert_type="LowFuel", timestamp__gte=alert_window
            ).exists()

            if fuel_level < 15 and not existing_fuel_alert:
                Alert.objects.create(
                    vehicle=vehicle,
                    alert_type="LowFuel",
                    message=f"Low fuel/battery: {fuel_level}%",
                )
                alert_messages.append(
                    f"Low fuel/battery: {fuel_level}% — please refuel/charge."
                )

            return JsonResponse(
                {"message": "Telemetry data saved", "alert": alert_messages}
            )

        except IntegrityError:
            return JsonResponse({"error": "Duplicate telemetry ignored"}, status=409)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "INVALID REQUEST — Only POST allowed"}, status=405)


# Endpoint to show complete elemetry history
def telemetry_history(request):
    try:
        records = Telemetry.objects.all()

        result = [
            {
                "timestamp": record.timestamp,
                "latitude": record.latitude,
                "longitude": record.longitude,
                "speed": record.speed,
                "fuel_level": record.fuel_level,
                "odometer": record.odometer,
                "engine_status": record.engine_status,
                "diagnostics_codes": record.diagnostics_codes,
            }
            for record in records
        ]

        return JsonResponse({"message": "Telemetry records found", "records": result})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)


# Endpoint to show latest telemetry history for a specific vehicle
def latest_telemetry(request, id):
    try:
        vehicle = get_object_or_404(Vehicle, vin=id)
        record = (
            Telemetry.objects.filter(vehicle=vehicle).order_by("-timestamp").first()
        )

        if not record:
            return JsonResponse(
                {"message": "No telemetry data found for this vehicle"}, status=404
            )

        data = {
            "timestamp": record.timestamp,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "speed": record.speed,
            "fuel_level": record.fuel_level,
            "odometer": record.odometer,
            "engine_status": record.engine_status,
            "diagnostics_codes": record.diagnostics_codes,
        }

        return JsonResponse(
            {"message": "Latest telemetry data for this vehicle", "record": data}
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)
