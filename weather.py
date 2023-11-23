import requests
import concurrent.futures

api_key = 'YOUR_API'

def get_city_info():
    with open('city.txt', 'r') as file:
        locations = []
        for city_name in file:
            city_name = city_name.strip()  
            url = f'https://geoapi.qweather.com/v2/city/lookup?location={city_name}&key={api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                city_data_json = response.json()
                if city_data_json.get('location'):
                    for location_data in city_data_json['location']:
                        locations.append({
                            "name": location_data['name'],
                            "city_code": location_data['id'],
                            "latitude": location_data['lat'],                           
                            "longitude": location_data['lon']
                        })
                        break
            else:
                print(f"请求失败 - {city_name}")
        return locations

def get_weather(location):
    city_name = location["name"]
    city_code = location["city_code"]
    city_lat = location["latitude"]
    city_lon = location["longitude"]
    url = f'https://api.qweather.com/v7/weather/now?location={city_code}&key={api_key}'
    
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        if weather_data.get('code') == '200':
            now_data = weather_data.get('now')
            if now_data:
                temperature = now_data.get('temp')
                condition = now_data.get('text')
                weather_info = f"{city_name} - 天气：{condition}, 温度：{temperature} ℃\n"
                lon_lat = f"{city_lat} {city_lon}\n"
                with open('weather_output.txt', 'a') as output_file:
                    output_file.write(weather_info)
                    output_file.write(lon_lat)
            else:
                print(f"无法获取 {city_name} 的天气数据")
        else:
            print(f"无法获取 {city_name} 的天气数据")
    else:
        print(f"请求 {city_name} 天气数据失败")
        
locations = get_city_info()

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(get_weather, locations)
