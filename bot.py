# -*-coding:utf8-*-
import nonebot
# import config


def main():
    nonebot.init()
    # nonebot.load_builtin_plugins()
    # 加载单独的一个插件，参数为合法的python包名
    nonebot.load_plugin("nonebot.plugins.base")
    # 加载插件目录，该目录下为各插件，以下划线开头的插件将不会被加载
    nonebot.load_plugins("src/plugins")
    app = nonebot.get_asgi()
    nonebot.run()


if __name__ == "__main__":
    main()
