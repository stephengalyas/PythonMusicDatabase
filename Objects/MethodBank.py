# Import packages.
import os
import datetime
from Objects.LogHandler import LogHandler

class MethodBank:
    '''
    Purpose: defines project-wide variables and methods
    '''
    logHandler = LogHandler()

    @staticmethod
    def initialize():
        MethodBank.logHandler.create(fileName = "Test123.log", writeToConsole = "False")

    @staticmethod
    def projectDataDir():
        '''
        Purpose: returns project data directory. If directory does not exist, creates it.
        '''
        if os.path.exists('C:\\ProgramData\\MusicDatabasePython') == False:
            os.mkdir('C:\\ProgramData\\MusicDirectoryPython')
        return 'C:\\ProgramData\\MusicDatabasePython\\'

    @staticmethod
    def mainDB():
        '''
        Purpose: returns the main database file
        '''
        return MethodBank.projectDataDir() + 'mainDB.db'

    @staticmethod
    def loggingEnabled():
        '''
        Purpose: returns if logging is enabled.
        '''
        return True

    @staticmethod
    def writeToLog(level, message):
        '''
        Purpose: writes a message to the log.
        '''
        MethodBank.logHandler.Write(level, message)

    @staticmethod
    def flushLog():
        '''
        Purpose: flushes the log.
        '''
        MethodBank.logHandler.Flush()
