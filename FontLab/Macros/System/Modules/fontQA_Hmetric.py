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
This module contains tests for the horizontal metric of fonts.
'''
import fontQAlib
__version__ = fontQAlib.__version__
__author__  = fontQAlib.__author__
__email__   = fontQAlib.__email__

from FL import *
from fontQAlib import Nothing, Info, Passed, Warn, Error, Abort, ErrorTypes
from fontQAlib import FontStatistic, GlyphTest
from fontQAtools import trueBBox, getLSB, getRSB

#----------------------------------------------------------------------------
class Width_Statistic(FontStatistic):
  '''
  Width statistic for every font
  '''
  def __init__(self):
    FontStatistic.__init__(self, 'Width')

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if anyGlyph.width > 0:
        result.append(anyGlyph.width)
    return result


#----------------------------------------------------------------------------
class LSB_Statistic(FontStatistic):
  '''
  Left Sidebearing statistic for every font
  '''
  def __init__(self):
    FontStatistic.__init__(self, 'Left Sidebearing')

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      lsb = getLSB(anyGlyph)
      if lsb != None:
        result.append(lsb)
    return result


#----------------------------------------------------------------------------
class RSB_Statistic(FontStatistic):
  '''
  Right Sidebearing statistic for every font
  '''
  def __init__(self):
    FontStatistic.__init__(self, 'Right Sidebearing')

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      rsb = getRSB(anyGlyph)
      if rsb != None:
        result.append(rsb)
    return result


#----------------------------------------------------------------------------
class LSB_test(GlyphTest):
  '''
  Verify that not more than 30% of the glyphs bounding box 
  is outside the left edge of the glyphs width.
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'suspect left sidebearing')
    self.testFail               = Warn
    self.ErrorMessages[Passed]  = 'The left sidebearing for all fonts is in a normal range.'
    self.ErrorMessages[Warn]    = 'Some glyphs have suspect left sidebearing.'
    self.DetailMessages[Passed] = 'The left sidebearing for all glyphs is in a normal range.'
    self.DetailMessages[Warn]   = 'Some glyphs have suspect left sidebearing.'

  def _testFont(self, TheFont):
    result = []
    isAny = False
    for anyGlyph in TheFont.glyphs:
      myLSB = getLSB(anyGlyph)
      if myLSB != None and myLSB < 0:
        myBBox = trueBBox(anyGlyph)
        if abs(myLSB) > myBBox.width * 0.3 :
          result.append(anyGlyph.name + ': ' + str(myLSB)) 
    return result


#----------------------------------------------------------------------------
class RSB_test(GlyphTest):
  '''
  Verify that not more than 50% of the glyphs bounding box 
  is outside the right edge of the glyphs width.
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'suspect right sidebearing')
    self.testFail               = Warn
    self.ErrorMessages[Passed]  = 'The right sidebearing for all fonts is in a normal range.'
    self.ErrorMessages[Warn]    = 'Some glyphs have suspect right sidebearing.'
    self.DetailMessages[Passed] = 'The right sidebearing for all glyphs is in a normal range.'
    self.DetailMessages[Warn]   = 'Some glyphs have suspect right sidebearing.'

  def _testFont(self, TheFont):
    result = []
    isAny = False
    for anyGlyph in TheFont.glyphs:
      myRSB = getRSB(anyGlyph)
      if myRSB != None and myRSB < 0:
        myBBox = trueBBox(anyGlyph)
        if abs(myRSB) > myBBox.width * 0.5 :
          result.append(anyGlyph.name + ': ' + str(myRSB))
    return result


#EOF
