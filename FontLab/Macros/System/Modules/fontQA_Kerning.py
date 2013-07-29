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
This module contains tests for kerning.
'''
import fontQAlib
__version__ = fontQAlib.__version__
__author__  = fontQAlib.__author__
__email__   = fontQAlib.__email__

from FL import *
from fontQAlib import FamilyStatistic

class KernCount(FamilyStatistic):
  '''
  Kerning statistic for the whole family
  '''
  def __init__(self):
    FamilyStatistic.__init__(self, 'Number of Kerningpairs')

  def _testFont(self, TheFont):
    result = 0
    for anyGlyph in TheFont.glyphs:
      result += len(anyGlyph.kerning)
    return result

#EOF
