# -*- encoding: utf-8 -*-

from parse import parse as python_parse
from datetime import datetime
from urllib.parse import urlparse
from collections import Counter, defaultdict
import re

PATTERN = '[{}] "{} {} {}" {} {}'
FILE_PATTERN = '^.*\/[\w-]+\.[A-Za-z]{1,4}$'
DATETIME_PATTERN = '%d/%b/%Y %H:%M:%S'
FILE_NAME = 'log.log'

def request_parser(request_string):
    """Parses the request string to tuple (date, type, request, url, response_time)"""
    data = python_parse(PATTERN, request_string)
    if data is not None:
        line_request_date = datetime.strptime(data[0], DATETIME_PATTERN)
        line_request_type = data[1]
        line_request = urlparse(data[2])
        line_url = line_request.netloc + line_request.path
        line_response_time = int(data[5])
        return (line_request_date, line_request_type,
                line_request, line_url, line_response_time)
    else:
        raise ValueError

def is_url_of_file(url):
    """Checks if url links to file"""
    return re.fullmatch(FILE_PATTERN, url)

def strip_www(url):
    """Removes www. from url"""
    if url[:4] == 'www.':
        return url[4:]
    else:
        return url

def prepare_url_list(urls, ignore_www):
    """Converts urls to netloc+path format and removes www. if necessary"""
    for i, url in enumerate(urls):
        parsed = urlparse(url)
        urls[i] = parsed.netloc + parsed.path
        if ignore_www:
            urls[i] = strip_www(url)

def get_5_slowest_queries(url_counter, sum_response_times):
    """Gets 5 slowest queries"""
    for url, sum_response_time in sum_response_times.items():
        url_counter[url] = int(float(sum_response_time) / url_counter[url])
    return [avg_response_time for url, avg_response_time in url_counter.most_common(5)]


def parse(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):

    with open(FILE_NAME) as log_file:
        url_counter = Counter()
        if slow_queries:
            sum_response_times = defaultdict(int)

        if ignore_urls:
            prepare_url_list(ignore_urls, ignore_www)

        for line in log_file:
            try:
                line_request_date, line_request_type, \
                line_request, line_url, line_response_time = request_parser(line)
            except ValueError:
                continue

            # Applying function parameters
            if ignore_www:
                line_url = strip_www(line_url)

            # Checking conditions
            if request_type and request_type != line_request_type:
                continue
            if line_url in ignore_urls:
                continue
            if ignore_files and is_url_of_file(line_url):
                continue
            if start_at and line_request_date < start_at :
                continue
            if stop_at and stop_at < line_request_date:
                continue

            # Got here, if request and url are valid
            url_counter[line_url] += 1

            # Accumulate query time if needed
            if slow_queries:
                sum_response_times[line_url]+=line_response_time

    # Function returns
    if slow_queries:
        return get_5_slowest_queries(url_counter, sum_response_times)
    else:
        return [count for name, count in url_counter.most_common(5)]

def main():
    print (parse(slow_queries=True))
    # pass

if __name__ == "__main__":
    main()