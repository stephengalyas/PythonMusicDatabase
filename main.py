from Objects.LogHandler import LogHandler
from Objects.LogHandler import LoggingLevel
from Objects.Album import Album
from Objects.Artist import Artist
from Objects.Genre import Genre
from Objects.Song import Song
from Objects.MethodBank import MethodBank

import sqlite3

albums = []
artists = []

def main():

    #logger = LogHandler(fileName = 'Test123.log')

    initialize()
    initializeDatabase()
    loadDataFromDatabase()
    #createDummyData()

    optionDisplay = str('0) Exit program\n')
    optionDisplay += str('1) View all albums\n')
    optionDisplay += str('2) View an album\'s details\n')
    optionDisplay += str('3) Add an album\n')
    optionDisplay += str('4) Edit an album\n')
    optionDisplay += str('5) Remove an album\n')
    optionDisplay += str('6) Find album by song\n')
    optionDisplay += str('7) View all artists\n')
    optionDisplay += str('8) View all songs\n')
    optionDisplay += str('9) View all genres\n')
    optionDisplay += str('10) Print all songs in database\n')
    optionDisplay += str('11) Add an artist\n')
    optionDisplay += str('12) Edit artist\n')

    optionSelected = int(-1)

    while optionSelected != 0:
        print()
        print(optionDisplay)
        try:
            MethodBank.flushLog()
            optionSelected = int(input('Select an option: '))
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'User selected menu option ' + str(optionSelected))
            if optionSelected == 1:
                # Print all albums.
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Printing all albums')
                for album in albums:
                    print(album)
            elif optionSelected == 2:
                # Print select album.
                albumToPrint = str(input('Enter album name: '))
                for album in albums:
                    if album.getName().lower() == albumToPrint.lower():
                        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Printing album ' + albumToPrint)
                        print(album)
                        break
                else:
                    MethodBank.writeToLog(LoggingLevel.WARNING, 'Cannot find album ' + albumToPrint)
                    print('Cannot find this album!')
            elif optionSelected == 3:
                # Add an album
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Getting ready to create new album')
                createAlbum()
                print('New album added')
            elif optionSelected == 4:
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Getting ready to edit album')
                editAlbum()
            elif optionSelected == 5:
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Getting ready to remove album')
                removeAlbum()
            elif optionSelected == 6:
                # Find album by song.
                songNameToSearch = str(input('Enter song name: ').lower().strip())
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Searching for song ' + songNameToSearch)
                for album in albums:
                    for albumSong in album.getSongs():
                        if albumSong.getTitle().lower().strip() == songNameToSearch:
                            print(f'{album.getName()} ({albumSong})')
            elif optionSelected == 7:
                # Print all artists
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Printing all artists')
                allArtists = []
                uniqueArtists = set()
                for album in albums:
                    for artist in artists:
                        if artist.getArtistID() == album.getArtistID():
                            allArtists.append(artist.getName())
                sortedArtists = sorted(allArtists, reverse=True)
                for artist in sortedArtists:
                    uniqueArtists.add(artist)
                print('Artists:')
                for uniqueArtist in uniqueArtists:
                    print(uniqueArtist)
            elif optionSelected == 8:
                # Print all songs
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Printing all songs')
                allSongs = []
                uniqueSongs = set()
                for album in albums:
                    for song in album.getSongs():
                        allSongs.append(str(song))
                sortedSongs = sorted(allSongs)
                for sortedSong in sortedSongs:
                    uniqueSongs.add(sortedSong)
                print('Songs:')
                for uniqueSong in uniqueSongs:
                    print(uniqueSong)
            elif optionSelected == 9:
                # Print all genres
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Printing all genres')
                allGenres = []
                uniqueGenres = set()
                for album in albums:
                    allGenres.append(album.getGenre())
                sortedGenres = sorted(allGenres, reverse=True)
                for sortedGenre in sortedGenres:
                    uniqueGenres.add(sortedGenre)
                print('Genres:')
                for uniqueGenre in uniqueGenres:
                    print(uniqueGenre)
            elif optionSelected == 10:
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Testing database action')
                testDatabaseAction()
            elif optionSelected == 11:
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Getting ready to create artist')
                createArtist()
            elif optionSelected == 12:
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Getting ready to edit artist')
                editArtist()
        except Exception as exc:
            MethodBank.writeToLog(LoggingLevel.ERROR, 'Error while selecting menu item - ' + str(exc))
            print(f'ERROR! {exc}')
            continue

