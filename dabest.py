import sqlite3

def mess_with_db(func, *args):
    # for everything that requires the database
    # add some error-handling later ok?
    def wrapper(*args):
        db = sqlite3.connect('chars.db')
        cursor = db.cursor()
        retval = func(db, cursor, *args)
        db.close()
        return retval
        
    return wrapper
        
@mess_with_db
def createNewDatabase(db, cursor):
    cursor.execute('''
        CREATE TABLE worlds (
        world_id integer PRIMARY KEY AUTOINCREMENT,
        name text NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE  characters (
            char_id integer PRIMARY KEY AUTOINCREMENT,
            name text,
            world_id integer,
                FOREIGN KEY ( world_id ) REFERENCES worlds ( char_id )
        );
    ''')
    
    cursor.execute('''
        CREATE TABLE chardata (
            id integer PRIMARY KEY AUTOINCREMENT,
            label text NOT NULL,
            content text,
            owner_id integer NOT NULL, 
                FOREIGN KEY ( owner_id ) REFERENCES characters ( char_id )
        );
    ''')
    db.commit()
    
@mess_with_db
def droptables(db, cursor):
    """Drop everything. Be careful!"""
    cursor.execute('''DROP TABLE IF EXISTS worlds;''')
    cursor.execute('''DROP TABLE IF EXISTS characters''')
    cursor.execute('''DROP TABLE IF EXISTS chardata''')
    db.commit()
    
@mess_with_db
def listAllChars(db, cursor):
    cursor.execute('''SELECT char_id, name FROM characters''')
    allchars = cursor.fetchall()
    return allchars
    
@mess_with_db
def addChar(db, cursor, name):
    cursor.execute('''INSERT INTO characters (name) VALUES (:name)''', {'name':name})
    db.commit()
    
@mess_with_db
def getChar(db, cursor, charid):
    charid = str(charid)
    character = {}
    cursor.execute('''
        SELECT char_id, name 
        FROM characters 
        WHERE char_id=?''', charid )
   
    singlechar = cursor.fetchone()
    if singlechar is None:
        return "NOCHAR"
    character['id'] = singlechar[0]
    character['name'] = singlechar[1]
    
    cursor.execute ('''
        SELECT label, content
        FROM chardata
        WHERE owner_id=?''', (charid))
    for row in cursor.fetchall():
        character[row[0]] = row[1]
    
    return character
    
@mess_with_db
def addCharData(db, cursor, charid, label, content):
    charid = str(charid)
    cursor.execute('''
        INSERT INTO chardata (label, content, owner_id) 
        VALUES (:label, :content, :owner_id)''', {'label': label, 'content':content, 'owner_id':charid}
    )
    db.commit()

@mess_with_db
def removeCharData(db, cursor, charid, label):
    charid = str(charid)
    cursor.execute('''
        DELETE FROM chardata
        WHERE label=:label AND owner_id=:owner_id''', {'label': label, 'owner_id': charid}
    )
    db.commit()

@mess_with_db
def editCharData(db, cursor, charid, label, content):
    charid = str(charid)
    cursor.execute('''
        UPDATE chardata
        SET content = :content
        WHERE label=:label AND owner_id=:owner_id''', {'content': content, 'label': label, 'owner_id': charid}
    )
    db.commit()
