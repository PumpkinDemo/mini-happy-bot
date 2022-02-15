from audioop import alaw2lin
import os
import random
from nonebot import CommandSession, on_command
from nonebot import MessageSegment
import requests
import datetime
import yaml
from hashlib import md5


SETU_DIR = './setu'
SETU_ABS_PATH = '/data/setu'
SETU_ALIAS_PATH = './setu_alias.txt'

alias = {}
alias_file_md5 = ''


def get_setu_alias():
    alias_path = './setu_alias.yml'
    if not os.path.exists(alias_path):
        os.system(f'touch {alias_path}')
    with open(alias_path, 'rb') as f:
        h = md5(f.read()).hexdigest()
    if h == alias_file_md5:
        return
    globals()['alias_file_md5'] = h
    alias.clear()
    with open(alias_path, 'r') as f:
        data = yaml.safe_load(f)
        for k in data.keys():
            for v in data[k]:
                alias[v] = k
    print('alias update')
    return


def get_random_setu(name=None):
    files = os.listdir(SETU_DIR)
    if name:
        files = list(filter(lambda f:f.startswith(name+'_'), files))
    if not len(files):
        return None
    img = random.choice(files)
    return f'file://{SETU_ABS_PATH}/{img}'


def save_setu(img_url, name=None):
    r = requests.get(img_url)
    ext = r.headers['Content-Type'].split('image/')[-1]
    t = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S_%f')
    setu_name = f'{t}.{ext}'
    if name:
        setu_name = f'{name}_' + setu_name
    with open(f'{SETU_DIR}/{setu_name}', 'wb') as f:
        f.write(r.content)


def name_check(name:str) -> bool:
    if ' ' in name:
        return False
    if '/' in name:
        return False
    return True


def setu_alias_handle(name:str):
    get_setu_alias()
    return alias.get(name, name)


@on_command('setupost', only_to_me=False)
async def setupost(session:CommandSession):
    images = session.current_arg_images
    if not len(images):
        await session.send('no image')
        return
    for img_url in images:
        save_setu(img_url)
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
        for url in images:
            save_setu(url)
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
    
    setus = session.current_arg_images
    real_name = setu_alias_handle(name)
    if not len(setus):
        setu = get_random_setu(real_name)
        errmsg = f'no setu labeled for {name} currently'
        msg = MessageSegment.image(setu) if setu else errmsg
    else:
        for url in setus:
            save_setu(url, real_name)
        msg = f'setu of {name} received'
    await session.send(msg)
