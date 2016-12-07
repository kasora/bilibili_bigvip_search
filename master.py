#!/usr/bin/env python3
# -*- coding : utf-8 -*-

import time,queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support
import pymysql

user = "";
passwd = "";
db =  "";
userNumber = 70000000;


jump = 1000;

task_number = userNumber//jump;

task_queue = queue.Queue(task_number);
result_queue = queue.Queue(task_number);

lastSet = set(range(task_number));

def gettask():
    return task_queue;
def getresult():
     return result_queue;
 
def test():
    BaseManager.register('get_task',callable = gettask);
    BaseManager.register('get_result',callable = getresult);
    manager = BaseManager(address = ('0.0.0.0',5011),authkey = b'kasora');

    manager.start();

    task = manager.get_task();
    result = manager.get_result();


    for i in range(task_number):
        task.put(i);

    while(len(lastSet)>0):
        time.sleep(60);
        print(str(len(lastSet))+" left")
        conn = pymysql.connect(host="127.0.0.1",user=user,passwd=passwd,db=db,use_unicode=True, charset="utf8")
        cur = conn.cursor()
        for i in range(result.qsize()):
            ans = result.get();
            try:
                lastSet.remove(int(ans[0]));
            except KeyError:
                continue;
            if(len(ans[1])==0):
                pass;
            else:
                for userinfo in ans[1]:
                    insertsql = 'insert into vipuserinfo (uid, ulevel) values (%s, %s)';
                    cur.execute(insertsql, [userinfo["uid"], userinfo["level"]]);
                    conn.commit();
        cur.close()
        conn.close()
        if(task.empty() and len(lastSet)>0):
            for i in lastSet:
                task.put(i);
    time.sleep(1);

    manager.shutdown();
        
if __name__ == '__main__':
    freeze_support()
    test();
