Database
========

#### Software
MySQL 

#### Tables
VipUserInfo:

|Name|Type|Primary Key|Comments|
|----|----|-----------|--------|
|uid|VARCHAR(20)|FALSE| |
|ulevel|VARCHAR(20)|FALSE| |

#### SQL
```SQL
DROP TABLE IF EXISTS VipUserInfo;
CREATE TABLE VipUserInfo(
    uid INT(200) Primary Key,
    ulevel VARCHAR(200)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
