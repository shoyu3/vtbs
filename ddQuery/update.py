import os
import json
import requests
from ddQuery import api
from apscheduler.schedulers.asyncio import AsyncIOScheduler

spath = os.path.split(__file__)[0]

def update_vtbs_info():
    r = api.get_vtb_info()
    if r == None:
        return
    with open(f'{spath}/data/vtb_data_simple.json', 'w', encoding = 'utf8') as fp:
        fp.write(r)
    
def start_update():
    update_vtbs_info()
    scheduler_vtb = AsyncIOScheduler({'apscheduler.timezone': 'UTC'})
    scheduler_vtb.add_job(update_vtbs_info, 'interval', seconds = 3600)
    scheduler_vtb.start()
