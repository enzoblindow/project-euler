#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Quickly add new solution from the euler project list and create the barebone
python main.py file for it.
Also adds a new item to the list in the repositories README.md
"""
import logging
import os

import requests

import click
from bs4 import BeautifulSoup


@click.command()
@click.option('--pid', prompt='Project #: ', help='Number of the problem.')
def create(pid):
    pid = int(pid)
    zid = str(pid).zfill(3)
    cwd = os.getcwd()

    if os.path.isdir('{}/solutions/p{}'.format(cwd, zid)):
        logging.warn('Solution already exists, aborting..')
        return

    filename = '{}/solutions/p{}/README.md'.format(cwd, zid)
    url = 'https://projecteuler.net/problem={}'.format(pid)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')

    # Grab problem title and body from project euler website
    title = soup.h2.string
    title = title.replace('$', '')
    assignment = []
    for i in soup.findAll("div", {"class": "problem_content"}):
        for k in i.contents:
            try:
                for s in k.stripped_strings:
                    assignment += repr(s)
                assignment += ['\n\n']
            except:
                pass
    assignment = ''.join(assignment)
    assignment = assignment.replace("u'", "").replace("'", " ")
    logging.info('Euler problem title and assignment fetched')

    # Create directory
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
            logging.info('p{} directory created'.format(zid))
        except OSError as e:
            logging.error(e.message)
            return

    # Create euler problems README.md
    with open(filename, 'w') as f:
        f.write('# {}\n'.format(title))
        f.write('### Problem {}\n'.format(zid))
        f.write('\n{}'.format(assignment))
        logging.info('/solutions/p{}/README.md created'.format(zid))
        f.close()

    # Create euler problems main.py
    filename = '{}/solutions/p{}/__main__.py'.format(cwd, zid)
    MAIN_PY = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
from euler import euler


@euler(pid={}, update_readme=False)
def solve():
    return 'WIP'


if __name__ == '__main__':
    print(solve())

    """.format(pid)
    with open(filename, 'w') as f:
        f.write(MAIN_PY)
        logging.info('/solutions/p{}/__main__.py created'.format(zid))
        f.close()

    # Add new entry to the repository README.md
    filename = '{}/README.md'.format(cwd)
    readme_line = f"| [{zid}](https://github.com/enzoblindow/project-euler/tree/master/solutions/p{zid}) |"
    readme_line += f" [{title}](https://projecteuler.net/problem={pid}) |"
    readme_line += f" [Python](https://github.com/enzoblindow/project-euler/blob/master/solutions/p{zid}/__main__.py) |"
    readme_line += f" | | | | | | |"
    with open(filename, "r+") as f:
        content = f.readlines()
        for idx, line in enumerate(content):
            try:
                sid = int(line[3:6])
            except ValueError:
                continue
            if int(sid) > int(pid):
                content.insert(idx, readme_line + '\n')
                logging.info('Added row in project README.md'.format(zid))
                break
        f.seek(0)
        f.write(''.join(content))
        f.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    create()