def initialize():
    try:
        MethodBank.initialize()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Initialized program')
    except Exception as exc:
        print('Cannot initialize MethodBank - ' + str(exc))

'''
def createDummyData():
    
    Purpose: creates dummy data in memory until a database is available
    
    tempArtist = Artist(name='Pink Floyd')
    artists.append(tempArtist)
    album = Album(name = 'Dark Side of the Moon', year=1973, genre='Progressive Rock', artist=tempArtist)
    album.addSong(title='Speak To Me/Breathe', trackNmbr=1, length=246)
    album.addSong(title='Time', trackNmbr=3, length=413)
    album.addSong(title='On the Run', trackNmbr=2, length=225)
    albums.append(album)
'''

def editAlbum():
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to edit album')
    database = sqlite3.connect(MethodBank.mainDB())
    # Edit album
    albumToEdit = str(input('Enter name of album to edit: '))
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'User entered album name ' + albumToEdit)
    albumToEditObj = None
    for album in albums:
        if album.getName().lower() == albumToEdit.lower():
            albumToEditObj = album
            break
    if albumToEditObj is None:
        MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot edit album ' + str(albumToEdit) + ' - corresponding album object cannot be found')
        raise Exception('Cannot find album {albumToEdit} ')
    print('1) Edit album details\n2) Edit songs')
    editAlbumOptionSelected = int(input('Select an option: '))
    if editAlbumOptionSelected == 1:
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Getting ready to edit album details')
        # Edit album details
        # Edit name
        print(f'Current album name: {albumToEditObj.getName()}')
        updateName = str(input('Update name? (y/n): '))
        if updateName.lower()[0] == 'y':
            albumToEditObj.updateName(input('Enter name: '))
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Updated album name to ' + albumToEditObj.getName())
        # Edit artist
        print(f'Current artist info: {albumToEditObj.getArtist()}')
        updateArtist = str(input('Update artist? (y/n): '))
        if updateArtist.lower()[0] == 'y':
            albumToEditObj.updateArtist(createArtist())
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Updated album artist')
        # Edit genre
        print(f'Current genre: {albumToEditObj.getGenre()}')
        updateGenre = str(input('Update genre? (y/n): '))
        if updateGenre.lower()[0] == 'y':
            albumToEditObj.updateGenre(input('Enter genre: '))
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Updated genre to ' + albumToEditObj.getGenre())
        # Edit year
        print(f'Current year: {albumToEditObj.getYear()}')
        updateYear = str(input('Update year? (y/n): '))
        if updateYear.lower()[0] == 'y':
            albumToEditObj.updateYear(input('Enter year: '))
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Updated year to ' + str(albumToEditObj.getYear()))
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Getting ready to update album data in database')
        albumToEditObj.updateData(database)
        print('Album updated')
    elif editAlbumOptionSelected == 2:
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Getting ready to edit album songs')
        # Edit songs
        for albumSong in albumToEditObj.getSongs():
            print(f'Current song: {albumSong}')
            updateSong = str(input('Update song? (y/n)'))
            if updateSong.lower()[0] == 'y':
                # User wishes to update song.
                newSongNmbr = str(input('Enter track number for song (enter "remove" to remove song): '))
                if newSongNmbr.lower().strip() == 'remove':
                    # Remove song
                    albumToEditObj.removeSong(database, albumSong.getSongID())
                    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Removed song ' + str(albumSong))
                    continue
                else:
                    # Update song
                    newSong = createSong(int(newSongNmbr))
                    albumToEditObj.removeSong(database, albumSong.getSongID())
                    albumToEditObj.addSong(title=newSong.getTitle(), length=newSong.getLength(), trackNmbr=newSong.getTrackNmbr())
                    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Updated song ' + str(albumSong) + ' to ' + str(newSong))
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished updating album')

