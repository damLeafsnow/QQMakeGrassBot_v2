from nonebot import on_command
from nonebot.plugin import on_keyword
from nonebot.adapters.cqhttp import Bot, Event
from nonebot import scheduler, get_bots
from time import sleep
from os import path
import json
import re
from .bilibili import get_bilibili_info_by_avid, get_bilibili_info_by_bvid
from .bilibili import get_bilibili_info_by_b23tv, get_bilibili_live_info
from .bilibili import getUserInfobyUID
from .bilibili import GetDynamicStatus, GetLiveStatus

bilibili_vid = on_keyword({"BV", "bv", "Bv", "bV", "AV", "av", "Av", "aV"},
                          priority=1,
                          block=True)
bilibili_b23 = on_keyword({"b23.tv"}, priority=1, block=True)
bilibili_live = on_keyword({"live.bilibili.com"}, priority=1, block=True)
bilibili_uid = on_keyword({"space.bilibili.com"}, priority=1, block=True)
bilibili_user = on_command('用户查询', aliases={'uid'}, priority=1, block=True)
bilibili_adddy = on_command('添加动态关注',
                            aliases={'biliadddy'},
                            priority=1,
                            block=True)
bilibili_deldy = on_command('取消动态关注',
                            aliases={'bilideldy'},
                            priority=1,
                            block=True)
bilibili_addly = on_command('添加直播关注',
                            aliases={'biliaddlive'},
                            priority=1,
                            block=True)
bilibili_delly = on_command('取消直播关注',
                            aliases={'bilidellive'},
                            priority=1,
                            block=True)
bilibili_dylist = on_command('动态关注列表',
                             aliases={'bilidylist'},
                             priority=1,
                             block=True)
bilibili_lylist = on_command('直播关注列表',
                             aliases={'bililivelist'},
                             priority=1,
                             block=True)
debug_group = 1087849813
bot_list = [2433627163, 1721190339]
dynamic_list = {}
live_list = {}
uid_dict = {}
turn = 0


@scheduler.scheduled_job('interval', minutes=10)
# @scheduler.scheduled_job('interval', seconds=40)     # 测试用
async def get_bilibili_infos():
    global turn
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    # 获取当前bot
    bots = get_bots()
    bot = 0
    for bot_num in bot_list:
        if str(bot_num) in bots.keys():
            bot = bots[str(bot_num)]
            break

    # 获取动态更新
    for key in dynamic_list.keys():
        for uid in dynamic_list[key]:
            # print('dynamic'+uid)
            sleep(1)
            dynamic_content = GetDynamicStatus(uid, key)
            if dynamic_content:
                print(uid+'有新动态。')
                await bot.send_group_msg(group_id=debug_group,
                                         message=uid + '有新动态,正在推送.')
                for content in dynamic_content:
                    await bot.send_group_msg(group_id=key, message=content)
            else:
                print(uid+'没有新动态。')

    # 获取直播更新
    for key in live_list.keys():
        for uid in live_list[key]:
            # print('live'+uid)
            sleep(1)
            live_msg = GetLiveStatus(uid, key)
            if live_msg:
                print(uid+'正在直播。')
                await bot.send_group_msg(group_id=debug_group,
                                         message=uid + '有新直播消息,正在推送.')
                # for content in live_msg:
                await bot.send_group_msg(group_id=key, message=live_msg)
            else:
                print(uid+'未开播。')
    turn += 1
    print('第%d次动态、直播获取完成。' % turn)


@bilibili_vid.handle()
async def handle_vid(bot: Bot, event: Event, state: dict):
    # 防止bot套娃
    sender = event.sender['user_id']
    if sender in bot_list:
        print("send by bot,ignore")
        return

    msg = str(event.message)
    # msg = msg.lower()

    # 检索视频号
    # list = msg.split('/')
    list = re.split("/|\?|\？|\n|\r|,|&", msg)
    print(list)
    vid = 0
    info = []
    for i in list:
        if i.lower().startswith('av') or i.lower().startswith('bv'):
            vid = i
            break

    # 清理可能存在的多余后缀信息
    if vid.find('?'):
        vid = vid.split('?')[0]

    # 获取数据
    if vid.lower().startswith('av'):
        await bot.send_group_msg(group_id=debug_group, message='解析到av号:' + vid)
        info = get_bilibili_info_by_avid(vid[2:])
    elif vid.lower().startswith('bv'):
        await bot.send_group_msg(group_id=debug_group, message='解析到BV号:' + vid)
        info = get_bilibili_info_by_bvid(vid)
    if not info:
        await bot.send_group_msg(group_id=debug_group, message='解析完成,非b站链接')
        return

    # 消息推送
    await bilibili_vid.finish(info)


