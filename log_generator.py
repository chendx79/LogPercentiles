#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ConfigParser
import os
import datetime
import random

def gen_dates(base_date, days):
    """
    Generate days list
    :param base_date: start date
    :param days: how many days to generate the list
    :return: days list
    """
    day = datetime.timedelta(days = 1)
    for i in range(days):
        yield base_date + day * i

def generate_log(dir, start_date, end_date, ip_addr, http_verb_uri_collect, http_verb_uri_other, per_200, resp_time_90, resp_time_95, resp_time_99):
    """
    Generate logs
    :param dir: the directory to generate logs
    :param start_date: start date
    :param end_date: end date
    :param ip_addr: ip address
    :param http_verb_uri_collect: the http verb uri to collect
    :param http_verb_uri_other: the interferential http verb uri
    :param per_200: the percentage of success response
    :param resp_time_90: the response time in milliseconds to generate in 90% of requests
    :param resp_time_95: the response time in milliseconds to generate in 95% of requests
    :param resp_time_99: the response time in milliseconds to generate in 99% of requests
    :return:
    """
    for date in gen_dates(start_date, (end_date - start_date).days + 1):
       filename = date.strftime(dir + "%Y-%m-%d" + ".log")
       next_day = start_date + datetime.timedelta(days = 1)
       log_time = start_date

       with open(filename, "w") as log_file:
            log_time = log_time + datetime.timedelta(milliseconds = random.randint(100, 200))

            while log_time < next_day:
                log_ip_addr = ip_addr.replace("*", str(random.randint(2, 5)))

                if random.randint(1, 10) <=9:
                    http_verb_uri = http_verb_uri_collect.replace("%d", str(random.randint(1, 99)))
                else:
                    http_verb_uri = http_verb_uri_other

                if random.randint(1, 100) <= per_200:
                    response_status = "200"
                else:
                    response_status = "404"

                randnum = random.randint(1, 100)
                if randnum <= 90:
                    response_time = str(random.randint(1, resp_time_90))
                elif randnum > 90 and randnum <= 95:
                    response_time = str(random.randint(resp_time_90 + 1, resp_time_95))
                elif randnum > 95 and randnum <= 99:
                    response_time = str(random.randint(resp_time_95 + 1, resp_time_99))
                else:
                    response_time = str(random.randint(resp_time_99 + 1, resp_time_99 * 2))

                #10.2.3.4 [2018/13/10:14:02:39] "GET /api/playeritems?playerId=3" 200 1230
                #10.3.4.5 [2018/13/10:14:02:41] "GET /api/playeritems?playerId=2" 200 4630
                log = "{} [{}] {} {} {}\n".format(log_ip_addr, log_time.strftime('%Y-%m-%d %H:%M:%S:%f')[:-3], http_verb_uri, response_status, response_time)
                log_file.write(log)

                log_time = log_time + datetime.timedelta(milliseconds = random.randint(100, 200))

            log_file.close()
    return

def main():
    #get config from config file
    config = ConfigParser.ConfigParser()
    with open("logper.cfg", "r") as cfg_file:
        config.readfp(cfg_file)

        for section in config.sections():
            #config is in Generator section
            if section == "Generator":
                dir = config.get(section, "dir")
                start_date = datetime.datetime.strptime(config.get(section, "start_date"), '%Y-%m-%d')
                end_date = datetime.datetime.strptime(config.get(section, "end_date"), '%Y-%m-%d')
                ip_addr = config.get(section, "ip_address")
                http_verb_uri_collect = config.get(section, "http_verb_uri_collect")
                http_verb_uri_other = config.get(section, "http_verb_uri_other")
                per_200 = int(config.get(section, "per_200"))
                resp_time_90 = int(config.get(section, "resp_time_90"))
                resp_time_95 = int(config.get(section, "resp_time_95"))
                resp_time_99 =int(config.get(section, "resp_time_99"))

                #create directory if not exist
                if not os.path.exists(dir):
                    os.makedirs(dir)
            
                #generate log according to config
                generate_log(dir, start_date, end_date, ip_addr, http_verb_uri_collect, http_verb_uri_other, per_200, resp_time_90, resp_time_95, resp_time_99)

if __name__ == '__main__':
    main()
