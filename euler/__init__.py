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
    'CORRECT': u'\U00002705',
    'INCORRECT': u'\U0000274C',
}


def euler(pid, update_readme=False):
    """
    Used as a decorator for measuring runtime. When update_readme is omitted,
    we update the projects README.md with runtime and emoji indicator.
    """
    def decorated(f):
        def wrapper(*args, **kwargs):
            logging.basicConfig(level=logging.INFO)

            # run
            start = time.time()
            result = f(*args, **kwargs)
            runtime = time.time() - start
            runtime_string = get_timestring(runtime)

            # check result
            expected_result = get_expected_result(pid=pid)
            is_correct = True if str(result) == expected_result else False
            is_correct_string = 'Correct' if is_correct else 'Incorrect'
            
            # print results
            logging.info('=======================')
            logging.info(f'Solution: {result} ({is_correct_string}, expected result: {expected_result})')
            logging.info(u'Runtime: {}'.format(runtime_string))
            
            # store results
            if update_readme:
                update_runtime(pid=pid, runtime_string=runtime_string, is_correct=is_correct)
            
            return result
        return wrapper
    return decorated


def update_runtime(pid, runtime_string, is_correct):
    filename = '{}/README.md'.format(os.getcwd())
    
    with io.open(filename, "r+", encoding='utf8') as f:
        content = f.readlines()
        for idx, line in enumerate(content):
            try:
                sid = int(line[2:5])
            except ValueError:
                continue
            if sid == int(pid):
                # update runtime string
                look_for = '/__main__.py)'
                time_string = u'(in {})'.format(runtime_string)
                row = content[idx]
                start = row.find(look_for) + len(look_for) + 1
                end = row.find('|', start - 1) - 1
                content[idx] = row[:start] + time_string + row[end:]

                # update status indicator
                status_indicator = STATUS['CORRECT'] if is_correct else STATUS['INCORRECT']
                row = content[idx]
                content[idx] = row[:-6] + f'| {status_indicator} |\n'

                logging.info('Updated row in project README.md')
                break
        f.seek(0)
        f.write(u''.join(content))
        f.close()


def get_timestring(runtime):
    if runtime < 0.001:
        unit = u'µs'
        runtime *= 1000000
        runtime = int(runtime)
    elif runtime < 1:
        unit = u'ms'
        runtime *= 1000
        runtime = int(runtime)
    elif runtime < 300:
        unit = u's'
        runtime *= 1
        runtime = round(runtime, 1)
    elif runtime < 120 * 60:
        unit = u'm'
        runtime *= 1 / 60
        runtime = round(runtime, 1)
    elif runtime < 120 * 60 * 60:
        unit = u'h'
        runtime *= 1 / 60 * 1 / 60
        runtime = round(runtime, 2)
    else:
        unit = u'd'
        runtime *= 1 / 60 * 1 / 60 * 1 / 24
        runtime = round(runtime, 1)
    return u'{}{}'.format(runtime, unit)


def get_expected_result(pid, file_path='./data/expected_values.txt'):
    result_dict = {}
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split(' ', 1)
                result_dict[key] = value
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return result_dict[f'{pid}']

