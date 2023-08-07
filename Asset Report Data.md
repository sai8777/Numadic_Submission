# Asset Report Data 
This file provides documentation for the Vehicle Asset Report API, which generates an asset report in Excel format based on the data provided in the zipped folder (NU-raw-location-dump.zip) and the CSV file (Trip-Info.csv).

## Problem Statement
Given a zipped folder containing CSV files with vehicle trails. Each file represents the trail of a unique vehicle and contains the following parameters:
- `fk_asset_id`: Unique identifier for the vehicle
- `lic_plate_no`: Registration number of the vehicle
- `lat`: Latitude of the point
- `lon`: Longitude of the point
- `lname`: Geocoded location name of the point
- `tis`: Epoch timestamp in UTC 0:00:00
- `spd`: Speed in kmph
- `harsh_acceleration`: Boolean flag representing if harsh acceleration occurred at the point
- `hbk`: Boolean flag representing if harsh braking occurred at the point
- `osf`: Boolean flag representing if overspeeding occurred at the point
Other parameters present in the file are ignored.

The file "Trip-Info.csv" contains information related to trips completed by all the vehicles and includes the following parameters:
- `trip_id`: Unique identifier for the trip
- `transporter_name`: Name of the transport company to which the vehicle belongs
- `quantity`: Quantity of material carried for a trip
- `vehicle_number`: Registration number of the vehicle
- `date_time`: Timestamp of trip creation in YYYYMMDDHHMMSS format

## API Functionality
The Vehicle Asset Report API will take the following input parameters:
- `start_time`: Start time of the report period in epoch format.
- `end_time`: End time of the report period in epoch format.

The API will generate an asset report in Excel format, containing the following columns:
- `License Plate Number`: Registration number of the vehicle.
- `Distance`: The total distance covered by the vehicle during the specified period. The distance can be computed using the Haversine formula based on latitude and longitude data.
- `Number of Trips Completed`: The total number of trips completed by the vehicle during the specified period.
- `Average Speed`: The average speed of the vehicle during the specified period, calculated using the speed data available.
- `Transporter Name`: The name of the transport company to which the vehicle belongs.
- `Number of Speed Violations`: The total number of speed violations (overspeeding) recorded for the vehicle during the specified period.

Additionally, the API will handle cases where there is no data available for the time period mentioned by the user and send a suitable error response in such situations.

## Tech Stack
The following project uses :
- Python 
- Pandas 
- flask
- json
- math
- requests

## Implemetation
- The distance  is computed using the Haversine formula,utilizing the latitude and longitude data present in the CSV files for each vehicle trail.
- No of trips and transported name is determined using the trip_info.csv file.
- Speed violations is  calculated by checking the "osf" flag in the vehicle trail data.
- The API  generated Excel report with appropriate headers and data is then stored in the machine.

## Steps to run the code 
Run the vehicle_trip_data.py to start the server 
```sh
python vehicle_trip_data.py
```
To send request to the Api 
```sh
python request.py
```


