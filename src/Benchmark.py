import time
#===============================================================================================
class Benchmark:
	#===============================================================================================
	def __init__(self, desc : str, fct, *args):
		self.startTime = None
		self.fct = fct
		self.fct_args = [arg for arg in args]
		self.desc = desc
		self.timeFunc()
	#===============================================================================================
	def timeFunc(self) -> float:
		self.startTime = time.time()
		(lambda *args:self.fct(*args))(*self.fct_args)
		duration = time.time() - self.startTime
		formattedDuration = "{0:.3f}".format(duration)
		print(f'{self.desc} time : {formattedDuration}s\n')
		return duration