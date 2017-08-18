#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
GUI로 출력하여 디버깅 해볼 수 있음
GUI for visual debugging
"""

import threading

import wx
import wx.grid
import wx.lib.newevent
import wx.lib.colourdb

from position.PositionModule import *
from common.InitializationCode import *
import common.InitializationCode as ic

EVT_OBJECT_RESULT_ID = wx.NewId()


def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_OBJECT_RESULT_ID, func)


# 이벤트 결과를 받을 클래스
class ObjectEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, leftTopCoordinate, _object, isSet):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_OBJECT_RESULT_ID)
        self.leftTopCoordinate = leftTopCoordinate
        self.object = _object
        self.isSet = isSet


# Gui 틀이 될 Grid 클래스
class GridFrame(wx.Frame):
    def __init__(self, parent, title):
        self.worker = None
        # wxframe 을 초기화 한다
        wx.Frame.__init__(self, parent, -1, title, pos=(0, 0),
                          size=(ic.floors[0].width, ic.floors[0].length + 150))
        self.CentreOnScreen(wx.BOTH)

        self.ColorList = [wx.TheColourDatabase.Find("GRAY"), wx.RED, wx.CYAN, wx.TheColourDatabase.Find("AQUAMARINE"),
                          wx.TheColourDatabase.Find("BROWN"),
                          wx.TheColourDatabase.Find("CORAL"), wx.TheColourDatabase.Find("GOLD"),
                          wx.TheColourDatabase.Find("KHAKI"),
                          wx.TheColourDatabase.Find("MAGENTA"), wx.TheColourDatabase.Find("NAVY"),
                          wx.TheColourDatabase.Find("PURPLE"),
                          wx.TheColourDatabase.Find("SEA GREEN"), wx.TheColourDatabase.Find("TURQUOISE"),
                          wx.TheColourDatabase.Find("YELLOW"),
                          wx.TheColourDatabase.Find("TAN"), wx.TheColourDatabase.Find("SIENNA"),
                          wx.TheColourDatabase.Find("PLUM")]

        # 후보해 검색을 시각적으로 표현하기 위한 변수들
        self.xCacheRange = []
        self.yCacheRange = []
        self.defaultColor = None

        # 이벤트 연결
        EVT_RESULT(self, self.handler)

        # grid 변수들
        self.space = ic.floors[0]
        width = self.space.width / 100
        height = self.space.length / 100

        # grid setting 하는 코드들
        grid = wx.grid.Grid(self, -1)
        # 그리드 생성
        grid.CreateGrid(height, width)

        # col 과 row 의 크기를 설정한다
        grid.SetColLabelSize(0)
        grid.SetRowLabelSize(0)
        # grid.SetColMinimalAcceptableWidth(5)
        # grid.SetRowMinimalAcceptableHeight(5)
        for i in range(height):
            grid.SetRowSize(i, 1)
        for j in range(width):
            grid.SetColSize(j, 1)

        for ent in self.space.entrances:
            for i in range(ent.coordinate.x, ent.coordinate.x + ent.width + 1):
                for j in range(ent.coordinate.y, ent.coordinate.y + ent.length + 1):
                    grid.SetCellBackgroundColour(i, j, wx.BLUE)

        for obs in self.space.obstacles:
            for i in range(obs.coordinate.x, obs.coordinate.x + obs.width + 1):
                for j in range(obs.coordinate.y, obs.coordinate.y + obs.length + 1):
                    grid.SetCellBackgroundColour(i, j, wx.BLACK)

        # 버튼 몇개를 만들어 용도에 따라 처리 함수와 연결
        self.btn = btn = wx.Button(self, label="Start MaxRects")
        btn2 = wx.Button(self, label="next")
        btn3 = wx.Button(self, label="Straight")
        btn.Bind(wx.EVT_BUTTON, self.onButton)
        btn2.Bind(wx.EVT_BUTTON, self.onNextButton)
        btn3.Bind(wx.EVT_BUTTON, self.onGoButton)

        # sizer 생성 및 연결
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 1, wx.ALL, 0)
        sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(btn2, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(btn3, 0, wx.ALL | wx.CENTER, 5)
        self.grid = grid
        self.defaultColor = self.grid.GetDefaultCellBackgroundColour()

        self.SetSizer(sizer)

    # 이벤트 처리 핸들러
    def handler(self, evt):
        # 화물을 탐색하는 것은 회색, 배치되는것은 빨간색으로 칠하는 코드
        height = evt.object.getHeight()
        width = evt.object.getWidth()

        # 이전에 배치됐던 영역의 색을 원래대로 돌리고
        for coordY in self.yCacheRange:
            for coordX in self.xCacheRange:
                self.grid.SetCellBackgroundColour(coordY, coordX, self.defaultColor)

        # 후보 탐색 하는 상태인지 화물 배치 상태인지 봐가며 색을 결정한다.
        targetColor = self.ColorList[0]
        if evt.isSet:
            targetColor = self.ColorList[1]

        # x 값과 y 값의 범위를 결정한다
        self.yCacheRange = range(evt.leftTopCoordinate.y, evt.leftTopCoordinate.y + height)
        self.xCacheRange = range(evt.leftTopCoordinate.x, evt.leftTopCoordinate.x + width)
        if evt.isSet:
            self.yCacheRange = []
            self.xCacheRange = []

        # 다시 색을 칠한다.
        for coordY in range(evt.leftTopCoordinate.y, evt.leftTopCoordinate.y + height):
            for coordX in range(evt.leftTopCoordinate.x, evt.leftTopCoordinate.x + width):
                self.grid.SetCellBackgroundColour(coordY, coordX, targetColor)

        # grid 를 refresh 하여 결과를 시각적으로 반영한다
        self.grid.Refresh()

    # MaxRects 알고리즘 수행 버튼
    def onButton(self, event):
        # 쓰레드 객체를 만들어서 수행시킴
        self.worker = WorkerThread(self, self.space)
        self.worker.start()
        btn = event.GetEventObject()
        btn.Disable()

    # 한칸씩 진행하는 버튼
    def onNextButton(self):
        self.worker.nextJob()

    # 끝까지 실행하는 버튼
    def onGoButton(self):
        self.worker.goUntilEnd()


# 화물을 탐색하는 것도 보여주고 싶을때 사용하는 이벤트 생성기 클래스
class ObjectEventEmitter:
    def __init__(self, eventTarget):
        # create the event
        self.eventTarget = eventTarget

    # 이벤트 발생 함수
    def emit(self, leftTopCoordinate, obj, isSet):
        wx.PostEvent(self.eventTarget, ObjectEvent(leftTopCoordinate, obj, isSet))


# Gui 윈도우 클래스
class SimpleApp(wx.App):
    def OnInit(self):
        # grid frame 을 생성하여 보여준다
        frame = GridFrame(None, "GUIApp")
        frame.Show()
        self.SetTopWindow(frame)
        return True

    def OnExit(self):
        pass


# 알고리즘을 수행시킬 thread
class WorkerThread(threading.Thread):
    def __init__(self, eventTarget, space):
        threading.Thread.__init__(self)

        # 이벤트를 실행시킬 emitter 를 만든다
        self.eventEmitter = ObjectEventEmitter(eventTarget)
        # 배치 시킬 공간
        self.space = space
        # Gui 제어 변수들
        self.next = False
        self.go = False

        # 알고리즘 모듈 생성
        self.pm = PositionModule()

        # 이벤트를 실행하는 클래스를 넘겨준다
        self.pm.setEventEmitter(self.eventEmitter)

        self.totalAlgorithmTime = 0

    # thread 가 동작할 때 수행할 코드
    def run(self):
        """
        Overrides Thread.run. Don't call this directly its called internally
        when you call Thread.start().
        """

        print "width : " + str(self.space.width) + ", height : " + str(self.space.height)

        self.setPosition(getObjectSampleList())

    # 화물이 하나씩 배치될 떄 마다 이벤트를 받기 위해 따로 뽑아낸 코드
    # PositionModule 클래스의 setPosition 함수와 같은 역할을 함
    def setPosition(self, ObjectList):
        placedNumber = 0
        notPlacedNumber = 0
        usedSpace = 0

        # list 에 있는 모든 object 를 배치
        for obj in ObjectList:
            # Gui 제어 변수들을 보고 화면을 제어하는 코드
            if not self.go:
                # 한 스텝씩 진행하지 않고 끝까지 수행하는 상태가 아니라면
                while not self.next:
                    # 다음 배치 버튼을 누를때까지 무한 대기
                    time.sleep(0.01)

                # 다음 배치 변수를 다시 False 로 바꾼다
                self.next = False

            check1 = time.time()
            coordinate = self.pm.algorithmModule.searchPosition(obj)
            # 화물을 배치하는 코드
            if coordinate is not None:
                placedNumber += 1
                # 배치 잘 됨
                usedSpace += obj.getWidth() * obj.getLength()
                self.pm.algorithmModule.updateLayout(coordinate, obj)
                check2 = time.time()
                self.totalAlgorithmTime = self.totalAlgorithmTime + check2 - check1
            else:
                # 배치 실패
                print str(obj.id) + " 번째 화물 배치 실패. 화물 크기 : " + str(obj.getWidth()) + "*" + str(obj.getLength())
                check2 = time.time()
                self.totalAlgorithmTime = self.totalAlgorithmTime + check2 - check1
                notPlacedNumber += 1

        print
        print "총 걸린 시간 : " + str(self.totalAlgorithmTime)
        print "남은 면적 : " + str(self.space.availSpace - usedSpace)
        print "Number of placed cargoes : " + str(placedNumber)
        print "Number of failed to place cargoes : " + str(notPlacedNumber)
        print

    # 다음 화물 하나를 배치하라는 제어 함수
    def nextJob(self):
        self.next = True

    # 끝까지 쭉 배치하라는 제어 함수
    def goUntilEnd(self):
        self.go = True
        self.next = True


# Gui 프로그램 실행하는 main
def main():
    initialize()
    SimpleApp(redirect=False).MainLoop()


if __name__ == '__main__':
    main()
