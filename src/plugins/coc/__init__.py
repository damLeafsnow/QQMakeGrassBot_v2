# -*-coding:utf8-*-
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from .coc import rollCard, dice

coc_card = on_command('coc', aliases={'车卡'}, priority=1, block=True)
coc_roll = on_command('roll', priority=1, block=True)
coc_check = on_command('check', aliases={'检定'}, priority=1, block=True)
coc_sc = on_command('sancheck', aliases={'sc'}, priority=1, block=True)
coc_mindcheck = on_command('心理学', priority=1, block=True)


@coc_card.handle()
async def handle_grass(bot: Bot, event: Event, state: dict):
    card = rollCard()
    await coc_card.finish(card)


@coc_roll.handle()
async def handle_roll(bot: Bot, event: Event, state: dict):
    maxpoint = 100
    reg = str(event.message).strip()
    if reg:
        print(reg)
        if reg.isdigit():
            # print('is digit')
            maxpoint = int(reg)
            if maxpoint < 1:
                await coc_roll.finish('爬.')
                return
        else:
            # print('not digit')
            await coc_roll.finish('格式错误,请输入正整数或留空(默认100).')
            return

    result = dice(maxpoint)
    user = event.sender['nickname']
    await coc_roll.finish('%sroll出了%d库啵.' % (user, result))


@coc_check.handle()
async def handle_check(bot: Bot, event: Event, state: dict):
    reg = str(event.message).strip()
    user = event.sender['nickname']
    if not reg:
        await coc_check.finish('未输入参数,格式为.check/.检定 技能名 技能等级')
        return
    skill = reg.split(" ")
    if len(skill) == 2 and skill[1].isdigit():
        skill_lv = int(skill[1])
        point = dice(100)
        if point == 1:
            await coc_check.finish('%s的%s技能获得了大成功,效果拔群.' % (user, skill[0]))
        elif point <= skill_lv / 5:
            await coc_check.finish('%s的%s技能获得了极难成功(%d),效果喜人.' % (user, skill[0], point))
        elif point <= skill_lv / 2:
            await coc_check.finish('%s的%s技能获得了困难成功(%d),效果不错.' % (user, skill[0], point))
        elif point <= skill_lv:
            await coc_check.finish('%s的%s技能使用成功(%d),可喜可贺.' % (user, skill[0], point))
        elif point > skill_lv:
            if point == 100:
                await coc_check.finish('%s的%s技能大失败(%d),那可真蠢.' % (user, skill[0], point))
            elif skill_lv < 50 and point >= 96:
                await coc_check.finish('%s的%s技能大失败(%d),一定是技能等级太低的问题.' % (user, skill[0], point))
            else:
                await coc_check.finish('%s的%s技能失败了(%d),令人遗憾.' % (user, skill[0], point))
    else:
        await coc_check.finish('参数格式错误,格式为.check/.检定 技能名 技能等级')
        return


@coc_sc.handle()
async def handle_sc(bot: Bot, event: Event, state: dict):
    reg = str(event.message).strip()
    user = event.sender['nickname']
    if not reg:
        await coc_sc.finish('未输入参数,格式为.sancheck/.sc 当前san值')
        return
    if reg.isdigit():
        skill_lv = int(reg)
        point = dice(100)
        if point <= skill_lv:
            await coc_sc.finish('%s的san check成功通过(%d),令人遗憾.' % (user, point))
        else:
            await coc_sc.finish('%s的san check失败了(%d).' % (user, point))
    else:
        await coc_sc.finish('参数格式错误,格式为.sancheck/.sc 当前san值')
        return


@coc_mindcheck.handle()
async def handle_mindcheck(bot: Bot, event: Event, state: dict):
    reg = str(event.message).strip()
    if not reg:
        await coc_mindcheck.finish('你要对谁过心理学?(格式:.心理学 目标)')
        return
    rnd = dice(100)
    user = event.sender['nickname']
    msg = ''
    if rnd == 1:
        msg += '%s认为%s说的宛若人间真理,信服的鼓起了掌.' % (user, reg)
    elif rnd > 1 and rnd <= 10:
        msg += '%s认为%s说的很有道理,不应质疑.' % (user, reg)
    elif rnd > 10 and rnd <= 50:
        msg += '%s认为%s说的没有问题.' % (user, reg)
    elif rnd > 50 and rnd <= 90:
        msg += '%s认为%s在一派胡言.' % (user, reg)
    elif rnd > 90 and rnd <= 99:
        msg += '%s认为%s说的狗屁不通.' % (user, reg)
    elif rnd == 100:
        msg += '%s仿佛听到%s说了天底下最大的笑话,并笑出了声.' % (user, reg)
    await coc_mindcheck.finish(msg)
