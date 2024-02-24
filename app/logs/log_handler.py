'''
Logger for error, info, etc..
'''
import traceback
import logging.handlers
from datetime import datetime
from logging import Formatter, getLogger, DEBUG, ERROR
from os import makedirs
from os.path import dirname, exists, realpath
from sys import stderr, stdout
from colorlog import ColoredFormatter
import os
import json

debug = json.loads(os.environ.get('DEBUG').lower()
                   ) if os.environ.get('DEBUG') else True

folder_path = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'files')


class LibLogger():
    '''
    Custom Logging class
    '''

    def __init__(self, folder_path=folder_path, file_name=f'{datetime.now().strftime("%Y_%m_%d")}',
                 save_log_in_file=debug, debug=debug):
        '''
          Initialize logger
          Args:
              folder_name: folder path. Defaults to /log.
              file_name: log file name. Defaults to current_date_time.log.
          '''
        self.enable_debug = debug
        self.file_name = file_name
        self.folder = folder_path
        self.loggers = {}

        if save_log_in_file:
            self.logger = self.get_file_logger()
        else:
            self.logger = self.get_stream_logger()

        if debug:
            self.logger.setLevel(DEBUG)
        else:
            self.logger.setLevel(ERROR)

    def get_or_create_logger(self):
        '''method to create a logger if not exist
        '''
        if self.loggers.get(self.file_name):
            logger = self.loggers.get(self.file_name)
        else:
            logger = getLogger(self.file_name)

        return logger

    def get_stream_logger(self):
        '''method to create stream logger
        '''
        stream_log_formatter = ColoredFormatter((" %(log_color)s%(levelname)2s %(asctime)"
                                                 "-8s%(reset)s | "
                                                 "%(log_color)s%(message)s%(reset)s"))

        if self.enable_debug:
            hndlr = logging.StreamHandler(stdout)
        else:
            hndlr = logging.StreamHandler(stderr)

        hndlr.setFormatter(stream_log_formatter)

        logger = self.get_or_create_logger()
        if not logger.handlers:
            logger.addHandler(hndlr)

        self.loggers[self.file_name] = logger

        return logger

    def get_file_logger(self):
        '''
          Method to crate file logger
        '''

        file_log_formatter = Formatter('%(levelname)s %(asctime)-9s %(message)s')
        if self.folder:
            if not exists(self.folder):
                makedirs(self.folder)
            file_path = str(self.folder) + '/' + str(self.file_name) + '.log'
        else:
            file_path = str(dirname(realpath(__file__))) + \
                str(self.file_name) + '.log'

        logger = self.get_or_create_logger()
        if len(logger.handlers) <= 0:
            max_file_size = 500000
            max_files = 30
            hndlr = logging.handlers.RotatingFileHandler(
                file_path, 'a', max_file_size, max_files)
            logger.addHandler(hndlr)
            hndlr.setFormatter(file_log_formatter)

        self.loggers[self.file_name] = logger
        return logger

    def info(self, string):
        '''
          Method to save information
          Args:
              string: String to save
        '''
        try:
            self.logger.info(str(string))
        except KeyError:
            pass

    def error(self, exception):
        '''
          Method to save error
          Args:
              string: String to save
        '''
        try:
            full_trace = traceback.format_exc()
            self.logger.error(full_trace)
        except KeyError:
            pass

    def warning(self, string):
        '''
          Method to save warnings
          Args:
              string: String to save
        '''
        try:
            self.logger.warning(str(string))
        except KeyError:
            pass

    def debug(self, string):
        '''
          Method to save debugging information
          Args:
              string: String to save
        '''
        try:
            self.logger.debug(str(string))
        except KeyError:
            pass

    def critical(self, string):
        '''
          Method to save critical information
          Args:
              string: String to save
        '''
        try:
            self.logger.critical(str(string))
        except KeyError:
            pass
