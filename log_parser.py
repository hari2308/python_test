#!/usr/bin/python3
"""
"""
import re
from collections import Counter
import argparse

MYREX = r'([\w\d.-]+)\s-\s(?:\w+|-)\s\[\w+/[A-Za-z]+/\w+:\w+:\w+:\w+ -\w+]\s\"[A-Z]+\s([\d\w./-]+)\s?(?:[\w/.]+|)\"\s(\d+)\s+[\w-]+'
KEYS = ["host", "request", "status"]

class LogParser():
    """
    """

    def __init__(self, file):
        """
        """
        self.file = file
        self.host_list,self.request_list, self.status_list,self.dict_list = self._parsing()
        self.unreq_count, self.per_suc, self.per_unsuc = self._calculation()

    def _parsing(self):
        """
        """
        host_list = []
        request_list = [] 
        status_list = [] 
        dict_list = []

        with open(self.file, "r", encoding='utf-8', errors='ignore') as f:
            log = f.read()
            my_list = re.findall(MYREX,log)
            for data in my_list:
                host_list.append(data[0])
                request_list.append(data[1])
                status_list.append(data[2])
                dicts = dict(map(lambda key, values: (key,values), KEYS, data))
                dict_list.append(dicts)

        return host_list, request_list, status_list, dict_list        

    def req_page(self):
        """
        """
        request_count = Counter(self.request_list)
        print("\nTop 10 Requested pages along with count:\n")
        for key, value in request_count.most_common(10):
            print(f'Request page - "{key}",  Hits - {value}')      

    def _calculation(self):
        """
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
        
        print(f'\nPercentage of successful requests - {self.per_suc *100}')

    def unsuccessful_per(self):
        
        print(f'\nPercentage of unsuccessful requests - {self.per_unsuc *100}')

    def mosthost(self):
        """
        """
        host_count = Counter(self.host_list)
        print("\nTop 10 Host along with count:\n")
        for key, value in host_count.most_common(10):
            print(f'Host IP - "{key}",  Hits - {value}')

    def unsucreq(self):

        print("\nTop 10 unsuccessful request along with count:\n")
        for key, value in self.unreq_count.most_common(10):
            print(f'unsuccessful requests - "{key}",  Hits - {value}')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='HTTP Log parser')
    parser.add_argument("--logfile", help="logfile input")
    parser.add_argument("--most_req", help="Mosted requested pages and count")
    parser.add_argument("--per_suc", help="percentage of Successful requests ")
    parser.add_argument("--per_unsuc", help="percentage of Unsuccessful requests")
    parser.add_argument("--most_unreq", help="Mosted unsuccessful requests")
    parser.add_argument("--host", help="Most requested by host and there count")
    args = parser.parse_args()


    LOG = LogParser(args.logfile)

    LOG.req_page()
    LOG.mosthost()
    LOG.successful_per()
    LOG.unsuccessful_per()
    LOG.unsucreq()
