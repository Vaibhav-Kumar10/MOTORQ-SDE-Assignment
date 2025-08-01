from django.urls import path
from .views import receive_telemetry_data, telemetry_history, latest_telemetry

app_name = "telemetry"

urlpatterns = [
    # Recieve telemetry data endpoint
    path("telemetry/receive/", receive_telemetry_data, name="receive"),
    # Show complete telemetry history endpoint
    path("telemetry/history/", telemetry_history, name="history"),
    # Show latest telemetry history for a specific vehicle endpoint
    path("telemetry/latest/<str:id>", latest_telemetry, name="latest"),
]
