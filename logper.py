#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ConfigParser
import datetime

class DefaultOption(dict):
    def __init__(self, config, section, **kv):
        self._config = config
        self._section = section
        dict.__init__(self, **kv)

    def items(self):
        _items = []
        for option in self:
            if not self._config.has_option(self._section, option):
                _items.append((option, self[option]))
            else:
                value_in_config = self._config.get(self._section, option)
                _items.append((option, value_in_config))
        return _items

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

def collect_data(dir, start_date, end_date, filter_ip_addr, filter_api_uri, filter_status_code):
    for date in gen_dates(start_date, (end_date - start_date).days + 1):
        filename = date.strftime(dir + "%Y-%m-%d" + ".log")
        with open(filename, "r") as log_file:
            data = log_file.readline()
            line_count = 0
            while data != "":
                #10.0.0.4 [2019-04-07 01:21:30:724] "GET /api/playeritems?playerId=26" 200 22

                end_ip_addr = data.find(" ", 0)
                ip_addr = data[0 : end_ip_addr]
                if filter_ip_addr != "" and ip_addr != filter_ip_addr:
                    data = log_file.readline()
                    continue

                end_log_time = data.find("]", end_ip_addr) + 1

                end_api_uri = data.find("\"", end_log_time + 2) + 1
                api_uri = data[end_log_time + 1 : end_api_uri]
                if filter_api_uri != "" and api_uri.find(filter_api_uri) < 0:
                    data = log_file.readline()
                    continue

                end_status_code = data.find(" ", end_api_uri + 2)
                status_code = data[end_api_uri + 1 : end_status_code]
                if filter_status_code != "" and status_code != filter_status_code:
                    data = log_file.readline()
                    continue

                end_resp_time = len(data) - 1
                resp_time = data[end_status_code + 1: end_resp_time]

                # print data
                # print "{0}|{1}|{2}|{3}".format(ip_addr, api_uri, status_code, resp_time)
                line_count += 1

                data = log_file.readline()
        print filename, line_count

def print_percentage():
    return

def main():
    config = ConfigParser.ConfigParser()
    with open("logper.cfg", "r") as cfgfile:
        config.readfp(cfgfile)

        for section in config.sections():
            #config is in Percentile section
            if section == "Percentile":
                dir = config.get(section, "dir")
                start_date = datetime.datetime.strptime(config.get(section, "start_date"), '%Y-%m-%d')
                end_date = datetime.datetime.strptime(config.get(section, "end_date"), '%Y-%m-%d')
                filter_ip_addr = config.get(section, "filter_ip_addr", vars=DefaultOption(config, section, filter_ip_addr = ""))
                filter_api_uri = config.get(section, "filter_api_uri", vars=DefaultOption(config, section, filter_api_uri = ""))
                filter_status_code = config.get(section, "filter_status_code", vars=DefaultOption(config, section, filter_status_code = ""))

                collect_data(dir, start_date, end_date, filter_ip_addr, filter_api_uri, filter_status_code)

if __name__ == '__main__':
    main()