def createArtist(**artistData):
    '''
    Purpose: creates a new Artist object
    Returns: artist object
    If all required fields are not passed as parameter, user input will be required.
    '''
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to create Artist instance')
    artistDataCopy = dict(artistData)
    for requiredField in Artist.REQUIRED_FIELDS:
        if requiredField in artistData:
            # Found this required field in the parameters passed to this method. Continue.
            continue
        else:
            # Missing required field. Require user input.
            userInput = str(input(f'Artist: enter {requiredField}: '))
            artistDataCopy[requiredField] = userInput.strip()

    newAlbumArtistObj = None
    for artist in artists:
        if artist.getName().lower() == artistDataCopy['name'].lower():
            MethodBank.writeToLog(LoggingLevel.WARNING, 'An Artist instance that matches the requested new Artist already exists in memory, and will not be created')
            newAlbumArtistObj = artist
            break
    if newAlbumArtistObj is None:
        newAlbumArtistObj = Artist()
        newAlbumArtistObj.createNew(**artistDataCopy)
        artists.append(newAlbumArtistObj)
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'New Artist instance created')
    return newAlbumArtistObj

def editArtist():
    '''
    Purpose: edits an Artist object.
    '''
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to edit Artist instance')
    artistObjToEdit = None
    userInput = str(input('Enter name of artist to update: '))
    for artist in artists:
        if artist.getName().lower().strip() == userInput.lower().strip():
            artistObjToEdit = artist
            break
    if artistObjToEdit is not None:
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Found matching Artist instance in memory, about to update Artist instance')
        # Update name
        userInput = str(input('Enter artist name (leave blank to skip update): '))
        if userInput.strip() != '':
            artistObjToEdit.setName(userInput)
        # Update member count
        userInput = str(input('Enter member count (leave blank to skip update): '))
        if userInput.strip() != '':
            artistObjToEdit.setMemberCount(int(userInput))
        print('Updated artist ' + artistObjToEdit.getName())
    else:
        MethodBank.writeToLog('Could not find Artist instance in memory that matches search item')
        print('Could not find artist ' + userInput + '!')

def createAlbum(**albumData):
    '''
    Purpose: creates an Album object
    Returns Album object
    If all required fields are not passed as parameter, user input will be required
    '''
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to create Album instance.')
    albumDataCopy = dict(albumData)
    for requiredField in Album.REQUIRED_FIELDS:
        if requiredField in albumData:
            continue
        else:
            # Missing required field, get user input.
            if requiredField == 'artistID':
                # Artist field needs to be Artist instance
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Missing artist ID, about to create new Artist object')
                albumDataCopy[requiredField] = (createArtist()).getArtistID()
            else:
                missingFieldData = input(f'Album: enter {requiredField.lower()}: ')
                albumDataCopy[requiredField] = missingFieldData

    # Check if an album with this name already exists
    for existingAlbum in albums:
        if existingAlbum.getName().lower() == albumDataCopy['name'].lower():
            shouldUserContinue = str(input('An album with this name already exists. Continue? (y/n): '))
            if shouldUserContinue[0] == 'n':
                # User canceled add album action.
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'An Album already exists with this name. User chose to cancel CreateAlbum action')
                return None
            else:
                MethodBank.writeToLog(LoggingLevel.VERBOSE, 'An Album already exists with this name. User chose to continue CreateAlbum action')
                break

    # Album does not exist, or user wishes to continue.
    newAlbumObj = Album()
    newAlbumObj.createNew(**albumDataCopy)

    # Add songs
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to ask user to add Songs to Album')
    newAlbumTrackTotal = int(input('How many tracks? '))
    newAlbumTrackIndex = 0
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Number of songs to add: ' + str(newAlbumTrackTotal))
    while newAlbumTrackIndex < newAlbumTrackTotal:
        newAlbumTrackIndex = newAlbumTrackIndex + 1
        newSongObj = createSong(newAlbumTrackIndex, **dict())
        newAlbumObj.addSong(title=newSongObj.getTitle(), length=newSongObj.getLength(), trackNmbr=newSongObj.getTrackNmbr())
    albums.append(newAlbumObj)

    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished creating new Album instance')
    return newAlbumObj

def createSong(trackNmbr, **songData):
    '''
    Purpose: creates a Song object
    Returns Song object
    If all required fields are not passed as parameter, user input will be required
    '''
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to create new Song instance')
    songDataCopy = dict(songData)
    for requiredField in Song.REQUIRED_FIELDS:
        if requiredField in songData:
            continue
        elif requiredField != 'trackNmbr':
            # Skip track number, as this is passed to this function as a separate parameter
            missingFieldData = input(f'Song: enter {requiredField.lower()}: ')
            songDataCopy[requiredField] = missingFieldData

    songDataCopy['trackNmbr'] = trackNmbr
    newSongObj = Song()
    newSongObj.loadFromMemory(**songDataCopy)
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Finished creating new Song instance')
    return newSongObj

