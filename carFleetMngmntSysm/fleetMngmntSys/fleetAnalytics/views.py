from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from django.utils.timezone import now, timedelta
from django.db.models import Avg, Sum, Count

from vehicleFleet.models import Vehicle
from telemetry.models import Telemetry, Alert


def analytics(request):
    try:
        # The 24 hr interval
        time24hr = now() - timedelta(hours=24)

        total_vehicles = Vehicle.objects.count()

        telemetry_24hr = Telemetry.objects.filter(timestamp__gte=time24hr)
        id_active_vehicle = telemetry_24hr.values_list(
            "vehicle_id", flat=True
        ).distinct()
        active_cnt = Vehicle.objects.filter(id__in=id_active_vehicle).count()
        inactive_cnt = total_vehicles - active_cnt

        avg_fuel = telemetry_24hr.aggregate(avg=Avg("fuel_level"))["avg"]
        avg_fuel = round(avg_fuel or 0, 2)

        latest_vehicle = telemetry_24hr.order_by("vehicle_id", "-timestamp").distinct(
            "vehicle_id"
        )
        distance = latest_vehicle.aggregate(total=Sum("odometer"))["total"] or 0

        all_alerts = Alert.objects.values("alert_type").annotate(count=Count("id"))
        alerts_summary = list(all_alerts)

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
