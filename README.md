# zentao-daily-gen
根据禅道数据自动生成日报、周报、月报，并发送到邮件列表。

---

原本想用爬虫爬网页数据，后来想想是有病，直接玩禅道的数据库不就得了。


### How to Use

```
python3 zentao-daily-gen.py -c config.ini
```
若不指定配置文件，默认使用当前目录下的config.ini
```
python3 zentao-daily-gen.py 
```

### 注意
- 连接MySQL需要安装[PyMySQL](https://pypi.org/project/PyMySQL/):
```
pip3 install pymysql
```


