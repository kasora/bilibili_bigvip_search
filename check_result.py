#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" you can use this script to check the result """

import pymysql
import config

USER = config.DATABASE['user']
PASSWD = config.DATABASE['password']
DBNAME = config.DATABASE['name']

def getresult():

    """
    It will print the percent of bigvip in each level.
    It also return a dict of the user number of each level.
    """

    ans = {}
    conn = pymysql.connect(
        host="127.0.0.1",
        user=USER,
        passwd=PASSWD,
        db=DBNAME,
        use_unicode=True,
        charset="utf8"
    )
    cur = conn.cursor()

    for i in range(7):
        countsql = 'select count(ulevel) from vipuserinfo where ulevel = %s'
        cur.execute(countsql, i)

        res = cur.fetchall()
        for row in res:
            ans[str(i)] = int(row[0])

    cur.close()
    conn.close()

    allnum = sum([ans[i] for i in ans])

    print('There are '+str(allnum)+' user is big vip.')
    for i in range(7):
        _si = str(i)
        print('level '+_si+':'+str(ans[_si])+'    '+str(ans[_si]/allnum*100)+'%')
    return ans

if __name__ == '__main__':
    getresult()
