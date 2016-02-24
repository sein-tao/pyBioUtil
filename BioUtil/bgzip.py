#!/usr/bin/env python3
"""
bgzip file IO
TODO: extend to generally pipe IO ??

Sein Tao, <sein.tao@gmail.com>
2015-08-21 16:40:08 CST
"""

import io
import subprocess
import warnings
import builtins
import types


def open(filename, mode='r', 
        encoding=None, errors=None, newline=None):
    "open bgzip file, handles text wrapper"
    zmode = mode.replace("t", "")
    binary_file = BGzipFile(filename, zmode)
    if "b" not in mode:
        return io.TextIOWrapper(binary_file, encoding, errors, newline)
    else:
        return binary_file

class BGzipFile(io.BufferedIOBase):
    "BGzipFile handles IO from bgzip command."
    _cmd = 'bgzip'
    def __new__(cls, filename, mode='r'):
        "Constructor, program indecates the path to excutable file"
        raw_mode = mode
        if 't' in mode:
            warnings.warn("'t' in BGzipFile: not competable mode.")
            mode = mode.replace('t','')
        if 'b' not in mode:
            mode += 'b'

        if 'r' in mode:
            pipe = subprocess.Popen([cls._cmd, '-d'], 
                    stdin = builtins.open(filename, mode), 
                    stdout=subprocess.PIPE)
            fh = pipe.stdout
        elif 'w' in mode:
            pipe = subprocess.Popen([cls._cmd,],
                    stdin = subprocess.PIPE,
                    stdout = builtins.open(filename, mode))
            fh = pipe.stdin
        else:
            raise ValueError("Invalid mode: {}".format(raw_mode))

        def close(fh):
            fh._close()
            if pipe.wait() != 0:
                warnings.warn("file close error:{}".format(filename))
            # else:
            #     print("pipe closed correctly")
        fh._close = fh.close 
        fh.close = types.MethodType(close, fh)
        return fh

"""
class BGzipFile(io.BufferedIOBase):
    def __init__(self, filename, mode='r'):
        self.filename = filename
        if 'b' not in mode:
            mode += 'b'
        if mode.startswith('r'):
            self._pipe = subprocess.Popen(
                    [_cmd, '-d'], 
                    stdin = builtins.open(filename, mode), 
                    stdout=subprocess.PIPE)
            self._fh = self._pipe.stdout
        elif mode.startswith('w'):
            self._pipe = subprocess.Popen(
                    [_cmd,],
                    stdin = subprocess.PIPE,
                    stdout = builtins.open(filename, mode))
            self._fh = self._pipe.stdin
                    
            
    def __getattr__(self, attr):
        return getattr(self._fh, attr)
        # try:
        #     getattr(self._fh, attr)
        # except AttributeError:
        #     AttributeError("{}.{}".format(self.__class__.name__, attr))

    def close(self):
        self._fh.close()
        if self._pipe.wait() != 0:
            warnings.warn("file close error:{}".format(self.filename))
"""

