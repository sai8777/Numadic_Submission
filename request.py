import requests
api_url = "http://127.0.0.1:5000/generate_asset_report" #api url
start_time = 1510617600
end_time = 1730682400
#print('iam here')
response = requests.get(api_url, params={"start_time": start_time, "end_time": end_time})
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error:", response.text)
