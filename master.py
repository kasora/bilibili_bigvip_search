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
    manager = BaseManager(address=('0.0.0.0', SERVER_PORT), authkey=AUTHKEY)

    manager.start()

    task = manager.get_task()
    result = manager.get_result()
    lastset = set(range(TASK_NUMBER))


    for i in range(TASK_NUMBER):
        task.put(i)

    while len(lastset) > 0:
        time.sleep(60)
        print(str(len(lastset))+" left")
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
                    insertsql = 'insert into vipuserinfo (uid, ulevel) values (%s, %s)'
                    cur.execute(insertsql, [userinfo["uid"], userinfo["level"]])
                    conn.commit()
        cur.close()
        conn.close()
        if task.empty() and len(lastset) > 0:
            for i in lastset:
                task.put(i)
    time.sleep(1)

    manager.shutdown()

if __name__ == '__main__':
    freeze_support()
    startserver()
