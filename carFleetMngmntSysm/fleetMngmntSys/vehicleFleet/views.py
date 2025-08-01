from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# from django import forms

import json
from .models import Vehicle
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
# from ratelimit.decorators import ratelimit

# Endpoint to create a vehicle record
@csrf_exempt
# @ratelimit(key="ip", rate="3/m", block=True)
def create_vehicle(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
# vin = request.POST.gte('vin')
            vin = data.get("vin")
            vManufacturer = data.get("vManufacturer")
            vModel = data.get("vModel")
            fleetID = data.get("fleetID")
            ownerInfo = data.get("ownerInfo")
            regStatus = data.get("regStatus")

            if not vin:
                raise ValueError("VIN is required")
            if not vManufacturer:
                raise ValueError("vManufacturer is required")
            if not vModel:
                raise ValueError("vModel is required")
            if not fleetID:
                raise ValueError("fleetID is required")
            if not ownerInfo:
                raise ValueError("ownerInfo is required")
            if not regStatus:
                raise ValueError("regStatus is required")

            Vehicle.objects.create(
                vin=vin,
                vManufacturer=vManufacturer,
                vModel=vModel,
                fleetID=fleetID,
                ownerInfo=ownerInfo,
                regStatus=regStatus,
            )

            return JsonResponse({"message": "Vehicle created successfully"})
        except ValueError as ve:
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST method allowed"}, status=405)


# Endpoint to list a specific vehicle record
# @ratelimit(key="ip", rate="10/m", block=True)
def list_vehicle(request, id):
    try:
        vehicle = get_object_or_404(Vehicle, vin=id)
        return JsonResponse(
            {
                "message": "Vehicle found",
                "vehicle": {
                    "vin": vehicle.vin,
                    "vManufacturer": vehicle.vManufacturer,
                    "vModel": vehicle.vModel,
                    "fleetID": vehicle.fleetID,
                    "ownerInfo": vehicle.ownerInfo,
                    "regStatus": vehicle.regStatus,
                },
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)


# Endpoint to list all vehicles record
# @ratelimit(key="ip", rate="20/m", block=True)
def list_vehicles(request):
    vehicles = list(Vehicle.objects.values())
    return JsonResponse({"message": "Live", "vehicles": vehicles})


# Endpoint to query any vehicle based on the various attributes provided in the get method.
# @ratelimit(key="ip", rate="15/m", block=True)
def query_vehicle(request):
    try:
        # Store all the query parameters passed, if any
        query_filters = {}

        # Get query parameters from URL
        vin = request.GET.get("vin")
        vManufacturer = request.GET.get("vManufacturer")
        vModel = request.GET.get("vModel")
        fleetID = request.GET.get("fleetID")
        regStatus = request.GET.get("regStatus")

        if vin:
            query_filters["vin"] = vin
        if vManufacturer:
            query_filters["vManufacturer__icontains"] = vManufacturer
        if vModel:
            query_filters["vModel__icontains"] = vModel
        if fleetID:
            query_filters["fleetID__icontains"] = fleetID
        if regStatus:
            query_filters["regStatus__iexact"] = regStatus

        # Query vehicles with the matching query parameters
        vehicles = Vehicle.objects.filter(**query_filters).values()

        if not query_filters:
            return JsonResponse({"error": "No query parameters provided"}, status=400)

        if not vehicles:
            return JsonResponse(
                {
                    "message": "No vehicles found that match with the passed query parameters. Try something else."
                },
                status=404,
            )

        return JsonResponse(
            {
                "message": "Found vehicles with matching query parameters",
                "vehicles": list(vehicles),
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# Endpoint to delete a specific vehicle record
@csrf_exempt
# @ratelimit(key="ip", rate="5/m", block=True)
def delete_vehicle(request, id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Only DELETE method allowed"}, status=405)

    try:
        vehicleRecord = Vehicle.objects.get(vin=id)
        vehicleRecord.delete()
        return JsonResponse({"message": "Vehicle record deleted"})
        # Record successfully deleted
    except Vehicle.DoesNotExist as e:
        # Handle case where record with given ID does not exist
        return JsonResponse({"error": str(e)}, status=404)
