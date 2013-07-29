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
This module contains tests for Type 1 hints.
'''
import string

import fontQAlib
__version__ = fontQAlib.__version__
__author__  = fontQAlib.__author__
__email__   = fontQAlib.__email__

from FL import *
from fontQAtools import trueBBox
from fontQAlib import Nothing, Info, Passed, Warn, Error, Abort, ErrorTypes
from fontQAlib import TestItem, MatchValue, GlyphTest


#----------------------------------------------------------------------------
class Hint_Check(GlyphTest):
  '''
  Verify that there is at least one hint for each glyph in each font.
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Hint-Check')
    self.testFail               = Warn
    self.ErrorMessages[Passed]  = 'All glyphs with outlines have at least one hint.'
    self.ErrorMessages[Warn]    = "Some glyphs with outlines don't have any hints."
    self.DetailMessages[Passed] = 'All glyphs with outlines have at least one hint.'
    self.DetailMessages[Warn]   = "Some glyphs with outlines don't have any hints."

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph) > 0:
        if len(anyGlyph.hhints) + len(anyGlyph.vhints) == 0:
          result.append(anyGlyph.name)
    return result


#----------------------------------------------------------------------------
class NoHint_Check(GlyphTest):
  '''
  Verify that there are no hints in glyphs without outlines.
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'No-Hint-Check')
    self.testFail               = Warn
    self.ErrorMessages[Passed]  = "All glyphs without outlines don't have any hints."
    self.ErrorMessages[Warn]    = "Some glyphs without outlines have hints."
    self.DetailMessages[Passed] = "All glyphs without outlines don't have any hints."
    self.DetailMessages[Warn]   = "Some glyphs without outlines have hints."

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph) == 0:
        if len(anyGlyph.hhints) + len(anyGlyph.vhints) != 0:
          result.append(anyGlyph.name)
    return result


#----------------------------------------------------------------------------
class HHintBBox(GlyphTest):
  '''
  Verify that every horizontal hint is inside the glyphs bounding box.
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'H-Hint BBox')
    self.ErrorMessages[Info]    = "The font has no horizontal hints."
    self.ErrorMessages[Passed]  = "All horizontal hints are inside the glyphs bounding box."
    self.ErrorMessages[Error]   = "Not all horizontal hints are inside the glyphs bounding box."

  def _testFont(self, TheFont):
    result = None
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph) > 0 and len(anyGlyph.hhints) > 0:
        if result == None:
          result = []
        myBBox = trueBBox(anyGlyph)
        myRange = xrange(myBBox.ll.y, myBBox.ur.y + 1)
        for anyHHint in anyGlyph.hhints:
          if anyHHint.position not in myRange or anyHHint.position + anyHHint.width not in myRange:
            result.append('%s: (p=%s, w=%s)' % (anyGlyph.name, anyHHint.position, anyHHint.width))
    return result


#----------------------------------------------------------------------------
class VHintBBox(GlyphTest):
  '''
  Verify that every vertical hint is inside the glyphs bounding box.
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'V-Hint BBox')
    self.ErrorMessages[Info]    = "The font has no vertical hints."
    self.ErrorMessages[Passed]  = "All vertical hints are inside the glyphs bounding box."
    self.ErrorMessages[Error]   = "Not all vertical hints are inside the glyphs bounding box."

  def _testFont(self, TheFont):
    result = None
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph) > 0 and len(anyGlyph.vhints) > 0:
        if result == None:
          result = []
        myBBox = trueBBox(anyGlyph)
        myRange = xrange(myBBox.ll.x, myBBox.ur.x + 1)
        for anyVHint in anyGlyph.vhints:
          if anyVHint.position not in myRange or anyVHint.position + anyVHint.width not in myRange:
            result.append('%s: (p=%s, w=%s)' % (anyGlyph.name, anyVHint.position, anyVHint.width))
    return result


#EOF
