#!/usr/bin/python

'''
Example of how to use argparse to pass an argument to show debug logs
Easier to manage than commenting/uncommenting a bunch of print lines
usage: ./logger.py -ll DEBUG

Log levels:
    DEBUG:    shows CRITICAL, ERROR, WARNING, INFO, DEBUG
    INFO:     shows CRITICAL, ERROR, WARNING, INFO
    WARNING:  shows CRITICAL, ERROR, WARNING
    ERROR:    shows CRITICAL, ERROR
    CRITICAL: shows CRITICAL

    Default (no arguments) is WARNING
'''

from argparse import ArgumentParser
import logging

def main():
    parser = ArgumentParser(description="Foo app")
    parser.add_argument('-ll', '--loglevel',
                        type=str,
                        choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'],
                        help='Set the logging level')
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    logger = logging.getLogger()

    logger.debug('foo debug message')
    logger.info('foo info message')
    logger.warning('foo warning message')
    logger.error('foo error message')
    logger.critical('foo critical message')

if __name__ == '__main__':
    main()
