#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
import nonebot.config

# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
config_setting = {
    'command_start': {"."},
    'command_sep': {","},
}
nonebot.init(**config_setting)
app = nonebot.get_asgi()

nonebot.load_builtin_plugins()
nonebot.load_plugins("src/plugins")

# Modify some config / config depends on loaded configs
# 
# config = nonebot.get_driver().config
# do something...


if __name__ == "__main__":
    nonebot.run(app="bot:app")
