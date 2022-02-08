import requests
import datetime
import random
import os
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot import MessageSegment


SAYING_DIR = './sayings'
SAYING_ABS_PATH = '/data/sayings'

alias = {
    'ccgg': 'cc',
}


def get_file_contents(file):
    if not os.path.exists(file):
        os.system(f'touch {file}')
    with open(file, 'r') as f:
        content = f.read()
    return content


def save_image(path, image_url):
    r = requests.get(image_url)
    ext = r.headers['Content-Type'].split('image/')[-1]
    t = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S_%f')
    with open(f'{path}/{t}.{ext}', 'wb') as f:
        f.write(r.content)


def save_saying_of(name, img_url):
    r = requests.get(img_url)
    ext = r.headers['Content-Type'].split('image/')[-1]
    t = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S_%f')
    with open(f'{SAYING_DIR}/{name}_{t}.{ext}', 'wb') as f:
        f.write(r.content)


def get_random_saying():
    files = os.listdir('./sayings')
    img = random.choice(files)
    return f'file://{SAYING_ABS_PATH}/{img}'


def get_random_saying_of(name):
    files = os.listdir('./sayings')
    files = [f for f in files if f.startswith(name+'_')]
    if not len(files):
        return None
    img = random.choice(files)
    return f'file://{SAYING_ABS_PATH}/{img}'


def has_saying(name:str) -> bool:
    if name in alias.keys():
        name = alias[name]
    if get_random_saying_of(name):
        return True
    return False


def name_check(name:str) -> bool:
    if ' ' in name:
        return False
    if '/' in name:
        return False
    return True


@on_command('saying', only_to_me=False)
async def saying(session:CommandSession):
    sayings = session.current_arg_images
    if not len(sayings):
        saying = get_random_saying()
        msg = MessageSegment.image(saying)
    else:
        for s in sayings:
            save_image(SAYING_DIR, s)
        msg = 'saying received'
    await session.send(msg)


@on_command('sayingof', only_to_me=False)
async def sayingof(session:CommandSession):
    name = session.current_arg_text.strip()
    if len(name) == 0:
        await session.send('name required')
        return
    if not name_check(name):
        await session.send('invaliad name')
        return
    sayings = session.current_arg_images
    if not len(sayings):
        if name in alias.keys():
            name = alias[name]
        saying = get_random_saying_of(name)
        if not saying:
            msg = f'no saying labeled for {name} currently'
        else:
            msg = MessageSegment.image(saying)
    else:
        for s in sayings:
            save_saying_of(name, s)
        msg = f'saying of {name} received'
    await session.send(msg)


# @on_command('spsaying')
async def special(session:CommandSession):
    try:
        key = int(session.current_arg_text.strip())
        table = get_file_contents('saying_table.txt').split('\n')
        table = list(map(lambda s: s.split(',')[0].strip(), table))
        if key >= len(table):
            return
        img = table[key]
        path = f'file://{SAYING_ABS_PATH}/{img}'
        msg = MessageSegment.image(path)
        await session.send(msg)
    except Exception as e:
        print(e)
        return
