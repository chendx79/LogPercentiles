#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ConfigParser

def collect_data():
    return

def print_percentage():
    return

def main():
    config = ConfigParser.ConfigParser()
    with open("logper.cfg", "r") as cfgfile:
        config.readfp(cfgfile)

        for section in config.sections():
            dir = config.get(section, "dir")

if __name__ == '__main__':
    main()