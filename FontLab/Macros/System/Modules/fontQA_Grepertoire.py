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
This module contains tests for the glyphrepertoire of fonts.
'''
import fontQAlib
__version__ = fontQAlib.__version__
__author__  = fontQAlib.__author__
__email__   = fontQAlib.__email__

from FL import *
from fontQAlib import Nothing, Info, Passed, Warn, Error, Abort, ErrorTypes
from fontQAlib import FamilyStatistic, GlyphTest


#----------------------------------------------------------------------------
class GlyphCount(FamilyStatistic):
  '''
  Glyph statistic for the whole family
  '''
  def __init__(self):
    FamilyStatistic.__init__(self, 'Number of Glyphs')

  def _testFont(self, TheFont):
    return len(TheFont)


#----------------------------------------------------------------------------
class EncodedChars(GlyphTest):
  '''
  Every font in a family should share the same set of encoded glyphs
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Encoded Characters')
    self.testFail               = Error
    self.ErrorMessages[Info]    = 'Only one font tested.'
    self.ErrorMessages[Passed]  = 'All fonts share the same set of encoded glyphs.'
    self.ErrorMessages[Error]   = 'Not all fonts share the same set of encoded glyphs.'
    self.DetailMessages[Passed] = 'The set of encoded glyphs matches the set of th whole family.'
    self.DetailMessages[Error]  = 'Some encoded glyphs are missing.'
    self.nameList = []

  def _testFonts(self):
    for anyFont in self.testFontList:
      for anyGlyph in anyFont.glyphs:
        if anyGlyph.unicode and anyGlyph.name not in self.nameList:
          self.nameList.append(anyGlyph.name)
    GlyphTest._testFonts(self)
    
  def _testFont(self, TheFont):
    result = None
    if len(self.testFontList) > 1:
      result = []
      for anyName in self.nameList:
        if not TheFont.has_key(anyName):
          result.append(anyName)
    return result


#----------------------------------------------------------------------------
class DotNameCounterpart(GlyphTest):
  '''
  For every Glyph with a dot in then name a baseglyph (counterpart) should exist.
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Dot-Name counterpart')
    self.testFail               = Error
    self.ErrorMessages[Info]    = 'The fonts do not contain any glyphs with Dot-Names.'
    self.ErrorMessages[Passed]  = 'All glyphs with Dot-Names have valid counterparts.'
    self.ErrorMessages[Error]   = 'Not all glyphs with Dot-Names have valid counterparts.'
    self.DetailMessages[Info]   = 'The font does not contain any glyphs with Dot-Names.'

  def _testFont(self, TheFont):
    result = []
    ignoreExtName = ('uc', 'lc')
    isAny = False
    for anyGlyph in TheFont.glyphs:
      if anyGlyph.name.count('.') == 1 and anyGlyph.name.index('.') > 0:
        #print anyGlyph.name
        baseName, extName = anyGlyph.name.split('.')
        if extName not in ignoreExtName:
          isAny = True
          if not TheFont.has_key(baseName):
            result.append(anyGlyph.name)
    if isAny:
      return result
    else:
      return None


#----------------------------------------------------------------------------
class missingInOne(GlyphTest):
  '''
  Check for glyphs which are present in all but one font
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Missing in one')
    self.testFail               = Warn
    self.ErrorMessages[Info]    = 'Only one font tested.'
    self.ErrorMessages[Passed]  = 'No glyphs are missing which are present in all other fonts.'
    self.ErrorMessages[Warn]    = 'Some fonts are missing glyphs which are present in all other fonts.'
    self.DetailMessages[Passed] = 'No glyphs are missing which are present in all other fonts.'
    self.DetailMessages[Warn]   = 'Some glyphs are missing which are present in all other fonts.'
    self.nameDict = {}

  def _testFonts(self):
    for anyFont in self.testFontList:
      for anyGlyph in anyFont.glyphs:
        if anyGlyph.name in self.nameDict:
          self.nameDict[anyGlyph.name] += 1
        else:
          self.nameDict[anyGlyph.name] = 1
    GlyphTest._testFonts(self)
    
  def _testFont(self, TheFont):
    result = None
    if len(self.testFontList) > 1:
      result = []
      nameList = self.nameDict.keys()
      nameList.sort()
      for anyName in nameList:
        if self.nameDict[anyName] == len(self) - 1 and not TheFont.has_key(anyName):
          result.append(anyName)
    return result


#----------------------------------------------------------------------------
class presentInOne(GlyphTest):
  '''
  Check for glyphs which are present in one font only
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Present in one')
    self.testFail               = Warn
    self.ErrorMessages[Info]    = 'Only one font tested.'
    self.ErrorMessages[Passed]  = 'No glyphs are present in only one font.'
    self.ErrorMessages[Warn]    = 'Some fonts have glyphs which are present in only one font.'
    self.DetailMessages[Passed] = 'No glyphs are present which exist only in this font.'
    self.DetailMessages[Warn]   = 'Some glyphs are present which exist only in this font.'
    self.nameDict = {}

  def _testFonts(self):
    for anyFont in self.testFontList:
      for anyGlyph in anyFont.glyphs:
        if anyGlyph.name in self.nameDict:
          self.nameDict[anyGlyph.name] += 1
        else:
          self.nameDict[anyGlyph.name] = 1
    GlyphTest._testFonts(self)
    
  def _testFont(self, TheFont):
    result = None
    if len(self.testFontList) > 1:
      result = []
      nameList = self.nameDict.keys()
      nameList.sort()
      for anyName in nameList:
        if self.nameDict[anyName] == 1 and TheFont.has_key(anyName):
          result.append(anyName)
    return result


#----------------------------------------------------------------------------
class otherMissing(GlyphTest):
  '''
  Check for glyphs which are missing in some fonts.
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Other missing')
    self.testFail               = Warn
    self.ErrorMessages[Info]    = 'Only one font tested.'
    self.ErrorMessages[Passed]  = 'No glyphs are missing which are present in some other font.'
    self.ErrorMessages[Warn]    = 'Some fonts are missing glyphs which are present in some other fonts.'
    self.nameDict = {}

  def _testFonts(self):
    for anyFont in self.testFontList:
      for anyGlyph in anyFont.glyphs:
        if anyGlyph.name in self.nameDict:
          self.nameDict[anyGlyph.name] += 1
        else:
          self.nameDict[anyGlyph.name] = 1
    GlyphTest._testFonts(self)
    
  def _testFont(self, TheFont):
    result = None
    if len(self.testFontList) > 1:
      result = []
      nameList = self.nameDict.keys()
      nameList.sort()
      for anyName in nameList:
        if self.nameDict[anyName] > 1 and self.nameDict[anyName] < len(self) - 1 and not TheFont.has_key(anyName):
          result.append(anyName)
    return result

#EOF
