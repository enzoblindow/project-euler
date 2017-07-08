#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Decorator for main.py to measure runtime in s and update README.md with time
automatically.s
"""
import logging
import time
import os
import io

STATUS = {
    'WIP': u'\U0001F914',
    'OPTIMAL': u'\U0001F60D',
    'WELL_DONE': u'\U0001F60E',
    'DONE': u'\U0001F60F',
    'OK': u'\U0001F642',
    'NOT_STARTED': u'\U0001F636',
    'IMPROVE': u'\U0001F644',
    'BAD': u'\U0001F625',
}

def euler(pid, update_readme=False):
    """
    Used as a decorator for measuring runtime. When update_readme is omitted,
    we update the projects README.md with runtime and emoji indicator.
    """
    def decorated(f):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = f(*args, **kwargs)
            runtime = time.time() - start
            runtime_string = get_timestring(runtime)
            logging.info('=======================')
            logging.info('Solution: {}'.format(result))
            logging.info(u'Runtime: {}'.format(runtime_string))
            if update_readme:
                update_runtime(pid=pid, runtime_string=runtime_string)
            return result
        return wrapper
    return decorated


def update_runtime(pid, runtime_string):
    cwd = os.getcwd()
    filename = '{}/README.md'.format(cwd)
    with io.open(filename, "r+", encoding='utf8') as f:
        content = f.readlines()
        for idx, line in enumerate(content):
            try:
                sid = int(line[2:5])
            except ValueError:
                continue
            if sid == int(pid):
                look_for = '/__init__.py)'
                time_string = u'(in {})'.format(runtime_string)
                row = content[idx]
                start = row.find(look_for) + len(look_for) + 1
                end = row.find('|', start-1) - 1
                content[idx] = row[:start] +  time_string + row[end:]
                logging.info('Updated row in project README.md')
                break
        f.seek(0)
        f.write(u''.join(content))
        f.close()


def get_timestring(runtime):
    if runtime < 0.001:
        unit = u'µs'
        runtime *= 1000000
    elif runtime < 1:
        unit = u'ms'
        runtime *= 1000
    elif runtime < 300:
        unit = u's'
        runtime *= 1
    elif runtime < 120*60:
        unit = u'm'
        runtime /= 60
    elif runtime < 120*60*60:
        unit = u'h'
        runtime *= 1/60 * 1/60
    else:
        unit = u'd'
        runtime *= 1/60 * 1/60 * 1/24
    return u'{}{}'.format(round(runtime, 1), unit)
