# QQMakeGrassBot
基于nonebot2的qq bot

### 环境要求

1. 环境
   - python3.7+
- ~~Mirai-console/Mirai-ok~~
- go-cqhttp
2. python模块
   - **nonebot2**[full]
   - requests
   - APScheduler
   - ujson
   - msgpack
- beautifulsoup
   
3. 酷Q插件

   - HTTP API

     > 首次运行后生成默认配置
     >
     > 添加 ``"enable_heartbeat": true ``项
     >
     > 修改 ``use_ws_reverse``项为``true``
     >
     > 修改 ``ws_reverse_url`` 项为 ``ws://127.0.0.1:8080/ws/``
     >
     > 修改 ``ws_reverse_api_url`` 项为 ``ws://127.0.0.1:8080/ws/api/``
     >
     > 修改 ``ws_reverse_event_url`` 项为``ws://127.0.0.1:8080/ws/event/``

   - ~~Mirai~~

     > ~~下载 `miraiOK_windows_平台名.exe` ,运行下载基础文件后在 `config.txt ` 添加~~bot~~账号信息~~
     >
     > ~~下载 `CQHTTPMirai-0.1.4.jar` ,放入 `plugins` 文件夹,重新运行~~

### 文件结构(更新中)

- QQMakeGrassBot_v2

  - bot

    > 主文件，用于启动bot

  - datas

    > 数据文件夹，存放数据文件

    - BAIDU_API

      > 百度翻译api,插件用

    - PIXIV_Account

      > p站账号信息,插件用

    - dynamiclist.json

      > 序列化的数据文件,通过指令管理

    - livelist.json

      > 序列化的数据文件,通过指令管理
      
    - uidlist.json

      > 序列化的数据文件,通过指令管理

  - dynamics

    > 临时文件夹，运行时生成的临时文件，用于标记动态更新

  - pixdata

    > 找图插件临时文件夹,用于转发图片

  - src/plugins

    > 插件文件夹，存放自定义插件

    - usage

      > 输出插件列表

    - weather

      > 天气查询

    - bilibili

      > 解析b站视频直播间链接,定时推送动态

    - coc

      > 跑团插件(施工中)

    - makegrass

      > 生草复读机

    - pixiv

      > 爬p站瑟图

    - searchimage

      > 搜图

    - translate

      > 翻译

### 开发进度

迁移至nonebot2中