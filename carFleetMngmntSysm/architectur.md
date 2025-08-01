# API Endpoints

## Vehicle Management (/vehicleFleet/)

- Create Vehicle:  
   POST /vehicleFleet/vehicles/create/  
   Params: vin, vManufacturer, vModel, fleetID, ownerInfo, regStatus

- List All Vehicles:  
   GET /vehicleFleet/vehicles/list/

- List Specific Vehicle:  
   GET /vehicleFleet/vehicle/list/<vin>

- Delete Vehicle:  
   GET /vehicleFleet/vehicles/delete/<vin>

- Query Vehicles:  
   GET /vehicleFleet/vehicles/query/?<param>=<value>

## Telemetry (/telemtry/)

- Send Telemetry Data:  
   POST /telemtry/telemetry/receive/  
   Params: vin, timestamp, speed, latitude, longitude, fuel_level, odometer, diagnostics_codes, engine_status

- Get All Telemetry History:  
   GET /telemtry/telemetry/history/

- Get Latest Telemetry (by VIN):  
   GET /telemtry/telemetry/latest/<vin>

## Analytics (/fleetAnalytics/)

- Get Fleet Analytics:  
   GET /fleetAnalytics/fleetAnalytics/analytics/
