'''
@File: zentao-weekly-report.py
@Author: leon.li(l2m2lq@gmail.com)
@Date: 2019-01-16 13:34:14
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

__version__ = '0.5'

class ZentaoWeeklyReport:
  """
  用于协助项目组进行工时统计
  1. 统计上周的工时情况
  2. 以Excel的方式邮件发送给具体人
  """

  def __init__(self, cfg_filename):
    conf = configparser.ConfigParser()
    conf.read(cfg_filename)
    self._zentao_url = conf.get('zentao', 'url')
    self._mysql_host = conf.get('zentao_db', 'host')
    self._mysql_port = int(conf.get('zentao_db', 'port'))
    self._mysql_user = conf.get('zentao_db', 'user')
    self._mysql_passwd = conf.get('zentao_db', 'password')
    self._weekly_report_users = ["'"+i+"'" for i in conf.get('weekly_report', 'users').split(',')]
    self._weekly_report_to_mails = [x.strip() for x in conf.get('weekly_report', 'to_mails').split(',') if x.strip() != '']
    if conf.has_option('weekly_report', 'cc_mails'):
      self._weekly_report_cc_mails = [x.strip() for x in conf.get('weekly_report', 'cc_mails').split(',') if x.strip() != '']
    if conf.has_option('weekly_report', 'bcc_mails'):
      self._weekly_report_bcc_mails = [x.strip() for x in conf.get('weekly_report', 'bcc_mails').split(',') if x.strip() != '']
    self._mail_user = conf.get('core', 'mail_user')
    self._mail_host = conf.get('core', 'mail_host')
    self._mail_passwd = conf.get('core', 'mail_password')

  def _previous_week_range(self, date):
    """
    获取上周的起始日期和结束日期 
    """
    start_date = date + datetime.timedelta(-date.weekday(), weeks=-1)
    end_date = date + datetime.timedelta(-date.weekday() - 1)
    return start_date, end_date

  def _get_weekly_detail_data(self):
    sql = """
      SELECT A.task AS task_id, 
      C.name AS sprint_title, 
      D.name AS module_title, 
      B.name AS task_title, 
      B.story,
      B.finishedBy,
      B.closedBy,
      B.finishedDate,
      B.closedDate,
      B.estimate,
      A.consumed, B.left
      FROM (
        SELECT task, account, ROUND(SUM(consumed),1) AS consumed
        FROM zt_taskestimate
        WHERE date >= '{start_date}' AND date <= '{end_date}'
        AND account IN ({users}) 
        GROUP BY task, account 
      ) A
      LEFT JOIN zt_task B ON A.task = B.id
      LEFT JOIN zt_project C ON B.project = C.id
      LEFT JOIN zt_module D ON B.module = D.id
      ORDER BY A.task ASC
      """
    start_date, end_date = self._previous_week_range(datetime.date.today())
    sql = sql.format(users=','.join(self._weekly_report_users), start_date=start_date, end_date=end_date)

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
        cursor.execute(sql)
        rs = cursor.fetchall()
    finally:
      conn.close()
    return rs

  def _get_weekly_report_data(self):
    pass

  def gen_weekly_report(self):
    detail_data = self._get_weekly_detail_data()
    print(detail_data)
    return True

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
  gen = ZentaoWeeklyReport(cfg_filename)
  if not gen.gen_weekly_report():
    print("generating daily failed.")
  else:
    print("generating daily done.")