def removeAlbum():
    '''
    Purpose: removes an Album object from the collection of Album objects.
    Returns: the Album object that was removed from the collection.
    '''
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to remove Album instance')
    albumToRemove = None
    albumNameToRemove = str(input('Enter the album name to remove: '))
    index = 0
    while index < len(albums):
        if(albums[index].getName().lower() == albumNameToRemove.lower().strip()):
            database = sqlite3.connect(MethodBank.mainDB())
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to remove Album instance from memory')
            albumToRemove = albums.pop(index)
            MethodBank.writeToLog(LoggingLevel.VERBOSE, 'About to remove Album instance from database')
            albumToRemove.removeAlbum(database)
            print('Removed album')
            break
    else:
        MethodBank.writeToLog(LoggingLevel.ERROR, 'Cannot remove Album instance from memory or database, could not find Album instance in memory')
        raise Exception(f'Could not remove album {albumNameToRemove} because an album with this name could not be found')
    return albumToRemove

def initializeDatabase(dropExistingData = False):
    '''
    Purpose: initializes database
    '''
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Initializing database')

    database = sqlite3.connect(MethodBank.mainDB())   # Creates database file if it does not already exist
    dbCursor = database.cursor()

    # Create Artist table
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Initializing Artist table')

    if dropExistingData == True:
        dbCursor.execute('DROP TABLE IF EXISTS Artist')

    dbCursor.execute("""
                    CREATE TABLE IF NOT EXISTS Artist (
                    RowID integer PRIMARY KEY,
                    Name varchar(250) NOT NULL, 
                    MemberCount tinyint NOT NULL
                    )""")

    # Create Album table
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Initializing Album table')

    if dropExistingData == True:
        dbCursor.execute('DROP TABLE IF EXISTS Album')

    dbCursor.execute("""
                    CREATE TABLE IF NOT EXISTS Album (
                    RowID integer PRIMARY KEY,
                    ArtistID int NOT NULL,
                    Name varchar(250) NOT NULL,
                    Genre varchar(100) NOT NULL,
                    Year smallint NOT NULL
                    )
                    """)

    # Create Song table
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Initializing Song table')

    if dropExistingData:
        dbCursor.execute('DROP TABLE IF EXISTS Song')

    dbCursor.execute("""
                    CREATE TABLE IF NOT EXISTS Song (
                    RowID integer PRIMARY KEY,
                    AlbumID int NOT NULL,
                    Title varchar(250) NOT NULL,
                    Length int NOT NULL,
                    TrackNmbr smallint NOT NULL
                    )
                    """)

    # Create Genre table
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Initializing Genre table')

    if dropExistingData == True:
        dbCursor.execute('DROP TABLE IF EXISTS Genre')

    dbCursor.execute("""
                    CREATE TABLE IF NOT EXISTS Genre (
                    RowID integer PRIMARY KEY,
                    Name varchar(250) NOT NULL
                    )
                    """)

    # If genre table is blank, add genres.
    dbCursor.execute('SELECT TOP 1 RowID FROM Genre')
    genresInDB = dbCursor.fetchall()
    if len(genresInDB) == 0:
        genresToInsert = '''
        INSERT INTO Genre (Name) VALUES ('Blues');
		INSERT INTO Genre (Name) VALUES ('African Blues');
		INSERT INTO Genre (Name) VALUES ('Chicago Blues');
		INSERT INTO Genre (Name) VALUES ('Country Blues');
		INSERT INTO Genre (Name) VALUES ('Delta Blues');
		INSERT INTO Genre (Name) VALUES ('Detroit Blues');
		INSERT INTO Genre (Name) VALUES ('Louisiana Blues');
		INSERT INTO Genre (Name) VALUES ('New Orleans Blues');
		INSERT INTO Genre (Name) VALUES ('Rhythm and Blues');
		INSERT INTO Genre (Name) VALUES ('St. Louis Blues');
		INSERT INTO Genre (Name) VALUES ('Swamp Blues');
		INSERT INTO Genre (Name) VALUES ('Texas Blues');
		INSERT INTO Genre (Name) VALUES ('Calypso');
		INSERT INTO Genre (Name) VALUES ('Mambo');
		INSERT INTO Genre (Name) VALUES ('Merengue');
		INSERT INTO Genre (Name) VALUES ('Meringue');
		INSERT INTO Genre (Name) VALUES ('Reggae');
		INSERT INTO Genre (Name) VALUES ('Rumba');
		INSERT INTO Genre (Name) VALUES ('Ska');
		INSERT INTO Genre (Name) VALUES ('Salsa');
		INSERT INTO Genre (Name) VALUES ('Comedy');
		INSERT INTO Genre (Name) VALUES ('Comedy Rock');
		INSERT INTO Genre (Name) VALUES ('Alternative Country');
		INSERT INTO Genre (Name) VALUES ('Americana');
		INSERT INTO Genre (Name) VALUES ('Bluegrass');
		INSERT INTO Genre (Name) VALUES ('Cajun');
		INSERT INTO Genre (Name) VALUES ('Classic Country');
		INSERT INTO Genre (Name) VALUES ('Country');
		INSERT INTO Genre (Name) VALUES ('Country Blues');
		INSERT INTO Genre (Name) VALUES ('Country Pop');
		INSERT INTO Genre (Name) VALUES ('Country Rap');
		INSERT INTO Genre (Name) VALUES ('Country Rock');
		INSERT INTO Genre (Name) VALUES ('Cowboy Pop');
		INSERT INTO Genre (Name) VALUES ('Honky Tonk');
		INSERT INTO Genre (Name) VALUES ('Outlaw Country');
		INSERT INTO Genre (Name) VALUES ('Progressive Country');
		INSERT INTO Genre (Name) VALUES ('Rockability');
		INSERT INTO Genre (Name) VALUES ('Western Swing');
		INSERT INTO Genre (Name) VALUES ('Elevator Music');
		INSERT INTO Genre (Name) VALUES ('Lounge Music');
		INSERT INTO Genre (Name) VALUES ('New Age');
		INSERT INTO Genre (Name) VALUES ('Ambient');
		INSERT INTO Genre (Name) VALUES ('Drone');
		INSERT INTO Genre (Name) VALUES ('Disco');
		INSERT INTO Genre (Name) VALUES ('Downtempo');
		INSERT INTO Genre (Name) VALUES ('Electronic Rock');
		INSERT INTO Genre (Name) VALUES ('Dance Rock');
		INSERT INTO Genre (Name) VALUES ('New Wave');
		INSERT INTO Genre (Name) VALUES ('Synth Pop');
		INSERT INTO Genre (Name) VALUES ('Post Rock');
		INSERT INTO Genre (Name) VALUES ('Space Rock');
		INSERT INTO Genre (Name) VALUES ('Electronica');
		INSERT INTO Genre (Name) VALUES ('Progressive Electronic');
		INSERT INTO Genre (Name) VALUES ('Afrobeats');
		INSERT INTO Genre (Name) VALUES ('Hardcore');
		INSERT INTO Genre (Name) VALUES ('Doomcore');
		INSERT INTO Genre (Name) VALUES ('Chillwave');
		INSERT INTO Genre (Name) VALUES ('Vaporwave');
		INSERT INTO Genre (Name) VALUES ('Afroswing');
		INSERT INTO Genre (Name) VALUES ('Alternative Hip Hop');
		INSERT INTO Genre (Name) VALUES ('Hipster Hop');
		INSERT INTO Genre (Name) VALUES ('Emo Rap');
		INSERT INTO Genre (Name) VALUES ('Electro');
		INSERT INTO Genre (Name) VALUES ('Lo-Fi');
		INSERT INTO Genre (Name) VALUES ('Lofi');
		INSERT INTO Genre (Name) VALUES ('EBM');
		INSERT INTO Genre (Name) VALUES ('Industrial Hip Hop');
		INSERT INTO Genre (Name) VALUES ('Industrial Metal');
		INSERT INTO Genre (Name) VALUES ('Industrial Rock');
		INSERT INTO Genre (Name) VALUES ('Glitch');
		INSERT INTO Genre (Name) VALUES ('Techno');
		INSERT INTO Genre (Name) VALUES ('Acid Techno');
		INSERT INTO Genre (Name) VALUES ('Ambient Techno');
		INSERT INTO Genre (Name) VALUES ('Trance');
		INSERT INTO Genre (Name) VALUES ('Dream Trance');
		INSERT INTO Genre (Name) VALUES ('Progressive Trance');
		INSERT INTO Genre (Name) VALUES ('Psychedelic Trance');
		INSERT INTO Genre (Name) VALUES ('Dubstep');
		INSERT INTO Genre (Name) VALUES ('Post Dubstep');
		INSERT INTO Genre (Name) VALUES ('Grime');
		INSERT INTO Genre (Name) VALUES ('Acid House');
		INSERT INTO Genre (Name) VALUES ('Ambient House');
		INSERT INTO Genre (Name) VALUES ('Deep House');
		INSERT INTO Genre (Name) VALUES ('House');
		INSERT INTO Genre (Name) VALUES ('Electro Swing');
		INSERT INTO Genre (Name) VALUES ('Garage House');
		INSERT INTO Genre (Name) VALUES ('Progressive House');
		INSERT INTO Genre (Name) VALUES ('Celtic');
		INSERT INTO Genre (Name) VALUES ('Folk Rock');
		INSERT INTO Genre (Name) VALUES ('Indie Folk');
		INSERT INTO Genre (Name) VALUES ('Industrial Folk');
		INSERT INTO Genre (Name) VALUES ('Neofolk');
		INSERT INTO Genre (Name) VALUES ('Progressive Folk');
		INSERT INTO Genre (Name) VALUES ('Protest Song');
		INSERT INTO Genre (Name) VALUES ('Psychedelic Folk');
		INSERT INTO Genre (Name) VALUES ('Singer-Songwriter');
		INSERT INTO Genre (Name) VALUES ('Traditional Folk');
		INSERT INTO Genre (Name) VALUES ('Western Music');
		INSERT INTO Genre (Name) VALUES ('Alternative Hip Hop');
		INSERT INTO Genre (Name) VALUES ('Crunk');
		INSERT INTO Genre (Name) VALUES ('Drill');
		INSERT INTO Genre (Name) VALUES ('Industrial Hip Hop');
		INSERT INTO Genre (Name) VALUES ('Instrumental Hip Hop');
		INSERT INTO Genre (Name) VALUES ('Trap');
		INSERT INTO Genre (Name) VALUES ('Acid Jazz');
		INSERT INTO Genre (Name) VALUES ('Avante Garde Jazz');
		INSERT INTO Genre (Name) VALUES ('Bebop');
		INSERT INTO Genre (Name) VALUES ('Boogie Woogie');
		INSERT INTO Genre (Name) VALUES ('Bosssa Nova');
		INSERT INTO Genre (Name) VALUES ('Cool Jazz');
		INSERT INTO Genre (Name) VALUES ('Dixieland');
		INSERT INTO Genre (Name) VALUES ('Free Funk');
		INSERT INTO Genre (Name) VALUES ('Free Jazz');
		INSERT INTO Genre (Name) VALUES ('Jazz Blues');
		INSERT INTO Genre (Name) VALUES ('Fusion Jazz');
		INSERT INTO Genre (Name) VALUES ('Neoswing');
		INSERT INTO Genre (Name) VALUES ('Nu Jazz');
		INSERT INTO Genre (Name) VALUES ('Progressive Jazz');
		INSERT INTO Genre (Name) VALUES ('Psychedelic Jazz');
		INSERT INTO Genre (Name) VALUES ('Smooth Jazz');
		INSERT INTO Genre (Name) VALUES ('Swing');
		INSERT INTO Genre (Name) VALUES ('Big Band and Swing');
		INSERT INTO Genre (Name) VALUES ('Big Band & Swing');
		INSERT INTO Genre (Name) VALUES ('Vocal Jazz');
		INSERT INTO Genre (Name) VALUES ('Adult Contemporary');
		INSERT INTO Genre (Name) VALUES ('Baroque Pop');
		INSERT INTO Genre (Name) VALUES ('Christian Pop');
		INSERT INTO Genre (Name) VALUES ('Country Pop');
		INSERT INTO Genre (Name) VALUES ('Dance Pop');
		INSERT INTO Genre (Name) VALUES ('Electropop');
		INSERT INTO Genre (Name) VALUES ('Europop');
		INSERT INTO Genre (Name) VALUES ('Folk Pop');
		INSERT INTO Genre (Name) VALUES ('Indie Pop');
		INSERT INTO Genre (Name) VALUES ('K-Pop');
		INSERT INTO Genre (Name) VALUES ('Pop Rock');
		INSERT INTO Genre (Name) VALUES ('Soft Rock');
		INSERT INTO Genre (Name) VALUES ('Pop Punk');
		INSERT INTO Genre (Name) VALUES ('Emo Pop');
		INSERT INTO Genre (Name) VALUES ('Progressive Pop');
		INSERT INTO Genre (Name) VALUES ('Psychedelic Pop');
		INSERT INTO Genre (Name) VALUES ('Space Age Pop');
		INSERT INTO Genre (Name) VALUES ('Synthpop');
		INSERT INTO Genre (Name) VALUES ('Teen Pop');
		INSERT INTO Genre (Name) VALUES ('Funk');
		INSERT INTO Genre (Name) VALUES ('Freestyle');
		INSERT INTO Genre (Name) VALUES ('Alternative R&B');
		INSERT INTO Genre (Name) VALUES ('Rhythm And Blues');
		INSERT INTO Genre (Name) VALUES ('Rthymn & Blues');
		INSERT INTO Genre (Name) VALUES ('Soul');
		INSERT INTO Genre (Name) VALUES ('Doo Wop');
		INSERT INTO Genre (Name) VALUES ('Alternative Rock');
		INSERT INTO Genre (Name) VALUES ('Dream Pop');
		INSERT INTO Genre (Name) VALUES ('Grunge');
		INSERT INTO Genre (Name) VALUES ('Post-Grunge');
		INSERT INTO Genre (Name) VALUES ('Indie Rock');
		INSERT INTO Genre (Name) VALUES ('Math Rock');
		INSERT INTO Genre (Name) VALUES ('Slowcore');
		INSERT INTO Genre (Name) VALUES ('Christian Rock');
		INSERT INTO Genre (Name) VALUES ('Electronic Rock');
		INSERT INTO Genre (Name) VALUES ('Experimental Rock');
		INSERT INTO Genre (Name) VALUES ('Art Rock');
		INSERT INTO Genre (Name) VALUES ('Post Punk');
		INSERT INTO Genre (Name) VALUES ('Gothic Rock');
		INSERT INTO Genre (Name) VALUES ('Noise Rock');
		INSERT INTO Genre (Name) VALUES ('Post Rock');
		INSERT INTO Genre (Name) VALUES ('Post Metal');
		INSERT INTO Genre (Name) VALUES ('Folk Rock');
		INSERT INTO Genre (Name) VALUES ('Garage Rock');
		INSERT INTO Genre (Name) VALUES ('Hard Rock');
		INSERT INTO Genre (Name) VALUES ('Glam Rock');
		INSERT INTO Genre (Name) VALUES ('Heavy Metal');
		INSERT INTO Genre (Name) VALUES ('Jazz Rock');
		INSERT INTO Genre (Name) VALUES ('New Wave');
		INSERT INTO Genre (Name) VALUES ('Progressive Rock');
		INSERT INTO Genre (Name) VALUES ('Soft Rock');
		INSERT INTO Genre (Name) VALUES ('New Prog');
		INSERT INTO Genre (Name) VALUES ('Space Rock');
		INSERT INTO Genre (Name) VALUES ('Psychedelic Rock');
		INSERT INTO Genre (Name) VALUES ('Acid Rock');
		INSERT INTO Genre (Name) VALUES ('Punk Rock');
		INSERT INTO Genre (Name) VALUES ('Rap Rock');
		INSERT INTO Genre (Name) VALUES ('Rock And Roll');
		INSERT INTO Genre (Name) VALUES ('Rock & Roll');
		INSERT INTO Genre (Name) VALUES ('Southern Rock');
		INSERT INTO Genre (Name) VALUES ('Stoner Rock');
		INSERT INTO Genre (Name) VALUES ('Alternative Metal');
		INSERT INTO Genre (Name) VALUES ('Avante Garde Metal');
		INSERT INTO Genre (Name) VALUES ('Black Metal');
		INSERT INTO Genre (Name) VALUES ('Christian Metal');
		INSERT INTO Genre (Name) VALUES ('Death Metal');
		INSERT INTO Genre (Name) VALUES ('Doom Metal');
		INSERT INTO Genre (Name) VALUES ('Sludge Metal');
		INSERT INTO Genre (Name) VALUES ('Folk Metal');
		INSERT INTO Genre (Name) VALUES ('Celtic Metal');
		INSERT INTO Genre (Name) VALUES ('Funk Metal');
		INSERT INTO Genre (Name) VALUES ('Glam Metal');
		INSERT INTO Genre (Name) VALUES ('Gothic Metal');
		INSERT INTO Genre (Name) VALUES ('Grindcore');
		INSERT INTO Genre (Name) VALUES ('Metalcore');
		INSERT INTO Genre (Name) VALUES ('Nu Metal');
		INSERT INTO Genre (Name) VALUES ('Post Metal');
		INSERT INTO Genre (Name) VALUES ('Progressive Metal');
		INSERT INTO Genre (Name) VALUES ('Rap Metal');
		INSERT INTO Genre (Name) VALUES ('Thrash Metal');
		INSERT INTO Genre (Name) VALUES ('Christian Punk');
		INSERT INTO Genre (Name) VALUES ('Art Punk');
		INSERT INTO Genre (Name) VALUES ('Folk Punk');
		INSERT INTO Genre (Name) VALUES ('Celtic Punk');
		INSERT INTO Genre (Name) VALUES ('Garage Punk');
		INSERT INTO Genre (Name) VALUES ('Hardcore Punk');
		INSERT INTO Genre (Name) VALUES ('Post Hardcore');
		INSERT INTO Genre (Name) VALUES ('Emo');
		INSERT INTO Genre (Name) VALUES ('Emo Pop');
		INSERT INTO Genre (Name) VALUES ('Screamo');
		INSERT INTO Genre (Name) VALUES ('Ska Punk)
        '''

        dbCursor.execute(genresToInsert)
        dbCursor.execute('SELECT COUNT(RowID) FROM Genre')
        genresInDB = dbCursor.fetchall()
        database.commit()
        MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Added ' + str(len(genresInDB.count)) + ' genres to Genre table')

    database.close()

