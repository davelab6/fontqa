#------------------------------------------------------------------------------
#
# This file is part of the fontQA framework
# Copyright (C) 2005  published by FSI Fonts und Software GmbH
# written by Andreas (Eigi) Eigendorf
# 
# This programming framework is free software; you can redistribute it 
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This programming framework is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this programming framework; if not, write to the 
# Free Software Foundation, Inc.
# 51 Franklin Street, Fifth Floor
# Boston, MA  02110-1301, USA.
# 
#------------------------------------------------------------------------------
'''
This module contains tests for glyph outlines.
'''
import fontQAlib
__version__ = fontQAlib.__version__
__author__  = fontQAlib.__author__
__email__   = fontQAlib.__email__

from FL import *
from fontQAlib import Nothing, Info, Passed, Warn, Error, Abort, ErrorTypes
from fontQAlib import FontStatistic, GlyphTest
from fontQAtools import trueBBox

#----------------------------------------------------------------------------
class Contour_Statistic(FontStatistic):
  '''
  Number of contours per glyph statistic for every font
  '''
  def __init__(self):
    FontStatistic.__init__(self, 'Contours per glyph')

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph) > 0:
        result.append(anyGlyph.GetContoursNumber())
      else:
      	result.append(0)
    return result


#----------------------------------------------------------------------------
class Node_Statistic(FontStatistic):
  '''
  Number of nodes per contour statistic for every font
  '''
  def __init__(self):
    FontStatistic.__init__(self, 'Nodes per contour')

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph) > 0:
        for i in range(anyGlyph.GetContoursNumber()):
          result.append(anyGlyph.GetContourLength(i))
      else:
      	result.append(0)
    return result


#----------------------------------------------------------------------------
class Area_Statistic(FontStatistic):
  '''
  Area per contour statistic for every font
  '''
  def __init__(self):
    FontStatistic.__init__(self, 'Area per contour')

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph) > 0:
        for i in range(anyGlyph.GetContoursNumber()):
          myBBox = trueBBox(Glyph(1, anyGlyph[anyGlyph.GetContourBegin(i) : anyGlyph.GetContourBegin(i) + anyGlyph.GetContourLength(i)]))
          result.append(myBBox.width * myBBox.height)
    return result


#----------------------------------------------------------------------------
class MinContourLength(GlyphTest):
  '''
  Verify that every contour consists of at least three nodes.
  ''' 
  def __init__(self):
    GlyphTest.__init__(self, 'Min contour length')
    self.testFail               = Error
    self.ErrorMessages[Passed]  = "All contours consists of at least three nodes."
    self.ErrorMessages[Error]   = "Some contours have less than three nodes."

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph) > 0:
        for i in range(anyGlyph.GetContoursNumber()):
          if anyGlyph.GetContourLength(i) < 3:
            result.append(anyGlyph.name + ': (x=' + str(anyGlyph.nodes[anyGlyph.GetContourBegin(i)].x) + ', y=' + str(anyGlyph.nodes[anyGlyph.GetContourBegin(i)].y) + ')')
    return result


#----------------------------------------------------------------------------
class MinContourArea(GlyphTest):
  '''
  Verify that every contour has a area of  at least 100 squareunits.
  ''' 
  def __init__(self):
    GlyphTest.__init__(self, 'Min contour area')
    self.testFail               = Error
    self.ErrorMessages[Passed]  = "The area of all contours is greater than 100 squareunits."
    self.ErrorMessages[Error]   = "The area of some contours is less than 100 squareunits."

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph) > 0:
        for i in range(anyGlyph.GetContoursNumber()):
          myBBox = trueBBox(Glyph(1, anyGlyph[anyGlyph.GetContourBegin(i) : anyGlyph.GetContourBegin(i) + anyGlyph.GetContourLength(i)]))
          myArea = myBBox.width * myBBox.height
          if myArea < 100:
            result.append(anyGlyph.name + ' (' + str(int(myBBox.x)) + ',' + str(int(myBBox.y)) + ')')
    return result

#----------------------------------------------------------------------------
class ExtremumPoint(GlyphTest):
  '''
  Verify that every contour has nodes on its extremes.
  ''' 
  def __init__(self):
    GlyphTest.__init__(self, 'Extremum point')
    self.testFail               = Warn
    self.ErrorMessages[Passed]  = "No missing extremum points detected."
    self.ErrorMessages[Warn]    = "It is recommended to add nodes at extremum points."

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph) > 0:
        auditList = anyGlyph.Audit()
        PointList = []
        for anyAuditRec in auditList:
          if anyAuditRec.id == 'Extremum point':
            myPoint = (anyAuditRec.p.x, anyAuditRec.p.y)
            if myPoint not in PointList:
              PointList.append(myPoint)
        if len(PointList) > 0:
          myMessage = anyGlyph.name + ': '
          for anyPoint in PointList:
            myMessage += '(' + str(int(anyPoint[0])) + ',' + str(int(anyPoint[1])) + '), '
          result.append(myMessage[:-2])
    return result

#----------------------------------------------------------------------------
class UnnecInflect(GlyphTest):
  '''
  Verify that no contour has unnecessery inflections.
  ''' 
  def __init__(self):
    GlyphTest.__init__(self, 'Unnecessary inflection')
    self.testFail               = Warn
    self.ErrorMessages[Passed]  = "No unnecessary inflection detected."
    self.ErrorMessages[Warn]    = "It is recommended to reconfigure the curve or add nodes."

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph) > 0:
        auditList = anyGlyph.Audit()
        PointList = []
        for anyAuditRec in auditList:
          if anyAuditRec.id == 'Unnecessary inflection. ':
            myPoint = (anyAuditRec.p.x, anyAuditRec.p.y)
            if myPoint not in PointList:
              PointList.append(myPoint)
        if len(PointList) > 0:
          myMessage = anyGlyph.name + ': '
          for anyPoint in PointList:
            myMessage += '(' + str(int(anyPoint[0])) + ',' + str(int(anyPoint[1])) + '), '
          result.append(myMessage[:-2])
    return result

#----------------------------------------------------------------------------
class UnnecExtreme(GlyphTest):
  '''
  Verify that no contour has unnecessery extremums.
  ''' 
  def __init__(self):
    GlyphTest.__init__(self, 'Unnecessary extremum')
    self.testFail               = Warn
    self.ErrorMessages[Passed]  = "No unnecessary extremum detected."
    self.ErrorMessages[Warn]    = "It is recommended to reconfigure the curve or add nodes."

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph) > 0:
        auditList = anyGlyph.Audit()
        PointList = []
        for anyAuditRec in auditList:
          if anyAuditRec.id == 'Unnecessary extremum':
            myPoint = (anyAuditRec.p.x, anyAuditRec.p.y)
            if myPoint not in PointList:
              PointList.append(myPoint)
        if len(PointList) > 0:
          myMessage = anyGlyph.name + ': '
          for anyPoint in PointList:
            myMessage += '(' + str(int(anyPoint[0])) + ',' + str(int(anyPoint[1])) + '), '
          result.append(myMessage[:-2])
    return result

#EOF
