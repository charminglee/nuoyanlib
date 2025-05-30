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
#   Last Modified : 2025-05-29
#
# ====================================================


from ..config import ENABLED_LOG as _ENABLED_LOG


try:
    import logging
except ImportError:
    logging = None


if _ENABLED_LOG and logging:
    _lgr = logging.getLogger("nuoyanlib")
    _lgr.setLevel(logging.INFO)
    _hdr = logging.StreamHandler()
    _hdr.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"))
    _lgr.addHandler(_hdr)
    info = _lgr.info
    warning = _lgr.warning
    error = _lgr.error
    debug = _lgr.debug
else:
    info = lambda *_: None
    warning = lambda *_: None
    error = lambda *_: None
    debug = lambda *_: None


def disable_modsdk_loggers():
    if logging:
        logging.getLogger("Developer").disabled = 1
        logging.getLogger("Engine").disabled = 1
        logging.getLogger("Part").disabled = 1
        # logging.getLogger("mcp").disabled = 1


















