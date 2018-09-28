# 用Linux自带的crontab实现定时任务

# Step 1: 
# 写入crontab命令到/etc/crontab
# 1、每分钟执行一次 
# * * * * * user command
# 2、每隔2小时执行一次 
# * */2 * * * user command (/表示频率)
# 3、每天8:30分执行一次
# 30 8 * * * user command
# 4、每小时的30和50分各执行一次 
# 30,50 * * * * user command（,表示并列）
# 4、每个月的3号到6号的8:30执行一次
# 30 8 3-6 * * user command （-表示范围）
# 5、每个星期一的8:30执行一次
# 30 8 * * 1 user command （周的范围为0-7,0和7代表周日）

echo "* * * * * root /usr/bin/python3.6 /data/zentao-daily-gen/zentao-daily-gen.py > /tmp/zentao-daily-gen.log" >> /etc/crontab