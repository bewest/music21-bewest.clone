#!/usr/bin/python
#-------------------------------------------------------------------------------
# Name:         environment.py
# Purpose:      Storage for user environment settings and defaults
#
# Authors:      Christopher Ariza
#               Michael Scott Cuthbert
#
# Copyright:    (c) 2009 The music21 Project
# License:      LGPL
#-------------------------------------------------------------------------------


import os, sys
import tempfile
import doctest, unittest
import xml.sax

import music21
from music21 import common
from music21 import node


_MOD = 'environment.py'


#-------------------------------------------------------------------------------
class EnvironmentException(Exception):
    pass





#-------------------------------------------------------------------------------
class Settings(node.NodeList):
    '''
    '''
    def __init__(self):
        '''
        >>> a = Settings()
        '''
        node.NodeList.__init__(self)
        self._tag = 'settings' # assumed for now
        self.componentList = [] # list of Part objects

    def _getComponents(self):
        return self.componentList


class Preference(node.Node):
    '''
    '''
    def __init__(self):
        '''
        >>> a = Preference()
        '''
        node.Node.__init__(self)
        self._tag = 'preference' # assumed for now
        # attributes
        self._attr['name'] = None
        self._attr['value'] = None



#-------------------------------------------------------------------------------
class SettingsHandler(xml.sax.ContentHandler):
    '''
    >>> a = SettingsHandler()
    '''
    def __init__(self, tagLib=None):
        self.storage = Settings()        

    def startElement(self, name, attrs):
        if name == 'preference':        
            slot = Preference()
            slot.loadAttrs(attrs)
            self.storage.append(slot)

    def getSettings(self):
        return self.storage


