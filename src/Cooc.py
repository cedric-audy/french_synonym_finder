from typing import List

from Book import Book
from Benchmark import Benchmark
from exceptions import WordNotFound
from Model import Model

#===============================================================================================
class Cooc:
	#===============================================================================================
	def __init__(self, window, encoding, filePaths):
		self.windowSize = window
		self.encoding = encoding
		self.filePaths = filePaths[0]
		self.books : List[Book] = []
		self.model = Model()
	#===============================================================================================
	def loadTrainingData(self) -> None:
		for file in self.filePaths:
			print(file)
			self.books.append(Book(file, self.encoding))
		return None
	#===============================================================================================
	def train(self, *args) -> None:
		self.model.train(self.books, self.windowSize)
		return None
	#===============================================================================================

