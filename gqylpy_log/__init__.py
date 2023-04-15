"""
Secondary encapsulation `logging`, more convenient and fast to create the
logger. Use this module can quickly create instances of `logging.Logger` and
complete a series of log configuration, make your code cleaner.

    >>> import gqylpy_log as glog
    >>> glog.info(...)

    @version: 1.0.4
    @author: 竹永康 <gqylpy@outlook.com>
    @source: https://github.com/gqylpy/gqylpy-log

────────────────────────────────────────────────────────────────────────────────
Copyright (c) 2022, 2023 GQYLPY <http://gqylpy.com>. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging
from typing import Optional, Union, Any

try:
    from typing import Literal
except ImportError:
    Literal = Union

NOTSET   = 'NOTSET'
DEBUG    = 'DEBUG'
INFO     = 'INFO'
WARN     = 'WARN'
WARNING  = 'WARNING'
ERROR    = 'ERROR'
CRITICAL = 'CRITICAL'
FATAL    = 'FATAL'

level   = NOTSET
output  = 'stream'
logfile = '/var/log/{default is your startup filename}.log'
datefmt = '%F %T'
logfmt  = '[%(asctime)s] [%(module)s.%(funcName)s.line%(lineno)d] ' \
          '[%(levelname)s] %(message)s'

OutputMode = Literal['stream', 'file', 'stream,file']


def __init__(
        name:    Optional[str],
        *,
        level:   Optional[str]        = None,
        output:  Optional[OutputMode] = None,
        logfmt:  Optional[str]        = None,
        datefmt: Optional[str]        = None,
        logfile: Optional[str]        = None,
        gname:   Optional[str]        = None
) -> logging.Logger:
    """Get a `logging.Logger` instance.

    @param name:    The name is required and will be passed directly to
                    `logging.Logger`, one string is recommended.
    @param level:   Log level, default "NOTSET".
    @param output:  Log output mode, stream and/or file, default "stream".
    @param logfmt:  Passed to `logging.Formatter`, default "[%(asctime)s]
                    [%(module)s.%(funcName)s.line%(lineno)d] [%(levelname)s]
                    %(message)s".
    @param datefmt: Passed to `logging.Formatter`, default "%F %T"
    @param logfile: Default is "/var/log/{your startup filename}.log", if the
                    parameter `output` is "file" or "stream,file", otherwise
                    ignore.
    @param gname:   Create a pointer to the `logging.Logger` instance in the
                    gqylpy_log module, if not None.
    """


def debug    (msg: Any, *, gname: Union[str, logging.Logger] = None, **kw): ...
def info     (msg: Any, *, gname: Union[str, logging.Logger] = None, **kw): ...
def warning  (msg: Any, *, gname: Union[str, logging.Logger] = None, **kw): ...
def error    (msg: Any, *, gname: Union[str, logging.Logger] = None, **kw): ...
def exception(msg: Any, *, gname: Union[str, logging.Logger] = None, **kw): ...
def critical (msg: Any, *, gname: Union[str, logging.Logger] = None, **kw): ...
def fatal    (msg: Any, *, gname: Union[str, logging.Logger] = None, **kw): ...


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    import sys

    gpath = f'{__name__}.g {__name__[7:]}'
    __import__(gpath)

    gpack = sys.modules[__name__]
    gcode = globals()[f'g {__name__[7:]}']

    for gname in globals():
        try:
            assert gname[0] != '_' or gname == '__init__'
            gfunc = getattr(gcode, gname)
            assert gfunc.__module__ in (gpath, __package__)
        except (AssertionError, AttributeError):
            continue
        gfunc.__module__ = __package__
        gfunc.__doc__ = getattr(gpack, gname).__doc__
        setattr(gpack, gname, gfunc)
