#!/usr/bin/python3
"""
"""
import re
from collections import Counter

MYREX = r'([\w\d.-]+)\s-\s(?:\w+|-)\s\[\w+/[A-Za-z]+/\w+:\w+:\w+:\w+ -\w+]\s\"[A-Z]+\s([\d\w./-]+)\s?(?:[\w/.]+|)\"\s(\d+)\s+[\w-]+'
KEYS = ["host", "request", "status"]

class LogParser():
    """
    """

    def __init__(self, file):
        """
        """
        self.file = file
        self.host_list = []
        self.request_list = []
        self.status_list = []
        self.dict_list = []

    def parsing(self):
        """
        """
        with open(self.file, "r", encoding='utf-8', errors='ignore') as f:
            log = f.read()
            my_list = re.findall(MYREX,log)
            for data in my_list:
                self.host_list.append(data[0])
                self.request_list.append(data[1])
                self.status_list.append(data[2])
                dicts = dict(map(lambda key, values: (key,values), KEYS, data))
                self.dict_list.append(dicts)

        return self.host_list, self.request_list, self.status_list, self.dict_list        

    def req_page(self):
        """
        """
        request_count = Counter(self.request_list)
        print("\nTop 10 Requested pages along with count:\n")
        for key, value in request_count.most_common(10):
            print(f'Request page - "{key}",  Hits - {value}  ') 
       

    def percentage_calculation(self, option=None):
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
        per_unsuc = (count/total) * 100
        per_suc = (1-(count/total)) * 100

        if option == "unsuc_per":
            print(f'\nPercentage of unsuccessful requests - {per_unsuc}')
        elif option == "suc_per":
            print(f'\nPercentage of successful requests - {per_suc}')
        elif option == "unsuc_req":
            print("\nTop 10 unsuccessful request along with count:\n")
            for key, value in unreq_count.most_common(10):
                print(f'Host IP - "{key}",  Hits - {value} ')
        else:
            print(f'\nPercentage of unsuccessful requests - {per_unsuc}')
            print(f'\nPercentage of successful requests - {per_suc}')
            print("\nTop 10 unsuccessful request along with count:\n")
            for key, value in unreq_count.most_common(10):
                print(f'unsuccessful requests - "{key}",  Hits - {value} ')

    
    def mostrequest(self):
        """
        """
        host_count = Counter(self.host_list)
        print("\nTop 10 Host along with count:\n")
        for key, value in host_count.most_common(10):
            print(f'Host IP - "{key}",  Hits - {value}  ') 


if __name__ == "__main__":
    LOG = LogParser("testfile")
    LOG.parsing()
    LOG.req_page()
    LOG.mostrequest()
    LOG.percentage_calculation()

