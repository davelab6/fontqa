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
This module contains tests for glyphnames and unicode codepoints.
'''
from string import digits

import fontQAlib
__version__ = fontQAlib.__version__
__author__  = fontQAlib.__author__
__email__   = fontQAlib.__email__

from FL import *
from fontQAlib import Nothing, Info, Passed, Warn, Error, Abort, ErrorTypes
from fontQAlib import TestItem, GlyphTest
from fontQAtools import formatUni

#----------------------------------------------------------------------------
class multiDotName(GlyphTest):
  '''
  Glyphnames should have at most one dot
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'multiDot-Name check')
    self.testFail       = Error
    self.ErrorMessages[Passed] = "No glyphs have names with multiple dots."
    self.ErrorMessages[Error]  = 'Some glyphs have names with multiple dots.'
  
  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if anyGlyph.name.count('.') > 1:
        result.append(anyGlyph.name)
    return result


#----------------------------------------------------------------------------
class startNumber(GlyphTest):
  '''
  Glyphnames should not begin with a number
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'startNumber-Name check')
    self.testFail       = Error
    self.ErrorMessages[Passed] = "No glyphs have names starting with a number."
    self.ErrorMessages[Error]  = 'Some glyphs have names starting with a number.'

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph.name) > 0:
        if anyGlyph.name[0] in digits:
          result.append(anyGlyph.name)
      else:
        result.append('Glyph.index: '+str(anyGlyph.index)+' has no name.')
    return result


#----------------------------------------------------------------------------
class startUnderscore(GlyphTest):
  '''
  Glyphnames should not begin with a underscore
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'startUnderscore-Name check')
    self.testFail = Error
    self.ErrorMessages[Passed] = "No glyphs have names starting with a underscore."
    self.ErrorMessages[Error]  = 'Some glyphs have names starting with a underscore.'

  def _testFont(self, TheFont):
    result = []
    for anyGlyph in TheFont.glyphs:
      if len(anyGlyph.name) > 0:
        if anyGlyph.name[0] == '_':
          result.append(anyGlyph.name)
    return result


#----------------------------------------------------------------------------
class DotName_noUnicode(GlyphTest):
  '''
  Glyphs with Dot-Names should have no Unicode
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Dot-Name no Unicode')
    self.testFail       = Error
    self.ErrorMessages[Info]   = 'The fonts do not contain any glyphs with Dot-Names.'
    self.ErrorMessages[Passed] = "All glyphs with Dot-Names don't have Unicodes."
    self.ErrorMessages[Error]  = 'Some glyphs with Dot-Names have Unicodes.'
#   self.DetailMessages[Info]   = 'The font do not contain any glyphs with Dot-Names.'
#   self.DetailMessages[Passed] = "All glyphs with Dot-Names don't have Unicodes."
#   self.DetailMessages[Error]  = 'Some glyphs with Dot-Names have Unicodes.'

  def _testFont(self, TheFont):
    result = []
    isAny = False
    for anyGlyph in TheFont.glyphs:
      if '.' in anyGlyph.name and anyGlyph.name.index('.') > 0:
        isAny = True
        if anyGlyph.unicode != None:
          result.append(anyGlyph.name)
    if isAny:
      return result
    else:
      return None


#----------------------------------------------------------------------------
class UnderscoreName_noUnicode(GlyphTest):
  '''
  Glyphs with Underscore-Names should have no Unicode
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Underscore-Name no Unicode')
    self.testFail               = Error
    self.ErrorMessages[Info]    = 'The fonts do not contain any glyphs with Underscore-Names.'
    self.ErrorMessages[Passed]  = "All glyphs with Underscore-Names don't have Unicodes."
    self.ErrorMessages[Error]   = 'Some glyphs with Underscore-Names have Unicodes.'
    self.DetailMessages[Info]   = 'The font do not contain any glyphs with Underscore-Names.'
#   self.DetailMessages[Passed] = "All glyphs with Underscore-Names don't have Unicodes."
#   self.DetailMessages[Error]  = 'Some glyphs with Underscore-Names have Unicodes.'

  def _testFont(self, TheFont):
    result = []
    isAny = False
    for anyGlyph in TheFont.glyphs:
      if '_' in anyGlyph.name and anyGlyph.name.index('_') > 0:
        isAny = True
        if anyGlyph.unicode != None:
          result.append(anyGlyph.name)
    if isAny:
      return result
    else:
      return None


