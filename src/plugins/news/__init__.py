from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
import requests
from bs4 import BeautifulSoup

news = on_command("新闻", priority=1, block=True)


# 添加一个处理函数
@news.handle()
async def handle_news(bot: Bot, event: Event, state: dict):
    

def get_pages():
    url = 'http://top.baidu.com/buzz?b=1&fr=20811'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    all_topics = soup.find_all('tr')[1:]
    news_res = ""
    for each_topic in all_topics:
        topic_times = each_topic.find('td', class_='last')  # 搜索指数
        topic_rank = each_topic.find('td', class_='first')  # 排名
        topic_name = each_topic.find('td', class_='keyword')  # 标题
        if topic_rank != None and topic_name != None and topic_times != None:
            topic_rank = each_topic.find('td', class_='first').get_text().replace(
                ' ', '').replace('\n', '')
            topic_name = each_topic.find('td', class_='keyword').get_text().replace(
                ' ', '').replace('\n', '')[:-6]
            topic_times = each_topic.find(
                'td', class_='last').get_text().replace(' ', '').replace('\n', '')
            news_res += '{}.{}({})'.format(
                topic_rank, topic_name, topic_times) + '\n'
    return news_res