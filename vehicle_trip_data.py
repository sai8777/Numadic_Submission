import os
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify
from openpyxl import Workbook
import json
import math
from flask import Flask
app = Flask(__name__)
#function to compute distance
def haversine(lat1, lon1, lat2, lon2):
	lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
	dlat = lat2 - lat1
	dlon = lon2 - lon1
	a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	radius = 6371
	distance = radius * c
	return distance
#Function to read data from trip_info.csv
def load_trip_info(trip_info_file):
	print('Reading load_trip_info')
	df_trip = pd.read_csv(trip_info_file)
	df_trip['date_time'] = df_trip['date_time'].apply(lambda x: int(datetime.strptime(str(x), '%Y%m%d%H%M%S').timestamp()))
	print('completed load_trip_info')
	return df_trip
# function to read data from veheicle_trails folder
def load_vehicle_trails(folder_path):
	print('Reading vehicle')
	vehicle_trails = pd.DataFrame()
	for file in os.listdir(folder_path):
		if file.endswith('.csv'):
			file_path = os.path.join(folder_path, file)
			df = pd.read_csv(file_path)
			df['tis'] = df['tis'].astype(int)
			vehicle_trails = pd.concat([vehicle_trails, df], ignore_index=True)
	#vehicle_trails=vehicle_trails[:90000]
	print('completed vehicle_trip')
	return vehicle_trails
#functiom to encapsulate all the the methods for computimg and returning the desired datframe
def compute_function(vehicle_trails_filtered,df_trip):
	print('Computing')
	df_v=vehicle_trails_filtered[['lic_plate_no','lat','lon','lname','tis','spd','harsh_acceleration','harsh_acceleration','osf']]
	merged_df = df_v.merge(df_trip, left_on='lic_plate_no', right_on='vehicle_number')
	print('Merge Complete')
	distances = []
	#merged_df=merged_df[:100]
	prev_lat, prev_lon = None, None
	for _, row in merged_df.iterrows():
		lat, lon = row['lat'], row['lon']
		if prev_lat is not None and prev_lon is not None:
			distances.append(haversine(lat, lon, prev_lat, prev_lon))
		else:
			distances.append(0.0)
		prev_lat, prev_lon = lat, lon
	merged_df['distance'] = distances
	print('Distance computation complete')
	report_df = merged_df.groupby('lic_plate_no').agg({'distance': 'sum','trip_id': 'count','spd': 'mean','transporter_name': 'first','osf': 'sum'}).reset_index()
	report_df.rename(columns={'lic_plate_no': 'License plate number','distance': 'Distance','trip_id': 'Number of Trips Completed','spd': 'Average Speed','transporter_name': 'Transporter Name','osf': 'Number of Speed Violations'}, inplace=True)
	print(report_df)
	return report_df
# Function that is the entry point of the api to compute and save the dataframe in xslx
@app.route('/generate_asset_report')
def generate_asset_report():
	start_time = int(request.args.get('start_time', 1630617600))
	end_time = int(request.args.get('end_time', 1630682400))
	print(start_time)
	print(end_time)
	df_trip=load_trip_info('Data\Trip-Info.csv')
	vehicle_trails=load_vehicle_trails('Data\Eol_dump')
	vehicle_trails_filtered = vehicle_trails[(vehicle_trails['tis'] >= start_time) & (vehicle_trails['tis'] <= end_time)]
	if vehicle_trails_filtered.empty:
		return jsonify({'error': 'No data available for the specified time period.'})
	df=compute_function(vehicle_trails_filtered,df_trip)
	file_name='asset_report_'+str(end_time)+'.xlsx'
	df.to_excel(file_name)
	result_dict = df.to_dict(orient='records')
	return jsonify({'Success': 'The data is written'})
	#return jsonify(result_dict)
@app.route('/')
def enter_point():
	l=[(1,'sai','23')]
	df=pd.DataFrame(l,columns=['id','name','age'])
	df.to_excel("output.xlsx")
	return 'The data is written'
if __name__ == '__main__':
	app.run()
