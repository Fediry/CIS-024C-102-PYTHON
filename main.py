# -------- START: don't modify anything below this line ------
from collections.abc import ItemsView
import json
from re import template

with open('.lesson/data.json') as f:
  data = json.load(f)
# -------- END: don't modify anything above this line ------

# the dictionary you need to process is in `data` variable
# data is the weather forecast for the next 5 days in 3 hour interval
# However, the raw JSON file is not really human readable
# So, what you need to do is to process it, and summarize it into something like this:
"""
City Name: <string>
Country Name: <string>
Average temperature (use temp, not feels_like): <float, keep two digits after decimal>
Average humidity when wind speed is greater than 1: <float>
All distinct weather descriptions: <string separated by comma>
Minimum temperature(in Fahrenheit, data is in Kelvin): <float, same, two digits>
Timestamp for mininum temperature: <string>
Maxinum temperature: <float, two digits>
Timestamp for maximum temperature: <string>
"""
# Your final answer should be exactly this (All distinct weather descriptions can be in any order!):
"""
City Name: San Jose
Country Name: US
Average Temperature: 68.69
Average humidity when wind speed is greater than 1: 50.94
All distinct weather descriptions: scattered clouds, few clouds, overcast clouds, broken clouds, clear sky
Minimum temperature: 57.83
Timestamp for mininum temperature: 2023-09-18 12:00:00
Maximum temperature: 90.03
Timestamp for maximum temperature: 2023-09-15 21:00:00
"""

# EXTRA POINTS:
# print out dates of the coolest and the hottest day (not a certain hour of a day!)
# and the average temperature of the coolest and hottest day

# -------- Your program starts here! -----------
# You can use `print(data)` to see what it actually looks like
# hint: you can copy and paste the data to some online JSON formater website (like https://jsonformatter.org/) to get a better understanding of how the whole data is like

def kelvin_to_fahrenheit(number):
  """ Receive an number, convert it from Kelvin to Fahrenheit and return the result"""
  return 1.8 * (number - 273.15) + 32

def find_average(numbers):
  """ Receive a list of numbers, find the average and return the result"""
  return sum(numbers) / len(numbers)

def get_unique_descriptions(descriptions):
  """ Recieve a list, compare the contents for duplicates and return a list of only 
      unique items"""
  unique_items = []
  for item in descriptions:
    if item['description'] not in unique_items:
      unique_items.append(item['description'])
  return ", ".join(unique_items)

def find_min_with_date(temps_with_dates):
  """ Receive a tuple of temperatures and dates, find the smallest temperature
      and return a tuple of that temperature and the date"""
  smallest = temps_with_dates[0]
  for item in temps_with_dates:
    if item[0] < smallest[0]:
      smallest = item
  return smallest

def find_max_with_date(temps_with_dates):
  """ Receive a tuple of temperatures and dates, find the largest temperature
      and return a tuple of that temperature and the date"""
  largest = temps_with_dates[0]
  for item in temps_with_dates:
    if item[0] > largest[0]:
      largest = item
  return largest

# Get all temps
all_temps = [kelvin_to_fahrenheit(item['main']['temp'])
             for item in data['list']]

# Get all temps and corresponding dates into a tuple
all_temps_with_dates = [(kelvin_to_fahrenheit(item['main']['temp']), item['dt_txt'])
                        for item in data['list']]

min_temp_with_date = find_min_with_date(all_temps_with_dates)
max_temp_with_date = find_max_with_date(all_temps_with_dates)

# Find humidity for all entries with a wind speed greater than 1
humidity_for_wind_over_one = [(item['main']['humidity'])
                     for item in data['list'] 
                     if item['wind']['speed'] > 1]

# Find all distinct weather descriptions
weather_descriptions = [items['weather'][0]
           for items in data['list']]

# # Find all temps for coolest and warmest days and average them
# # Get only the date from the coolest and warmest date-times
# coolest_day = min_temp_with_date[1].split()[0]
# warmest_day = max_temp_with_date[1].split()[0]
# coolest_day_temps = find_average([temp
#                      for temp, date in all_temps_with_dates
#                      if date.split()[0] == coolest_day])

# warmest_day_temps = find_average([temp
#                      for temp, date in all_temps_with_dates
#                      if date.split()[0] == warmest_day])

# BONUS Attempt number 2
days = {}
for temp, date_code in all_temps_with_dates:
  day = date_code.split()[0]
  if day in days:
    days[day].append(temp)
  else:
    days[day] = [temp]

avg_temp_days = {}
for day, temps in days.items():
  avg_temp_days[day] = find_average(temps)

coolest_day = min(avg_temp_days.items())
warmest_day = max(avg_temp_days.items())

print(f"City Name: {data['city']['name']}")
print(f"Country Name: {data['city']['country']}")
print(f"Average Temperature: {find_average(all_temps):.2f}")
print(f"Average Humidity when wind speed is greater than 1: {find_average(humidity_for_wind_over_one):.2f}")
print(f"All distinct weather descriptions: {get_unique_descriptions(weather_descriptions)}")
print(f"Minimum temperature: {min_temp_with_date[0]:.2f}")
print(f"Timestamp for minimum temperature: {min_temp_with_date[1]}")
print(f"Maximum temperature: {max_temp_with_date[0]:.2f}")
print(f"Timestamp for maximum temperature: {max_temp_with_date[1]}")
print("BONUS:")
print(f"Coolest day: {coolest_day[0]}")
print(f"Average temperature on coolest day: {coolest_day[1]:.2f}")
print(f"Hottest day: {warmest_day[0]}")
print(f"Average temperature on hottest day: {warmest_day[1]:.2f}")

