
import argparse
import sys
import fnmatch

def output(line):
    print(line)

def grep_output(lines, params, all_numbers, context_numbers):
    if params.count:
        output(str(len(all_numbers)))
    else:
        for n in all_numbers:
            if params.line_number:
                if n in context_numbers:
                    output(f'{n+1}-{lines[n]}')
                else:
                    output(f'{n+1}:{lines[n]}')
            else:
                output(lines[n])

def grep(lines, params):
    to_print = set() # индексы строк, включая контекстные
    found = set() # индексы строк, исключая контекстные

    for n, line in enumerate(lines):
        line = line.rstrip()
        if params.ignore_case:
            line = line.lower()

        match = fnmatch.fnmatchcase(line, '*'+params.pattern+'*')
        if params.invert:
            match = not match

        b = max(params.before_context,params.context)
        a = max(params.after_context,params.context)

        if match:
            found.add(n)
            for i in range(max(0,n-b),min(n+a+1,len(lines))):
                to_print.add(i)

    grep_output(lines, params, to_print, to_print.difference(found))


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
