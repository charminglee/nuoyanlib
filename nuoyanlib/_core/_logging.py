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
#   Last Modified : 2025-05-23
#
# ====================================================


from time import (
    time as _time,
    strftime as _strftime,
    localtime as _localtime,
)
from ..config import ENABLE_LOG as _ENABLE_LOG


def disable_modsdk_loggers():
    import logging
    logging.getLogger("Developer").disabled = 1
    logging.getLogger("Engine").disabled = 1
    logging.getLogger("Part").disabled = 1
    # logging.getLogger("mcp").disabled = 1


def log(msg, cls=None, level="INFO"):
    if not _ENABLE_LOG:
        return
    ct = _time()
    t = _strftime("%Y-%m-%d %H:%M:%S", _localtime(ct))
    msecs = (ct - long(ct)) * 1000
    s = "%s,%03d" % (t, msecs)
    if cls:
        msg = "(%s) %s" % (cls.__name__, msg)
    print "[%s] [%s] [nuoyanlib] %s" % (s, level, msg)


if __name__ == "__main__":
    log("Hello, world!")
    class Test(object): pass
    log("Hello, world!", Test)
    log("Hello, world!", Test, "ERROR")
    import logging
    lg = logging.getLogger()
    lg.setLevel(logging.INFO)
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [nuoyanlib] %(message)s"))
    lg.addHandler(hdlr)
    lg.info("Hello, world!")
















