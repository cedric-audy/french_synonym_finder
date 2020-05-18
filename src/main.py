import argparse
import sys

from CoocDB import CoocDB
from Cooc import Cooc
from Model import Model

#===============================================================================================
usage = '''Usage:
	main.py -e -t <taille> --enc <encoding> --chemin <path>
	main.py -r -t <taille>
	main.py -c
	main.py --reset

[Options]
	-e        entraînement
	-r        recherche
	-c        trim DB
	--reset   reset DB'''

#===============================================================================================
def print_usage_and_exit(exitMsg : str = ""):
	print(usage)
	sys.exit(exitMsg)

#===============================================================================================
def parse_args():
	parser = argparse.ArgumentParser(description='Cooc matrix argParser')
	mutualExclusion = parser.add_mutually_exclusive_group()
	mutualExclusion.add_argument('-e', action='store_true')
	mutualExclusion.add_argument('-r', action='store_true')
	mutualExclusion.add_argument('-c', action='store_true')
	mutualExclusion.add_argument('--reset', action='store_true')
	parser.add_argument('-t', type=int)
	parser.add_argument('--enc', type=str)
	parser.add_argument('--chemin', type=str, nargs='+', action='append')

	args = parser.parse_args()

	if not args.c and not args.reset:
		if args.e and (args.t is None or args.enc is None or args.chemin is None):
			print_usage_and_exit('training requires window width, encoding and path(s)')
		if args.r and args.t is None:
			print_usage_and_exit('searching requires odd window size')
		if args.t is not None and args.t % 2 == 0:
			print_usage_and_exit('window size must be odd')
		if not args.r and not args.e and not args.c and not args.reset is None:
			print_usage_and_exit()
	return args

#===============================================================================================
if __name__ == '__main__':
	args = parse_args()
	if args.e:
		cooc = Cooc(args.t, args.enc, args.chemin)
		cooc.loadTrainingData()
		cooc.train()
	elif args.r and args.t:
		model = Model()
		model.prepMatrix(args.t)
		model.showMenu(args.t)
	elif args.c or args.reset:
		db = CoocDB()
		if args.c:
			db.trim()
		if args.reset:
			if input('Reset DB? Y for yes :  ').split(" ")[0] == 'Y':
				db.init()
				print('DB deleted')
			else:
				print('DB not deleted')
