# coding:utf-8
"""
Copyright (c) 2022-2025 GQYLPY <http://gqylpy.com>. All rights reserved.

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

from logging import handlers as logging_handlers

gpack = sys.modules[__package__]
gcode = sys.modules[__name__]

logging_handlers.Handler       = logging.Handler
logging_handlers.StreamHandler = logging.StreamHandler
logging_handlers.FileHandler   = logging.FileHandler


def __init__(
        name,
        level     = 0,
        formatter = logging.Formatter(),
        filters   = [],
        options   = {},
        handlers  = [],
        gname     = None
):
    logger = logging.Logger(name, level)

    if isinstance(formatter, dict):
        formatter = logging.Formatter(**formatter)

    for handler_or_params in handlers:
        if isinstance(handler_or_params, logging.Handler):
            if handler_or_params.level == 0:
                handler_or_params.setLevel(level)
            if handler_or_params.formatter is None:
                handler_or_params.setFormatter(formatter)
            for x in filters:
                handler_or_params.addFilter(x)
            if options.get("onlyRecordCurrentLevel"):
                handler_or_params.filters.append(
                    only_record_current_level(handler_or_params.level)
                )
            logger.addHandler(handler_or_params)
            continue

        if "formatter" in handler_or_params:
            the_formatter = handler_or_params.pop("formatter")
            if the_formatter.__class__ is dict:
                the_formatter = logging.Formatter(**the_formatter)
        else:
            the_formatter = formatter

        the_level = handler_or_params.pop("level", level)
        the_filters = handler_or_params.pop("filters", filters)
        the_options = handler_or_params.pop("options", options)

        handler_type = getattr(logging_handlers, handler_or_params.pop("name"))

        if issubclass(handler_type, logging.FileHandler):
            filename = handler_or_params["filename"]
            logdir = os.path.dirname(os.path.abspath(filename))
            try:
                os.makedirs(logdir)
            except OSError:
                pass

        handler = handler_type(**handler_or_params)
        handler.setLevel(the_level)
        handler.setFormatter(the_formatter)
        for x in the_filters:
            handler.addFilter(x)
        if the_options.get("onlyRecordCurrentLevel"):
            handler.filters.append(only_record_current_level(handler.level))

        logger.addHandler(handler)

    if gname:
        if not hasattr(gcode, "default") or gcode.default.name == "default":
            gcode.default = logger
        setattr(gpack, gname, logger)

    return logger


def only_record_current_level(levelno):
    class OnlyRecordCurrentLevel(logging.Filter):
        def filter(self, record):
            return record.levelno == levelno

    return OnlyRecordCurrentLevel()


def log(msg, oneline=False, linesep="; ", method=None, gname=None, **kw):
    if gname is None:
        if not hasattr(gcode, "default"):
            __init__("default", gname="default", **gpack.default)
        gobj = getattr(gcode, "default")
    elif gname.__class__ is str:
        gobj = getattr(gpack, gname, None)
        if gobj.__class__ is not logging.Logger:
            raise NameError(
                "gname '%s' not found in '%s'." % (gname, __package__)
            )
    elif gname.__class__ is logging.Logger:
        gobj = gname
    else:
        raise TypeError(
            "parameter 'gname' type must be 'str' or 'logging.Logger', "
            "not '%s'." % gname.__class__.__name__
        )

    if sys.version_info >= (3, 8):
        if "stacklevel" not in kw:
            kw["stacklevel"] = 2
        elif kw["stacklevel"] < 2:
            kw["stacklevel"] = 2

    if oneline:
        msg = linesep.join(
            m.strip() for m in msg.split("\n") if m and not m.isspace()
        )

    getattr(gobj, method)(msg, **kw)


def debug(msg, oneline=None, linesep=None, gname=None, **kw):
    log(
        msg, oneline=oneline, linesep=linesep, method='debug', gname=gname, **kw
    )


def info(msg, oneline=None, linesep=None, gname=None, **kw):
    log(
        msg, oneline=oneline, linesep=linesep, method='info', gname=gname, **kw
    )


def warning(msg, oneline=None, linesep=None, gname=None, **kw):
    log(
        msg, oneline=oneline, linesep=linesep, method='warning', gname=gname,
        **kw
    )


def error(msg, oneline=None, linesep=None, gname=None, **kw):
    log(
        msg, oneline=oneline, linesep=linesep, method='error', gname=gname, **kw
    )


def exception(msg, oneline=None, linesep=None, gname=None, **kw):
    log(
        msg, oneline=oneline, linesep=linesep, method='exception', gname=gname,
        **kw
    )


def critical(msg, oneline=None, linesep=None, gname=None, **kw):
    log(
        msg, oneline=oneline, linesep=linesep, method='critical', gname=gname,
        **kw
    )


def fatal(msg, oneline=None, linesep=None, gname=None, **kw):
    log(
        msg, oneline=oneline, linesep=linesep, method='fatal', gname=gname, **kw
    )
