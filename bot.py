from random import random
from aiocqhttp import MessageSegment
import nonebot
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from sympy import im
import config
import os
import requests

from plugins.saying import has_saying
from plugins.setu import has_setu

# config = Config()

HOST = '127.0.0.1'
PORT = 5000


def get_bv_info(bv):
    api = 'api.bilibili.com/x/web-interface/view'
    query = f'https://{api}?bvid={bv}'
    res = requests.get(query).json()
    if res['code']:
        return None
    data = res['data']
    title = data['title']
    cover = data['pic']
    desc = data['desc']
    return title, cover, desc


def get_file_contents(file):
    if not os.path.exists(file):
        os.system(f'touch {file}')
    with open(file, 'r') as f:
        content = f.read()
    return content


@on_command('help', only_to_me=False)
async def help(session:CommandSession):
    await session.send('no help~')


@on_command('about', only_to_me=False)
async def about(session:CommandSession):
    msg = get_file_contents('./txts/about.txt')
    await session.send(msg)


@on_command('changelog', only_to_me=False)
async def changelog(session:CommandSession):
    msg = get_file_contents('./txts/changelog.txt')
    await session.send(msg)


@on_command('usage', only_to_me=False)
async def usage(session:CommandSession):
    msg = get_file_contents('./txts/usage.txt')
    await session.send(msg)


@on_command('sese', only_to_me=False)
async def sese(session:CommandSession):
    await session.send('不可以色色～')


@on_natural_language(keywords={'来点'}, only_to_me=False)
async def some(session:NLPSession):
    msg = session.msg_text.strip()
    if not msg.startswith('来点'):
        return
    key = msg.split('来点')[1]
    if not key:
        return
    if key in ['涩图', '色图', 'setu']:
        return IntentCommand(80.0, 'setu')
    if key in ['语录']:
        return IntentCommand(80.0, 'saying')
    if has_saying(key):
        return IntentCommand(80.0, 'sayingof', current_arg=key)
    if has_setu(key):
        return IntentCommand(80.0, 'setuof', current_arg=key)
    r = random()
    res = 'o(╯□╰)o'
    if r < 0.2:
        res = f'现在还没有"{key}"的涩图/语录哦～'
        # res = f'现在还没有"{key}"的语录哦～'
    elif r < 0.4:
        res = f'unknown keyword "{key}", 开摆～'
    await session.send(res)
    

# @on_command('bb', only_to_me=False)
async def label(session:CommandSession):
    print(session.event.message)
    print(session.event.message_id)


@on_command('bili', only_to_me=False)
async def bili(session:CommandSession):
    bv = session.current_arg_text.strip()
    res = get_bv_info(bv)
    if not res:
        msg = f'invalid BV number: {bv}'
    else:
        title, cover, desc = res
        url = f'https://www.bilibili.com/video/{bv}'
        msg = MessageSegment.share(url=url, title=title, content=desc, image_url=cover)
    await session.send(msg)


if __name__ == '__main__':
    nonebot.init(config_object=config)
    # nonebot.load_builtin_plugins()
    nonebot.load_plugin('plugins.saying')
    nonebot.load_plugin('plugins.setu')
    nonebot.run(host=HOST, port=PORT)
