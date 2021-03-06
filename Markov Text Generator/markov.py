from db import Db
from gen import Generator
from parse import Parser
from sql import Sql
from rnd import Rnd
import sys
import sqlite3
import codecs

SENTENCE_SEP = '.'
WORD_SEP = ' '

if __name__ == '__main__':
	#get arguments from the cmd line
	args = sys.argv
	usage = 'Usage: %s (parse <name> <depth> <path to txt file>|gen <name> <count>)' % (args[0], )

	#len(args) counts the number of arguments passed
	if (len(args) < 3):
		raise ValueError(usage)

	mode  = args[1] #parse or gen
	name  = args[2]	#depth or count
	
	if mode == 'parse':
		if (len(args) != 5): #implying 4 arguements plus args[0]
			raise ValueError(usage)
		
		depth = int(args[3]) 
		file_name = args[4]  
		
		db = Db(sqlite3.connect(name + '.db'), Sql())
		db.setup(depth)
		
		txt = codecs.open(file_name, 'r', 'utf-8').read()
		Parser(name, db, SENTENCE_SEP, WORD_SEP).parse(txt)
	
	elif mode == 'gen':
		count = int(args[3])
		db = Db(sqlite3.connect(name + '.db'), Sql())
		generator = Generator(name, db, Rnd())
		for i in range(0, count):
			print generator.generate(WORD_SEP)
	
	else:
		raise ValueError(usage)