#----------------------------------------------------------------------------
class UniName_UniCode(GlyphTest):
  '''
  Every Glyph with a Uni-Name should have the corresponding Unicode
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Uni-Name to Unicode')
    self.testFail               = Error
    self.ErrorMessages[Info]    = 'The fonts do not contain any glyphs with Uni-Names.'
    self.ErrorMessages[Passed]  = 'All glyphs with Uni-Names have valid Unicodes.'
    self.ErrorMessages[Error]   = 'Not all glyphs with Uni-Names have valid Unicodes.'
    self.DetailMessages[Info]   = 'The font do not contain any glyphs with Uni-Names.'
    self.DetailMessages[Passed] = 'All glyphs with Uni-Names have valid Unicodes.'
    self.DetailMessages[Error]  = 'Not all glyphs with Uni-Names have valid Unicodes.'

  def _testFont(self, TheFont):
    result = []
    isAny = False
    for anyGlyph in TheFont.glyphs:
      if anyGlyph.name[:3] == 'uni' \
          and '.' not in anyGlyph.name \
          and '_' not in anyGlyph.name:
        isAny = True
        if eval('0x' + anyGlyph.name[3:]) != anyGlyph.unicode:
          result.append(anyGlyph.name)
    if isAny:
      return result
    else:
      return None


#----------------------------------------------------------------------------
class UnicodeDoublemapping(GlyphTest):
  '''
  A glyph should have at most one Unicode
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Unicode-Double-Mapping')
    self.testFail               = Error
    self.ErrorMessages[Info]    = 'The fonts do not contain any glyphs with Unicodes.'
    self.ErrorMessages[Passed]  = 'No Unicode-Double-Mapping is present.'
    self.ErrorMessages[Error]   = 'Some glyphs have Unicode-Double-Mapping.'
    self.DetailMessages[Info]   = 'The font does not contain any glyphs with Unicodes.'
    self.DetailMessages[Passed] = 'No Unicode-Double-Mapping is present.'
    self.DetailMessages[Error]  = 'Some glyphs have Unicode-Double-Mapping.'

  def _testFont(self, TheFont):
    result = []
    isAny = False
    for anyGlyph in TheFont.glyphs:
      if anyGlyph.unicode != None:
        isAny = True
        if len(anyGlyph.unicodes) > 1:
          myResult = anyGlyph.name + ': '
          for anyUni in anyGlyph.unicodes:
            myResult += formatUni(anyUni) + ', '
          result.append(myResult[:-2])
    if isAny:
      return result
    else:
      return None


#----------------------------------------------------------------------------
class doubleGlyphnames(GlyphTest):
  '''
  All glyphnames sould be unique in a font.
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Duplicate Glyphnames')
    self.testFail               = Error
    self.ErrorMessages[Passed]  = 'All glyphnames are unique.'
    self.ErrorMessages[Error]   = 'Some Fonts have glyphs with duplicate names.'
    self.DetailMessages[Passed] = 'All glyphnames are unique.'
    self.DetailMessages[Error]  = 'Some glyphs have duplicate names.'

  def _testFont(self, TheFont):
    result = []
    nameDict = {}
    for anyGlyph in TheFont.glyphs:
      if anyGlyph.name in nameDict:
        nameDict[anyGlyph.name] += 1
      else:
        nameDict[anyGlyph.name] = 1
    nameList = nameDict.keys()
    nameList.sort()
    for anyName in nameList:
      if nameDict[anyName] > 1:
        result.append(str(nameDict[anyName]) + ' x ' + anyName)
    return result


#----------------------------------------------------------------------------
class doubleUnicode(GlyphTest):
  '''
  All Unicodes-Codepoints sould be unique in a font.
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Duplicate Unicodes')
    self.testFail               = Error
    self.ErrorMessages[Passed] = 'All Unicodes-Codepoints are unique.'
    self.ErrorMessages[Error]  = 'Some Fonts have glyphs with duplicate Unicodes-Codepoints.'
    self.DetailMessages[Passed] = 'All Unicodes-Codepoints are unique.'
    self.DetailMessages[Error]  = 'Some glyphs have duplicate Unicodes-Codepoints.'

  def _testFont(self, TheFont):
    result = []
    uniDict = {}
    for anyGlyph in TheFont.glyphs:
      for anyUni in anyGlyph.unicodes:
        if anyUni in uniDict:
          uniDict[anyUni] += 1
        else:
          uniDict[anyUni] = 1
    uniList = uniDict.keys()
    uniList.sort()
    for anyUni in uniList:
      if uniDict[anyUni] > 1:
        result.append(str(uniDict[anyUni]) + ' x ' + formatUni(anyUni))
    return result


