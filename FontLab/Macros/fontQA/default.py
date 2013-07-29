#FLM: fontQA default testsuite

from FL import *
from fontQAlib import TestSuite
from fontQA_Names import *
from fontQA_Outline import *
from fontQA_Vmetric import *
from fontQA_Hmetric import *
from fontQA_Kerning import *
from fontQA_GnameUni import *
from fontQA_Grepertoire import *
from fontQA_Composites import *
from fontQA_Hints import *

mySuite = TestSuite()

Name_Tests = mySuite.addBlock('Names and Identification', 'Name_Ident')
Name_Tests.addItem(lead_trai_space)
Name_Tests.addItem(double_space)
Name_Tests.addItem(hyphen_Name)

Outline_Tests = mySuite.addBlock('Outline', 'Outline')
Outline_Tests.addItem(Contour_Statistic)
Outline_Tests.addItem(Node_Statistic)
Outline_Tests.addItem(Area_Statistic)
Outline_Tests.addItem(MinContourLength)
Outline_Tests.addItem(MinContourArea)
Outline_Tests.addItem(ExtremumPoint)
Outline_Tests.addItem(UnnecInflect)
Outline_Tests.addItem(UnnecExtreme)

V_Metric_Tests = mySuite.addBlock('Vertical Metrics', 'V_metric')
V_Metric_Tests.addItem(Ymin_Statistic)
V_Metric_Tests.addItem(Ymax_Statistic)
V_Metric_Tests.addItem(UPM_Test)
V_Metric_Tests.addItem(Equal_Ascender)
V_Metric_Tests.addItem(Equal_Descender)
V_Metric_Tests.addItem(TypoAscender)
V_Metric_Tests.addItem(TypoDescender)
V_Metric_Tests.addItem(Equal_TypoLineGap)
V_Metric_Tests.addItem(WinAscent)
V_Metric_Tests.addItem(WinDescent)
V_Metric_Tests.addItem(hhea_Ascender)
V_Metric_Tests.addItem(hhea_Descender)
V_Metric_Tests.addItem(height_test)

H_Metric_Tests = mySuite.addBlock('Horizontal Metrics', 'H_metric')
H_Metric_Tests.addItem(Width_Statistic)
H_Metric_Tests.addItem(LSB_Statistic)
H_Metric_Tests.addItem(RSB_Statistic)
H_Metric_Tests.addItem(LSB_test)
H_Metric_Tests.addItem(RSB_test)

Kerning_Tests = mySuite.addBlock('Kerning', 'Kerning')
Kerning_Tests.addItem(KernCount)

G_name_uni_Tests = mySuite.addBlock('Glyphnames and Unicode', 'G_name_uni')
G_name_uni_Tests.addItem(startNumber)
G_name_uni_Tests.addItem(startUnderscore)
G_name_uni_Tests.addItem(multiDotName)
G_name_uni_Tests.addItem(DotName_noUnicode)
G_name_uni_Tests.addItem(UnderscoreName_noUnicode)
G_name_uni_Tests.addItem(UniName_UniCode)
G_name_uni_Tests.addItem(UnicodeDoublemapping)
G_name_uni_Tests.addItem(doubleGlyphnames)
G_name_uni_Tests.addItem(doubleUnicode)
G_name_uni_Tests.addItem(GlyphNameExtensions)

GlyphRepertoire = mySuite.addBlock('Glyph-Repertoire', 'GlyphRepertoire')
GlyphRepertoire.addItem(GlyphCount)
GlyphRepertoire.addItem(EncodedChars)
GlyphRepertoire.addItem(missingInOne)
GlyphRepertoire.addItem(presentInOne)
GlyphRepertoire.addItem(otherMissing)
GlyphRepertoire.addItem(DotNameCounterpart)

Composites = mySuite.addBlock('Composites', 'Composites')
Composites.addItem(CompositeCount)
Composites.addItem(emptyComponent)
Composites.addItem(doubleComponent)
Composites.addItem(overlappingComponent)

Hinting = mySuite.addBlock('Hinting', 'Hinting')
Hinting.addItem(Hint_Check)
Hinting.addItem(NoHint_Check)
Hinting.addItem(VHintBBox)
Hinting.addItem(HHintBBox)

if len(fl) > 0:
  if mySuite.showDialog() == 1:
    mySuite.doTest()
  print 'done'
else:
  print 'Please open fonts to scan in fontlab.'

#EOF
