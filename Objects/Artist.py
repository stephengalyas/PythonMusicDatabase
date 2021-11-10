import sqlite3

from .MethodBank import MethodBank
from .LogHandler import LogHandler
from .LogHandler import LoggingLevel

class Artist:
    '''
    Purpose: represents an artist
    '''
    # Static variables
    REQUIRED_FIELDS = ('name', 'memberCount')
    # End static variables

    def __init__(self):
        '''
        Purpose: create an Artist object
        '''
        # Begin object variables
        self._rowID = None
        self._name = None
        self._memberCount = int(-1)
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Created new blank Artist instance in memory')
        # End object variables

    def createNew(self, **kwargs):
        '''
        Purpose: creates a new Artist object in memory and writes the object's data to the database.
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to load data into this Artist instance and create a new record in database')
        for var in self.REQUIRED_FIELDS:
            if var not in kwargs:
                MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot load data into this Artist instance in memory nor create new record in database, missing required field ' + str(var))
                raise Exception(f'Expecting {var} argument, but could not be found')
        self._name = str(kwargs['name'])
        try:
            self._memberCount = int(kwargs['memberCount'])
        except:
            MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot load data into this Artist instance in memory nor create new record in database, MemberCount value is not valid')
            raise TypeError('Cannot create Artist object, MemberCount is not in a valid format')

        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to connect to database')
        database = sqlite3.connect(MethodBank.mainDB())
        dbCursor = database.cursor()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to create Artist record in database')
        dbCursor.execute('INSERT INTO Artist (Name, MemberCount) VALUES (\'' + str(self.getName()) + '\', ' + str(self.getMemberCount()) + ')')
        database.commit()
        rowsInserted = dbCursor.rowcount
        if rowsInserted > 0:
            # Successfully created new record in database. Update object in memory with unique record ID in database.
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Successfully created Artist record in database')
            dbCursor.execute('SELECT MAX(RowID) FROM Artist')
            newArtistID = dbCursor.fetchone()
            if newArtistID is not None:
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'ID of new Artist record in database is ' + str(newArtistID[0]))
                self._rowID = int(newArtistID[0])
        else:
            MethodBank.writeToLog(LoggingLevel.ERROR, 'Could not create Artist record in database')
        database.commit()
        database.close()

    def loadFromMemory(self, **kwargs):
        '''
        Purpose : creates a new Artist object using values in memory.
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to load data into this Artist instance in memory')
        for var in self.REQUIRED_FIELDS:
            if var not in kwargs:
                raise Exception(f'Expecting {var} argument, but could not be found')
        self._name = str(kwargs['name'])
        self._memberCount = int(kwargs['memberCount'])
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished loading data into this Artist instance in memory')

    def loadFromDB(self, database, rowID):
        '''
        Purpose: creates an Artist object from memory.
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to load data into Artist instance in memory with data in database')
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Artist ID is ' + str(rowID))
        database.row_factory = sqlite3.Row
        dbCursor = database.cursor()
        dbCursor.execute('SELECT * FROM Artist WHERE RowID = ' + str(rowID))
        artistInDB = dbCursor.fetchone()
        if artistInDB is not None:
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Found Artist data in database, about to load data into Artist instance in memory')
            self._rowID = int(artistInDB['RowID'])
            self._name = str(artistInDB['Name']).strip()
            self._memberCount = int(artistInDB['MemberCount'])
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Artist object for Artist ID ' + str(self.getArtistID()) + ' (' + self.getName() + ') created')
        else:
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'ERROR: could not find artist data for Artist ID ' + str(rowID))
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished loading data into Artist instance in memory with data in database')

    def __str__(self):
        '''
        Purpose: displays a string representation of an Artist object
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Printing string representation of this Artist instance')
        retVal = self._name
        if self._memberCount > 0:
            retVal = f'{retVal} ({str(self._memberCount)} members)'
        return retVal

    # Begin defining comparisons
    def __gt__(self,other):
        if not isinstance(other, Artist):
            raise TypeError('Cannot compare Artist object to another object of different type')
        return self.getName().lower() > other.getName().lower()

    def __ge__(self,other):
        if not isinstance(other, Artist):
            raise TypeError('Cannot compare Artist object to another object of different type')
        return self.getName().lower() >= other.getName().lower()

    def __lt__(self,other):
        if not isinstance(other, Artist):
            raise TypeError('Cannot compare Artist object to another object of different type')
        return self.getName().lower() < other.getName().lower()

    def __le__(self,other):
        if not isinstance(other, Artist):
            raise TypeError('Cannot compare Artist object to another object of different type')
        return self.getName().lower() <= other.getName().lower()

    def __eq__(self,other):
        if not isinstance(other, Artist):
            raise TypeError('Cannot compare Artist object to another object of different type')
        return self.getName().lower() == other.getName().lower()

    def __ne__(self,other):
        return not self.__eq__(other)
    # End defining comparisons

    def getName(self):
        '''
        Purpose: return name of artist.
        '''
        return self._name

    #def setName(self, name):
        #'''
        #Purpose: sets the Name property of this Artist object
        #'''
    #    self._name = str(name).strip()
    #    self._isDirty = True

    def getMemberCount(self):
        '''
        Purpose: returns artist member count.
        '''
        return self._memberCount

    #def setMemberCount(self, memberCount):
        #'''
        #Purpose: sets the MemberCount property of this Artist object
        #'''
    #    self._memberCount = int(memberCount)
    #    self._isDirty = True

    def getArtistID(self):
        '''
        Purpose: returns unique artist ID for this Artist instance
        '''
        return self._rowID

    def updateData(self, database, **kwargs):
        '''
        Purpose: updates this Artist instance in memory and in the database
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to update Artist instance in memory')
        if 'name' in kwargs:
            self._name = str(kwargs['name'])
        if 'memberCount' in kwargs:
            try:
                self._memberCount = int(kwargs['memberCount'])
            except:
                MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot update Artist instance in memory, MemberCount value is not valid')
                raise TypeError('Cannot update Artist instance, MemberCount value is not in a valid format')

        dbCursor = database.cursor()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to update Artist data in database')
        dbCursor.execute('UPDATE Artist SET Name = \'' + str(self.getName()) + '\', MemberCount = ' + str(self.getMemberCount()) + ' WHERE RowID = ' + str(self.getArtistID()))
        database.commit()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished updating Artist instance in database')
        dbCursor.close()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished updating Artist instance in memory and in the database')