def testDatabaseAction():
    '''
    Purpose: used for testing database logic
    '''
    connection = sqlite3.connect(MethodBank.mainDB())
    dbCursor = connection.cursor()

    rows = dbCursor.execute('SELECT * FROM Song').fetchall()
    for row in rows:
        print(row)

def loadDataFromDatabase():
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Load data from database')
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Connecting to database')

    database = sqlite3.connect(MethodBank.mainDB())
    dbCursor = database.cursor()

    # Get artist data.
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Retrieving Artist IDs')

    dbCursor.execute('SELECT RowID FROM Artist ORDER BY RowID ASC')
    artistDataInDB = dbCursor.fetchall()

    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Database returned ' + str(len(artistDataInDB)) + ' Artist IDs')

    for artistInDB in artistDataInDB:
        tempArtistObj = Artist()
        tempArtistObj.loadFromDB(database, artistInDB[0])
        artists.append(tempArtistObj)

    MethodBank.writeToLog(LoggingLevel.VERBOSE, str(len(artists)) + ' Artist objects created')

    # Get album data (also loads songs)
    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Retrieving Album IDs and Song IDs')

    dbCursor.execute('SELECT RowID FROM Album ORDER BY RowID ASC')
    albumDataInDB = dbCursor.fetchall()

    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Database returned ' + str(len(albumDataInDB)) + ' Album IDs')

    for albumInDB in albumDataInDB:
        tempAlbumObj = Album()
        tempAlbumObj.loadFromDB(database, albumInDB[0])
        albums.append(tempAlbumObj)

    MethodBank.writeToLog(LoggingLevel.VERBOSE, str(len(albums)) + ' Album objects created')

    totalSongs = 0
    for album in albums:
        totalSongs += len(album.getSongs())

    MethodBank.writeToLog(LoggingLevel.VERBOSE, str(totalSongs) + ' Song objects created')

    MethodBank.writeToLog(LoggingLevel.VERBOSE, 'Retrieving Genre data')
    Genre.initialize(database)

    database.close()

if __name__ == '__main__' : main()
