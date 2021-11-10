# Begin import statements
from sqlite3.dbapi2 import enable_shared_cache
import tempfile
import datetime
from enum import Enum
# End import statements

class LoggingLevel(Enum):
    '''
    Purpose: used to filter log data written to file
    '''
    DISABLED = 0,
    VERBOSE = 1,
    WARNING = 2,
    ERROR = 3

class LogHandler:
    '''
    Purpose: write log data to a file for diagnostics
    '''

    # Begin class and object variables
    LOG_DIRECTORY = tempfile.gettempdir()

    # End class and object variables

    def __init__(self):
        self._fileName = ''  # File name for log file.
        self._loggingLevel = LoggingLevel.DISABLED   # Logging level.
        self._buffer = []    # Logging buffer
        self._writeToConsole = False

    def create(self, **kwargs):
        '''
        Purpose: initialize LogHandler object.
        '''
        try:
            if 'fileName' in kwargs:
                self._fileName = kwargs['fileName']
            else:
                self._fileName = datetime.datetime.now().strftime('%y%m%d_PracticeProject1.log')
            if 'loggingLevel' in kwargs:
                self._loggingLevel = LoggingLevel[str(kwargs['loggingLevel'])]
            else:
                self._loggingLevel = LoggingLevel.WARNING
            if 'writeToConsole' in kwargs:
                self._writeToConsole = str(kwargs['writeToConsole']).lower() == "true"
            else:
                self._writeToConsole = False
        except Exception as exc:
            # Print error and use default values
            print(f'Error in {type(self)} class. Error type: {type(exc)}. Error message: {str(exc)}')
            self._fileName = datetime.datetime.now().strftime('%y%m%d_PracticeProject1.log')
            self._loggingLevel = LoggingLevel.WARNING
        self.Write(LoggingLevel.VERBOSE, 'Log file: ' + self._fileName + ' --- Level: ' + LoggingLevel(self._loggingLevel).name)

    def Write(self, level, message):
        '''
        Purpose: write a log message to the buffer
        '''
        if self._loggingLevel != LoggingLevel.DISABLED:
            logMessage = str(datetime.datetime.now())
            logMessage += ' --- '
            logMessage += LoggingLevel(level).name
            logMessage += ' --- '
            logMessage += str(message)
            self._buffer.append(logMessage)
            if self._writeToConsole == True:
                print(logMessage)

    def Flush(self):
        flushSuccess = True
        try:
            logFile = open(self._fileName, "a")
            index = 0
            while index < len(self._buffer):
                logFile.write(self._buffer[index] + '\n')
                index = index + 1
            logFile.close()
        except Exception as exc:
            flushSuccess = False
            print('ERROR: cannot flush logging data to file - ' + str(exc) + '\n')

        if flushSuccess:
            # Reset buffer
            self._buffer = []