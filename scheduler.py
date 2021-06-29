#!/usr/bin/env python

"""Top-level script to invoke plotmoving implementation."""

import argparse
import pycrontab
import os
import sys
from daemoniker import Daemonizer

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--info', action='store_true')


def execute():
    cron = pycrontab.PyCronTab(tabfile="crontab.cron")
    for result in cron.run_scheduler():
        print("Job is running. Output: " + result)


def processes(name):
    os.system('tasklist /FI "IMAGENAME eq %s" > processes.txt' % name)
    tmp = open('processes.txt', 'r')
    return [int(i.split()[1]) for i in tmp.readlines()[3:]]


def start_process():
    with Daemonizer() as (is_setup, daemonizer):
        if is_setup:
            sys.stdout = open("log.txt", "a")
            # This code is run before daemonization.
            print("Daemonizer setup completed!")

        # We need to explicitly pass resources to the daemon; other variables
        # may not be correct
        is_parent, my_arg1, my_arg2 = daemonizer(
            'process.pid',
            '',
            ''
        )

        if is_parent:
            # Run code in the parent after daemonization
            pid = os.getpid()
            print("Daemonizer job executing...pid: {}".format(pid))

            print(processes('pythonw.exe'))
            sys.stdout.flush()
            execute()

        sys.stdout.close()


def main():
    args = parser.parse_args()
    if args.info:
        print(processes('pythonw.exe'))
    else:
        print('start_process')
        start_process()
        pass


if __name__ == "__main__":
    main()
