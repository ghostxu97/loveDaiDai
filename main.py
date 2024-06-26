from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://t.weather.sojson.com/api/weather/city/101020100"
  res = requests.get(url).json()
  weather = res['data']['forecast'][0]
  return weather['type'], weather['high'], weather['low']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days + 1

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature_max, temperature_min = get_weather()
data = {"letter":{"value":wea},"temperature":{"value":temperature_min + "~" + temperature_max},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"weather":{"value":get_words()}}
res = wm.send_template(user_id, template_id, data)
print(res)
res = wm.send_template("ozt7455T6o7SIKhm2h49agvaQtbw", template_id, data)
print(res)
