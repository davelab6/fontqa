#----------------------------------------------------------------------------
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
#----------------------------------------------------------------------------
'''
This module contains tests for composite glyphs.
'''

import fontQAlib
__version__ = fontQAlib.__version__
__author__  = fontQAlib.__author__
__email__   = fontQAlib.__email__

from FL import *
from fontQAlib import Nothing, Info, Passed, Warn, Error, Abort, ErrorTypes
from fontQAlib import TestItem, FamilyStatistic, GlyphTest
from fontQAtools import trueBBox


#----------------------------------------------------------------------------
class CompositeCount(FamilyStatistic):
  '''
  Composite statistic for the whole family
  '''
  def __init__(self):
    FamilyStatistic.__init__(self, 'Number of Composites')

  def _testFont(self, TheFont):
    result = 0
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph.components) > 0:
        result += 1
    return result


#----------------------------------------------------------------------------
class doubleComponent(GlyphTest):
  '''
  Check for overlaying components in composite glyphs
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Overlaying components')
    self.testFail               = Error
    self.ErrorMessages[Info]    = 'The fonts do not contain any composite glyphs.'
    self.ErrorMessages[Passed]  = 'No composite glyphs with overlaying components found.'
    self.ErrorMessages[Error]   = 'Some composite glyphs have overlaying components.'

  def _testFont(self, TheFont):
    result = []
    isAny = False
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph.components) > 0:
        isAny = True
        compoDict = {}
        for anyComponent in anyGlyph.components:
          compoStr = str(anyComponent.index) + ',' + str(anyComponent.delta.x) + ',' + str(anyComponent.delta.y)
          compoStr += ',' + str(anyComponent.scale.x) + ',' + str(anyComponent.scale.y)
          if compoStr in compoDict:
            compoDict[compoStr] += 1
          else:
            compoDict[compoStr] = 1
        for anyCompoStr in compoDict:
          if compoDict[anyCompoStr] > 1:
            result.append(anyGlyph.name)
    if isAny:
      return result
    else:
      return None


#----------------------------------------------------------------------------
class overlappingComponent(GlyphTest):
  '''
  This test looks for overlapping bounding boxes! 
  If there are real overlapping outlines,  
  those glyphs should be decomposed and the overlapp should be removed.
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Overlapping components')
    self.testFail               = Warn
    self.ErrorMessages[Info]    = 'The fonts do not contain any composite glyphs.'
    self.ErrorMessages[Passed]  = "No composite glyphs with overlapping Component-BBoxes found."
    self.ErrorMessages[Warn]    = 'Some composite glyphs have overlapping Component-BBoxes.'

  def _testFont(self, TheFont):
    result = []
    isAny = False
    for anyGlyph in TheFont.glyphs:
      compoCount = len(anyGlyph.components)
      if compoCount > 0:
        isAny = True
        rectDict = {}
        for i in range(compoCount):
          tempGlyph = Glyph(anyGlyph.parent.glyphs[anyGlyph.components[i].index])
          if len(tempGlyph) > 0:
            tempGlyph.Scale(anyGlyph.components[i].scale, Point(0,0))
            tempGlyph.Shift(anyGlyph.components[i].delta)
            rectDict[i] = trueBBox(tempGlyph)
          else:
            rectDict[i] = None
        for i in range(compoCount):
          for j in range(compoCount):
            if i != j:
              if type(rectDict[i]) != type(None) and type(rectDict[j]) != type(None):
                if rectDict[i].Check(rectDict[j]) and anyGlyph.name not in result:
                  result.append(anyGlyph.name)
    if isAny:
      return result
    else:
      return None


#----------------------------------------------------------------------------
class emptyComponent(GlyphTest):
  '''
  Check for empty components in composite glyphs
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Empty components')
    self.testFail               = Error
    self.ErrorMessages[Info]    = 'The fonts do not contain any composite glyphs.'
    self.ErrorMessages[Passed]  = "No composite glyphs with empty components found."
    self.ErrorMessages[Error]   = 'Some composite glyphs have empty components.'

  def _testFont(self, TheFont):
    result = []
    isAny = False
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph.components) > 0:
        isAny = True
        badComponents = []
        for anyComponent in anyGlyph.components:
          if len(TheFont.glyphs[anyComponent.index]) == 0:
            badComponents.append(TheFont.glyphs[anyComponent.index].name)
        if badComponents:
          result.append(anyGlyph.name + '->(' + ', '.join(badComponents) + ')')
    if isAny:
      return result
    else:
      return None

#EOF
