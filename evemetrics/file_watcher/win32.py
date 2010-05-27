import sys, os, time, traceback
import win32file
import win32con
import pywintypes
from PyQt4 import QtCore
from PyQt4.QtCore import QThread
import os; 
from .generic import FileMonitor

class Win32FileMonitor( FileMonitor ):
    def __init__( self, factory, path ):
        QThread.__init__(self, factory)
        self.exiting = False
        self.tree = None
        self.path = path
        self.factory = factory
        self.last_run = time.time()
    def __del__(self):
        self.exiting = True
        self.wait()    
    
    def Run( self ):
        # testing stuff
        #self.factory.emit(QtCore.SIGNAL("fileChanged(QString)"), QtCore.QString('C:\\Users\\Dominik\\AppData\\Local\\CCP\\EVE\\e_eve_tranquility\\cache\\MachoNet\\87.237.38.200\\235\\CachedMethodCalls\\757f.cache'))
        #self.factory.emit(QtCore.SIGNAL("fileChanged(QString)"), QtCore.QString('C:\\Users\\Dominik\\AppData\\Local\\CCP\\EVE\\e_eve_tranquility\\cache\\MachoNet\\87.237.38.200\\235\\CachedMethodCalls\\2488.cache'))
        self.start()

    def run( self ):
        try:
            hDir = win32file.CreateFile (
                self.path,
                0x0001,
                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS,
                None
            )
        except pywintypes.error, e:
            print "Invalid cache file path: ", e
            return
    
        while not self.exiting:
            results = win32file.ReadDirectoryChangesW (
                hDir,
                1024,
                False,
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,
                None,
                None
            )
            for action, file in results:
                full_filename = os.path.join (self.path, file)
                #print "ACTION------------------> %s" % action
                if (action == 3):
                    self.factory.emit(QtCore.SIGNAL("fileChanged(QString)"), QtCore.QString(full_filename))