@bilibili_b23.handle()
async def handle_b23(bot: Bot, event: Event, state: dict):
    # 防止bot套娃
    sender = event.sender['user_id']
    if sender in bot_list:
        print("send by bot,ignore")
        return

    msg = str(event.message)

    # 检索视频号
    # list = msg.split('/')
    list = re.split("/|\?|\？|\n|\r|,|&", msg)
    info = []
    vid = ''
    i = 0
    for s in list:
        if s == 'b23.tv':
            vid = list[i + 1]
            break
        i += 1

    # 清理可能存在的多余后缀信息
    if vid.find('?'):
        vid = vid.split('?')[0]

    # 获取数据
    await bot.send_group_msg(group_id=debug_group, message='解析到加密短链:' + vid)
    info = get_bilibili_info_by_b23tv(vid)
    if not info:
        await bot.send_group_msg(group_id=debug_group, message='解析完成,非b站链接')
        return

    # 消息推送
    await bilibili_b23.finish(info)


#  直播间解析
@bilibili_live.handle()
async def handle_live(bot: Bot, event: Event, state: dict):
    # 防止bot套娃
    sender = event.sender['user_id']
    if sender in bot_list:
        print("send by bot,ignore")
        return

    msg = str(event.message)

    # 检索直播间号
    # list = msg.split('/')
    list = re.split("/|\?|\？|\n|\r|,|&", msg)
    info = []
    vid = ''
    i = 0
    for s in list:
        if s == 'live.bilibili.com':
            vid = list[i + 1]
            break
        i += 1

    #  清理多余后缀信息
    if vid.find('?'):
        vid = vid.split('?')[0]

    # 获取数据
    await bot.send_group_msg(group_id=debug_group, message='解析到直播间地址:' + vid)
    info = get_bilibili_live_info(vid)
    if not info:
        await bot.send_group_msg(group_id=debug_group, message='解析完成,直播间不存在')
        return

    # 消息推送
    await bilibili_live.finish(info)


# 根据uid查询用户信息
@bilibili_user.handle()
async def bili_uid_search(bot: Bot, event: Event, state: dict):
    uid = str(event.message).strip()

    # 输入检查
    if not uid or not uid.isdigit():
        await bilibili_user.finish('你uid有问题.')

    user_info = getUserInfobyUID(uid)
    msg = ''
    if user_info:
        msg += '用户名:' + user_info['name'] + '  性别:' + user_info['sex'] + '\n'
        msg += '[CQ:image,file=' + user_info['face'] + ']'
        msg += '个人签名:\n' + user_info['sign']
        msg += '\n\n个人主页:https://space.bilibili.com/' + uid

        # 更新uid数据
        # todo

        await bilibili_user.finish(msg)
    else:
        await bilibili_user.finish('用户不存在.')


# 用户空间解析
@bilibili_uid.handle()
async def handle_uid(bot: Bot, event: Event, state: dict):
    # 防止bot套娃
    sender = event.sender['user_id']
    if sender in bot_list:
        print("send by bot,ignore")
        return

    msg = str(event.message)

    # 检索uid号
    list = msg.split('/')
    vid = ''
    i = 0
    for s in list:
        if s == 'space.bilibili.com':
            vid = list[i + 1]
            break
        i += 1

    #  清理多余后缀信息
    if vid.find('?'):
        vid = vid.split('?')[0]

    # 获取数据
    await bot.send_group_msg(group_id=debug_group, message='解析到个人uid:' + vid)
    user_info = getUserInfobyUID(vid)
    msg = ''
    if user_info:
        msg += '用户名:' + user_info['name'] + '  性别:' + user_info['sex'] + '\n'
        msg += '[CQ:image,file=' + user_info['face'] + ']'
        msg += '个人签名:\n' + user_info['sign']
        msg += '\n\n个人主页:https://space.bilibili.com/' + vid
    else:
        await bot.send_group_msg(group_id=debug_group, message='解析完成,用户不存在')
        return

    # 消息推送
    await bilibili_uid.finish(msg)


# 添加动态关注
@bilibili_adddy.handle()
async def handle_bilibili_adddy(bot: Bot, event: Event, state: dict):
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    group = str(event.group_id)
    uid = str(event.message).strip()
    user_info = getUserInfobyUID(uid)
    msg = ''
    if user_info:
        msg += '已添加到动态关注:\n' + user_info['name']
        msg += '(' + uid + ')\n'
        msg += '[CQ:image,file=' + user_info['face'] + ']'
        msg += '\n性别:' + user_info['sex'] + '\n个人签名:\n' + user_info['sign']

        # 添加uid名称映射
        if uid not in uid_dict.keys():
            uid_dict[uid] = user_info['name']
        saveUIDdata()

        # 添加uid到数据库
        if group in dynamic_list.keys():
            dynamic_list[group].append(uid)
        else:
            dynamic_list[group] = []
            dynamic_list[group].append(uid)
        saveDatas()
    else:
        msg += '未查询到用户.'

    # 消息推送
    await bilibili_adddy.finish(msg)


# 取消动态关注
@bilibili_deldy.handle()
async def handle_bilibili_deldy(bot: Bot, event: Event, state: dict):
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    group = str(event.group_id)
    uid = str(event.message).strip()
    msg = ''
    # 删除
    if group in dynamic_list.keys():
        if uid in dynamic_list[group]:
            dynamic_list[group].remove(uid)
            msg += '用户' + str(uid) + '已取消动态关注.'
            saveDatas()
        else:
            msg += '未关注该用户.'
    else:
        msg += '未关注该用户.'

    # 消息推送
    await bilibili_deldy.finish(msg)