#-------------------------------------------------------------------------------
class Environment(object):
    '''Environment stores platform-specific, user preferences
    '''

    def __init__(self, modName=None):
        '''
        >>> a = Environment()
        '''
        self.ref = {}
        self.loadDefaults() # defines all valid keys in ref
        # read will only right over values if set in field
        self.read()
        # store the name of the module that is using this object
        # this is used for printing debug information
        self.modNameParent = modName


    def loadDefaults(self):
        '''Keys are derived from these defaults
        '''
        self.ref['directoryScratch'] = None # will use temp files
        self.ref['lilypondPath'] = None # path to lilypond
        self.ref['lilypondVersion'] = None # version of lilypond
        self.ref['lilypondFormat'] = 'pdf' 
        self.ref['lilypondBackend'] = 'ps' 
        self.ref['musicxmlPath'] = None # path to a musicxml reader
        self.ref['midiPath'] = None # path to a midi reader
        self.ref['graphicsPath'] = None # path to a graphcis viewer
        self.ref['debug'] = 0


        platform = common.getPlatform()

        if platform == 'win':
            for name, value in [
                ('lilypondPath', 'lilypond'),
                ]:
                self.__setitem__(name, value) # use for key checking
        elif platform == 'nix':
            for name, value in [('lilypondPath', 'lilypond')]:
                self.__setitem__(name, value) # use for key checking
        elif platform ==  'darwin':
            for name, value in [
                ('lilypondPath', '/Applications/Lilypond.app/Contents/Resources/bin/lilypond'),
                ('musicxmlPath', '/Applications/Finale Reader/Finale Reader.app'),
                ('graphicsPath', '/Applications/Preview.app'),
                ]:
                self.__setitem__(name, value) # use for key checking

    def __getitem__(self, key):
        '''Dictionary like getting. 
        '''
        # could read file here to update from disk
        # could store last update tiem and look of file is more recent
        #self.read()
        if key not in self.ref.keys():
            raise EnvironmentException('no preference: %s' % key)
        value = self.ref[key]
        valueStr = str(value).lower()

        if key in ['debug']: # debug expects a number
            if valueStr == 'true':
                value = common.DEBUG_USER
            elif valueStr == 'false':
                value = common.DEBUG_OFF
            elif 'off' in valueStr:
                value = common.DEBUG_OFF
            elif 'user' in valueStr:
                value = common.DEBUG_USER
            elif 'devel' in valueStr:
                value = common.DEBUG_DEVEL
            elif 'all' in valueStr:
                value = common.DEBUG_ALL
            else:
                value = int(value)
        if value == '':
            value = None # return None for values not set
        return value

    def __setitem__(self, key, value):
        '''Dictionary-like setting. Changes are made only to local dictonary.
        Music call  write() to make permanant

        >>> a = Environment()
        >>> a['debug'] = 1
        >>> a['graphicsPath'] = '/test&Encode'
        >>> a['graphicsPath']
        '/test&amp;Encode'
        '''
        #saxutils.escape # used for escaping strings going to xml
        # with unicode encoding
        # http://www.xml.com/pub/a/2002/11/13/py-xml.html?page=2
        # saxutils.escape(msg).encode('UTF-8')

        if key not in self.ref.keys():
            raise EnvironmentException('no preference: %s' % key)
        if value == '':
            value = None # always replace '' with None
        if common.isStr(value):
            value = xml.sax.saxutils.escape(value).encode('UTF-8')
        self.ref[key] = value

    def __repr__(self):
        return repr(self.ref)

    def keys(self):
        return self.ref.keys()

    #---------------------------------------------------------------------------
    def getSettingsPath(self):
        '''Return the path to the platform specific settings file.
        '''
        platform = common.getPlatform()
        if platform == 'win':
            # try to use defined app data directory for preference file
            # this is not available on all windows versions
            if 'APPDATA' in os.environ.keys():
                dir = os.environ['APPDATA']
            elif ('USERPROFILE' in os.environ.keys() and
                os.path.exists(os.path.join(
                os.environ['USERPROFILE'], 'Application Data'))):
                dir = os.path.join(os.environ['USERPROFILE'], 
                                   'Application Data')
            else: # use home directory
                dir = os.path.expanduser('~')       
            return os.path.join(dir, 'music21-settings.xml')
        elif platform in ['nix', 'darwin']:
            # alt : os.path.expanduser('~') 
            dir = os.environ['HOME']
            return os.path.join(dir, '.music21rc')

        # darwin specific option
        # os.path.join(os.environ['HOME'], 'Library',)

     

    #---------------------------------------------------------------------------
    def read(self, fp=None):
        '''Load from an XML file if and only if available and has been 
        written in the past. This means that no preference file will ever be 
        written unless manually done so. 
        '''
        if fp == None:
            fp = self.getSettingsPath()
        if not os.path.exists(fp):
            return None # do nothing if no file exists

        saxparser = xml.sax.make_parser()
        saxparser.setFeature(xml.sax.handler.feature_external_ges, 0)
        saxparser.setFeature(xml.sax.handler.feature_external_pes, 0)
        saxparser.setFeature(xml.sax.handler.feature_namespaces, 0)  
    
        h = SettingsHandler() 
        saxparser.setContentHandler(h)
        f = open(fp) # file i/o might be done outside of loop
        saxparser.parse(f)
        f.close()    

        # load from XML into dictionary
        storage = h.getSettings()
        for slot in storage:
            name = slot.get('name')
            value = slot.get('value')
            if name not in self.ref.keys():
                continue
                # do not set, ignore for now
                #raise EnvironmentException('no such defined preference: %s' % name)
            else:
                self.ref[name] = value

    def write(self, fp=None):
        '''Write an XML file.

        This must be manually called to store preferences. 
        
        fp is the file path.
        preferences are stored in self.ref
        '''
        if fp == None:
            fp = self.getSettingsPath()

        # need to use __getitem__ here b/c need to covnert debug value
        # to an integer
        self.printDebug([_MOD, 'writing preference file', self.ref])


        dir, fn = os.path.split(fp)
        if fp == None or not os.path.exists(dir):
            raise EnvironmentException('bad file path: %s' % fp)

        storage = Settings()
        for key, item in self.ref.items():
            slot = Preference()
            slot.set('name', key)
            slot.set('value', item)
            storage.append(slot)

        f = open(fp, 'w')
        f.write(storage.xmlStr())
        f.close()

    #---------------------------------------------------------------------------
    # utility methods for commonly needed OS services

    def getTempFile(self, suffix=''):
        '''Return a file path to a temporary file with the specified suffix
        '''
        if self.ref['directoryScratch'] == None:
            if common.getPlatform() != 'win':
                fd, fp = tempfile.mkstemp(suffix=suffix) 
                if isinstance(fd, int):
                    pass # see comment below
                else:
                    fd.close()
            else:
                if sys.hexversion < 0x02030000:
                    raise EnvironmentException("Need at least Version 2.3 on Windows to" +
                                               "create temporary files!")
                else:
                    tf = tempfile.NamedTemporaryFile(suffix=suffix)
                    fp = tf.name
                    tf.close()
        else:
            if not os.path.exists(self.ref['directoryScratch']):    
                raise EnvironmentException('user-specified scratch directory (%s) does not exists.' % self.ref['directoryScratch'])
            if common.getPlatform() != 'win':
                fd, fp = tempfile.mkstemp(dir=self.ref['directoryScratch'], 
                                          suffix=suffix)
                if isinstance(fd, int):
                    # on MacOS, fd returns an int, like 3, when this is called
                    # in some context (specifically, programmatically in a 
                    # TestExternal class. the fp is still valid and works
                    pass
                else:
                    fd.close() 
            else: # win
                if sys.hexversion < 0x02030000:
                    raise EnvironmentException("Need at least Version 2.3 on Windows to" +
                                               "create temporary files!")
                else:
                    tf = tempfile.NamedTemporaryFile(
                                dir=self.ref['directoryScratch'], 
                                suffix=suffix)
                    fp = tf.name
                    tf.close()

        self.printDebug([_MOD, 'temporary file:', fp])
        return fp


    
    def launch(self, fmt, fp, options=''):
        '''Open a file with an application specified by a preference (?)
        
        Optionally, can add additional command to erase files, if necessary 
        Erase could be called from os or command-line arguemtns after opening
        the file and then a short time delay.

        TODO: Move showImageDirectfrom lilyString.py ; add MIDI
        '''
        # see common.fileExtensions for format names 
        format, ext = common.findFormat(fmt)
        if format == 'lilypond':
            fpApp = self.ref['lilypondPath']
        elif format in ['png', 'jpeg']:
            fpApp = self.ref['graphicsPath']   
        elif format == 'musicxml':
            fpApp = self.ref['musicxmlPath']   


        platform = common.getPlatform()
        if fpApp is None and platform != 'win':
            raise EnvironmentException("Cannot find an application for format %s, specify this in your environment", fmt)
        
        if platform == 'win':
            # no need to specify application here: windows starts the program based on the file extension
            cmd = 'start %s' % (fp)
        elif platform == 'darwin':
            cmd = 'open -a"%s" %s %s' % (fpApp, options, fp)
        elif platform == 'nix':
            cmd = '%s %s %s' % (fpApp, options, fp)
        os.system(cmd)


    
    def printDebug(self, msg, statusLevel=common.DEBUG_USER):
        '''Format one or more data elements into string suitable for printing
        straight to stderr or other outputs.
    
        The first arg can be a list of string; lists are concatenated with common.formatStr(). 
        '''
        if not common.isNum(statusLevel):
            raise EnvironmentException('bad statusLevel argument given: %s' % statusLevel)

        if common.isStr(msg):
            msg = [msg] # make into a list
        if msg[0] != self.modNameParent and self.modNameParent != None:
            msg = [self.modNameParent] + msg

        msg = common.formatStr(*msg)
        if self.__getitem__('debug') >= statusLevel:
            sys.stderr.write(msg)
    



#-------------------------------------------------------------------------------
class Test(unittest.TestCase):
    '''Unit tests
    '''

    def setUp(self):
        pass

    def runTest(self):
        pass

    def testTest(self):
        self.assertEqual(1, 1)

    def testSettings(self):

        storage = Settings()
        for i in range(10):
            slot = Preference()
            slot.set('name', 'name%s' % i)
            slot.set('value', i)
            storage.append(slot)
    
        self.assertEqual("""<?xml version="1.0" encoding="utf-8"?>
<settings>
  <preference name="name0" value="0"/>
  <preference name="name1" value="1"/>
  <preference name="name2" value="2"/>
  <preference name="name3" value="3"/>
  <preference name="name4" value="4"/>
  <preference name="name5" value="5"/>
  <preference name="name6" value="6"/>
  <preference name="name7" value="7"/>
  <preference name="name8" value="8"/>
  <preference name="name9" value="9"/>
</settings>
""", storage.xmlStr())


#-----------------------------------------------------------------||||||||||||--
if __name__ == "__main__":
    music21.mainTest(Test)