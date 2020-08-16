#!/usr/bin/env python3
'''
Program for parsing Host, sites and status
from HTTP log file
'''
import re
from collections import Counter
import argparse
import os

MYREX = r'([\w\d.-]+)\s-\s(?:\w+|-)\s\[\w+/[A-Za-z]+/\w+:\w+:\w+:\w+ -\w+]\s\"[A-Z]+\s([\d\w./-]+)\s?(?:[\w/.]+|)\"\s(\d+)\s+[\w-]+'
KEYS = ["host", "request", "status"]

class LogParser():
    """
    log parser class which contains functions like parsing
    """

    def __init__(self, files, reg, keys_list):
        """
        constructor for created necessary variables
        """
        self.file = files
        self.reg = reg
        self.key_list = keys_list
        self.host_list, self.request_list, \
        self.status_list, self.dict_list = self._parsing()
        self.unreq_count, self.per_suc, self.per_unsuc = self._calculation()

    def _parsing(self):
        """
        parsing data from log files and returns
        parsed dictionary, hosts, requests and
        status
        """
        host_list = []
        request_list = []
        status_list = []
        dict_list = []

        with open(self.file, "r", encoding='utf-8', errors='ignore') as data:
            log = data.read()
            my_list = re.findall(self.reg, log)
            for data in my_list:
                host_list.append(data[0])
                request_list.append(data[1])
                status_list.append(data[2])
                dicts = dict(map(lambda key, values: (key, values), self.key_list, data))
                dict_list.append(dicts)

        return host_list, request_list, status_list, dict_list

    def req_page(self):
        """
        prints the data of most requested pages
        """
        request_count = Counter(self.request_list)
        print("\nTop 10 Requested pages along with count:\n")
        for key, value in request_count.most_common(10):
            print(f'Request page - "{key}",  Hits - {value}')

    def _calculation(self):
        """
        Calculates percentage of successful and unsuccessful status
        and returns the unsuccessful requests as well
        """
        status_count = Counter(self.status_list)
        total = sum(map(int, status_count.values()))
        count = 0
        unlist = []
        for i in range(len(self.dict_list)):
            if int(self.dict_list[i]["status"]) >= 400:
                unlist.append(self.dict_list[i]["request"])
                count = count+1
        unreq_count = Counter(unlist)
        if total != 0:
            per_unsuc = count/total
            per_suc = 1-(count/total)
        else:
            per_unsuc = 0
            per_suc = 0

        return unreq_count, per_suc, per_unsuc

    def successful_per(self):
        """
        prints the successful percents of requests
        """

        print('\nPercentage of successful requests - {:0.2f}%'.format(self.per_suc *100))

    def unsuccessful_per(self):
        """
        prints the successful percents of requests
        """

        print('\nPercentage of unsuccessful requests - {:0.2f}%'.format(self.per_unsuc *100))

    def mosthost(self):
        """
        prints the top hosts
        """
        host_count = Counter(self.host_list)
        print("\nTop 10 Host along with count:\n")
        for key, value in host_count.most_common(10):
            print(f'Host IP - "{key}",  Hits - {value}')

    def unsucreq(self):
        """
        prints the top unsuccessful requests made
        """

        print("\nTop 10 unsuccessful request along with count:\n")
        for key, value in self.unreq_count.most_common(10):
            print(f'unsuccessful requests - "{key}",  Hits - {value}')

    def tophostdata(self):
        """
        prints the data of top hosts along with their top requests
        """

        host_count = Counter(self.host_list)
        print("Data of Top 10 hosts, with Top 5 sites with count:")
        for key in host_count.most_common(10):
            most_data = []
            for i in range(len(self.dict_list)):
                if self.dict_list[i]["host"] == key[0]:
                    most_data.append(self.dict_list[i]["request"])
            cov = Counter(most_data)
            print(f"\nSites visited by host '{key[0]}'\n")
            for site, count in cov.most_common(5):
                print(f"site - '{site}' and no.of visits- {count}")

    @staticmethod
    def checkfile(files):
        """
        Used for checking if passed file exist or not at argument
        level.
        """
        if not os.path.isfile(files):
            raise argparse.ArgumentTypeError(f"{files} - file doesn't exist")

        return files

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='HTTP Log parser')
    parser.add_argument("-l", "--logfile", help="logfile input",\
                        type=LogParser.checkfile, required=True)
    parser.add_argument("-a", "--all", help="prints all data", default=True)
    parser.add_argument("-rq", "--most_req", help="Mosted requested pages and count", \
                        action='store_true')
    parser.add_argument("-ps", "--per_suc", help="percentage of Successful requests", \
                        action='store_true')
    parser.add_argument("-pu", "--per_unsuc", help="percentage of Unsuccessful requests",\
                        action='store_true')
    parser.add_argument("-mu", "--most_unreq", help="Mosted unsuccessful requests", \
                        action='store_true')
    parser.add_argument("-ip", "--host", \
                        help="Most requested by host and there count",\
                        action='store_true')
    parser.add_argument("-tp", "--top", help="prints the  top 10 data",\
                        action='store_true')
    args = parser.parse_args()

    arg = [args.most_req, args.per_suc, args.per_unsuc, \
           args.most_unreq, args.host, args.top]

    if args.all == any(arg):
        args.all = False

    LOG = LogParser(args.logfile, MYREX, KEYS)

    if args.all or args.most_req:
        LOG.req_page()
    if args.all or args.host:
        LOG.mosthost()
    if args.all or args.per_suc:
        LOG.successful_per()
    if args.all or args.per_unsuc:
        LOG.unsuccessful_per()
    if args.all or args.most_unreq:
        LOG.unsucreq()
    if args.all or args.top:
        LOG.tophostdata()
