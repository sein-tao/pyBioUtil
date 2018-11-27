#!/usr/bin/env python

import sys
import logging
import functools
import math
from logging import info, warning, error, debug
from logging import DEBUG, INFO, WARNING, ERROR
import threading
from datetime import datetime, timedelta

__all__ = ['getLogger', 'basicConfig',
         'posLogger', 'recordLogger', 'periodLogger',
         'debug','info', 'warning', 'error',
         'DEBUG', 'INFO', 'WARNING', 'ERROR',
         ] 
_format="%(asctime)s%(levelname)8s: %(message)s"
_datefmt="%Y-%m-%d %H:%M:%S"
_level=logging.INFO

getLogger = logging.getLogger
# def getLogger(name=None,
#         level = _level, 
#         format = _format, 
#         datefmt = _datefmt,
#         file = None, stream=sys.stderr):
#     logger = logging.getLogger(name)
#     logger.setLevel(level)
#     if not logger.handlers:
#         fmt = logging.Formatter(fmt=format, datefmt=datefmt)
#         handler = logging.StreamHandler(stream)
#         handler.setFormatter(fmt)
#         logger.addHandler(handler)
#     return logger
 

_basicConfig = functools.partial(logging.basicConfig,
        level= _level, 
        format=_format, 
        datefmt=_datefmt)

def basicConfig(*args, **kwargs):
    _basicConfig(*args, **kwargs)

class LoggerBase (logging.Logger):
    def __new__(cls, name = None, *args, **kwargs):
        if name is None:
            basicConfig() # in case root is not inited
        self = logging.getLogger(name)
        self.__class__ = cls
        return self
    def __init__(self, name=None, level=logging.INFO, *args, **kwargs):
        self.msg_level = level

    def message(self, msg, *args, **kwargs):
        self.log(self.msg_level, msg, *args, **kwargs)


class posLogger(LoggerBase):
    "chr, pos logger updated peroidically"
    def __init__(self, name=None, step = 1E6, 
            level=logging.INFO):
        super().__init__(name=name, level=level)
        #self.logger = logging.getLogger(name)
        #self.msg_level = level
        self.step = step
        order = int(math.log10(step) / 3)
        self.unit = ("","k","M")[order] 
        self.factor = step / pow(10, 3 * order)
        if int(self.factor) == self.factor:
            self.factor = int(self.factor)
        self.chrom = None
        self.block = None

    def update(self, chrom, pos):
        "update to current position, return True if new block"
        block = int(pos / self.step)
        if chrom != self.chrom or block != self.block:
            self.chrom, self.block = chrom, block
            self.message("Deal with {}:{}{}".format(
                self.chrom, self.block * self.factor, self.unit))
            return True

class recordLogger(LoggerBase):
    "number of records processed, update log peroidically"
    def __init__(self, name=None, step = 1000, level=logging.INFO):
        super().__init__(name, level)
        #self.logger = logging.getLogger(name)
        #self.level = level
        self.step = step
        self.count = 0

    def update(self):
        self.count += 1
        if self.count % self.step == 0:
            self.message("{:,} records processed".format(self.count))
            return True

    def done(self):
        self.message("{:,} records processed in total".format(self.count))

class periodLogger(LoggerBase):
    "logger updated on an certain time period"
    # period update code from 
    # http://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds
    def __init__(self, name=None, period=30, level=logging.INFO, template="{}"):
        """init period logger
        :param peroid: int, interval for update in second
        :prarm template: the output string template used by str.format
        """
        super().__init__(name, level)
        # self.logger = logging.getLogger(name)
        # self.level = level
        self.interval = period
        self.template = template
        self.msg = None
        self.args = None
        self.kwargs = None
        # self.str, self.old_str = None, None
        self.start_time = None
        self._start()

    def output(self):
        if self.args is not None or self.kwargs is not None:
            self.msg = self.template.format(*self.args, **self.kwargs)
        if not self.msg:
            self.msg = "no message"
        passed = datetime.now() - self.start_time
        passed = timedelta(seconds = int(passed.total_seconds())) # remove microseconds
        self.message(str(passed) + " - " + self.msg)

    def update(self, *args, **kwargs):
        "update log by feed new message"
        self.args = args
        self.kwargs = kwargs

    def _run(self):
        # start function when every peroid end
        self._start()
        self.output()

    def _start(self):
        "start logger"
        self.timer = threading.Timer(self.interval, self._run)
        self.timer.daemon = True
        self.timer.start()
        if self.start_time is None:
            self.start_time = datetime.now()
        return self

    def start(self):
        if self.start_time is None:
            self._start()
        return self

    def stop(self, msg=""):
        "stop logger manually"
        self.timer.cancel()
        self.output()
        if msg:
            self.message(msg)
        self.start_time =  None

    def __enter__(self):
        if not self.start_time:
            self._start()
        return self

    def __exit__(self, *args):
        self.stop()

