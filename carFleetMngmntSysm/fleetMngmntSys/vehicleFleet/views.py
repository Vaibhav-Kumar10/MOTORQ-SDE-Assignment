from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse

from .models import Vehicle


def create_vehicle(request):
    if request.method == "POST":
        try:
            vin = request.POST.get("vin")
            vManufacturer = request.POST.get("vManufacturer")
            vModel = request.POST.get("vModel")
            fleetID = request.POST.get("fleetID")
            ownerInfo = request.POST.get("ownerInfo")
            regStatus = request.POST.get("regStatus")

            Vehicle.objects.create(
                vin=vin,
                vManufacturer=vManufacturer,
                vModel=vModel,
                fleetID=fleetID,
                ownerInfo=ownerInfo,
                regStatus=regStatus,
            )
            return JsonResponse({"message": "Vehicle created successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse(
        {"error": "INVALID REQUEST : only POST request accepted"}, status=405
    )


def list_vehicle(request, id):
    try:
        vehicle = get_object_or_404(Vehicle, vin=id)
        return JsonResponse({"message": f"Vehicle found", "vehicle": vehicle})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)


def list_vehicles(request):
    try:
        vehicles = list(Vehicle.objects.values())
        return JsonResponse({"message": f"Vehicles found", "vehicles": vehicles})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)


def query_vehicle(request):
    
    pass


def delete_vehicle(request, id):
    try:
        vehicleRecord = Vehicle.objects.get(vin=id)
        vehicleRecord.delete()
        return JsonResponse({"message": "Vehicle record deleted"})
        # Record successfully deleted
    except Vehicle.DoesNotExist as e:
        # Handle case where record with given ID does not exist
        return JsonResponse({"error": str(e)}, status=404)
