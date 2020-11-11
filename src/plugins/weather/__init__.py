from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
import urllib.request
import requests
import sys
import importlib
import json
importlib.reload(sys)

weather = on_command("天气", priority=5)


# 添加一个处理函数
@weather.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["city"] = args  # 如果用户发送了参数则直接赋值


# 指示 NoneBot 当 state 中不存在 key 时向用户发送 prompt 等待用户回复并赋值给 state[key]
@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city(bot: Bot, event: Event, state: dict):
    city = state["city"]
    # if city not in ["上海", "北京"]:
        # 这个函数用于结束当前事件处理函数，强制接收一条新的消息再再次运行当前消息处理函数
        # await weather.reject("你想查询的城市暂不支持，请重新输入！")
    city_weather = await get_weather(city)
    # 这个函数用于直接结束当前事件处理
    await weather.finish(city_weather)


async def get_weather(city: str):
    # return f"{city}的天气是..."
    host = 'http://wthrcdn.etouch.cn/weather_mini?city='
    url = host + urllib.parse.quote(city)
    r = requests.get(url)
    jsons = json.loads(r.text)
    res = city+'天气:\n'
    for i in jsons['data']['forecast']:
        res += i['date']+':天气'+i['type']+' 最'+i['low']+' 最'+i['high']+'\n'
    return res
