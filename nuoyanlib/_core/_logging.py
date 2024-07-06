# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-07-06
#
# ====================================================


import logging as _logging
from logging.config import dictConfig as _dictConfig


__all__ = [
    "log",
]


_config = {
    'version': 1,
    'formatters': {
        'formatter': {
            'format': "%(asctime)s | nuoyanlib | %(levelname)s | %(message)s",
        }
    },
    'handlers': {
        'handler': {
            'class': "logging.StreamHandler",
            'level': "DEBUG",
            'formatter': "formatter",
            'stream': "ext://sys.stdout",
        },
        'err_handler': {
            'class': "logging.StreamHandler",
            'level': "ERROR",
            'formatter': "formatter",
            'stream': "ext://sys.stderr",
        }
    },
    'loggers': {
        'logger': {
            'handlers': ["handler"],
            'level': 'DEBUG',
        },
        'err_logger': {
            'handlers': ["err_handler"],
            'level': 'ERROR',
        }
    },
}
_dictConfig(_config)
_logger = _logging.getLogger("logger")
_err_logger = _logging.getLogger("err_logger")


def log(msg, cls=None, level="INFO"):
    logger = _err_logger if level == "ERROR" else _logger
    level = _logging.getLevelName(level)
    if cls:
        logger.log(level, "%s: %s" % (cls.__name__, msg))
    else:
        logger.log(level, msg)


if __name__ == "__main__":
    log("Hello, world!")
    class Test(object): pass
    log("Hello, world!", Test)
    log("Hello, world!", Test, "ERROR")

