#----------------------------------------------------------------------------
class GlyphNameExtensions(GlyphTest):
  '''
  Check for valid Glyphname-Extensions.
  '''
  def __init__(self):
    GlyphTest.__init__(self, 'Glyphname-Extensions')
    self.testFail               = Error
    self.ErrorMessages[Passed]  = 'All Glyphname-Extensions are valid.'
    self.ErrorMessages[Error]   = 'Some Fonts have glyphs with invalid Glyphname-Extensions.'
    self.ErrorMessages[Info]    = 'No glyphnames with extensions are present.'
    self.DetailMessages[Info]   = 'The font does not contain any glyphs with Dot-Names.'
    self.DetailMessages[Passed] = 'All Glyphname-Extensions are valid.'
    self.DetailMessages[Error]  = 'Some glyphs have invalid Glyphname-Extensions.'
    self.ValidExtensions = ('afrc', 'case', 'clig', 'cs_b', 'cs_e', 'cs_i', 'dnom', 'hist', 
                            'hlig', 'init', 'lc', 'lf', 'numr', 'osf', 'pcap', 
                            'pclf', 'pctf', 'pcosf', 'pctosf',
                            'salt', 'sinf', 
                            'sc', 'sclf', 'sctf', 'scosf', 'sctosf', 'comp', 
                            'ss01', 'ss02', 'ss03', 'ss04', 'ss05', 'ss06', 'ss07', 'ss08', 'ss09', 'ss10', 
                            'ss11', 'ss12', 'ss13', 'ss14', 'ss15', 'ss16', 'ss17', 'ss18', 'ss19', 'ss20', 
                            'sc_ss01', 'sc_ss02', 'sc_ss03', 'sc_ss04', 'sc_ss05', 
                            'sc_ss06', 'sc_ss07', 'sc_ss08', 'sc_ss09', 'sc_ss10', 
                            'sc_ss11', 'sc_ss12', 'sc_ss13', 'sc_ss14', 'sc_ss15', 
                            'sc_ss16', 'sc_ss17', 'sc_ss18', 'sc_ss19', 'sc_ss20', 
                            'pc_ss01', 'pc_ss02', 'pc_ss03', 'pc_ss04', 'pc_ss05', 
                            'pc_ss06', 'pc_ss07', 'pc_ss08', 'pc_ss09', 'pc_ss10', 
                            'pc_ss11', 'pc_ss12', 'pc_ss13', 'pc_ss14', 'pc_ss15', 
                            'pc_ss16', 'pc_ss17', 'pc_ss18', 'pc_ss19', 'pc_ss20', 
                            'ti_ss01', 'ti_ss02', 'ti_ss03', 'ti_ss04', 'ti_ss05', 
                            'ti_ss06', 'ti_ss07', 'ti_ss08', 'ti_ss09', 'ti_ss10', 
                            'ti_ss11', 'ti_ss12', 'ti_ss13', 'ti_ss14', 'ti_ss15', 
                            'ti_ss16', 'ti_ss17', 'ti_ss18', 'ti_ss19', 'ti_ss20', 
                            'subs', 'sups', 'swsh', 'tf', 
                            'titl', 'tilf', 'titf', 'tiosf', 'titosf',
                            'tosf', 'uc', 'zero')

  def _testFont(self, TheFont):
    result = []
    isAny = False
    for anyGlyph in TheFont.glyphs:
      if '.' in anyGlyph.name and anyGlyph.name.index('.') > 0:
        isAny = True
        name_ext = anyGlyph.name.split('.', 1)
        if len(name_ext) == 2:
          myExt = name_ext[1]
          if myExt not in self.ValidExtensions:
            #print 'myExt', myExt
            if len(myExt) == 6:
              if myExt[:3] != 'alt' or myExt[3] not in digits or myExt[4] not in digits or myExt[5] not in digits:
                result.append(anyGlyph.name)
            if len(myExt) == 7:
              if myExt[:3] != 'alt' or myExt[3] not in digits or myExt[4] not in digits or myExt[5] not in digits or myExt[6] not in digits:
                result.append(anyGlyph.name)
            else:
              result.append(anyGlyph.name)
        else:
          result.append(anyGlyph.name)
    if isAny:
      return result
    else:
      return None


#EOF
