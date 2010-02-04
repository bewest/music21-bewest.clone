#!/usr/bin/python
#-------------------------------------------------------------------------------
# Name:         conf.py
# Purpose:      Documentation configuration file
#
# Authors:      Michael Scott Cuthbert
#               Christopher Ariza
#
# Copyright:    (c) 2009 The music21 Project
# License:      LGPL
#-------------------------------------------------------------------------------

import sys, os
import unittest, doctest
import music21


# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'contents'

extensions = ['rst2pdf.pdfbuilder']


# General substitutions.
project = 'music21'
release = music21.VERSION_STR
copyright = 'music21 project'


html_last_updated_fmt = '%b %d, %Y'

# Content template for the index page.
html_index = 'index.html'



def _shell():
    '''
    >>> True
    True
    '''
    pass





#-------------------------------------------------------------------------------
class Test(unittest.TestCase):

    def runTest(self):
        pass

    def setUp(self):
        pass

    def testToRoman(self):
        self.assertEqual(True, True)



if __name__ == "__main__":
    import music21
    music21.mainTest(Test)
