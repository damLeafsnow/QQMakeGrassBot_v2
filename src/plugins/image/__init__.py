# from nonebot import on_command
# from nonebot.adapters.cqhttp import Bot, Event
# from aiocqhttp import MessageSegment
# import os
# from .image import getPic

# image_acg = on_command('acg', priority=1, block=True)


# @image_acg.handle()
# async def handle_vid(bot: Bot, event: Event, state: dict):
#     if getPic():
#         seq = MessageSegment.image(os.getcwd()+'\\pixdata\\x.png')
#         try:
#             await image_acg.finish(seq)
#         except CQHttpError as e:
#                 print(e)
