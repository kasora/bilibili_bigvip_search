Database
========

#### Software
MySQL 

#### Tables
VipUserInfo:

|Name|Type|Primary Key|Comments|
|----|----|-----------|--------|
|uid|INT(200)|TRUE| |
|ulevel|VARCHAR(200)|FALSE| |

#### SQL
```SQL
DROP TABLE IF EXISTS VipUserInfo;
CREATE TABLE VipUserInfo(
    uid INT(200) Primary Key,
    ulevel VARCHAR(200)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
