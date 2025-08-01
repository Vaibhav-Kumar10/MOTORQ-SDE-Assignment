from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from django.db.models import Avg, Sum, Count

from vehicleFleet.models import Vehicle
from telemetry.models import Telemetry, Alert


def analytics(request):
    try:
        # The 24 hr
        time24hr = now() - timedelta(hours=24)

        total_vehicles = Vehicle.objects.count()

        telemetry_24hr = Telemetry.objects.filter(timestamp__gte=time24hr)

        # Active vehicles
        active_vehicle_ids = set(telemetry_24hr.values_list("vehicle_id", flat=True))
        active_cnt = len(active_vehicle_ids)
        inactive_cnt = total_vehicles - active_cnt

        # Average fuel level
        avg_fuel = telemetry_24hr.aggregate(avg=Avg("fuel_level"))["avg"] or 0
        avg_fuel = round(avg_fuel, 2)

        # Latest odometer per vehicle (manual deduplication)
        latest_records = telemetry_24hr.order_by("vehicle_id", "-timestamp")

        latest_record_for_vehicles = {}
        for rec in latest_records:
            if rec.vehicle_id not in latest_record_for_vehicles:
                latest_record_for_vehicles[rec.vehicle_id] = rec

        distance = sum(rec.odometer for rec in latest_record_for_vehicles.values())

        # Alerts summary
        alerts_summary = list(
            Alert.objects.values("alert_type").annotate(count=Count("id"))
        )

        return JsonResponse(
            {
                "active_vehicles": active_cnt,
                "inactive_vehicles": inactive_cnt,
                "average_fuel": avg_fuel,
                "distance_traveled_in_last_24h": distance,
                "alerts": alerts_summary,
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
