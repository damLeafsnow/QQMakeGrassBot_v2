from nonebot import on_message
from nonebot.adapters.cqhttp import Bot, Event
from random import randint

grass = on_message(priority=5, block=True)
tempmsg = []  # 复读延迟


@grass.handle()
async def handle_grass(bot: Bot, event: Event, state: dict):
    rnd = randint(1, 100)
    print("基本聊天,随机数:%d" % (rnd))
    if rnd <= 10:
        rnd = randint(1, 6)
        print('复读随机数:%d' % (rnd))
        if rnd == 1:
            print('生草')
            await grass.finish("草")
        if rnd == 2:
            print('复读')
            if event.raw_message:
                await grass.finish(event.raw_message)
        if rnd in range(3, 5):
            print('记录延迟复读')
            tempmsg.append(event.raw_message)
        if rnd in range(5, 7):
            print('复读延迟复读')
            if tempmsg:  # 判断非空
                i = randint(0, len(tempmsg)-1)
                msg = tempmsg[i]
                tempmsg.remove(tempmsg[i])
                await grass.finish(msg)
