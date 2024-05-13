[<img alt="LOGO" src="http://www.gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Release](https://img.shields.io/github/release/gqylpy/gqylpy-log.svg?style=flat-square")](https://github.com/gqylpy/gqylpy-log/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_log)](https://pypi.org/project/gqylpy_log)
[![License](https://img.shields.io/pypi/l/gqylpy_log)](https://github.com/gqylpy/gqylpy-log/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/gqylpy_log)](https://pepy.tech/project/gqylpy_log)

# gqylpy-log
[English](README.md) | 中文

> 二次封装 `logging`，更方便快捷的创建日志记录器。使用 `gqylpy_log` 模块可以快速创建 `logging.Logger` 实例并完成一系列的日志配置，使你的代码更简洁。  

<kbd>pip3 install gqylpy_log</kbd>

### 使用内置的日志记录器

`gqylpy_log` 中内置了一个基于 `logging.StreamHandler` 的日志记录器，你可以直接调用它：
```python
import gqylpy_log as glog

glog.debug(...)
glog.info(...)
glog.warning(...)
glog.error(...)
glog.critical(...)
```

它的默认配置如下：
```python
{
    "level": "NOTSET",
    "formatter": {
        "fmt": "[%(asctime)s] [%(module)s.%(funcName)s.line%(lineno)d] "
               "[%(levelname)s] %(message)s",
        "datefmt": "%F %T"
    },
    "handlers": [{"name": "StreamHandler"}]
}
```

你可以根据需要调整默认的日志记录器配置：
```python
glog.default["level"] = "INFO"
```
但要注意的是，默认的日志记录器是在第一次调用日志方法时被创建，你只有在这之前修改配置才会生效。

### 创建一个新的日志记录器

如下示例，将得到一个拥有三个处理程序的日志记录器：
```python
import gqylpy_log as glog

log: logging.Logger = glog.__init__(
    "alpha",
    level="DEBUG",
    formatter={"fmt": "[%(asctime)s] [%(levelname)s] %(message)s"},
    handlers=[
        {"name": "StreamHandler"},
        {
            "name": "FileHandler",
            "level": "ERROR",
            "filename": "/var/log/alpha/error.log",
            "encoding": "UTF-8",
            "formatter": {"fmt": "[%(asctime)s] %(message)s", "datefmt": "%c"},
            "options": {"onlyRecordCurrentLevel": True}
        },
        {
            "name": "TimedRotatingFileHandler",
            "level": "INFO",
            "filename": "/var/log/alpha/alpha.log",
            "encoding": "UTF-8",
            "when": "D",
            "interval": 1,
            "backupCount": 7
        }
    ]
)

log.info(...)
```

或者你希望始终通过 `gqylpy_log` 模块调用它，指定 `gname` 参数即可：
```python
glog.__init__(..., gname="alpha")
```
指定 `gname` 参数后，默认的日志记录器将被覆盖并永久失效。
