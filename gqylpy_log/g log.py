"""
─────────────────────────────────────────────────────────────────────────────────────────────────────
─██████████████─██████████████───████████──████████─██████─────────██████████████─████████──████████─
─██░░░░░░░░░░██─██░░░░░░░░░░██───██░░░░██──██░░░░██─██░░██─────────██░░░░░░░░░░██─██░░░░██──██░░░░██─
─██░░██████████─██░░██████░░██───████░░██──██░░████─██░░██─────────██░░██████░░██─████░░██──██░░████─
─██░░██─────────██░░██──██░░██─────██░░░░██░░░░██───██░░██─────────██░░██──██░░██───██░░░░██░░░░██───
─██░░██─────────██░░██──██░░██─────████░░░░░░████───██░░██─────────██░░██████░░██───████░░░░░░████───
─██░░██──██████─██░░██──██░░██───────████░░████─────██░░██─────────██░░░░░░░░░░██─────████░░████─────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██████████───────██░░██───────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██───────────────██░░██───────
─██░░██████░░██─██░░██████░░████───────██░░██───────██░░██████████─██░░██───────────────██░░██───────
─██░░░░░░░░░░██─██░░░░░░░░░░░░██───────██░░██───────██░░░░░░░░░░██─██░░██───────────────██░░██───────
─██████████████─████████████████───────██████───────██████████████─██████───────────────██████───────
─────────────────────────────────────────────────────────────────────────────────────────────────────

Copyright (C) 2022 GQYLPY <http://gqylpy.com>

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
import os
import sys
import logging

__first__: logging.Logger

gpack = sys.modules[__package__]
gcode = sys.modules[__name__]


def __init__(
        name: str,
        *,
        level: str = 'NOTSET',
        output: str = 'stream',
        logfmt: str = '[%(asctime)s] [%(module)s.%(funcName)s.'
                      'line%(lineno)d] [%(levelname)s] %(message)s',
        datefmt: str = '%F %T',
        logfile: str = None,
        gname: str = None
) -> logging.Logger:
    if output not in ("stream", "file", "stream,file", "file,stream"):
        raise type('ParameterError', (TypeError,), {})(
            'Parameter "output" optional values '
            'are ["stream", "file", "stream,file"].'
        )

    logger = logging.Logger(name, level)
    formatter = logging.Formatter(logfmt, datefmt)

    if 'stream' in output:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if 'file' in output:
        if logfile is None:
            starter: str = os.path.basename(sys.argv[0])
            logfile: str = f'/var/log/{starter[:-3]}.log'

        logdir: str = os.path.dirname(os.path.abspath(logfile))
        os.path.isdir(logdir) or os.makedirs(logdir)

        handler = logging.FileHandler(logfile, encoding='UTF-8')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if gname:
        if not hasattr(gcode, '__first__') or \
                gcode.__first__.name == 'built-in':
            gcode.__first__ = logger
        setattr(gpack, gname, logger)

    return logger


def __call__(func):
    def inner(
            msg: str,
            *,
            gname: (str, logging.Logger) = None,
            **kw
    ):
        if gname is None:
            if not hasattr(gcode, '__first__'):
                gobj: logging.Logger = __init__(
                    name='built-in',
                    level=gpack.level,
                    output=gpack.output,
                    logfmt=gpack.logfmt,
                    datefmt=gpack.datefmt,
                    **({'logfile': gpack.logfile} if gpack.logfile !=
                        '/var/log/{default is your startup filename}.log' else {}),
                    gname='built-in'
                )
                setattr(gcode, '__first__', gobj)
            gobj: logging.Logger = __first__
        elif gname.__class__ is str:
            gobj: logging.Logger = getattr(gpack, gname, None)
            if gobj.__class__ is not logging.Logger:
                raise NameError(f'gname "{gname}" not found in {__package__}.')
        elif gname.__class__ is logging.Logger:
            gobj: logging.Logger = gname
        else:
            x: str = gname.__class__.__name__
            raise TypeError(
                f'Parameter "gname" type must be a str '
                f'or logging.Logger instance. not "{x}".'
            )

        if 'stacklevel' in kw:
            if kw['stacklevel'].__class__ is not int:
                if not kw['stacklevel'].isdigit():
                    x: str = kw['stacklevel'].__class__.__name__
                    raise TypeError(
                        f'Parameter "stacklevel" type must be a "int", not "{x}".'
                    )
                kw['stacklevel'] = int(kw['stacklevel'])
            if kw['stacklevel'] < 2:
                kw['stacklevel'] = 2
        else:
            kw['stacklevel'] = 2

        getattr(gobj, func.__name__)(msg, **kw)

    return inner


@__call__
def debug(): ...
@__call__
def info(): ...
@__call__
def warning(): ...
exception = warning
@__call__
def error(): ...
@__call__
def critical(): ...
fatal = critical
