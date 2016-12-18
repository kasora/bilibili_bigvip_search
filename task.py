#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# task.py for windows

"""
start this script in any terminal you want
it will send requests to bilibili and send
the result to master.py
"""

import time
import json
from multiprocessing.managers import BaseManager
import requests
import config

SERVER_SITE = config.MASTER['server_site']
SERVER_PORT = config.MASTER['server_port']
AUTHKEY = config.MASTER['authkey']

BaseManager.register('get_task')
BaseManager.register('get_result')

INTERVAL = config.BILIBILI['interval']

ansl = []

def getvip(uid):

    """ get the data of user:uid """

    vipurl = "http://space.bilibili.com/ajax/member/getVipStatus"
    levelurl = "http://space.bilibili.com/ajax/member/GetInfo"
    head = {'Referer':'http://space.bilibili.com'}

    params = {"mid":uid}
    res = requests.get(vipurl, params={"mid":uid}, headers=head)
    try:
        info = json.loads(res.text)
    except:
        print("I'm killed. retrying...")
        return False
    try:
        viptype = info["data"]["vipType"]
    except:
        return True
    if viptype == 2:
        res = requests.post(levelurl, data=params, headers=head)
        info = json.loads(res.text)
        level = info["data"]["level_info"]["current_level"]
        ansl.append({"uid":uid, "level":level})
    return True

def getvips(startid):

    """ get the data of user id from startid to startid + interval """

    lid = startid*INTERVAL
    for i in range(lid, lid+INTERVAL):
        try:
            if not getvip(i):
                return False
        except:
            pass
    return True

def main():

    """ start a task """

    conn = BaseManager(address=(SERVER_SITE, SERVER_PORT), authkey=AUTHKEY)
    try:
        conn.connect()
        print("Connection succeeded.")
    except:
        print('Connection failed...retrying...')
        time.sleep(5)
        main()
        return

    task = conn.get_task()
    result = conn.get_result()

    while not task.empty():
        startid = task.get(timeout=5)
        print('deal with '+str(startid*INTERVAL)+' to '+str((startid+1)*INTERVAL))
        ansl.clear()
        while not getvips(startid):
            pass
        res = (startid, ansl)
        result.put(res)
        print('finish it.')

    print("finished all.")
    return

if __name__ == '__main__':
    main()
