from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
import json
import requests


image_acg = on_command('acg', priority=1, block=True)


@image_acg.handle()
async def handle_acg(bot: Bot, event: Event, state: dict):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }
    res = requests.get("https://yingserver.cn/open/acgimg/acgurl.php?return=json", headers=header)
    res.encoding = 'utf-8'
    cards_data = json.loads(res.text)
    print(cards_data)
    if cards_data['code'] == '200':
        seq = '[CQ:image,file=' + cards_data['acgurl'] + ']'
        await bot.send(event, seq)
    else:
        await bot.send(event, 'api异常,图片获取失败')
