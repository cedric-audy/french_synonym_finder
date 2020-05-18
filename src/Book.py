import re
from typing import List
#===============================================================================================
class Book:
	'''Charger et cleaner un livre'''
	nonWordCharPattern = re.compile('[^\\w]')
	#===============================================================================================
	def __init__(self, filePath, enc):
		self.data : List[str] = None
		with open(filePath, 'r', encoding = enc) as file:
			self.data = Book._clean(file.read()).split()
	#===============================================================================================
	@staticmethod
	def _clean(rawText : str) -> str:
		return Book.nonWordCharPattern.sub(' ', rawText).lower()