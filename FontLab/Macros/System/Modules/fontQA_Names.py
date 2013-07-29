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
This module contains tests for fontnames and other strings.
'''

from types import StringType

import fontQAlib
__version__ = fontQAlib.__version__
__author__  = fontQAlib.__author__
__email__   = fontQAlib.__email__

from FL import *
from fontQAlib import Nothing, Info, Passed, Warn, Error, Abort, ErrorTypes
from fontQAlib import simpleTest

class fontNameTest(simpleTest):
  '''
  Base class for Font-Name tests
  '''
  def __init__(self, TheName):
    simpleTest.__init__(self, TheName)
    self.stringAttrs = ['family_name', 
                        'full_name', 
                        'font_name', 
                        'menu_name', 
                        'apple_name', 
                        'pref_family_name', 
                        'mac_compatible']


class strAttrTest(fontNameTest):
  '''
  Base class for string-attribute tests
  '''
  def __init__(self, TheName):
    fontNameTest.__init__(self, TheName)
    self.stringAttrs += ['style_name', 
                        'pref_style_name', 
                        'weight', 
                        'designer', 
                        'designer_url', 
                        'copyright', 
                        'notice', 
                        'tt_version', 
                        'trademark', 
                        'vendor_url', 
                        'source']


class lead_trai_space(strAttrTest):
  '''
  Stringattributes should not have leading or tailing spaces.
  This rule is taken from Adobes compare family test.
  '''
  def __init__(self):
    strAttrTest.__init__(self, 'leading & trailing spaces')
    self.ErrorMessages[Passed] = 'No leading or tailing spaces found'
    self.ErrorMessages[Error]  = 'Some strings have leading or tailing spaces.'
    
  def _testFont(self, TheFont):
    result = []
    for anyAttr in self.stringAttrs:
      if hasattr(TheFont, anyAttr):
        myValue = getattr(TheFont, anyAttr)
        if type(myValue) == StringType:
          if myValue.startswith(' ') or myValue.endswith(' '):
            result.append(anyAttr)
    return result


class double_space(strAttrTest):
  '''
  Stringattributes should not have double spaces.
  This rule is taken from Adobes compare family test.
  '''
  def __init__(self):
    strAttrTest.__init__(self, 'double spaces')
    self.ErrorMessages[Passed] = 'No double spaces found'
    self.ErrorMessages[Error]  = 'Some strings have double spaces.'
    
  def _testFont(self, TheFont):
    result = []
    for anyAttr in self.stringAttrs:
      if hasattr(TheFont, anyAttr):
        myValue = getattr(TheFont, anyAttr)
        if type(myValue) == StringType:
          if myValue.find('  ') > -1:
            result.append(anyAttr)
    return result


class hyphen_Name(fontNameTest):
  '''
  Fontnames should not have multiple hyphens.
  '''
  def __init__(self):
    fontNameTest.__init__(self, 'hyphen in Fontnames')
    self.ErrorMessages[Passed] = 'No multiple hyphens found.'
    self.ErrorMessages[Error]  = 'Some Fontnames have multiple hyphens.'
    
  def _testFont(self, TheFont):
    result = []
    for anyAttr in self.stringAttrs:
      if hasattr(TheFont, anyAttr):
        myValue = getattr(TheFont, anyAttr)
        if type(myValue) == StringType:
          if myValue.count('-') > 1:
            result.append(anyAttr)
    return result


#EOF
