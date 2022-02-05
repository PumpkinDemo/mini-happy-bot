import nonebot
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import config
import os

from plugins.saying import has_saying

# config = Config()

HOST = '127.0.0.1'
PORT = 5000


def get_file_contents(file):
    if not os.path.exists(file):
        os.system(f'touch {file}')
    with open(file, 'r') as f:
        content = f.read()
    return content


@on_command('help', only_to_me=False)
async def help(session:CommandSession):
    await session.send('no help~ :)')


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
    if key in ['涩图']:
        return IntentCommand(80.0, 'setu')
    if key in ['语录']:
        return IntentCommand(80.0, 'saying')
    if has_saying(key):
        return IntentCommand(80.0, 'sayingof', current_arg=key)
    await session.send(f'unrecognized keyword: {key}')
    


if __name__ == '__main__':
    nonebot.init(config_object=config)
    # nonebot.load_builtin_plugins()
    nonebot.load_plugin('plugins.saying')
    nonebot.load_plugin('plugins.setu')
    nonebot.run(host=HOST, port=PORT)
