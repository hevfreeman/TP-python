# -*- encoding: utf-8 -*-

from parse import parse as python_parse
from datetime import datetime
from urllib.parse import urlparse
from collections import Counter

PATTERN = '[{}] "{} {} {}" {} {}'

def isfile(url):
    return url[-1] != '/' and '.' in url[-4:-1]


def parse(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):

    with open('log.log') as f:
        url_counter = Counter()

        if slow_queries:
            sum_response_times = dict()
            avg_response_times = dict()

        if ignore_www:
            for i, u in enumerate(ignore_urls):
                if u[:4] == 'www.':
                    ignore_urls[i] = u[4:]

        for line in f:
            data = python_parse(PATTERN, line)
            if data is not None:
                line_request_date = datetime.strptime(data[0], '%d/%b/%Y %H:%M:%S')
                line_request_type = data[1]
                line_request = urlparse(data[2])
                line_url = line_request.netloc + line_request.path
                line_protocol = data[3]
                line_response_code = int(data[4])
                line_response_time = int(data[5])

                if ignore_www:
                    if line_url[:4] == 'www.':
                        line_url = line_url[4:]

                if request_type and request_type != line_request_type:
                    continue

                if line_url in ignore_urls:
                    continue

                if ignore_files and isfile(line_url):
                    continue

                if start_at and line_request_date < start_at :
                    continue

                if stop_at and stop_at < line_request_date:
                    continue

                url_counter[line_url] += 1

                if slow_queries:
                    if line_url in sum_response_times:
                        sum_response_times[line_url]+=line_response_time
                    else:
                        sum_response_times[line_url]=line_response_time

    if slow_queries:
        for k in sum_response_times.keys():
            avg_response_times[k] = int(float(sum_response_times[k]) / url_counter[k])
        return sorted(avg_response_times.values(), reverse=True)[:5]
    else:
        return [count for name, count in url_counter.most_common(5)]

def main():
    # print (parse(slow_queries=True))
    pass

if __name__ == "__main__":
    main()