import os
import random
from nonebot import CommandSession, on_command
from nonebot import MessageSegment
import requests
import datetime


SETU_DIR = './setu'
SETU_ABS_PATH = '/data/setu'
SETU_ALIAS_PATH = './setu_alias.txt'


aliases = {
    '甘雨': 'ganyu',
    '申鹤': 'shenhe',
    '神里': 'ayaka',
}

def get_setu_alias():
    file = './setu_alias.txt'
    if not os.path.exists(file):
        os.system(f'touch {file}')
    with open(file, 'r') as f:
        content = f.read()
    lines = content.splitlines()
    res = {}
    for ln in lines:
        tup = ln.strip().split()
        if len(tup) != 2:
            continue
        res[tup[0]] = tup[1]
    return res


def save_image(path, image_url):
    r = requests.get(image_url)
    ext = r.headers['Content-Type'].split('image/')[-1]
    t = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S_%f')
    with open(f'{path}/{t}.{ext}', 'wb') as f:
        f.write(r.content)


def get_random_setu():
    files = os.listdir(SETU_DIR)
    img = random.choice(files)
    return f'file://{SETU_ABS_PATH}/{img}'


def save_setu_of(name, img_url):
    r = requests.get(img_url)
    ext = r.headers['Content-Type'].split('image/')[-1]
    t = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S_%f')
    with open(f'{SETU_DIR}/{name}_{t}.{ext}', 'wb') as f:
        f.write(r.content)


def get_random_setu_of(name):
    files = os.listdir(SETU_DIR)
    files = [f for f in files if f.startswith(name+'_')]
    if not len(files):
        return None
    img = random.choice(files)
    return f'file://{SETU_ABS_PATH}/{img}'


def name_check(name:str) -> bool:
    if ' ' in name:
        return False
    if '/' in name:
        return False
    return True


def has_setu(name:str) -> bool:
    alias = get_setu_alias()
    if name in alias.keys():
        name = alias[name]
    if get_random_setu_of(name):
        return True
    return False


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


@on_command('setuof', only_to_me=False)
async def setuof(session:CommandSession):
    name = session.current_arg_text.strip()
    if len(name) == 0:
        await session.send('name required')
        return
    if not name_check(name):
        await session.send('invaliad name')
        return
    
    alias = get_setu_alias()
    if name in alias.keys():
        name = alias[name]
    setus = session.current_arg_images
    if not len(setus):
        setu = get_random_setu_of(name)
        if not setu:
            msg = f'no setu labeled for {name} currently'
            msg += '\nfunction in building...'
        else:
            msg = MessageSegment.image(setu)
    else:
        for s in setus:
            save_setu_of(name, s)
        msg = f'setu of {name} received'
    await session.send(msg)
