#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# task.py for windows

import time, sys, queue, random, requests, json, threading
from multiprocessing.managers import BaseManager


serverSite = ''


BaseManager.register('get_task');
BaseManager.register('get_result');

lock = threading.Lock()
conn = BaseManager(address = (serverSite,5011), authkey = b'kasora');
vipurl = "http://space.bilibili.com/ajax/member/getVipStatus";
levelurl = "http://space.bilibili.com/ajax/member/GetInfo";
head = {'Referer':'http://space.bilibili.com'};
jump = 1000;

ansl = [];

def getvip(uid):
    params = {"mid":uid}
    r = requests.get(vipurl,params = {"mid":uid},headers = head);
    try:
        info = json.loads(r.text);
    except:
        print("I'm killed. retrying...")
        return False;
    try:
        viptype = info["data"]["vipType"];
    except:
        return True;
    if(viptype==2):        
        r = requests.post(levelurl,data = params,headers = head);
        info = json.loads(r.text);
        level = info["data"]["level_info"]["current_level"];
        lock.acquire()
        ansl.append({"uid":uid,"level":level})
        lock.release()
    return True

def getvips(startid):
    lid = startid*jump;  
    for i in range(lid,lid+jump):
        try:
            if(not getvip(i)):
                return False;
        except:
            pass;
    return True;
            
def main():
    try:
        conn.connect();
        print("Connection succeeded.")
    except:
        print('Connection failed...retrying...');
        time.sleep(5);
        main();
        return;

    task = conn.get_task();
    result = conn.get_result();

    while not task.empty():
        n = task.get(timeout = 5);
        print('deal with '+str(n*jump)+' to '+str((n+1)*jump))
        ansl.clear()
        while(not getvips(n)):
            pass;
        rt = (n, ansl);
        result.put(rt);
        print('finish it.')
        
    print("finished all.")
    return;

if __name__ == '__main__':
    main();
