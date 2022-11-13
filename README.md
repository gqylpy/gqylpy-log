[<img alt="LOGO" src="http://www.gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Release](https://img.shields.io/github/release/gqylpy/gqylpy-log.svg?style=flat-square")](https://github.com/gqylpy/gqylpy-log/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_log)](https://pypi.org/project/gqylpy_log)
[![License](https://img.shields.io/pypi/l/gqylpy_log)](https://github.com/gqylpy/gqylpy-log/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/gqylpy_log/month)](https://pepy.tech/project/gqylpy_log)

# gqylpy-log

> 二次封装 `logging`，更方便快捷的创建日志记录器。使用 `gqylpy_log` 模块可以快速创建 `logging.Logger` 实例并完成一系列的日志配置，使你的代码更简洁。  
> > 另外 `gqylpy_log` 中还内置了一个基于 `logging.StreamHandler` 的日志记录器，你可以直接调用它，它是在你第一次调用时自动创建的，前提是你未创建任何指定了参数 `gname` 的日志记录器，否则会使用你第一次创建的指定了参数 `ganme` 的日志记录器作为默认日志记录器，并自动替换和销毁掉内置的日志记录器。

<kbd>pip3 install gqylpy_log</kbd>

## 使用内置的日志记录器
```python
import gqylpy_log as glog

glog.debug(...)
glog.info(...)
glog.warning(...)
glog.error(...)
glog.critical(...)
```
像上面这样直接调用，使用的便是内置的日志记录器，它的配置信息是这样的：
```python
level   = 'NOTSET'
output  = 'stream'
logfile = '/var/log/{default is your startup filename}.log'
datefmt = '%F %T'
logfmt  = '[%(asctime)s] [%(module)s.%(funcName)s.line%(lineno)d] [%(levelname)s] %(message)s'
```
当然可以修改它：
```python
glog.level  = 'INFO'
```
不过需要注意的是，你只有在第一次调用前修改内置的日志记录器配置才会生效，因为在你第一次调用时默认的日志记录器就已经被创建！

## 创建一个新的日志记录器
```python
import gqylpy_log as glog

glog.__init__(
    'alpha',
    level  ='INFO',
    output ='stream,file',
    logfmt ='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%F %T',
    logfile='/var/log/alpha.log',
    gname  ='alpha'
)

glog.info(...)
```
或者你希望直接得到日志记录器实例，而不是始终通过 `gqylpy_log` 模块调用它：
```python
log: logging.Logger = glog.__init__('beta', ...)
log.info(...)
```
