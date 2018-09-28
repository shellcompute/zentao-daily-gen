# zentao-daily-gen
根据禅道数据自动生成日报、周报、月报，并发送到邮件列表。


### How to Use

```
python3 zentao-daily-gen.py -c config.ini
```
若不指定配置文件，默认使用当前目录下的config.ini
```
python3 zentao-daily-gen.py 
```

### 定时触发

用Linux自带的crontab
```
crontab -l 列出工作表里的命令 list user's crontab
crontab -e 编辑工作表 edit user's crontab
crontab -r 删除 delete user's crontab
```

crontab -e, 键入如下信息

每天23:35执行一次
```
35 23 * * * cd /data/zentao-daily-gen/ && /usr/bin/python3.6 /data/zentao-daily-gen/zentao-daily-gen.py >> /tmp/zentao-daily-gen.log
```


### 注意
- 连接MySQL需要安装[PyMySQL](https://pypi.org/project/PyMySQL/):
```
pip3 install pymysql
```


