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
This module contains the main dialog of the fontQA framework.
'''

import os

from FL import *

class SuiteDialog:
  def __init__(self, TheTestSuite):
    self.TestSuite = TheTestSuite
    self.result = 0
    X1 = 10
    X  = X1
    dX = 10
    Y1 = 10
    Y  = Y1
    dY = 25
    h1 =(len(self.TestSuite) + 1) * dY
    h2 = dY * 4
    w = 500
    h = Y1 + h1 + dY + h2 + 50
    wBtn = 50
    self.d = Dialog(self)
    self.d.size = Point(w, h)
    self.d.title = 'fontQA - TestSuite'
    self.d.Center()
    self.d.AddControl(STATICCONTROL,
                      Rect(X, Y, w-dX, Y+h1),
                      'frame01',
                      STYLE_FRAME)
    X += dX
    self.d.AddControl(STATICCONTROL,
                      Rect(X, Y-(dY/4), aAUTO, aAUTO),
                      'label01',
                      STYLE_LABEL,
                      ' select Test-Blocks ')
    Y += round(dY * 0.7)
    for anyBlock in self.TestSuite.testBlockList:
      self.d.AddControl(CHECKBOXCONTROL,
                        Rect(X, Y, w-X, aAUTO),
                        anyBlock.tag,
                        STYLE_CHECKBOX,
                        anyBlock.name)
      Y += dY
    X  = X1
    Y += dY
    self.d.AddControl(STATICCONTROL,
                      Rect(X, Y, w-dX, Y+h2),
                      'frame02',
                      STYLE_FRAME)
    X += dX
    self.d.AddControl(STATICCONTROL,
                      Rect(X, Y-(dY/4), aAUTO, aAUTO),
                      'label01',
                      STYLE_LABEL,
                      ' select Output-File ')
    Y += round(dY * 0.7)
    self.d.AddControl(EDITCONTROL,
                      Rect(X, Y, w-wBtn-(3*dX), aAUTO),
                      'OutPath',
                      STYLE_EDIT,
                      '')
    X = w-wBtn-(2*dX)
    self.d.AddControl(BUTTONCONTROL,
                      Rect(X, Y, X+wBtn, aAUTO),
                      'getOutPath',
                      STYLE_BUTTON,
                      '...')
    X = X1 + dX
    Y += 2 * dY
    if os.name == 'nt':
      self.d.AddControl(CHECKBOXCONTROL,
                        Rect(X, Y, w-X, aAUTO),
                        'openInBrowser',
                        STYLE_CHECKBOX,
                        'open report in browser after validation')
      self.openInBrowser = 1
    else:
      self.openInBrowser = 0
    for anyBlock in self.TestSuite.testBlockList:
      setattr(self, anyBlock.tag, anyBlock.isSelected)
    self.OutPath = self.TestSuite.OutPath

  def on_getOutPath(self, code):
    save = 0
    defaultExt = 'xml'
    strFilter =  'XML-File      (*.xml)|*.xml|'
    strFilter += 'HTML-File     (*.html)|*.html|'
    strFilter += 'All files     (*.*)|*.*|'
    if os.name == 'nt':
      myOutPath = fl.GetFileName(save, defaultExt, self.OutPath, strFilter)
    else:
      myOutPath = fl.GetFileName(save, defaultExt, 
                                 os.path.basename(self.OutPath), strFilter)
    #print myOutPath
    if myOutPath != '':
      self.OutPath = myOutPath
      self.d.PutValue('OutPath')

  def on_openInBrowser(self, code):
    self.d.GetValue('openInBrowser')

  def Run(self):
    self.d.Run()
    return self.result

  def on_ok(self, code):
    for anyBlock in self.TestSuite.testBlockList:
      self.d.GetValue(anyBlock.tag)
    self.result = 1

  def on_cancel(self, code):
    self.result = 2

#-----------------------------------------------------------------------------
# some debug stuff
#-----------------------------------------------------------------------------
def main():
  myList = ['Outline_Tests',
            'V_Metric_Tests',
            'H_Metric_Tests',
            'noch einer',
            'noch einer',
            'noch einer',
            'noch einer']
  dlg = SuiteDialog(myList)
  result = dlg.Run()

if __name__ == '__main__':
  main()


#EOF
