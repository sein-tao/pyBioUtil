"""
gzopen.pm - open (may) gzip/bz2 files
XU Yu, <xuyu@genomics.org.cn>
2012-07-07 19:33:41 CST
add compatibility support for Python3
Sein Tao, <sein.tao@gmail.com>
2015-08-17 18:30:15 CST
"""
# __debug = True
import sys
PY3 = sys.version_info > (3,)
if PY3:
    import builtins
else:
    import __builtin__ as builtins

def xzopen(file, mode='r', *args, **kargs):
    if file == '-':
        if 'w' in mode:
            return sys.stdout
        else:
            return sys.stdin
    # use text mode as defaullt
    if 'b' not in mode:
        if 't' not in mode:
            mode += 't'

    if file.endswith('.bgz') or file.endswith('.b.gz'):
        import bgzip
        return bgzip.open(file, mode, *args, **kargs)
    elif file.endswith('.gz'):
        import gzip
        return gzip.open(file, mode, *args, **kargs)
    elif file.endswith('.bz2'):
        import bz2
        return bz2.open(file, mode, *args, **kargs)
    else:
        return builtins.open(file, mode, *args, **kargs)

open = xzopen

if __name__ == '__main__':
    pass





