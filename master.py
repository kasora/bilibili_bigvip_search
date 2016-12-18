#!/usr/bin/env python3
# -*- coding : utf-8 -*-

' It will be set in server. '

from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support
import time
import queue
import pymysql
import config

USER = config.DATABASE['user']
PASSWD = config.DATABASE['password']
DBNAME = config.DATABASE['name']

SERVER_PORT = config.MASTER['server_port']
AUTHKEY = config.MASTER['authkey']
LOCALHOST = config.MASTER['localhost']

USER_NUMBER = config.BILIBILI['usernumber']
INTERVAL = config.BILIBILI['interval']
TASK_NUMBER = USER_NUMBER//INTERVAL

_task_queue = queue.Queue(TASK_NUMBER)
_result_queue = queue.Queue(TASK_NUMBER)

def _gettask():
    return _task_queue

def _getresult():
    return _result_queue

def startserver():

    """start the server"""

    BaseManager.register('get_task', callable=_gettask)
    BaseManager.register('get_result', callable=_getresult)
    manager = BaseManager(address=(LOCALHOST, SERVER_PORT), authkey=AUTHKEY)

    manager.start()

    task = manager.get_task()
    result = manager.get_result()
    lastset = set(range(TASK_NUMBER))


    for i in range(TASK_NUMBER):
        task.put(i)

    print('Tasks is ready.')

    while len(lastset) > 0:
        time.sleep(20)
        conn = pymysql.connect(
            host="127.0.0.1",
            user=USER,
            passwd=PASSWD,
            db=DBNAME,
            use_unicode=True,
            charset="utf8"
        )
        cur = conn.cursor()
        for i in range(result.qsize()):
            ans = result.get()
            try:
                lastset.remove(int(ans[0]))
            except KeyError:
                continue
            if len(ans[1]) == 0:
                pass
            else:
                for userinfo in ans[1]:
                    try:
                        insertsql = 'insert into vipuserinfo (uid, ulevel) values (%s, %s)'
                        cur.execute(insertsql, [userinfo["uid"], userinfo["level"]])
                        conn.commit()
                    except:
                        pass
        cur.close()
        conn.close()
        print(str(len(lastset))+" left")
        if task.empty() and len(lastset) > 0:
            print('Start another task.py please. Some work isn\'t finished.')
            for i in lastset:
                task.put(i)
    time.sleep(1)
    print('Finished it.')
    manager.shutdown()

if __name__ == '__main__':
    freeze_support()
    startserver()
