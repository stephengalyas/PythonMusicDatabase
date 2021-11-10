import sqlite3
from .MethodBank import MethodBank
from .LogHandler import LogHandler
from .LogHandler import LoggingLevel

class Song:
    '''
    Purpose: represents a song
    '''
    # Begin static variables
    REQUIRED_FIELDS = ('title', 'length', 'trackNmbr')
    # End object variables
    def __init__(self):
        # Begin object variables
        self._title = None       # Song title
        self._length = None      # lLngth in seconds
        self._trackNmbr = None   # Track number
        self._albumID = None
        self._rowID = None
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Created new blank Song instance in memory')
        # End object variables

    def createNew(self, database, albumID, **kwargs):
        '''
        Purpose: creates a Song object in memory and writes the object's data to the database
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to load data into this Song instance and create new record in database')
        for expectedVar in self.REQUIRED_FIELDS:
            if expectedVar not in kwargs:
                MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot load data into this Song instance nor create new record in database, missing required field ' + str(expectedVar))
                raise Exception(f'Expecting {expectedVar} argument, but could not be found')

        self._title = str(kwargs['title'])
        try:
            self. _length = int(kwargs['length'])
        except:
            MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot load data into this Song instance nor create new record in database, Length value is invalid')
            raise Exception(f'Cannot add song {self.getTitle()} - invalid song length format')
        try:
            self._trackNmbr = int(kwargs['trackNmbr'])
        except:
            MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot load data into this Song instance nor create new record in database, TrackNmbr value is invalid')
            raise Exception(f'Cannot add song {self.getTitle()} - invalid track number format')

        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to connect to database')
        database = sqlite3.connect(MethodBank.mainDB())
        database.row_factory = sqlite3.Row
        dbCursor = database.cursor()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to create Song record in database')
        dbCursor.execute('INSERT INTO Song (AlbumID, Title, Length, TrackNmbr) VALUES (' + str(albumID) + ', \'' + str(self.getTitle()) + '\', ' + str(self.getLength()) + ', ' + str(self.getTrackNmbr()) + ')')
        rowsUpdated = dbCursor.rowcount
        if rowsUpdated > 0:
            # Successfully created Song record in database. Updated object in memory with the record's unique ID.
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Successfully created Song record in database')
            dbCursor.execute('SELECT MAX(RowID) FROM Song')
            newSongID = dbCursor.fetchone()
            if newSongID is not None:
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'ID of new Song record in database is ' + str(newSongID[0]))
                self._rowID = int(newSongID[0])
        else:
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Could not create Song record in database')
        database.commit()
        database.close()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished loading data into this Song instance in memory and creating new record in database')

    def loadFromMemory(self, **kwargs):
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to load data into this Song instance in memory')
        for expectedVar in self.REQUIRED_FIELDS:
            if expectedVar not in kwargs:
                MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot load data into this Song instance in memory, missing required field ' + str(expectedVar))
                raise Exception(f'Expecting {expectedVar} argument, but could not be found')

        # All required arguments present
        self._title = str(kwargs['title'])
        try:
            self. _length = int(kwargs['length'])
        except:
            MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot load data into this Song instance in memory, Length value is invalid')
            raise Exception(f'Cannot add song {self._title} - invalid song length format')
        try:
            self._trackNmbr = int(kwargs['trackNmbr'])
        except:
            MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot load data into this Song instance in memory, TrackNmbr value is invalid')
            raise Exception(f'Cannot add song {self._title} - invalid track number format')
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished loading data into this Song instance in memory')

    def loadFromDB(self, database, songID):
        '''
        Purpose: populates a Song object in memory using data from the database
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to load data into Song instance in memory with data in database')
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Song ID is ' + str(songID))
        database.row_factory = sqlite3.Row
        dbCursor = database.cursor()
        dbCursor.execute('SELECT * FROM Song WHERE RowID = ' + str(songID))
        songRecordFromDB = dbCursor.fetchone()
        if songRecordFromDB is not None:
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Found Song data in database, about to load data into Song instance in memory')
            self._rowID = int(songRecordFromDB['RowID'])
            self._albumID = int(songRecordFromDB['AlbumID'])
            self._title = str(songRecordFromDB['Title'])
            self._length = int(songRecordFromDB['Length'])
            self._trackNmbr = int(songRecordFromDB['TrackNmbr'])
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Song object for Song ID ' + str(self.getSongID()) + ' (' + self.getTitle() + ') created')
        else:
            MethodBank.writeToLog(LoggingLevel.WARNING, 'ERROR: could not song data for Song ID' + str(self.getSongID()))
        dbCursor.close()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished loading data into Song instance in memory with data in database')

    def __str__(self):
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Printing string representation of this Song instance')
        return f'{str(self._trackNmbr).zfill(2)}. {self._title} ({int(int(self._length)/60)}:{str(int(self._length)%60).zfill(2)})'

    # Begin defining comparisons
    def __eq__(self,other):
        if not isinstance(other, Song):
            raise TypeError('Cannot compare Song object to another object of different type') # Cannot compare Song to another object of different type.
        return self._trackNmbr == other._trackNmbr

    def __ne__(self,other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if not isinstance(other, Song):
            raise TypeError('Cannot compare Song object to another object of different type') # Cannot compare Song to another object of different type.
        return self._trackNmbr > other._trackNmbr

    def __ge__(self, other):
        if not isinstance(other, Song):
            raise TypeError('Cannot compare Song object to another object of different type') # Cannot compare Song to another object of different type.
        return self._trackNmbr >= other._trackNmbr

    def __lt__(self, other):
        if not isinstance(other, Song):
            raise TypeError('Cannot compare Song object to another object of different type') # Cannot compare Song to another object of different type.
        return self._trackNmbr < other._trackNmbr

    def __le__(self, other):
        if not isinstance(other, Song):
            raise TypeError('Cannot compare Song object to another object of different type') # Cannot compare Song to another object of different type.
        return self._trackNmbr <= other._trackNmbr
    # End defining comparisons

    def remove(self, database):
        '''
        Purpose: removes a Song from the database.
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to remove Song instance from memory and database')
        dbCursor = database.cursor()
        dbCursor.execute('DELETE FROM Song WHERE AlbumID = ' + str(self.getAlbumID()) + ' AND RowID = ' + str(self.getSongID()))
        database.commit()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished removing Song instance from memory and database')

    def getTitle(self):
        '''
        Purpose: returns the title of a song
        '''
        return self._title

    def getTrackNmbr(self):
        '''
        Purpose: returns a song's track number
        '''
        return self._trackNmbr

    def getLength(self):
        '''
        Purpose: returns a track's length in seconds
        '''
        return self._length

    #def updateTitle(self, title):
    #    '''
    #   Purpose: updates the track's title
    #    '''
    #    self._title = str(title)

    #def updateLength(self, length):
    #    '''
    #    Purpose: updates the track's length
    #    '''
    #    self._length = length

    #def updateTrackNmbr(self, trackNmbr):
    #    '''
    #    Purpose: updates the track's number
    #    '''
    #    self._trackNmbr = trackNmbr

    def updateData(self, database, **kwargs):
        '''
        Purpose: update data pertaining to this Song object
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to update Song instance in memory')
        if 'title' in kwargs:
            self._title = str(kwargs['title'])
        if 'length' in kwargs:
            try:
                self._length = int(kwargs['length'])
            except:
                MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot update song length for Song instance, value is not in a valid format')
                raise TypeError('Cannot update song length, value is not in a valid format')
        if 'trackNmbr' in kwargs:
            try:
                self._trackNmbr = int(kwargs['trackNmbr'])
            except:
                MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot update song track number for Song instance, value is not in a valid format')
                raise TypeError('Cannot update track number, value is not in a valid format')
        database.row_factory = sqlite3.Row
        dbCursor = database.cursor()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to update Song instance in database')
        dbCursor.execute('UPDATE Song SET Title = \'' + str(self.getTitle()) + '\', Length = ' + str(self.getLength()) + ', TrackNmbr = ' + str(self.getTrackNmbr()) + ' WHERE RowID = ' + str(self.getSongID()))
        database.commit()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished updating Song instance in database')
        dbCursor.close()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished updating Song instance in memory and in the database')

    def getSongID(self):
        '''
        Purpose: gets the unique song ID for this Song object
        '''
        return self._rowID

    def getAlbumID(self):
        '''
        Purpose: returns the album ID that is used to relate this Song instance to an Album instance
        '''
        return self._albumID
