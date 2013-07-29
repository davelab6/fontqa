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
This module contains basic functions used by other tests.
'''

import math
from types import IntType,ListType

from FL import *

#-----------------------------------------------------------------------------
# some basic math
#-----------------------------------------------------------------------------
def average(TheList):
  '''
  @param TheList: numeric values (non-numeric value will raise a type error)
  @type  TheList: list
  @return: arithmetic mean over all values of the list
  @rtype : float
  '''
  Summe = 0.0
  for anyValue in TheList:
    Summe = Summe + anyValue
  return Summe / len(TheList)

def variation(TheList):
  '''
  @param TheList: numeric values (non-numeric value will raise a type error)
  @type  TheList: list
  @return: variation over all values of the list
  @rtype : float
  '''
  avg = average(TheList)
  result = 0
  for anyValue in TheList:
    result = result + (pow(anyValue - avg, 2))
  return result

def variance(TheList):
  '''
  @param TheList: numeric values (non-numeric value will raise a type error)
  @type  TheList: list
  @return: variance over all values of the list
  @rtype : float

  variance(TheList) = variation(TheList) / len(TheList)
  '''
  return variation(TheList) / len(TheList)

def StdDeviation(TheList):
  '''
  @param TheList: numeric values (non-numeric value will raise a type error)
  @type  TheList: list
  @return: standard deviation over all values of the list
  @rtype : float
  '''
  return math.sqrt(variance(TheList))

#-----------------------------------------------------------------------------
# some basic font related stuff
#-----------------------------------------------------------------------------
def trueBBox(TheGlyph, masterindex=0):
  '''
  Returns a Rect object enclosing all nodes
  AND all components of 'TheGlyph'.
  If 'masterindex' is omitted the boundingbox of
  the first master is returned.
  '''
  result = None
  if TheGlyph != None:
    if isinstance(TheGlyph, type(Glyph())):
      myGlyph = TheGlyph
    elif isinstance(TheGlyph, ListType): # assuming it is a list of nodes:
      myGlyph = Glyph(1, TheGlyph)
    else:
      raise TypeError, 'expected Glyph or list of Nodes, got: ' + str(type(TheGlyph))
    if len(myGlyph) == 0 and len(myGlyph.components) == 0:
      pass
    else:
      if len(myGlyph) > 0:
        result = myGlyph.GetBoundingRect(masterindex)
      for anyComponent in myGlyph.components:
        tempGlyph = Glyph(myGlyph.parent.glyphs[anyComponent.index])
        tempGlyph.Scale(anyComponent.scales[masterindex], Point(0,0), masterindex)
        tempGlyph.Shift(anyComponent.deltas[masterindex], masterindex)
        if isinstance(result, type(Rect())):
          result.Include(tempGlyph.GetBoundingRect(masterindex))
        else:
          result = tempGlyph.GetBoundingRect(masterindex)
  return result

def getLSB(TheGlyph, masterindex=0):
  '''
  Returns left sidebearing of 'TheGlyph's master as integer.
  If 'masterindex' is omitted the left sidebearing of
  the first master is returned.
  This function is Multiple Master - compatible!
  '''
  if TheGlyph != None:
    myBBox = trueBBox(TheGlyph, masterindex)
    if isinstance(myBBox, type(Rect())):
      return int(myBBox.ll.x)
    else: return None
  else: return None

def getRSB(TheGlyph, masterindex=0):
  '''
  Returns right sidebearing of 'TheGlyph's master as integer.
  If 'masterindex' is omitted the right sidebearing of
  the first master is returned.
  This function is Multiple Master - compatible
  '''
  if TheGlyph != None:
    myBBox = trueBBox(TheGlyph, masterindex)
    if isinstance(myBBox, type(Rect())):
      return int(TheGlyph.GetMetrics(masterindex).x - myBBox.ur.x)
    else: return None
  else: return None

def trueFontBox(TheFont, masterindex=0):
  '''
  @param TheFont: font
  @type  TheFont: FontLab Font object
  @type  masterindex: integer
  @return: a rectangle enclosing all nodes AND all components of all glyphs in 'TheFont'.
  @rtype : FontLab Rect object
  '''
  if TheFont != None and len(TheFont.glyphs) > 0:
    #result = Rect()
    result = None
    for anyGlyph in TheFont.glyphs:
      gRect = trueBBox(anyGlyph, masterindex)
      if type(gRect) != type(None) and type(result) is type(None):
        result = Rect()
        result.Include(gRect)
      elif type(gRect) != type(None) and not type(result) is type(None):
        result.Include(gRect)
    return result
  else:
    return None


#-----------------------------------------------------------------------------
# some other stuff
#-----------------------------------------------------------------------------
def formatUni(TheUnicode):
  if type(TheUnicode) == IntType:
    result = str(hex(TheUnicode)[2:]).upper()
    if len(result) <= 4:
      result = '0' * (4 - len(result)) + result
    else:
      result = '0' * (6 - len(result)) + result
    return result
  elif type(TheUnicode) == NoneType:
    return 'None'
  else:
    raise TypeError

#EOF
