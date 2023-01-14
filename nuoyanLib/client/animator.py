# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-01-15
#
# ====================================================


import mod.client.extraClientApi as _clientApi


_PLAYER_ID = _clientApi.GetLocalPlayerId()
_ClientCompFactory = _clientApi.GetEngineCompFactory()
_PlayerGameComp = _ClientCompFactory.CreateGame(_PLAYER_ID)


class Animator(object):
    def __init__(self, uiCtrl, fps, duration, isStay, endFunc=None, *endFuncArgs):
        self._fps = fps
        self._duration = duration
        self._totalFrame = fps * duration
        self._isStay = isStay
        self._endFunc = endFunc
        self._endFuncArgs = endFuncArgs
        self._allUiCtrl = uiCtrl if isinstance(uiCtrl, (tuple, list)) else [uiCtrl]
        self._animationArgs = {
            'alpha': [],
            'scale': [],
            'translation': [[], []]
        }
        self._initUiArgs = []
        for i in self._allUiCtrl:
            args = {
                'pos': i.GetPosition() if i else None,
                'size': i.GetSize() if i else None
            }
            self._initUiArgs.append(args)
        self._isStop = False
        self._isAlphaFinished = False
        self._isScaleFinished = False
        self._isTranslationFinished = False
        self._isPlaying = False

    # noinspection PyUnresolvedReferences
    def _startAlphaAnimation(self):
        aa = self._animationArgs['alpha']
        if aa:
            self._isPlaying = True
            start = float(aa[0])
            end = float(aa[1])
            per = (end - start) / self._totalFrame
            frame = [0]
            def func():
                if not self._isStop:
                    for i in self._allUiCtrl:
                        if i:
                            i.SetAlpha(start + (frame[0] + 1) * per)
                    frame[0] += 1
                    if frame[0] >= self._totalFrame:
                        self._isAlphaFinished = True
                        self._onAnimationFinish()
                    else:
                        _PlayerGameComp.AddTimer(1 / self._fps, func)
            func()
        else:
            self._isAlphaFinished = True
            self._onAnimationFinish()

    # noinspection PyUnresolvedReferences
    def _startScaleAnimation(self):
        if self._animationArgs['scale']:
            self._isPlaying = True
        else:
            self._isScaleFinished = True
            self._onAnimationFinish()

    # noinspection PyUnresolvedReferences
    def _startTranslationAnimation(self):
        ta = self._animationArgs['translation']
        if ta[0]:
            self._isPlaying = True
            startX = ta[0][0]
            endX = ta[1][0]
            perX = (endX - startX) / self._totalFrame
            startY = ta[0][1]
            endY = ta[1][1]
            perY = (endY - startY) / self._totalFrame
            frame = [0]
            def func():
                if not self._isStop:
                    for i in range(len(self._allUiCtrl)):
                        if self._allUiCtrl[i]:
                            self._allUiCtrl[i].SetPosition((
                                self._initUiArgs[i]['pos'][0] + (frame[0] + 1) * perX,
                                self._initUiArgs[i]['pos'][1] + (frame[0] + 1) * perY
                            ))
                    frame[0] += 1
                    if frame[0] >= self._totalFrame:
                        self._isTranslationFinished = True
                        self._onAnimationFinish()
                    else:
                        _PlayerGameComp.AddTimer(1 / self._fps, func)
            func()
        else:
            self._isTranslationFinished = True
            self._onAnimationFinish()

    def _recoveryUi(self):
        for i in range(len(self._initUiArgs)):
            if self._allUiCtrl[i]:
                self._allUiCtrl[i].SetPosition(self._initUiArgs[i]['pos'])
                self._allUiCtrl[i].SetSize(self._initUiArgs[i]['size'])
                self._allUiCtrl[i].SetAlpha(1.0)

    def _onAnimationFinish(self):
        if self._isAlphaFinished and self._isScaleFinished and self._isTranslationFinished:
            if self._endFunc:
                if self._endFuncArgs:
                    self._endFunc(*self._endFuncArgs)
                else:
                    self._endFunc()
            if not self._isStay:
                self._recoveryUi()
            self._isAlphaFinished = False
            self._isScaleFinished = False
            self._isTranslationFinished = False
            self._isPlaying = False

    def addAlphaAnimation(self, startAlpha, endAlpha):
        if not self._isPlaying:
            self._animationArgs['alpha'] = (startAlpha, endAlpha)
            self._isStop = False

    def addScaleAnimation(self, startMultiple, endMultiple):
        if not self._isPlaying:
            self._animationArgs['scale'] = (startMultiple, endMultiple)
            self._isStop = False

    def addTranslationAnimation(self, startRelativePos, endRelativePos):
        if not self._isPlaying:
            self._animationArgs['translation'] = (startRelativePos, endRelativePos)
            self._isStop = False

    def startAnimation(self):
        if not self._isPlaying:
            self._startAlphaAnimation()
            self._startScaleAnimation()
            self._startTranslationAnimation()

    def stopAnimation(self):
        if self._isPlaying:
            self._isStop = True
            self._recoveryUi()
            self._isPlaying = False














