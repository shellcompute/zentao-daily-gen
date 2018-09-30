'''
@File: zentao-daily-gen.py
@Author: leon.li(l2m2lq@gmail.com)
@Date: 2018-09-27 22:43:03
@Last Modified By: leon.li(l2m2lq@gmail.com>)
@Last Modified Time: 2018-09-28 23:33:43
'''

import argparse
import configparser
import os
import sys
import pymysql
import datetime
import itertools
import decimal
import smtplib
from email.mime.text import MIMEText
from email.header import Header

__version__ = '0.3'

class ZentaoDialyGen:
  def __init__(self, cfg_filename):
    conf = configparser.ConfigParser()
    conf.read(cfg_filename)
    self._zentao_url = conf.get('zentao', 'url')
    self._mysql_host = conf.get('zentao_db', 'host')
    self._mysql_port = int(conf.get('zentao_db', 'port'))
    self._mysql_user = conf.get('zentao_db', 'user')
    self._mysql_passwd = conf.get('zentao_db', 'password')
    self._dialy_users = ["'"+i+"'" for i in conf.get('daily', 'users').split(',')]
    self._dialy_to_mails = conf.get('daily', 'to_mails')
    self._dialy_cc_mails = conf.get('daily', 'cc_mails')
    self._daily_bcc_mails = conf.get('daily', 'bcc_mails')
    self._mail_user = conf.get('core', 'mail_user')
    self._mail_host = conf.get('core', 'mail_host')
    self._mail_passwd = conf.get('core', 'mail_password')
    self._today = datetime.datetime.today().strftime('%Y-%m-%d')

  def _get_daily_log(self):
    daily_lines = []
    daily_lines.append("""
    <p>This Below Daily Logs is auto-generated by Zentao Dialy Generator {version}.<br />
    Triggered every night at 23:45.<br />
    Please contact Leon(l2m2lq@gmail.com) if you have any questions. <br /></p>
    """.format(version=__version__))
    # Connect to the database
    print("Connect to the database...")
    conn = pymysql.connect(host=self._mysql_host,
                           port=self._mysql_port,
                           user=self._mysql_user,
                           password=self._mysql_passwd,
                           db='zentao',
                           cursorclass=pymysql.cursors.DictCursor)                      
    
    try:
      with conn.cursor() as cursor:
        sql = """
        SELECT A.realname, A.account, B.task, C.name AS task_title,
        B.consumed, C.fromBug
        FROM zt_user AS A
        LEFT JOIN (
          SELECT * FROM zt_taskestimate
          WHERE date = '{date}' AND consumed > 0
        ) B
        ON A.account = B.account
        LEFT JOIN zt_task AS C
        ON B.task = C.id
        WHERE A.account IN ({users})
        ORDER BY A.account, B.task
        """
        sql = sql.format(users=','.join(self._dialy_users), date=self._today)
        cursor.execute(sql)
        rs = cursor.fetchall()
        print("records count: ", len(rs))
        for key, group in itertools.groupby(rs, key=lambda x: x['account']):
          detail = list(group)
          daily_lines.append('<b>{name}{account}</b>'.format(name=detail[0]['realname'], account=key))
          num = 'a'
          for i in detail:
            if not i['consumed']:
              daily_lines.append('无')
              continue
            flag = str()
            if i['fromBug'] == 0:
              url = '{url}/zentao/task-view-{taskId}.html'.format(url=self._zentao_url, taskId=i['task'])
              flag = '<a href={url}><span style="color:#2ECC40">task</span></a>'.format(url=url)
            else:
              url = '{url}/zentao/bug-view-{bugId}.html'.format(url=self._zentao_url, bugId=i['fromBug'])
              flag = '<a href={url}><span style="color:#39CCCC">bug</span></a>'.format(url=url)
            line = '{num}). [{consumed} 小时]{flag} {task}.'.format(
              num=num, 
              consumed=decimal.Decimal(i['consumed']), 
              flag=flag,
              task=i['task_title'])
            daily_lines.append(line)
            num = chr(ord(num) + 1)
          daily_lines.append('')
    finally:
      conn.close()
    return '<br />'.join(daily_lines)

  def _addresses(self, addrstring):
    """Split in comma, strip surrounding whitespace."""
    return [x.strip() for x in addrstring.split(',')]

  def gen_daily(self):
    daily_log = self._get_daily_log()
    subject = 'Zentao Dialy {today}'.format(today=self._today)
    message = MIMEText(daily_log, 'html', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = self._mail_user
    message['To'] = self._dialy_to_mails
    message['Cc'] = self._dialy_cc_mails
    message['Bcc'] = self._daily_bcc_mails
    try:
      smtp = smtplib.SMTP_SSL(self._mail_host)
      print("connect to SMTP server...")
      conn_code, conn_msg  = smtp.connect(self._mail_host, 465)
      if conn_code != 220:
        print("SMTP connect reply code: {code}, message: {msg}".format(code=conn_code, msg=conn_msg))
        return False
      print("login in SMTP server...")
      smtp.login(self._mail_user, self._mail_passwd)
      smtp.sendmail(
        self._mail_user, 
        self._addresses(self._dialy_to_mails) + self._addresses(self._dialy_cc_mails) + self._addresses(self._daily_bcc_mails), 
        message.as_string()
      )
      smtp.quit()
      return True
    except smtplib.SMTPException as e:
      print(e)
    except Exception as e:
      print("Unexpected error:", e)
    return False

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Zentao Dialy Generator')
  parser.add_argument('--version', '-v', action='version', version='%(prog)s ' + __version__)
  parser.add_argument('--config', '-c', type=str, required=False, help='config file', metavar='config.ini')
  args = vars(parser.parse_args())
  cfg_filename = args['config']
  if not cfg_filename:
    print('using config.ini in current directory.')
    cfg_filename = 'config.ini'
  if not os.path.isfile(cfg_filename):
    print('{cfg} not found'.format(cfg=cfg_filename))
    sys.exit(1)
  gen = ZentaoDialyGen(cfg_filename)
  if not gen.gen_daily():
    print("generating daily failed.")
  else:
    print("generating daily done.")
  
  