# 添加直播关注
@bilibili_addly.handle()
async def handle_bilibili_addly(bot: Bot, event: Event, state: dict):
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    group = str(event.group_id)
    uid = str(event.message).strip()
    user_info = getUserInfobyUID(uid)
    msg = ''
    if user_info:
        msg += '已添加到直播关注:\n' + user_info['name']
        msg += '(' + uid + ')\n'
        msg += '[CQ:image,file=' + user_info['face'] + ']'
        msg += '\n性别:' + user_info['sex'] + '\n个人签名:\n' + user_info['sign']

        # 添加uid名称映射
        if uid not in uid_dict.keys():
            uid_dict[uid] = user_info['name']
        saveUIDdata()

        # 添加
        if group in live_list.keys():
            live_list[group].append(uid)
        else:
            live_list[group] = []
            live_list[group].append(uid)
        saveDatas()
    else:
        msg.append += '未查询到用户.'

    await bilibili_addly.finish(msg)


# 取消直播关注
@bilibili_delly.handle()
async def handle_bilibili_delly(bot: Bot, event: Event, state: dict):
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    group = str(event.group_id)
    uid = str(event.message).strip()
    msg = ''
    # 删除
    if group in live_list.keys():
        if uid in live_list[group]:
            live_list[group].remove(uid)
            msg += '用户' + str(uid) + '已取消直播关注.'
            saveDatas()
        else:
            msg += '未关注该用户.'
    else:
        msg += '未关注该用户.'
    await bilibili_delly.finish(msg)


# 动态关注列表
@bilibili_dylist.handle()
async def handle_bilibili_dylist(bot: Bot, event: Event, state: dict):
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    group = str(event.group_id)

    msg = ''
    if group in dynamic_list.keys() and dynamic_list[group]:
        msg += '本群(' + group + ')动态关注列表:'
        for uid in dynamic_list[group]:
            if uid in uid_dict.keys():
                msg += '\n' + uid + '(' + uid_dict[uid] + ')'
            else:
                user_info = getUserInfobyUID(uid)
                sleep(1)
                if user_info:
                    # 添加uid名称映射
                    if uid not in uid_dict.keys():
                        uid_dict[uid] = user_info['name']
                    saveUIDdata()
                    msg += '\n' + uid + '(' + uid_dict[uid] + ')'
                else:
                    msg += '\n' + uid + '(用户不存在)'
    else:
        msg += '本群关注列表为空'
    await bilibili_dylist.finish(msg)


# 直播关注列表
@bilibili_lylist.handle()
async def handle_bilibili_lylist(bot: Bot, event: Event, state: dict):
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    group = str(event.group_id)

    msg = ''
    if group in live_list.keys() and live_list[group]:
        msg += '本群(' + group + ')直播关注列表:'
        for uid in live_list[group]:
            if uid in uid_dict.keys():
                msg += '\n' + uid + '(' + uid_dict[uid] + ')'
            else:
                user_info = getUserInfobyUID(uid)
                sleep(1)
                if user_info:
                    # 添加uid名称映射
                    if uid not in uid_dict.keys():
                        uid_dict[uid] = user_info['name']
                    saveUIDdata()
                    msg += '\n' + uid + '(' + uid_dict[uid] + ')'
                else:
                    msg += '\n' + uid + '(用户不存在)'
    else:
        msg += '本群关注列表为空'
    await bilibili_lylist.finish(msg)


def loadUIDdata():
    global uid_dict
    uid_dict.clear()

    if not path.exists("./datas/uidlist.json"):
        f = open('./datas/uidlist.json', 'w')
        f.close()

    try:
        with open("./datas/uidlist.json", 'r') as f:
            uid_dict = json.load(f)
    except json.decoder.JSONDecodeError:
        print("uidlist file empty")


def saveUIDdata():
    with open("./datas/uidlist.json", "w") as f:
        json.dump(uid_dict, f)


def saveDatas():
    with open("./datas/dynamiclist.json", "w") as f:
        json.dump(dynamic_list, f)
    with open("./datas/livelist.json", "w") as f:
        json.dump(live_list, f)


def loadDatas():
    global dynamic_list, live_list
    dynamic_list.clear()
    live_list.clear()

    if not path.exists("./datas/dynamiclist.json"):
        f = open('./datas/dynamiclist.json', 'w')
        f.close()
    if not path.exists("./datas/livelist.json"):
        f = open('./datas/livelist.json', 'w')
        f.close()

    try:
        with open("./datas/dynamiclist.json", 'r') as f:
            dynamic_list = json.load(f)
    except json.decoder.JSONDecodeError:
        print("dynamiclist file empty")
    try:
        with open("./datas/livelist.json", 'r') as f:
            live_list = json.load(f)
    except json.decoder.JSONDecodeError:
        print("livelist file empty")
