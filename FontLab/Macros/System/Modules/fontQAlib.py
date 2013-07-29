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
This is the main module of the fontQA framework.
'''

__version__ = 'version 1.0, 2005'
__author__  = 'Andreas (Eigi) Eigendorf'
__email__   = 'mail@e-font.de'

import sys, traceback, os, shutil, webbrowser, time
from types import StringType, ListType
from xmlWriter import XMLWriter
from FL import *
import fontQAdialog
from fontQAdialog import SuiteDialog
from fontQAtools import average, StdDeviation
import re

shortNotice =  'fontQA ' + __version__ + ', Copyright (C) '+ __author__ + '\n' 
shortNotice += 'fontQA comes with ABSOLUTELY NO WARRANTY. ' 
shortNotice += 'This is free software, and you are welcome '
shortNotice += 'to redistribute it under certain conditions, ' 
shortNotice += 'see the GNU General Public License for details.\n'

Nothing = -1
Info    =  0
Passed  =  1
Warn    =  2
Error   =  3
Abort   =  4
ErrorTypes = {Nothing:'N', 
              Info:'I', 
              Passed:'P', 
              Warn:'W', 
              Error:'E', 
              Abort:'A'}

XSL_FileName = 'fontQA.xsl'

XSL_FilePath = os.path.join(os.path.dirname(fontQAdialog.__file__), \
                            XSL_FileName)


#----------------------------------------------------------------------------
class metaTestItem:
  '''
  Meta class for all testitems
  '''
  def __init__(self, TheName, TheTag):
    '''
    @param TheName: the name presented to the user
    @type  TheName: string
    @param TheTag: internal name used as tag in XML reports
    @type  TheTag: string
    Constructor
    '''
    self.name = TheName
    self.tag = TheTag
    self.parent = None
    self._childs = []
    self.suite = self
    self.isSelected = True
    self.testFontList = []
    self.XMLwriter = None
    self.indentStr = '  '

  def __len__(self):
    '''
    Implementation of the built-in function len().
    @return: Number of child objects.
    @rtype:  integer
    '''
    if self._childs:
      return len(self._childs)
    else:
      return 0

  def __getattr__(self, TheKey):
    result = None
    for anyChild in self._childs:
      if anyChild.tag == TheKey:
        result = anyChild
    if type(result) == type(None):
      raise KeyError
    else:
      return result

  def className(self):
    '''
    @return: Returns name of its class: self.__class__.__name__
    @rtype:  string
    '''
    return self.__class__.__name__

  def append(self, TheItem):
    '''
    @param TheItem: the item to append to the collection
    @type  TheItem: instance of metaTestItem or any of its subclasses
    appends TheItem to its child collection
    '''
    TheItem.parent = self
    TheItem.suite = self.suite
    TheItem.XMLwriter = self.suite.XMLwriter
    TheItem.testFontList = self.testFontList
    self._childs.append(TheItem)

#----------------------------------------------------------------------------
class TestSuite(metaTestItem):
  '''
  Collection of all TestBlocks
  '''
  def __init__(self, TheOutPath='', TheFontList=[]):
    metaTestItem.__init__(self, 'fontQA', 'fontQA')
    if TheOutPath != '':
      self.OutPath = TheOutPath
    else:
      self.OutPath = os.path.join(fl.path, 'fontQA_report.xml')
    self.suite = self
    self.showReport = True
    if TheFontList == [] and len(fl) > 0:
      for i in range(len(fl)):
        self.testFontList.append(fl[i])
    else:
      self.testFontList = TheFontList
    self.testBlockList = self._childs

  def addBlock(self, TheName, TheTag):
    m = re.search(r"\W", TheTag)
    if m:
      raise ValueError, 'Second parameter has to contain only alphanumeric characters ( \w or [a-zA-Z0-9_] ) .'
    result = TestBlock(TheName, TheTag)
    self.append(result)
    return result
    
  def showDialog(self):
    self.dialog = SuiteDialog(self)
    result = self.dialog.Run()
    if result == 1:
      for anyBlock in self.testBlockList:
        anyBlock.isSelected = getattr(self.dialog, anyBlock.tag)
      self.OutPath = self.dialog.OutPath
      self.showReport = self.dialog.openInBrowser
    return result

  def doTest(self):
    go_on = False
    if len(fl) > 0:
      if self.OutPath == '':
        if self.showDialog == OK:
          go_on = True
      else:
        if os.path.isdir(os.path.dirname(self.OutPath)):
          go_on = True
    if go_on:
      fl.BeginProgress('checking fonts', len(self))
      self.XMLwriter = XMLWriter(self.OutPath, self.indentStr)
      procInst = '<?xml-stylesheet type="text/xsl" href="%s"?>' % XSL_FileName
      self.XMLwriter.writeraw(procInst)
      self.XMLwriter.newline()
      timeStr = time.strftime('%Y.%m.%d-%H:%M:%S', time.localtime())
      self.XMLwriter.begintag(self.name, RunDateTime=timeStr)
      self.XMLwriter.newline()
      self.XMLwriter.begintag('FontList')
      self.XMLwriter.newline()
      for anyFont in self.testFontList:
        self.XMLwriter.simpletag('Font', 
                                  FullName=anyFont.full_name, 
                                  Path=anyFont.file_name)
        self.XMLwriter.newline()
      self.XMLwriter.endtag('FontList')
      self.XMLwriter.newline()
      self.XMLwriter.begintag('TestSuite')
      self.XMLwriter.newline()
      counter = 1
      for anyBlock in self.testBlockList:
        if anyBlock.isSelected:
          anyBlock.XMLwriter = self.XMLwriter
          anyBlock._doTest()
        fl.TickProgress(counter)
        counter += 1
      self.XMLwriter.endtag('TestSuite')
      self.XMLwriter.newline()
      self.XMLwriter.endtag(self.name)
      self.XMLwriter.newline()
      self.XMLwriter.close()
      fl.EndProgress()
      styleSheetTargetPath = os.path.join(os.path.dirname(self.OutPath), XSL_FileName)
      if os.path.isfile(styleSheetTargetPath):
        os.remove(styleSheetTargetPath)
      shutil.copy2(XSL_FilePath, styleSheetTargetPath)
      if self.showReport:
        webbrowser.open(self.OutPath)


#----------------------------------------------------------------------------
class TestBlock(metaTestItem):
  '''
  Collection of TestsItems
  '''
  def __init__(self, TheName, TheTag):
    metaTestItem.__init__(self, TheName, TheTag)
    self.testItemList = self._childs

  def addItem(self, TheItem):
    result = TheItem()
    self.append(TheItem())
    return result

  def _doTest(self):
    #print self.name
    self.XMLwriter.begintag(self.className(), name=self.name, tag=self.tag)
    self.XMLwriter.newline()
    for anyItem in self.testItemList:
      anyItem.XMLwriter = self.XMLwriter
      anyItem._doTest()
    self.XMLwriter.endtag(self.className())
    self.XMLwriter.newline()



#----------------------------------------------------------------------------
class TestItem(metaTestItem):
  '''
  Meta class for a test
  '''
  def __init__(self, TheName):
    metaTestItem.__init__(self, TheName, self.className())
    self._childs        = self.testFontList
    self.XMLwriter      = self.suite.XMLwriter
    self.ErrorMessages  = {Nothing:'-', 
                           Info:'-', 
                           Passed:'-', 
                           Warn:'-', 
                           Error:'-', 
                           Abort:'Test aborted'}
    self.DetailMessages = {Nothing:'', 
                           Info:'', 
                           Passed:'', 
                           Warn:'', 
                           Error:'', 
                           Abort:''}
    self.ErrorDetails   = ''
    self.testResultList = []
    self.testReportList = []
    self.testFail       = Error
    self.testPass       = Passed
    self.done           = False

  def __len__(self):
    '''
    Implementation of the built-in function len().
    @return: Number of child objects.
    @rtype:  integer
    '''
    if self.testFontList:
      return len(self.testFontList)
    else:
      return 0

  def ErrorNum(self):
    '''
    @return: highest error number from the test of all fonts
    @rtype:  integer
    '''
    ErrorNumList = []
    for anyTestReport in self.testReportList:
      ErrorNumList.append(anyTestReport['ErrorNum'])
    return max(ErrorNumList)

  def ErrorType(self):
    '''
    @return: type of the highest error from the test of all fonts
    @rtype:  string (N, I, P, W, E or A)
    '''
    return ErrorTypes[self.ErrorNum()]

  def ErrorMessage(self):
    '''
    @return: Message of the highest error from the test of all fonts
    @rtype:  string
    '''
    return self.ErrorMessages[self.ErrorNum()]

  def _testFonts(self):
    '''
    Calls the '_testFonts()' method for every font and 
    appends the return value to 'testResultList'
    '''
    for anyFont in self.testFontList:
      self.testResultList.append(self._tryTest(anyFont))
    self.done = True

  def _tryTest(self, TheFont):
    result = None
    if len(TheFont.glyphs) == 0:
      return result
    try:
      result = self._testFont(TheFont)
    except:
      l = traceback.format_tb(sys.exc_info()[2])
      s = l[-1]
      result = [Abort, str(sys.exc_info()[1]), s]
      traceback.print_exc()
    return result
      
  def _testFont(self, TheFont):
    '''
    This should be overwritten by subclasses.
    It should implement the test of a single font
    '''
    return None

  def _summarizeTests(self):
    '''
    This should be overwritten by subclasses
    '''
    pass

  def _writeReport(self):
    self.XMLwriter.begintag('TestItem',
                            name=self.name,
                            tag=self.tag,
                            ErrorType=self.ErrorType(),
                            Message=self.ErrorMessage(),
                            Details=self.ErrorDetails)
    self.XMLwriter.newline()
    if self.__doc__:
      self.XMLwriter.begintag('Description')
      self.XMLwriter.newline()
      self.XMLwriter.write(self.__doc__)
      self.XMLwriter.newline()
      self.XMLwriter.endtag('Description')
      self.XMLwriter.newline()
    for i in range(len(self.testFontList)):
      self.XMLwriter.simpletag('TestDetail',
                    FontName=self.testFontList[i].full_name,
                    ErrorType=ErrorTypes[self.testReportList[i]['ErrorNum']],
                    Message=self.testReportList[i]['Message'],
                    Details=self.testReportList[i]['Details'])
      self.XMLwriter.newline()
    self.XMLwriter.endtag('TestItem')
    self.XMLwriter.newline()

  def _doTest(self):
    self._testFonts()
    self._summarizeTests()
    self._writeReport()


#----------------------------------------------------------------------------
class simpleTest(TestItem):
  '''
  A base class for a simple fonttest
  '''
  def _summarizeTests(self):
    for i in range(len(self)):
      detailReport = {}
      detailReport['FontName'] = self.testFontList[i].full_name
      if self.testResultList[i] == None:
        detailReport['ErrorNum'] = Info
        if self.DetailMessages[Info]:
          detailReport['Message']  = self.DetailMessages[Info]
        else:
          detailReport['Message']  = self.ErrorMessages[Info]
        detailReport['Details']  = '-'
      elif self.testResultList[i] == []:
        detailReport['ErrorNum'] = self.testPass
        if self.DetailMessages[Info]:
          detailReport['Message']  = self.DetailMessages[self.testPass]
        else:
          detailReport['Message']  = self.ErrorMessages[self.testPass]
        detailReport['Details']  = '-'
      elif type(self.testResultList[i]) == ListType and \
           len(self.testResultList[i]) == 3 and \
           self.testResultList[i][0] == Abort:
        detailReport['ErrorNum'] = Abort
        detailReport['Message']  = self.testResultList[i][1]
        detailReport['Details']  = self.testResultList[i][2]
      else:
        detailReport['ErrorNum'] = self.testFail
        if self.DetailMessages[Info]:
          detailReport['Message']  = self.DetailMessages[self.testFail]
        else:
          detailReport['Message']  = self.ErrorMessages[self.testFail]
        detailReport['Details'] = ', '.join(self.testResultList[i])
      self.testReportList.append(detailReport)


#----------------------------------------------------------------------------
class MatchValue(TestItem):
  '''
  A required value is calculated for every font
  '''
  def __init__(self, TheValueName):
    TestItem.__init__(self, TheValueName)
    self.ValueName = TheValueName
    self.ErrorMessages[Passed] = 'All ' + self.ValueName + \
                                 ' values are matching the calculated value'
    self.ErrorMessages[Error]  = 'Not all ' + self.ValueName + \
                                 ' values are matching the required value'
    self.ErrorMessages[Warn]   = 'Not all ' + self.ValueName + \
                                 ' values are matching the recommended value'

  def _getRequiredValue(self, TheFont=None):
    return None

  def _summarizeTests(self):
    for i in range(len(self)):
      detailReport = {}
      detailReport['FontName'] = self.testFontList[i].full_name
      detailReport['Message']  = str(self.ValueName)
      requiredValue = self._getRequiredValue(self.testFontList[i])
      if self.testResultList[i] == requiredValue:
        detailReport['ErrorNum'] = self.testPass
        if self.testFail == Error:
          detailReport['Message'] = 'The ' + self.ValueName + \
                                    ' value matches the required value'
        else:
          detailReport['Message'] = 'The ' + self.ValueName + \
                                    ' value matches the recommended value'
        detailReport['Details'] = self.ValueName + ': ' + str(self.testResultList[i])
      else:
        detailReport['ErrorNum'] = self.testFail
        if self.testFail == Error:
          detailReport['Message'] = 'The ' + self.ValueName + \
                                    ' value does not match the required value'
          detailReport['Details'] = self.ValueName + ': ' + \
                                    str(self.testResultList[i]) + \
                                    ', required: ' + str(requiredValue)
        else:
          detailReport['Message'] = 'The ' + self.ValueName + \
                                    ' value does not match the recommended value'
          detailReport['Details'] = self.ValueName + ': ' + \
                                    str(self.testResultList[i]) + \
                                    ', recommended: ' + str(requiredValue)
      self.testReportList.append(detailReport)


#----------------------------------------------------------------------------
class allMatchOneValue(MatchValue):
  def __init__(self, TheValueName):
    MatchValue.__init__(self, TheValueName)

  def _summarizeTests(self):
    RequiredValue = self._getRequiredValue()
    self.ErrorDetails = str(RequiredValue)
    for i in range(len(self)):
      detailReport = {}
      detailReport['FontName'] = self.testFontList[i].full_name
      detailReport['Message']  = str(self.ValueName)
      if self.testResultList[i] == RequiredValue:
        detailReport['ErrorNum'] = self.testPass
      else:
        detailReport['ErrorNum'] = self.testFail
      detailReport['Details'] = str(self.testResultList[i])
      self.testReportList.append(detailReport)


#----------------------------------------------------------------------------
class allValuesEqual(TestItem):
  def __init__(self, TheValueName):
    TestItem.__init__(self, 'equal '+TheValueName)
    self.ValueName = TheValueName
    self.ErrorMessages[Passed] = 'All '     + self.ValueName + \
                                 ' values are equal.'
    self.ErrorMessages[Error]  = 'Not all ' + self.ValueName + \
                                 ' values are equal, which is required'
    self.ErrorMessages[Warn]   = 'Not all ' + self.ValueName + \
                                 ' values are equal, which is recommended'
    self.ResultDict = {}

  def ErrorNum(self):
    if len(self.ResultDict) == 1:
      return self.testPass
    else:
      return self.testFail

  def _summarizeTests(self):
    for i in range(len(self)):
      detailReport = {}
      detailReport['FontName'] = self.testFontList[i].full_name
      detailReport['ErrorNum'] = Nothing
      detailReport['Message']  = self.ValueName
      detailReport['Details'] = str(self.testResultList[i])
      self.testReportList.append(detailReport)
      if self.ResultDict.has_key(self.testResultList[i]):
        self.ResultDict[self.testResultList[i]] += 1
      else:
        self.ResultDict[self.testResultList[i]] = 1
    if self.ErrorNum() == self.testPass:
      self.ErrorDetails   = str(self.testResultList[0])
    else:
      for anyKey in self.ResultDict:
        self.ErrorDetails += str(self.ResultDict[anyKey]) + ' x ' + str(anyKey) + ', '
      self.ErrorDetails = self.ErrorDetails[:-2]


#----------------------------------------------------------------------------
class RangeCheck(TestItem):
  '''
  The valid valuerange is calculated for every font
  '''
  def __init__(self, TheValueName):
    TestItem.__init__(self, TheValueName)
    self.ValueName = TheValueName
    self.ErrorMessages[Passed] = 'All ' + self.ValueName + \
                                 ' values are in the calculated range'
    self.ErrorMessages[Error]  = 'Not all ' + self.ValueName + \
                                 ' values are in the required range'
    self.ErrorMessages[Warn]   = 'Not all ' + self.ValueName + \
                                 ' values are in the recommended range'

  def _getMinValue(self, TheFont=None):
    return None

  def _getMaxValue(self, TheFont=None):
    return None

  def _summarizeTests(self):
    for i in range(len(self)):
      detailReport = {}
      detailReport['FontName'] = self.testFontList[i].full_name
      detailReport['Message']  = str(self.ValueName)
      minVal = self._getMinValue(self.testFontList[i])
      maxVal = self._getMaxValue(self.testFontList[i])
      if self.testResultList[i] >= minVal and self.testResultList[i] <= maxVal:
        detailReport['ErrorNum'] = self.testPass
        if self.testFail == Error:
          detailReport['Message'] = 'The ' + self.ValueName + \
                                    ' value is in the required range'
        else:
          detailReport['Message'] = 'The ' + self.ValueName + \
                                    ' value is in the recommended range'
        detailReport['Details'] = self.ValueName + ': ' + str(self.testResultList[i])
      else:
        detailReport['ErrorNum'] = self.testFail
        if self.testFail == Error:
          detailReport['Message'] = 'The ' + self.ValueName + \
                                    ' value is not in the required range'
          detailReport['Details'] = self.ValueName + ': ' + \
                                    str(self.testResultList[i]) + \
                                    ', required: (' + str(minVal) + ' - ' + str(maxVal) + ')'
        else:
          detailReport['Message'] = 'The ' + self.ValueName + \
                                    ' value is not in the recommended range'
          detailReport['Details'] = self.ValueName + ': ' + \
                                    str(self.testResultList[i]) + \
                                    ', recommended: (' + str(minVal) + ' - ' + str(maxVal) + ')'
      self.testReportList.append(detailReport)


#----------------------------------------------------------------------------
class FamilyStatistic(TestItem):
  def __init__(self, TheValueName):
    TestItem.__init__(self, TheValueName)
    self.ValueName = TheValueName
    self.ErrorMessages[Info] ='Family Statistic'

  def _summarizeTests(self):
    if type(self.testResultList) is ListType and len(self.testResultList) > 0:
      if len(self.testResultList) == len(self):
        fontsNoAnalysisError = []
        fontsAnalysisError = []
        for i in range(len(self.testResultList)):
          try:
            int(self.testResultList[i])
            fontsNoAnalysisError.append(i)
          except:
            fontsAnalysisError.append(i)
        
        if fontsAnalysisError == []:
          _max = int(max(self.testResultList))
          _min = int(min(self.testResultList))
          _rng = int(abs(_max - _min))
          _avg = int(round(average(self.testResultList)))
          _sdv = int(round(StdDeviation(self.testResultList)))
          for i in range(len(self)):
            detailReport = {}
            detailReport['Message']  = self.ValueName
            detailReport['FontName'] = self.testFontList[i].full_name
            detailReport['ErrorNum'] = Info
#            if abs(self.testResultList[i] - _avg) > _sdv * 1.5:
#              detailReport['ErrorNum'] = Error
#            elif abs(self.testResultList[i] - _avg) > _sdv * 1.2:
#              detailReport['ErrorNum'] = Warn
#            else:
#              detailReport['ErrorNum'] = Info
            try:
              detailReport['Details'] = str(int(self.testResultList[i]))
            except:
              detailReport['Details'] = 'FamilyStatistic is not applicable because font contains no glyphs.'
            self.testReportList.append(detailReport)
          self.ErrorDetails   = 'min: ' + str(_min) + ', max: ' + str(_max) + ', rng: ' + str(_rng) + ', avg: ' + str(_avg) + ', sdv: '+ str(_sdv)
        else:
          for i in range(len(self.testResultList)):
            if i in fontsAnalysisError:
              detailReport = {}
              detailReport['Message']  = self.ValueName
              detailReport['FontName'] = self.testFontList[i].full_name
              detailReport['ErrorNum'] = Error
              detailReport['Details'] = 'FamilyStatistic is not applicable because at least one font contains no glyphs or glyphs have no outlines.'
              self.testReportList.append(detailReport)
            elif i in fontsNoAnalysisError:
              detailReport = {}
              detailReport['Message']  = self.ValueName
              detailReport['FontName'] = self.testFontList[i].full_name
              detailReport['ErrorNum'] = Warn
              detailReport['Details'] = 'FamilyStatistic is not applicable because at least one other opened font(s) contains no glyphs or glyphs have no outlines.'
              self.testReportList.append(detailReport)
      else:
        raise Exception 
    else:
      detailReport = {}
      detailReport['Message']  = self.ValueName
      detailReport['ErrorNum'] = Error
      detailReport['Details']  = 'FamilyStatistic is not applicable because font contains no glyphs.'
      detailReport['FontName'] = self.testFontList.full_name
      self.ErrorDetails   = 'FamilyStatistic is not applicable because font contains no glyphs.'
      self.testReportList.append(detailReport)



#----------------------------------------------------------------------------
class FontStatistic(TestItem):
  def __init__(self, TheValueName):
    TestItem.__init__(self, TheValueName)
    self.ValueName = TheValueName
    self.ErrorMessages[Info] ='Font Statistic'

  def ErrorNum(self):
    return Info

  def _summarizeTests(self):
    for i in range(len(self)):
      #print '-',self.testResultList[i], '-'
      if type(self.testResultList[i]) is ListType and len(self.testResultList[i]) > 0:
        _max = int(max(self.testResultList[i]))
        _min = int(min(self.testResultList[i]))
        _rng = int(abs(_max - _min))
        _avg = int(round(average(self.testResultList[i])))
        _sdv = int(round(StdDeviation(self.testResultList[i])))
        detailReport = {}
        detailReport['FontName'] = self.testFontList[i].full_name
        detailReport['ErrorNum'] = Info
        detailReport['Message']  = self.ValueName
        detailReport['Details'] = 'min: ' + str(_min) + ', max: ' + str(_max) + ', rng: ' + str(_rng) + ', avg: ' + str(_avg) + ', sdv: '+ str(_sdv)
      else:
        detailReport = {}
        detailReport['FontName'] = self.testFontList[i].full_name
        detailReport['ErrorNum'] = Warn
        detailReport['Message']  = self.ValueName
        detailReport['Details'] = 'FontStatistic is not applicable because font contains no glyphs or glyphs have no outlines.'
      self.testReportList.append(detailReport)


#----------------------------------------------------------------------------
class GlyphTest(TestItem):
  def __init__(self, TheValueName):
    TestItem.__init__(self, TheValueName)
#   self.ErrorMessages[Info]   = '-'
#   self.ErrorMessages[Passed] = '-'
#   self.ErrorMessages[Warn]   = '-'
#   self.ErrorMessages[Error]  = '-'
#   self.DetailMessages = {}
#   self.DetailMessages[Info]   = '-'
#   self.DetailMessages[Passed] = '-'
#   self.DetailMessages[Warn]   = '-'
#   self.DetailMessages[Error]  = '-'

  def _summarizeTests(self):
    for i in range(len(self)):
      detailReport = {}
      detailReport['FontName'] = self.testFontList[i].full_name
      if self.testResultList[i] == None:
        detailReport['ErrorNum'] = Info
        if self.DetailMessages[Info]:
          detailReport['Message']  = self.DetailMessages[Info]
        else:
          detailReport['Message']  = self.ErrorMessages[Info]
        detailReport['Details']  = '-'
      elif self.testResultList[i] == []:
        detailReport['ErrorNum'] = self.testPass
        if self.DetailMessages[Info]:
          detailReport['Message']  = self.DetailMessages[self.testPass]
        else:
          detailReport['Message']  = self.ErrorMessages[self.testPass]
        detailReport['Details']  = '-'
      elif self.testResultList[i][0] == Abort:
        detailReport['ErrorNum'] = Abort
        detailReport['Message']  = self.testResultList[i][1]
        detailReport['Details']  = self.testResultList[i][2]
      else:
        detailReport['ErrorNum'] = self.testFail
        if self.DetailMessages[self.testFail]:
          detailReport['Message'] = self.DetailMessages[self.testFail]
        else:
          detailReport['Message'] = self.ErrorMessages[self.testFail]
        myDetail = ''
        for anyGlyphName in self.testResultList[i]:
          myDetail += anyGlyphName + ', '
        detailReport['Details']  = myDetail[:-2]
      self.testReportList.append(detailReport)

print shortNotice

#EOF
