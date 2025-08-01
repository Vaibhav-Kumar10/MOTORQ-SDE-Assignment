import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from vehicleFleet.models import Vehicle
from .models import Telemetry, Alert
from django.utils.timezone import now, timedelta, make_aware, is_naive
from django.db import IntegrityError
from .tasks import process_alerts
from django.core.cache import cache
from ratelimit.decorators import ratelimit


@csrf_exempt
@ratelimit(key="ip", rate="10/m", block=True)  # Max 10 requests/min per IP
def receive_telemetry_data(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "INVALID REQUEST — Only POST allowed"}, status=405
        )

    try:
        data = json.loads(request.body)
        vin = data.get("vin")
        timestamp_str = data.get("timestamp")

        if not vin or not timestamp_str:
            return JsonResponse({"error": "Missing VIN or timestamp"}, status=400)

        timestamp = parse_datetime(timestamp_str)
        if timestamp is None:
            return JsonResponse({"error": "Invalid timestamp format"}, status=400)
        if is_naive(timestamp):
            timestamp = make_aware(timestamp)

        vehicle = get_object_or_404(Vehicle, vin=vin)

        latest = (
            Telemetry.objects.filter(vehicle=vehicle).order_by("-timestamp").first()
        )
        if latest and timestamp <= latest.timestamp:
            return JsonResponse({"error": "Outdated telemetry ignored"}, status=400)

        speed = float(data.get("speed", 0))
        fuel_level = float(data.get("fuel_level", 0))

        telemetry = Telemetry.objects.create(
            vehicle=vehicle,
            timestamp=timestamp,
            speed=speed,
            latitude=float(data.get("latitude", 0)),
            longitude=float(data.get("longitude", 0)),
            fuel_level=fuel_level,
            odometer=float(data.get("odometer", 0)),
            diagnostics_codes=data.get("diagnostics_codes", ""),
            engine_status=data.get("engine_status"),
        )

        alerts_summary = cache.get("alerts_summary")
        if not alerts_summary:
            alerts_summary = list(
                Alert.objects.values("alert_type").annotate(count=Count("id"))
            )
            cache.set("alerts_summary", alerts_summary, timeout=300)

        process_alerts.delay(vehicle.id, speed, fuel_level)

        return JsonResponse({"message": "Telemetry data saved"})

    except IntegrityError:
        return JsonResponse({"error": "Duplicate telemetry ignored"}, status=409)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# Endpoint to show complete elemetry history
def telemetry_history(request):
    try:
        cached_data = cache.get("telemetry_history")
        if cached_data:
            return JsonResponse(
                {"message": "Cached telemetry records", "records": cached_data}
            )

        records = Telemetry.objects.only(
            "timestamp",
            "latitude",
            "longitude",
            "speed",
            "fuel_level",
            "odometer",
            "engine_status",
            "diagnostics_codes",
        ).order_by("-timestamp")

        result = [
            {
                "timestamp": r.timestamp,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "speed": r.speed,
                "fuel_level": r.fuel_level,
                "odometer": r.odometer,
                "engine_status": r.engine_status,
                "diagnostics_codes": r.diagnostics_codes,
            }
            for r in records
        ]

        cache.set("telemetry_history", result, timeout=300)  # cache for 5 min
        return JsonResponse({"message": "Telemetry records found", "records": result})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)


# Endpoint to show latest telemetry history for a specific vehicle
def latest_telemetry(request, id):
    try:
        cache_key = f"latest_telemetry_{id}"
        cached_record = cache.get(cache_key)
        if cached_record:
            return JsonResponse(
                {"message": "Cached latest telemetry", "record": cached_record}
            )

        vehicle = get_object_or_404(Vehicle, vin=id)
        record = (
            Telemetry.objects.only(
                "timestamp",
                "latitude",
                "longitude",
                "speed",
                "fuel_level",
                "odometer",
                "engine_status",
                "diagnostics_codes",
            )
            .filter(vehicle=vehicle)
            .order_by("-timestamp")
            .first()
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

        cache.set(cache_key, data, timeout=180)  # Cache for 3 minutes
        return JsonResponse({"message": "Latest telemetry", "record": data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)
