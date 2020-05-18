from typing import Dict, List, Set, Tuple

import numpy as np
import itertools

from Book import Book
from CoocDB import CoocDB
from exceptions import WordNotFound

# ===============================================================================================
STOP_WORDS_FILE = './stopWords.txt'
# ===============================================================================================
algos = {	0: {	'func'		: lambda vec1, vec2: int(np.multiply(vec1, vec2).sum()),
               'invSorting': False},
          1: {	'func'		: lambda vec1, vec2: int(np.square(vec1 - vec2).sum()),
               'invSorting': True},
          2: {	'func' 		: lambda vec1, vec2: int(np.absolute(vec1 - vec2).sum()),
               'invSorting': True}
          }
# ===============================================================================================
class Model:
    #===============================================================================================
    def __init__(self):
        self.words: Dict[str, int] = {}
        self.coocPairs = None
        self.stopWords = None
        self.coocMatrix: np.ndarray = None
        self.db = CoocDB()
    #===============================================================================================
    def parseBook(self, book, halfWindowSize, matrixWidth):
        # transférer les mots en indexes
        indexBook = [self.words[word] for word in book.data]
        for i in range(1, halfWindowSize):
            for j in range(0, i):
                # here, we append the coocs i distance at i-1 index of a 2d array, so that self.coocPairs[0] is not empty/useless
                self.coocPairs[i-1].extend(zip(
                    indexBook[j::i],
                    indexBook[j+i::i]))
    #===============================================================================================
    def train(self, books: List[Book], windowSize: int) -> None:
        self.words = self.db.getWordDict()

        newWords = []
        for book in books:
            for word in book.data:
                if word not in self.words:
                    newWords.append(word)
        self.db.feedNewWords(newWords)
        self.words = self.db.getWordDict()

        matrixWidth = self.db.getDictRowSize()
        halfWindowSize = (windowSize // 2)
        self.coocPairs = []
        for i in range(halfWindowSize):
            self.coocPairs.append([])
        for book in books:
            self.parseBook(book, halfWindowSize + 1, matrixWidth)

        for i in range(1, halfWindowSize+1):
            self.db.newCoocEntries(self.coocPairs[i-1], i)
        return None
    # =======================================================================================================
    def prepMatrix(self, windowSize):
        self.words = self.db.getWordDict()
        # Construct matrix cooc
        coocs = self.db.select('num_coocs')
        size = self.db.getDictRowSize()
        self.coocMatrix = np.zeros((size, size))

        self.stopWords = Model.getStopWords()
        for id1, id2, distance, frequency in coocs:
            if distance <= windowSize // 2:
                self.coocMatrix[id1][id2] += frequency
                self.coocMatrix[id2][id1] += frequency
    # =======================================================================================================
    def getSynonyms(self, targetWord: str, windowSize: int, nbSynonyms: int, scoringMethodIndex: int) -> List[Tuple[str, int]]:
        scoreAlgo = algos[scoringMethodIndex]['func']
        reverseSort = algos[scoringMethodIndex]['invSorting']
        try:
            targetVec: np.narray = self.coocMatrix[self.words[targetWord]]
        except:
            raise WordNotFound
        scores = zip([scoreAlgo(targetVec, row)
                      for row in self.coocMatrix], self.words.keys())
        scores = sorted(scores, reverse=reverseSort)
        results = []
        while len(results) < nbSynonyms:
            score, word = scores.pop()
            if word != targetWord and word not in self.stopWords:
                results.append((word, score))
        return results
    #===============================================================================================
    @staticmethod
    def getStopWords():
        # print(STOP_WORDS_FILE)
        with open(STOP_WORDS_FILE, 'r', encoding = 'utf-8') as file:
            s = file.read()[1:]
            return s.splitlines()
    #===============================================================================================
    def showMenu(self, windowSize) -> None:
        exitRequested = False
        while not exitRequested:
            print('Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul,\ni.e. produit scalaire: 0, least-squares: 1, city-block: 2\n')
            print('Tapez q pour quitter\n')
            args = input().split(' ')
            print()
            if len(args) == 3:
                targetWord = args[0]
                nbSynonyms = int(args[1])
                scoringMethodIndex = int(args[2])
                try:
                    results = self.getSynonyms(
                        targetWord, windowSize, nbSynonyms, scoringMethodIndex)
                    for word, score in results:
                        print(f'{word} --> {score}')
                    print()
                except WordNotFound:
                    print(f'Word \"{targetWord}\" not found in model.')
            else:
                if args[0] == 'q':
                    exitRequested = True
                else:
                    print('invalid input')
                    continue
        return None
