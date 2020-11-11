from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event

grass = on_command("草")


@grass.handle()
async def handle_grass(bot: Bot, event: Event, state: dict):
    await grass.finish("草")
