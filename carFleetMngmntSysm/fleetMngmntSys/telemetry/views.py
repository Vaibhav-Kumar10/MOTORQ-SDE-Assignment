from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from vehicleFleet.models import Vehicle
from .models import Telemetry, Alert

from django.shortcuts import render


# To store the telemetry data recieved
def receive_telemetry_data(request):
    if request.method == "POST":
        vin = request.POST.get("vin")
        timestamp = parse_datetime(request.POST.get("timestamp"))
        speed = float(request.POST.get("speed"))
        latitude = float(request.POST.get("latitude"))
        longitude = float(request.POST.get("longitude"))
        fuel_level = float(request.POST.get("fuel_level"))
        odometer = float(request.POST.get("odometer"))
        diagnostics_codes = request.POST.get("diagnostics_codes", "")
        engine_status = request.POST.get("engine_status")

        try:
            # Here we create a telemetry record
            vehicle = get_object_or_404(Vehicle, vin=vin)
            Telemetry.objects.create(
                vehicle=vehicle,
                timestamp=timestamp,
                speed=speed,
                latitude=latitude,
                longitude=longitude,
                fuel_level=fuel_level,
                odometer=odometer,
                diagnostic_codes=diagnostics_codes,
                engine_status=engine_status,
            )

            # Here we simultaneously check and generate alerts
            alert = []

            # Count previous recent speed violations for last 5 entries ( i.e., 2.5 minutes)
            speed_violations = Telemetry.objects.filter(
                vehicle=vehicle, speed__gt=100
            ).order_by("-timestamp")[:5]
            speed_violation_cnt = speed_violations.count()
            # Trigger alert only if 3 or more violations in last 5 records
            if speed > 100 and speed_violation_cnt >= 3:
                Alert.objects.create(
                    vehicle=vehicle,
                    alert_type="Speed",
                    message=f"Speed exceeded repeatedly : {speed} kmph",
                )
                alert.append[
                    f"Speed limit exceeded repeatedly : {speed} kmph!! \nVehicle crossed 100 kmph {speed_violation_cnt} times! \nKeep your speed below 100 kmph."
                ]
            if fuel_level < 15:
                Alert.objects.create(
                    vehicle=vehicle,
                    alert_type="LowFuel",
                    message=f"Low fuel/battery : {fuel_level} %",
                )
                alert.append[
                    f"Low fuel/battery : {fuel_level} % !! Please charge immediately"
                ]

            return JsonResponse({"message": "Telemetry data saved", "alert": alert})

        except Exception as e:
            return JsonResponse({"error": e}, status=404)

    return JsonResponse(
        {"error": "INVALID REQUEST : only POST request accepted"}, status=405
    )

# Endpoint to show complete elemetry history
def telemetry_history(request):
    try:
        records = Telemetry.objects.all()

        result = [
            {
                "timestamp": t.timestamp,
                "latitude": t.latitude,
                "longitude": t.longitude,
                "speed": t.speed,
                "fuel_level": t.fuel_level,
                "odometer": t.odometer,
                "engine_status": t.engine_status,
                "diagnostic_codes": t.diagnostic_codes,
            }
            for t in records
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
            return JsonResponse({"message": "No telemetry data found for this vehicle"}, status=404)

        data = {
            "timestamp": record.timestamp,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "speed": record.speed,
            "fuel_level": record.fuel_level,
            "odometer": record.odometer,
            "engine_status": record.engine_status,
            "diagnostic_codes": record.diagnostic_codes,
        }

        return JsonResponse({"message": "Latest telemetry data for thiss vehicle", "record": data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)
