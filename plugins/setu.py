import os
import random
from nonebot import CommandSession, on_command
from nonebot import MessageSegment
import requests
import datetime


SETU_DIR = './setu'
SETU_ABS_PATH = '/data/setu'


def save_image(path, image_url):
    r = requests.get(image_url)
    ext = r.headers['Content-Type'].split('image/')[-1]
    t = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S_%f')
    with open(f'{path}/{t}.{ext}', 'wb') as f:
        f.write(r.content)


def get_random_setu():
    # setu_abs_path = '/data/setu'
    files = os.listdir('./setu')
    img = random.choice(files)
    return f'file://{SETU_ABS_PATH}/{img}'


@on_command('setupost', only_to_me=False)
async def setupost(session:CommandSession):
    images = session.current_arg_images
    if not len(images):
        await session.send('no image')
        return
    for img in images:
        print(img)
        save_image(img)
    await session.send('saved')


@on_command('setuget', only_to_me=False)
async def setupost(session:CommandSession):
    img = get_random_setu()
    msg = MessageSegment.image(img)
    await session.send(msg)
    

@on_command('setu', only_to_me=False)
async def setu(session:CommandSession):
    images = session.current_arg_images
    if not len(images):
        img = get_random_setu()
        msg = MessageSegment.image(img)
    else:
        for img in images:
            save_image(SETU_DIR, img)
        msg = 'setu received'
    await session.send(msg)
