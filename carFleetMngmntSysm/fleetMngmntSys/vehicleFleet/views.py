from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import Vehicle


# Endpoint to create a vehicle record
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


# Endpoint to list a specific vehicle record
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
def list_vehicles(request):
    try:
        vehicles = list(Vehicle.objects.values())
        return JsonResponse({"message": f"Vehicles found", "vehicles": vehicles})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)


# Endpoint to query any vehicle based on the various attributes provided in the get method.
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
def delete_vehicle(request, id):
    try:
        vehicleRecord = Vehicle.objects.get(vin=id)
        vehicleRecord.delete()
        return JsonResponse({"message": "Vehicle record deleted"})
        # Record successfully deleted
    except Vehicle.DoesNotExist as e:
        # Handle case where record with given ID does not exist
        return JsonResponse({"error": str(e)}, status=404)
