from django.urls import path

from .views import (
    create_vehicle,
    list_vehicles,
    list_vehicle,
    delete_vehicle,
    query_vehicle,
)

app_name = "vehicleFleet"

urlpatterns = [
    # Create vehicle endpoint
    path("vehicles/create/", create_vehicle, name="create"),
    # List all vehicles endpoint
    path("vehicles/list/", list_vehicles, name="vehicles"),
    # List a specific vehicle endpoint
    path("vehicle/list/<str:id>", list_vehicle, name="vehicle"),
    # Delete a specific vehicle endpoint
    path("vehicles/delete/<str:id>", delete_vehicle, name="delete"),
    # Query a specific vehicle endpoint
    path("vehicles/query/", query_vehicle, name="vehicles"),
]
