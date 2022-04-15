from nonebot import scheduler
import nonebot
from datetime import datetime
import os
from aiocqhttp.exceptions import Error as CQHttpError

master_qqid = os.environ.get('MASTER_QQID')

# @scheduler.scheduled_job('cron', second='*/10')
async def test():
    bot = nonebot.get_bot()
    msg = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    try:
        await bot.send_private_msg(user_id=master_qqid, message=msg)
        print(master_qqid)
    except CQHttpError as e:
        print(e)


@scheduler.scheduled_job('cron', hour='8')
async def daily_report():
    msg = os.popen('./dailyreport.sh').read()
    bot = nonebot.get_bot()
    try:
        await bot.send_private_msg(user_id=master_qqid, message=msg)
        print(master_qqid)
    except CQHttpError as e:
        print(e)