from random import random
from aiocqhttp import MessageSegment
import nonebot
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import config
import os
import requests
from plugins.saying import get_random_saying, saying_alias_resolve
from plugins.setu import get_random_setu, setu_name_resolve
from pypinyin import lazy_pinyin, Style
from dotenv import load_dotenv


# config = Config()

HOST = '127.0.0.1'
PORT = 6000

keyword_cnt = {}


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


@on_natural_language(keywords={'色色'}, only_to_me=False)
async def sese_nlp(session:NLPSession):
    return IntentCommand(100*random(), 'sese')



@on_natural_language(keywords={'来点'}, only_to_me=False)
async def some(session:NLPSession):
    msg = session.msg_text.strip()
    if not msg.startswith('来点'):
        return
    key = msg.split('来点')[1]
    if not key:
        await session.send('来点啥?')
        return
    
    # keyword_cnt[key] = keyword_cnt.get(key, 0) + 1
    
    key_pinyin = ''.join(lazy_pinyin(key, style=Style.NORMAL))

    if key_pinyin == 'sese':
        return IntentCommand(80.0, 'sese')
    if key_pinyin == 'setu':
        return IntentCommand(80.0, 'setu')
    if key in ['语录', 'saying']:
        return IntentCommand(80.0, 'saying')
    if key in ['comic', '漫画']:
        return IntentCommand(80.0, 'comic')
    if key in ['老婆', '老公']:
        await session.send('醒醒，你没' + key)
        return
    # if key in ['矮子']:
        # await session.send('不敬仙师!')
        # return

    saying = get_random_saying(saying_alias_resolve(key))
    if saying:
        await session.send(MessageSegment.image(saying))
        return
    
    setu = get_random_setu(setu_name_resolve(key))
    if setu:
        await session.send(MessageSegment.image(setu))
        return
    
    r = random()
    res = 'o(╯□╰)o'
    if r < 0.2:
        res = f'现在还没有"{key}"的涩图/语录哦～'
    elif r < 0.4:
        res = f'unknown keyword "{key}", 开摆～'
    await session.send(res)
    


# @on_command('bb', only_to_me=False)
async def label(session:CommandSession):
    print(session.event.message)
    print(session.event.message_id)


# @on_command('bili', only_to_me=False)
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
    load_dotenv()
    nonebot.init(config_object=config)
    # nonebot.load_builtin_plugins()
    nonebot.load_plugin('plugins.saying')
    nonebot.load_plugin('plugins.setu')
    nonebot.load_plugin('plugins.comic')
    nonebot.load_plugin('plugins.cron')
    nonebot.run(host=HOST, port=PORT)


