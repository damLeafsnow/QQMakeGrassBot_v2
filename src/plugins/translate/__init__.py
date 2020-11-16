# -*-coding:utf8-*-
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from .translate import translate
from time import sleep

translate_tr = on_command('tr', priority=1, block=True)
translate_tra = on_command('翻译', priority=1, block=True)
translate_jf = on_command('机翻', priority=1, block=True)


@translate_tr.handle()
async def handle_tr(bot: Bot, event: Event, state: dict):
    reg = str(event.message).strip().split(' ', 2)
    if len(reg) == 3:
        from_reg = reg[0]
        to_reg = reg[1]
        text = reg[2]
        result = translate(text, from_reg, to_reg)
        if result:
            await translate_tr.finish('翻译:\n' + result)
        else:
            await translate_tr.finish('格式错误.')
    else:
        await translate_tr.finish('格式错误.')


@translate_tra.handle()
async def handle_tra(bot: Bot, event: Event, state: dict):
    reg = str(event.message).strip()
    if reg:
        from_reg = 'auto'
        to_reg = 'zh'
        text = reg
        result = translate(text, from_reg, to_reg)
        await translate_tra.finish('翻译:\n' + result)
    else:
        await translate_tra.finish('格式错误.')


@translate_jf.handle()
async def handle_jf(bot: Bot, event: Event, state: dict):
    reg = str(event.message).strip()
    if reg:
        string = reg
        string = translate(string, 'auto', 'zh')
        sleep(1)
        string = translate(string, 'zh', 'wyw')
        # print(string)
        sleep(1)
        str_list = list(string)
        str_list.reverse()
        string = ''.join(str_list)
        # print(string)
        string = translate(string, 'zh', 'jp')
        # print(string)
        sleep(1)
        str_list = list(string)
        str_list.reverse()
        string = ''.join(str_list)
        # print(string)
        string = translate(string, 'jp', 'en')
        # print(string)
        sleep(1)
        string = translate(string, 'en', 'zh')
        # print(string)
        await translate_jf.finish(string)
    else:
        await translate_jf.finish('格式错误')
