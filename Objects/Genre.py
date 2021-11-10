from .MethodBank import MethodBank
from .LogHandler import LoggingLevel

import sqlite3

class Genre():
    '''
    Purpose: represents a genre
    '''
    # Begin class static variables
    _genres = []
    # End class static variables

    # Begin class static methods
    @staticmethod
    def initialize(database):
        '''
        Purpose: initialize class by reading genres from file
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Initializing Genre class')

        database.row_factory = sqlite3.Row
        dbCursor = database.cursor()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to get Genre data from database')
        dbCursor.execute('SELECT Name FROM Genre ORDER BY RowID ASC')
        genresInDB = dbCursor.fetchall()
        for genreInDB in genresInDB:
            Genre._genres.append(str(genreInDB['Name']))
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Loaded ' + len(Genre._genres) + ' Genres into memory')

        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to sort Genres')
        Genre._genres.sort()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished sorting Genres')

    # End class static method
