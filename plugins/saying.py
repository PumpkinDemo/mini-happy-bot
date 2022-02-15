import requests
import datetime
import random
import os
from nonebot import MessageSegment
from nonebot import on_command, CommandSession


SAYING_DIR = './sayings'
SAYING_ABS_PATH = '/data/sayings'

alias = {
    'ccgg': 'cc',
    'xyjj': 'xy',
    '雪妖': 'xy',
}


def saying_alias_handle(name):
    return alias.get(name, name)


def get_file_contents(file):
    if not os.path.exists(file):
        os.system(f'touch {file}')
    with open(file, 'r') as f:
        content = f.read()
    return content


def save_saying(img_url, name=None):
    r = requests.get(img_url)
    ext = r.headers['Content-Type'].split('image/')[-1]
    t = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S_%f')
    img_name = f'{t}.{ext}'
    if name:
        img_name = f'{name}_' + img_name
    with open(f'{SAYING_DIR}/{img_name}', 'wb') as f:
        f.write(r.content)


def get_random_saying(name=None):
    files = os.listdir(SAYING_ABS_PATH)
    if name:
        files = [f for f in files if f.startswith(name+'_')]
    if not len(files):
        return None
    img = random.choice(files)
    return f'file://{SAYING_ABS_PATH}/{img}'


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
        for url in sayings:
            save_saying(url)
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
    real_name = saying_alias_handle(name)
    if not len(sayings):
        saying = get_random_saying(real_name)
        errmsg = f'no saying labeled for {name} currently'
        msg = MessageSegment.image(saying) if saying else errmsg
    else:
        for url in sayings:
            save_saying(url, real_name)
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
