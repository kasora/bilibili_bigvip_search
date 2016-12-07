import pymysql

user = ""
passwd = ""
db =  ""

ans = {}

conn = pymysql.connect(host="127.0.0.1",user=user,passwd=passwd,db=db,use_unicode=True, charset="utf8")
cur = conn.cursor()

for i in range(7):
    countsql = 'select count(ulevel) from vipuserinfo where ulevel = %s';
    cur.execute(countsql, i);

    res = cur.fetchall()
    for row in res:
        ans[str(i)] = int(row[0])

cur.close()
conn.close()

allnum = sum([ans[i] for i in ans])

print('There are '+str(allnum)+' user is big vip.')
for i in range(7):
    si = str(i)
    print('level '+si+':'+str(ans[si])+'    '+str(ans[si]/allnum*100)+'%')
    
    
        

