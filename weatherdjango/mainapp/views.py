from django.shortcuts import render
import requests
import json

def index(request):
    return render(request, 'index.html')

def separate_temperature_parts(temperature):
    temperature_str = str(temperature)
    if '.' in temperature_str:
        integer_part, decimal_part = temperature_str.split('.')
    else:
        integer_part = temperature_str
        decimal_part = '0'
    return {
        'integer_part': integer_part,
        'decimal_part': decimal_part,
    }

def cityview(request):
    city = request.POST.get('city')  # Retrieve the city name from the form
    print(city)
    if city:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID=f9c2f0f368afcfb53b6a73a394cfef82&units=metric'
        response = requests.get(url)
        data = json.loads(response.text)
        if 'main' in data:
            data['main']['temp_parts'] = separate_temperature_parts(data['main']['temp'])
            data['main']['temp_min_parts'] = separate_temperature_parts(data['main']['temp_min'])
            data['main']['temp_max_parts'] = separate_temperature_parts(data['main']['temp_max'])
            data['main']['feels_like_parts'] = separate_temperature_parts(data['main']['feels_like'])
        else:
            data = None
        print(data)
    else:
        data = None
    return render(request, 'cityview.html', {'data': data})