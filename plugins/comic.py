import os
from nonebot import on_command, CommandSession
from nonebot import MessageSegment
from typing import List
from requests import Session
import datetime
import random

COMIC_PATH = '/data/comics'

def get_random_comic():
    files = os.listdir(COMIC_PATH)
    if not len(files):
        return None
    img = random.choice(files)
    return f'file://{COMIC_PATH}/{img}'

def save_comics(urls:List[str]):
    s = Session()
    cnt = 0
    for url in urls:
        r = s.get(url)
        ext = r.headers['Content-Type'].split('image/')[-1]
        t = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S_%f')
        img_name = f'{t}.{ext}'
        with open(f'{COMIC_PATH}/{img_name}', 'wb') as f:
            f.write(r.content)
        cnt += 1
    return cnt

@on_command('comic', only_to_me=False)
async def comic(session:CommandSession):
    imgs = session.current_arg_images
    if not imgs:
        msg = MessageSegment.image(get_random_comic())
    else:
        cnt = save_comics(imgs)
        msg = f'{cnt} { "comics" if cnt > 1 else "comic" } received'
    await session.send(msg)