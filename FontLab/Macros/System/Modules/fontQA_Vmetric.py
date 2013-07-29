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
This module contains tests for the vertical metric of fonts.
'''
import fontQAlib
__version__ = fontQAlib.__version__
__author__  = fontQAlib.__author__
__email__   = fontQAlib.__email__

from FL import *
from fontQAlib import Nothing, Info, Passed, Warn, Error, Abort, ErrorTypes
from fontQAlib import FamilyStatistic, allMatchOneValue
from fontQAlib import allValuesEqual, MatchValue, GlyphTest
from fontQAtools import trueBBox, trueFontBox

#----------------------------------------------------------------------------
class Ymin_Statistic(FamilyStatistic):
  '''
  Y-Min statistic for the whole family
  '''
  def __init__(self):
    FamilyStatistic.__init__(self, 'Y-min')

  def _testFont(self, TheFont):
    if type(trueFontBox(TheFont)) is type(Rect()):
      return trueFontBox(TheFont).ll.y
    else:
      return None


#----------------------------------------------------------------------------
class Ymax_Statistic(FamilyStatistic):
  '''
  Y-Max statistic for the whole family
  '''
  def __init__(self):
    FamilyStatistic.__init__(self, 'Y-max')

  def _testFont(self, TheFont):
    if type(trueFontBox(TheFont)) is type(Rect()):
      return trueFontBox(TheFont).ur.y
    else:
      return None


#----------------------------------------------------------------------------
class UPM_Test(allMatchOneValue):
  '''
  The UPM-value should be 1000 for all fonts in a family
  '''
  def __init__(self):
    allMatchOneValue.__init__(self, 'UPM')

  def _getRequiredValue(self):
    return 1000

  def _testFont(self, TheFont):
    return TheFont.upm


#----------------------------------------------------------------------------
class Equal_Ascender(allValuesEqual):
  def __init__(self):
    allValuesEqual.__init__(self, 'Ascender')
    self.testFail = Error

  def _testFont(self, TheFont):
    return TheFont.ascender[0]


#----------------------------------------------------------------------------
class Equal_Descender(allValuesEqual):
  def __init__(self):
    allValuesEqual.__init__(self, 'Descender')
    self.testFail = Error

  def _testFont(self, TheFont):
    return TheFont.descender[0]


#----------------------------------------------------------------------------
class TypoAscender(MatchValue):
  '''
  The OS/2-sTypoAscender value should equal the Ascender value
  '''
  def __init__(self):
    MatchValue.__init__(self, 'OS/2-sTypoAscender')
    self.testFail = Error

  def _getRequiredValue(self, TheFont):
    return TheFont.ascender[0]

  def _testFont(self, TheFont):
    return TheFont.ttinfo.os2_s_typo_ascender


#----------------------------------------------------------------------------
class TypoDescender(MatchValue):
  '''
  The OS/2-sTypoDescender value should equal the Descender value
  '''
  def __init__(self):
    MatchValue.__init__(self, 'OS/2-sTypoDescender')
    self.testFail = Error

  def _getRequiredValue(self, TheFont):
    return TheFont.descender[0]

  def _testFont(self, TheFont):
    return TheFont.ttinfo.os2_s_typo_descender


#----------------------------------------------------------------------------
class Equal_TypoLineGap(allValuesEqual):
  def __init__(self):
    allValuesEqual.__init__(self, 'OS/2-sTypoLineGap')
    self.testFail = Error

  def _testFont(self, TheFont):
    return TheFont.ttinfo.os2_s_typo_line_gap


#----------------------------------------------------------------------------
class WinAscent(allMatchOneValue):
  '''
  The OS/2-usWinAscent should match the Y-Max value of the family
  '''
  def __init__(self):
    allMatchOneValue.__init__(self, 'OS/2-usWinAscent')
    self.testFail = Warn

  def _getRequiredValue(self):
    familyBBox = Rect()
    for i in range(len(self)):
      if type(trueFontBox(self.testFontList[i])) is type(Rect()):
        familyBBox.Include(trueFontBox(self.testFontList[i]))
    return int(familyBBox.ur.y)

  def _testFont(self, TheFont):
    return TheFont.ttinfo.os2_us_win_ascent


#----------------------------------------------------------------------------
class WinDescent(allMatchOneValue):
  '''
  The OS/2-usWinAscent should match the Y-Min value of the family
  '''
  def __init__(self):
    allMatchOneValue.__init__(self, 'OS/2-usWinDescent')
    self.testFail = Warn

  def _getRequiredValue(self):
    familyBBox = Rect()
    for i in range(len(self)):
      if type(trueFontBox(self.testFontList[i])) is type(Rect()):
        familyBBox.Include(trueFontBox(self.testFontList[i]))
    return int(familyBBox.ll.y) * -1

  def _testFont(self, TheFont):
    return TheFont.ttinfo.os2_us_win_descent


#----------------------------------------------------------------------------
class hhea_Ascender(MatchValue):
  '''
  The hhea-Ascender value should equal the OS/2-usWinAscent value
  '''
  def __init__(self):
    MatchValue.__init__(self, 'hhea-Ascender')
    self.testFail = Warn

  def _getRequiredValue(self, TheFont):
    return TheFont.ttinfo.os2_us_win_ascent

  def _testFont(self, TheFont):
    return TheFont.ttinfo.hhea_ascender


#----------------------------------------------------------------------------
class hhea_Descender(MatchValue):
  '''
  The hhea-Descender value should equal the OS/2-usWinDescent value
  '''
  def __init__(self):
    MatchValue.__init__(self, 'hhea-Descender')
    self.testFail = Warn

  def _getRequiredValue(self, TheFont):
    return TheFont.ttinfo.os2_us_win_descent * -1

  def _testFont(self, TheFont):
    return TheFont.ttinfo.hhea_descender

#----------------------------------------------------------------------------
class height_test(GlyphTest):
  '''
  Verify that the height of a glyphs bounding box is 
  not more than 150% of the fonts UPM size.
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'suspect BBox height')
    self.testFail               = Error
    self.ErrorMessages[Passed]  = 'The BBox height of all glyphs is in a normal range.'
    self.ErrorMessages[Error]   = 'Some glyphs have a suspect BBox height.'

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      myBBox = None
      myBBox = trueBBox(anyGlyph)
      if type(myBBox) != type(None):
        if myBBox.height > TheFont.upm * 1.5:
          print myBBox.ll, myBBox.ur
          for c in anyGlyph.components:
            print TheFont.glyphs[c.index]
            b = trueBBox(TheFont.glyphs[c.index]),
            print b
          result.append(anyGlyph.name + ': ' + str(myBBox.height)) 
    return result

#EOF
