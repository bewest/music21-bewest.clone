#!/usr/bin/python
#-------------------------------------------------------------------------------
# Name:         testPerformance.py
# Purpose:      Tests keep track of long-term performance targets
#
# Authors:      Christopher Ariza
#
# Copyright:    (c) 2009-2010 The music21 Project
# License:      LGPL
#-------------------------------------------------------------------------------

'''This method defines a number of performance test. Results for these performances are stored and dated, and used to track long-term performance changes.

This file is not run with the standard test battery presently.
'''


import doctest, unittest

import music21
from music21 import common, corpus

from music21 import environment
_MOD = 'test/testPerformance.py'
environLocal = environment.Environment(_MOD)

#-------------------------------------------------------------------------------
class Test(unittest.TestCase):

    def runTest(self):
        pass


    def runStreamIterationByIterator(self):
        '''Stream iteration by iterator
        '''
        from music21 import note, stream
        # create a stream with 750 notes, 250 rests
        s = stream.Stream()
        for i in range(1000):
            n = note.Note()
            s.append(n)
        for i in range(500):
            r = note.Rest()
            s.append(r)

        for x in range(100):        
            for x in s: # this will create an iterator instances
                pass

    def runStreamIterationByElements(self):
        '''Stream iteration by .elements access
        '''
        from music21 import note, stream
        # create a stream with 750 notes, 250 rests
        s = stream.Stream()
        for i in range(1000):
            n = note.Note()
            s.append(n)
        for i in range(500):
            r = note.Rest()
            s.append(r)

        for x in range(100):        
            for x in s.elements: # this will create an iterator instances
                pass


    def runGetElementsByClassType(self):
        '''Getting elements by class type
        '''
        from music21 import note, stream

        # create a stream with 750 notes, 250 rests
        s = stream.Stream()
        for i in range(1000):
            n = note.Note()
            s.append(n)
        for i in range(500):
            r = note.Rest()
            s.append(r)

        for x in range(2):        
            post = s.flat.getElementsByClass([note.Rest, note.Note])
            self.assertEqual(len(post), 1500)

    def runGetElementsByClassString(self):
        '''Getting elements by string
        '''
        from music21 import note, stream

        # create a stream with 750 notes, 250 rests
        s = stream.Stream()
        for i in range(1000):
            n = note.Note()
            s.append(n)
        for i in range(500):
            r = note.Rest()
            s.append(r)

        for x in range(2):        
            post = s.flat.getElementsByClass(['Rest', 'Note'])
            self.assertEqual(len(post), 1500)


    def runParseBeethoven(self):
        '''Loading file: beethoven/opus59no2/movement3
        '''
        x = corpus.parseWork('beethoven/opus59no2/movement3', forceSource=True)

    def runMusicxmlOutPartsBeethoven(self):
        '''Loading file and rendering musicxml output for each part: beethoven/opus59no2/movement3
        '''
        x = corpus.parseWork('beethoven/opus59no2/movement3', forceSource=True)
        #problem: doing each part is much faster than the whole score
        for p in x.parts:
            post = p.musicxml

    def runMusicxmlOutScoreBeethoven(self):
        '''Loading file and rendering musicxml output of complete score: beethoven/opus59no2/movement3
        '''
        x = corpus.parseWork('beethoven/opus59no2/movement3', forceSource=True)
        #problem: doing each part is much faster than the whole score
        post = x.musicxml

    def runParseHaydn(self):
        '''Loading file: haydn/opus74no1/movement3
        '''
        x = corpus.parseWork('haydn/opus74no1/movement3', forceSource=True)

    def runParseSchumann(self):
        '''Loading file: schumann/opus41no1/movement2
        '''
        x = corpus.parseWork('schumann/opus41no1/movement2', forceSource=True)

    def runParseLuca(self):
        '''Loading file: luca/gloria
        '''
        x = corpus.parseWork('luca/gloria', forceSource=True)


    def runMusicxmlOutLuca(self):
        '''Loading file and rendering musicxml output: luca/gloria
        '''
        x = corpus.parseWork('luca/gloria', forceSource=True)
        post = x.musicxml


    #---------------------------------------------------------------------------
    def testTimingTolerance(self):
        '''Test the performance of methods defined above, comparing the resulting time to the time obtained in past runs. 

        This should not produce errors as such, but is used to provide reference
        if overall performance has changed.
        '''
        # provide work and expected min/max in seconds
        for testMethod, best in [

            (self.runStreamIterationByIterator, 
                {'2010.09.20': 2.2524, 
                }),

            (self.runStreamIterationByElements, 
                {'2010.09.20': 0.8317, 
                }),


            (self.runGetElementsByClassType, 
                {'2010.09.20': 3.28, 
                }),

            (self.runGetElementsByClassString, 
                {'2010.09.20': 3.22, 
                }),

            (self.runParseBeethoven, 
                {'2009.12.14': 7.42, 
                 '2009.12.15': 6.686,
                 '2010.06.24': 7.475,
                 '2010.07.08': 3.562,
                }),

            (self.runMusicxmlOutPartsBeethoven, 
                {'2010.09.20': 7.706, 
                }),

            (self.runMusicxmlOutScoreBeethoven, 
                {'2010.09.20': 33.273, 
                }),


            (self.runParseHaydn, 
                {'2009.12.14': 4.08, 
                 '2009.12.15': 3.531,
                 '2010.06.24': 3.932,
                 '2010.07.08': 1.935,
                }),
            (self.runParseSchumann, 
                {'2009.12.14': 5.88, 
                 '2009.12.15': 5.126,
                 '2010.06.24': 5.799,
                 '2010.07.08': 2.761,
                }),
            (self.runParseLuca, 
                {'2009.12.14': 3.174, 
                 '2009.12.15': 2.954,
                 '2010.06.24': 3.063,
                 '2010.07.08': 1.508,
                }),

            (self.runMusicxmlOutLuca, 
                {'2010.09.20': 8.372, 
                }),


            ]:

            t = common.Timer()
            t.start()
            # call the test
            testMethod()
            t.stop()
            dur = t()
            environLocal.printDebug(['\n\ntiming tolerance for:',     
                str(testMethod.__doc__.strip()), 
                '\nthis run:', dur, '\nbest runs:', 
                ['%s: %s' % (x, y) for x, y in best.items()], '\n'
                ]
            )
            #self.assertEqual(True, dur <= max) # performance test




if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1: # normal conditions
        music21.mainTest(Test)

    elif len(sys.argv) > 1:
        a = Test()
        a.testGetElements()

