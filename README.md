# Problem Statement(HTTP log file parser)

To extract the information from provided logs and print the answers for provided questions. [Log file link](ftp://ita.ee.lbl.gov/traces/NASA_access_log_Aug95.gz)

## Implemented Questions

1. Top 10 requested pages and the number of requests made for each.
2. Percentage of successful requests (anything in the 200s and 300s range)
3. Percentage of unsuccessful requests (anything that is not in the 200s or 300s range)
4. Top 10 unsuccessful page requests.
5. The top 10 hosts making the most requests, displaying the IP address and number of requests made.
6. Option parsing to produce only the report for one of the previous points (e.g. only the top 10 urls, only the percentage of successful requests and so on).
7. For each of the top 10 hosts, show the top 5 pages requested and the number of requests for each.


## Points considered for implementation

1. Python version 3.6.9 and above.
2. Used modules:
   * re - Used for extracting data from logs
   * Collections - Used for creating dictionaries.
   * Argparse - Used for taking the command line arguments.
   * Os - Used to check if provided log files exist or not.
3. Considered provided log file is extracted and not compressed
4. Considered that log data is in the below formats:
    * in24.inetnebr.com - - [01/Aug/1995:00:00:01 -0400] "GET /shuttle/missions/sts-68/news/sts-68-mcc-05.txt HTTP/1.0" 200 1839
    * slppp6.intermind.net - - [01/Aug/1995:00:02:30 -0400] "GET /history/skylab/skylab-2.html" 200 1478
5. Only ip, request and status are extracted from the log files.


## Usage of Tool

1. Help Command
   ```bash
   python3 log_parser.py -h
   usage: log_parser.py [-h] -l LOGFILE [-a ALL] [-rq] [-ps] [-pu] [-mu] [-ip]
                     [-tp]

   HTTP Log parser

   optional arguments:
   -h, --help            show this help message and exit
   -l LOGFILE, --logfile LOGFILE
                        log file input
   -a ALL, --all ALL     prints all data
   -rq, --most_req       Most requested pages and count
   -ps, --per_suc        percentage of Successful requests
   -pu, --per_unsuc      percentage of Unsuccessful requests
   -mu, --most_unreq     Mosted unsuccessful requests
   -ip, --host           Most requested by host and there count
   -tp, --top            prints the top 10 data
   ```

2. User must and should pass the logfile to the tool else it throws an error.
   * Example 1: argument logfile not passed
     ```bash
     python3 log_parser.py
     usage: log_parser.py [-h] -l LOGFILE [-a ALL] [-rq] [-ps] [-pu] [-mu] [-ip]
                     [-tp]
     log_parser.py: error: the following arguments are required: -l/--logfile

     ```
   * Example 1: if log file not present 
     ```bash
     python3 log_parser.py -l test
     usage: log_parser.py [-h] -l LOGFILE [-a ALL] [-rq] [-ps] [-pu] [-mu] [-ip]
                     [-tp]
     log_parser.py: error: argument -l/--logfile: test - file doesn't exist
     ```

3. By default, all the arguments will be true and prints all the data, if no arguments are passed through the command line.

4. Example command for running the tool:
   * ```bash
     python3 log_parser.py -l <logfile>
     ```
   * Prints the output for all queries.
5. Users have the flexibility of fetching data for a particular query.
   * Example :
     ```bash
     python3 log_parser.py -l <log file> -tp 
     ```
   * Above command is used to show, For each of the top 10 hosts, show the top 5 pages requested and the number of requests for each. 
6. Example output file is present in the repo as output.txt
