import sqlite3

#===============================================================================================
class Command:
    ENABLE_FK = 'PRAGMA foreign_keys = 1'

    DROP_WORD_DICT = 'DROP TABLE IF EXISTS word_dict'
    CREATE_WORD_DICT = '''
CREATE TABLE IF NOT EXISTS word_dict
(
    id INTEGER PRIMARY KEY,
    word TEXT UNIQUE
)
'''
    DROP_NUMCOOCS = 'DROP TABLE IF EXISTS num_coocs'
    CREATE_NUMCOOCS = '''
CREATE TABLE IF NOT EXISTS num_coocs
(
    id INTEGER NOT NULL REFERENCES word_dict(id),
    id2 INTEGER NOT NULL REFERENCES word_dict(id),
    dist INTEGER NOT NULL,
    freq INTEGER NOT NULL
)
'''
    INSERT_NEW_WORD = 'INSERT INTO word_dict (id, word) VALUES (?, ?)'
    INSERT_FRESH_COOC = 'INSERT INTO num_coocs VALUES (?,?,?,1)'
    INSERT_COUNTED_COOC = 'INSERT INTO num_coocs VALUES (?,?,?,?)'
    UPDATE_COOC = 'UPDATE num_coocs SET frequence = frequence + 1 WHERE (id = ? AND id2 = ? AND dist = ?)'
    GET_COOCS_X_DIST = 'SELECT id, id2 FROM num_coocs WHERE dist = ?'

#===============================================================================================
class CoocDB:
    PATH = './coocBD.bd'
    #===============================================================================================
    def __init__(self):
        self.connection = sqlite3.connect(CoocDB.PATH)
        self.cursor = self.connection.cursor()
        if not self.isInit():
            self.init()
        self.execute(Command.ENABLE_FK)
    #===============================================================================================
    def execute(self, command) -> sqlite3.Cursor:
        answer = self.cursor.execute(command)
        return answer
    #===============================================================================================
    def isInit(self) -> bool:
        r = self.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='num_coocs' ''')
        return r.fetchone()[0] > 0
    #===============================================================================================
    def init(self) -> None:
        self.execute(Command.DROP_NUMCOOCS)
        self.execute(Command.DROP_WORD_DICT)
        self.execute(Command.CREATE_WORD_DICT)
        self.execute(Command.CREATE_NUMCOOCS)
        return None
    #===============================================================================================
    def getWordDict(self) -> dict:
        d = dict(self.select('word_dict'))
        d = { value:key for key, value in d.items()}
        return d
    #===============================================================================================
    def manyExecs(self, operation, tuples) -> None:
        try:
            self.cursor.executemany(operation, tuples)
            self.connection.commit()
        except:
            print('input list contains => 1 instance(s) already in table, no input inserted')
        return None
    #===============================================================================================
    def feedNewWords(self, strArr) -> None:
        '''this function feeds new words ONLY to the DB'''
        strArr = set(strArr) #one redundant word and it doesnt work
        cursize = self.getDictRowSize()
        WordTuples = zip(strArr,range(cursize ,cursize+len(strArr)))
        WordTuples = [(i,w) for w,i in WordTuples]
        self.manyExecs(Command.INSERT_NEW_WORD, WordTuples)
        return None
    #===============================================================================================
    def newCoocEntries(self, coocs, dist) -> None:
        self.manyExecs(Command.INSERT_FRESH_COOC,((a,b,dist) for a,b in coocs))
        return None
    #===============================================================================================
    def select(self, table):
        self.cursor.execute('SELECT * FROM {}'.format(table))
        return self.cursor.fetchall()
    #===============================================================================================
    def getDictRowSize(self) -> int:
        '''number of entries in word dictionnary'''
        self.cursor.execute('SELECT COUNT(*) from word_dict')
        return self.cursor.fetchall()[0][0] #unpacking
    #===============================================================================================
    def trim(self):
        '''takes all coocs as tuples and merges/counts all of them. recreates a table where num_coocs size = word_dict size'''
        coocs = tuple(self.select('num_coocs'))
        init_len = len(coocs)

        #probably a faster way to do this
        cooc_count_dict = { (a,b,c):1 for a,b,c,d in set(coocs)}
        for id1,id2,dist,freq in coocs:
            cooc_count_dict[(id1,id2,dist)]+=freq
        compact_coocs = [(a[0],a[1],a[2],b) for a,b in cooc_count_dict.items()]

        self.execute(Command.DROP_NUMCOOCS)
        self.execute(Command.CREATE_NUMCOOCS)
        self.manyExecs(Command.INSERT_COUNTED_COOC, compact_coocs)
        print('DB trimmed down from ' + str(init_len) + ' to ' + str(len(self.select('num_coocs'))) + ' rows')
