
import argparse
import sys
import fnmatch
from collections import deque

BUFFER_SIZE = 10

def output(line):
    print(line)

def grep_output(line, is_context=False, with_line_number=False, n=0):
    if with_line_number:
        if is_context:
            output(f'{n}-{line}')
        else:
            output(f'{n}:{line}')
    else:
        output(line)

def grep(lines, params):
    n = 0       # счетчик номера строки
    count = 0   # счетчик подходящих строк
    b = max(params.before_context, params.context)  # количество строк до искомой в контексте
    a = max(params.after_context, params.context)   # количество строк после искомой в контексте
    context_b = deque(maxlen=b) # очередь предыдущих строк контекста для печати в случае нахождения искомой
    context_a_count = 0         # счетчик оставшихся последующих строк контекста для печати

    for line in lines:
        n+=1
        line = line.rstrip()
        line_copy = line

        if params.ignore_case:
            line = line.lower()

        match = fnmatch.fnmatchcase(line, '*'+params.pattern+'*')
        if params.invert:
            match = not match

        if params.count and match:
            count+=1
        elif match:
            count+=1
            if b:
                delta = len(context_b)
                while context_b:
                    grep_output(context_b.popleft(), True, params.line_number, n-delta)
                    delta-=1
            grep_output(line_copy, False, params.line_number, n)
            if a:
                context_a_count = a
        else:
            if context_a_count:
                grep_output(line_copy, True, params.line_number, n)
                context_a_count-=1
            elif b and len(context_b) >= b:
                context_b.popleft()
                context_b.append(line_copy)
            else:
                context_b.append(line_copy)
    if params.count:
        output(str(count))

def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
