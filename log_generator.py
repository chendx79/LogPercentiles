#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ConfigParser
import os
import datetime

def gen_dates(base_date, days):
    day = datetime.timedelta(days = 1)
    for i in range(days):
        yield base_date + day * i

#10.2.3.4 [2018/13/10:14:02:39] "GET /api/playeritems?playerId=3" 200 1230
#10.3.4.5 [2018/13/10:14:02:41] "GET /api/playeritems?playerId=2" 200 4630
def generate_log(dir, ext, start_date, end_date):
    """
    生成日志
    :dir: 日志目录
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return:
    """
    for date in gen_dates(start_date, (end_date - start_date).days + 1):
       print date.strftime('%Y-%m-%d')
    return

####################################
#1. create directory if not exist
#2. create log file
####################################

def main():
    config = ConfigParser.ConfigParser()
    with open("logper.cfg", "r") as cfgfile:
        config.readfp(cfgfile)

        for section in config.sections():
            dir = config.get(section, "dir")
            ext = config.get(section, "ext")
            start_date = datetime.datetime.strptime(config.get(section, "start_date"), '%Y-%m-%d')
            end_date = datetime.datetime.strptime(config.get(section, "end_date"), '%Y-%m-%d')

            if not os.path.exists(dir):
                os.makedirs(dir)
            
            generate_log(dir, ext, start_date, end_date)

if __name__ == '__main__':
    main()
