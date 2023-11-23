import tkinter as tk
import requests

api_key = 'YOUR_API'

def get_weather(city_name, city_code, city_lat, city_lon):
    url = f'https://api.qweather.com/v7/weather/now?location={city_code}&key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()
        if weather_data.get('code') == '200':
            now_data = weather_data.get('now')
            if now_data:
                temperature = now_data.get('temp')
                condition = now_data.get('text')
                weather_info = f"{city_name} - 天气：{condition}, 温度：{temperature} ℃"
                lon_lat = f"经度: {city_lon}, 纬度: {city_lat}"
                display_weather_info(weather_info, lon_lat)
            else:
                display_error(f"无法获取 {city_name} 的天气数据")
        else:
            display_error(f"无法获取 {city_name} 的天气数据")
    else:
        display_error(f"请求 {city_name} 天气数据失败")

def display_weather_info(weather_info, lon_lat):
    result_label.config(text=f"{weather_info}\n{lon_lat}")

def display_error(message):
    result_label.config(text=message)

def on_click():
    city_name = entry.get()
    url = f'https://geoapi.qweather.com/v2/city/lookup?location={city_name}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        city_data_json = response.json()
        if city_data_json.get('location'):
            for location_data in city_data_json['location']:
                city_code = location_data['id']
                city_lat = location_data['lat']
                city_lon = location_data['lon']
                get_weather(city_name, city_code, city_lat, city_lon)
        else:
            display_error(f"未找到 {city_name} 的信息")
    else:
        display_error(f"请求 {city_name} 失败")

root = tk.Tk()
root.title('天气查询')

label = tk.Label(root, text='请输入城市名称：')
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text='查询', command=on_click)
button.pack()

result_label = tk.Label(root, text='')
result_label.pack()

root.mainloop()
