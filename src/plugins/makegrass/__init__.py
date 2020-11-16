from nonebot import on_message, on_startswith
from nonebot.adapters.cqhttp import Bot, Event
from random import randint

grass = on_message(priority=5, block=True)
disable = on_startswith(("不准", "不许"), priority=5, block=True)

tempmsg = []  # 复读延迟
disadlist = ['你', '我', '不', '没', '吗', '?', '？']
yygqlist = ['不对劲', '你有问题', u'؟?ذذ؟??¿؟زز¿؟¿???ذ¿', '我觉得不行', '你很懂哦',
            '挺好', '确实', '我觉得ok', '你这不行', '溜了溜了', '这不好吧', '不会吧?不会吧?',
            '啊,这', '就这?', '你在教我做事?', '有事?', '不愧是你.']
bot_list = [2433627163, 1721190339]


@grass.handle()
async def handle_grass(bot: Bot, event: Event, state: dict):
    rnd = randint(1, 100)
    print("基本聊天,随机数:%d" % (rnd))
    if rnd <= 25:
        # 反问
        rawmsg = event.plain_text
        for name in disadlist:
            if name in rawmsg:
                msg = rawmsg.strip('?？吗')+'!'
                if len(msg) >= 3:
                    msg = msg.replace('不过', '')
                    msg = msg.replace('不', '')
                    msg = msg.replace('没', '')
                    msg = msg.replace('你', '乪')
                    msg = msg.replace('我', '你')
                    msg = msg.replace('乪', '我')
                    await grass.finish(msg)
                    return
        rnd = randint(1, 10)
        print('复读随机数:%d' % (rnd))
        if rnd == 1:
            print('生草')
            await grass.finish("草")
        elif rnd == 2:
            print('复读')
            if event.raw_message:
                await grass.finish(event.raw_message)
        elif rnd in range(3, 5):
            print('记录延迟复读')
            tempmsg.append(event.raw_message)
        elif rnd in range(5, 7):
            print('复读延迟复读')
            if tempmsg:  # 判断非空
                i = randint(0, len(tempmsg)-1)
                msg = tempmsg[i]
                tempmsg.remove(tempmsg[i])
                await grass.finish(msg)
        elif rnd in range(7, 11):
            rnd = randint(0, len(yygqlist)-1)
            await grass.finish(yygqlist[rnd])
    elif rnd == 66:
        await grass.finish('http://game.granbluefantasy.jp/')


@disable.handle()
async def handle_disable(bot: Bot, event: Event, state: dict):
    # 防止bot套娃
    sender = event.sender['user_id']
    if sender in bot_list:
        print("send by bot,ignore")
        return

    key = event.plain_text[0:2]
    await grass.finish(key+event.plain_text)
