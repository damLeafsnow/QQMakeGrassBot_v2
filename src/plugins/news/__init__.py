from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
# import urllib.request
import requests
# import sys
# import importlib
import json
# importlib.reload(sys)

news = on_command("新闻", priority=1, block=True)


# 添加一个处理函数
@news.handle()
async def handle_news(bot: Bot, event: Event, state: dict):
    # res = requests.get('https://api.apiopen.top/getWangYiNews')
    # res.encoding = 'utf-8'
    # res = res.text
    # cards_data = json.loads(res)
    # index = 1
    # dynamic_content = []
    # if cards_data['code'] == 200:
    #     results = cards_data['result']
    #     for result in results:
    #         path = result['path']
    #         # image = result['image']
    #         # title = result['title']
    #         # passtime = result['passtime']
    #         # text = ''
    #         # text += '{0}.{1}({2})\n'.format(index, title, passtime)
    #         # text += '[CQ:image,file='+image+']'+'\n'
    #         # text += path
    #         # # print(text)
    #         # index += 1
    #         dynamic_content.append(path)
    # for content in dynamic_content:
    await bot.send(event, '不要搞大新闻')
