from .Song import Song
from .Genre import Genre
from .Artist import Artist
from .MethodBank import MethodBank
from .LogHandler import LoggingLevel

import sqlite3

class Album:
    '''
    Purpose: represents an album
    '''
    # Begin static variables
    REQUIRED_FIELDS = ('artistID', 'name', 'genre', 'year')
    # End static variables
    def __init__(self):
        '''
        Purpose: initialize Album object.
        '''
        # Begin object variables (if they are defined outside of this method, they are shared across objects!!!)
        self._artistID = None   # Artist ID in database
        self._songs = []      # Song objects related to this album
        self._genre = None    # Genre
        self._name = None     # Album name
        self._year = int(0)   # Album year
        self._rowID = None    # Unique ID in database
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Created new blank Album instance in memory')
        # End object variables

    def createNew(self, **kwargs):
        '''
        Purpose: creates an Album object in memory and writes the object's data to the database
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to load data into this Album instance and create new record in database')
        for var in self.REQUIRED_FIELDS:
            if var not in kwargs:
                MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot load data into this Album instance in memory nor create new record in database, missing required field ' + str(var))
                raise Exception(f'Expecting {var} argument, but could not be found.')

        self._songs = []
        self._genre = str(kwargs['genre'])
        self._name = str(kwargs['name'])
        try:
            self._artistID = int(kwargs['artistID'])
            self._year = int(kwargs['year'])
        except:
            MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot load data into this Album instance nor create new record in datanase, invalid required fields')
            raise TypeError('Cannot add album ' + str(kwargs['name']) + ', either the artist ID or year could not be converted to their corresponding type.')

        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to open database connection')
        database = sqlite3.connect(MethodBank.mainDB())
        dbCursor = database.cursor()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to create Album record in database')
        dbCursor.execute('INSERT INTO Album (ArtistID, Name, Genre, Year) VALUES (' + str(self.getArtistID()) + ', \'' + str(self.getName()) + '\', \'' + str(self.getGenre()) + '\', ' + str(self.getYear()) + ')')
        database.commit()
        rowsInserted = dbCursor.rowcount
        if rowsInserted > 0:
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Successfully created Album record in database')
            # Successfully created new record in database. Update object in memory with unique record ID in database.
            dbCursor.execute('SELECT MAX(RowID) FROM Album')
            newAlbumID = dbCursor.fetchone()
            if newAlbumID is not None:
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'ID of new Album record in database is ' + str(newAlbumID[0]))
                self._rowID = int(newAlbumID[0])
        else:
            MethodBank.writeToLog(LoggingLevel.ERROR, 'Could not create Album record in database')
        database.commit()
        database.close()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished loading data into this Album instance and creating new record in database')

    def loadFromMemory(self, **kwargs):
        '''
        Purpose: creates an Album object in memory.
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to load data into this Album instance in memory')
        for var in self.REQUIRED_FIELDS:
            if var not in kwargs:
                MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot load data into this Album instance in memory, missing required field ' + str(var))
                raise Exception(f'Expecting {var} argument, but could not be found')
        self._name = str(kwargs['name'])
        self._genre = str(kwargs['genre'])
        self._year = int(kwargs['year'])
        self._artistID = kwargs['artistID']
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished loading data into this Album instance in memory')

    def loadFromDB(self, database, rowID):
        '''
        Purpose: creates an Artist object from data stored in the database.
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to load data into Album instance in memory with data in database')
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Album ID is ' + str(rowID))
        self._songs = []    # Ensure list is empty
        database.row_factory = sqlite3.Row
        dbCursor = database.cursor()
        dbCursor.execute('SELECT * FROM Album WHERE RowID = ' + str(rowID))
        albumInDB = dbCursor.fetchone()
        if albumInDB is not None:
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Found Album data in database, about to load data into Album instance in memory')
            self._artistID = int(albumInDB['ArtistID'])
            self._genre = str(albumInDB['Genre'])
            self._name = str(albumInDB['Name'])
            self._year = int(albumInDB['Year'])
            self._rowID = int(albumInDB['RowID'])
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Album object for Album ID ' + str(self.getAlbumID()) + ' (' + self.getName() + ') created. About to create related Song objects.')

            # Get related songs.
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to create related Song instances from data in database')
            dbCursor.execute('SELECT RowID FROM Song WHERE AlbumID = ' + str(self.getAlbumID()))
            songsOnAlbum = dbCursor.fetchall()
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Number of related Songs: '+ str(len(songsOnAlbum)))
            for songOnAlbum in songsOnAlbum:
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to create new Song instance in memory')
                tempSong = Song()
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to load data for Song instance into memory with data in database')
                tempSong.loadFromDB(database, songOnAlbum[0])
                self._songs.append(tempSong)
        else:
            MethodBank.writeToLog(LoggingLevel.WARNING, 'ERROR: could not get album data for Album ID ' + str(self.getAlbumID()))
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished loading data into Album instance in memory with data in database')

    def updateData(self, database, **kwargs):
        '''
        Purpose: updates this Album object in memory as well as the database
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to update Album instance in memory')
        if 'name' in kwargs:
            self._name = str(kwargs['name'])
        if 'genre' in kwargs:
            self._genre = str(kwargs['genre'])
        if 'year' in kwargs:
            try:
                self._year = int(kwargs['year'])
            except:
                MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot update album year for Album instance, value is not in a valid format')
                raise TypeError('Cannot update album year, value is not in a valid format')

        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to update Album instance in database')
        dbCursor = database.cursor()
        dbCursor.execute('UPDATE Album SET Name = \'' + str(self.getName()) + '\', Year = ' + str(self.getYear()) + ', Genre = \'' + str(self.getGenre()) + '\' WHERE RowID = ' + str(self.getAlbumID()))
        database.commit()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished updating Album instance in database')
        dbCursor.close() 
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished updating Album instance in memory and in the database')

    def __str__(self):
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Printing string representation of this Album instance')
        strValue = 'Album name: ' + str(self._name) + ' (' + str(self._year) + ')\n'
        for song in self._songs:
            strValue += str(song) + '\n'
        return strValue

    # Begin defining comparisons
    def __eq__(self,other):
        if not isinstance(other, Album):
            raise TypeError('Cannot compare Album object to another object of different type') # Cannot compare ALbum to another object of different type.
        return self._name == other._name

    def __ne__(self,other):
        return not self.__eq__(other)
    # End defining comparisons

    def addSong(self, **kwargs):
        '''
        Purpose: adds a song to the album
        Returns: a Song object if successful, otherwise returns None
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to create a new Song instance and relate it to this Album instance')
        retVal = None
        # Make sure we do not add a song with a duplicate track number.
        for song in self.getSongs():
            if song.getTrackNmbr() == int(kwargs['trackNmbr']):
                MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot create Song instance because a track with this track number is already related to this Album instance')
                raise ValueError(f'Cannot create song {kwargs["title"]} because a track already exists on this album with track number {kwargs["trackNmbr"]} ')
        try:
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to connect to database')
            database = sqlite3.connect(MethodBank.mainDB())
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to create new Song instance in memory and database')
            tempSong = Song()
            tempSong.createNew(database, self.getAlbumID(), **kwargs)
            self._songs.append(tempSong)
            retVal = tempSong
            self._songs.sort()  # sort songs by track number
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Successfully created new Song instance in memory and the database, and related the Song instance to this Album instance')
        except Exception as exc:
            MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot create Song instance or relate Song instance to this Album instance - ' + str(exc))
            retVal = None
        return retVal


    '''
    def addSongObj(self, songObj):
        
        Purpose: adds a song to the album
        
        for song in self._songs:
            if song.getTrackNmbr() == int(songObj.getTrackNmbr()):
                raise ValueError(f'Cannot create song {songObj.getTitle()} because a track already exists on this album with track number {songObj.getTrackNmbr()} ')
        self._songs.append(songObj)
        self._songs.sort()
    '''

    def removeSong(self, database, songID):
        '''
        Purpose: removes a song from the album.
        Returns: if song is found, the removed Song object, otherwise None
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to remove Song instance from memory and database, and break relationship witht this Album instance')
        removedSong = None
        for song in self.getSongs():
            if (song.getSongID() == songID):
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to remove Song instance from memory')
                removedSong = self._songs.pop(self._songs.index(song))
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to remove Song instance from database')
                removedSong.remove(database)
                break
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished removing Song instance from memory and database, and breaking relationship with this Album instance')
        return removedSong

    def removeAlbum(self, database):
        '''
        Purpose: removes album and related songs from database
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to remove Album instance and related Song instances from memory and database')
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to remove all related Song instances from memory and database')
        for song in self.getSongs():
            self.removeSong(database, song.getSongID())

        dbCursor = database.cursor()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to remove Album instance from database')
        # Make sure all songs are cleaned up.
        dbCursor.exeucte('DELETE FROM Song WHERE AlbumID = ' + str(self.getAlbumID()))
        dbCursor.execute('DELETE FROM Album WHERE AlbumID = ' + str(self.getAlbumID()))
        database.commit()
        dbCursor.close()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished removing Album instance and related Song instances from memory and database')

    #
    #def removeSongObj(self, songToRemove):
    #    Purpose: removes a Song object's associated with this Album object
    #    Returns: if a match is found, a Song object; otherwise, None
    #    retVal = None
    #    for song in self._songs:
    #        if(song == songToRemove):
    #            retVal = self.removeSong(title = song.getTitle())
    #    return retVal
    #

    def getSong(self, title = None, trackNmbr = None):
        '''
        Purpose: finds the first song that matches either the specified title or the specified track number, and returns that song
        Returns: if a match is found, a Song object; otherwise, None
        '''
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to get a Song instance related to this Album instance')
        if title is None and trackNmbr is None:
            MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot search for Song instance, missing required fields')
            raise ValueError('Expecting title or track number, but neither was provided')
        if title is not None and trackNmbr is not None:
            MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot search for Song instance, too many fields provided')
            raise ValueError('Expecting either title OR track number, but both were provided')

        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to search for Song instance')
        songToReturn = None
        for song in self.getSongs():
            if (title is not None and song.getTitle() == title) or (trackNmbr is not None and song.getTrackNmbr() == trackNmbr):
                songToReturn = song
                break
        return songToReturn

    def getSongs(self):
        '''
        Purpose: returns a list of Song objects associated with this Album object.
        '''
        return self._songs


    #def updateSong(self, database, songID, **kwargs):
    #
    #    Purpose: updates a Song object in memory
    #    Returns: a Song object that represents the updated song
    #
    #    songToReturn = None;
    #    for song in self.getsongs():
    #        if(song.getSongID() == songID):
    #            songToReturn = song
    #            song.updateData(database, **kwargs)
    #            break
    #    return songToReturn
    # '''

    def getName(self):
        '''
        Purpose: returns the name of the album.
        '''
        return self._name

    def getGenre(self):
        '''
        Purpose: returns the album genre
        '''
        return self._genre

    def getYear(self):
        '''
        Purpose: returns album year
        '''
        return self._year

    #def updateName(self, name):
    #    '''
    #    Purpose: updates album name
    #    '''
    #    self._name = str(name)

    #def updateArtist(self, artist):
     #   '''
     #   Purpose: updates album artist.
     #   '''
    #   self._artist = artist

    #def updateGenre(self, genre):
    #   '''
     #   Purpose: updates album genre
     #   '''
    #    self._genre = str(genre)

    #def updateYear(self, year):
     #   '''
     #   Purpose: updates album year
     #   '''
    #    self._year = int(year)

    def getAlbumID(self):
        '''
        Returns: unique album ID for this Album instance
        '''
        return self._rowID

    def getArtistID(self):
        '''
        Purpose: returns the Artist ID with which this album is related.
        '''
        return self._artistID
    