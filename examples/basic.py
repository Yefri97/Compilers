# basic.py
# BASIC Compiler

from sly import Lexer

class BasicLexer(Lexer):

	keywords = (
		'LET', 'READ', 'DATA', 'PRINT', 'GOTO', 'IF', 'THEN',
		'FOR', 'TO', 'STEP', 'NEXT', 'END', 'STOP', 'DEF',
		'GOSUB', 'RETURN', 'DIM', 'REM', 'RUN', 'LIST',
		'NEW'
	)

	tokens = keywords + (
		'PLUS', 'MINUS', 'TIMES', 'DIVISION', 'POWER',
		'LT', 'LE', 'GT', 'GE', 'EQUALS', 'NE',
		'ID', 'INTEGER', 'FLOAT', 'STRING', 'NEWLINE',
	)

	literals = { '(', ')', ',', ';' }
	ignore = ' \t'

	# Definicion de Simbolos (tokes)

	EQUALS   = r'='
	PLUS     = r'\+'
	MINUS    = r'-'
	TIMES    = r'\*'
	DIVISION = r'/'
	POWER    = r'^'
	LT       = r'<'
	LE       = r'<='
	GT       = r'>'
	GE       = r'>='
	NE       = r'<>'
	STRING   = r'\".*\"'

	@_(r'\d+')
	def INTEGER(self, t):
		t.value = int(t.value)
		return t

	@_(r(('\d*\.\d+)(E[-+]?\d+)?|([1-9]\d*)(E[-+]?\d+))')
	def FLOAT(self, t):
		t.value = float(t.value)
		return t


	@_(r'REM .*')
	def REM(self, t):
		return t

	@_(r'[A-Z][A-Z0-9]*')
	def ID(self, t):
		if t.value in self.keywords:
			t.type = t.value
		return t

	@_(r'\n')
	def NEWLINE(self, t):
		self.lineno += 1
		return t

	def error(self, value):
		print('caracter ilegal: %s' % value[0])
		self.index += 1

# --------------------------------------------------------------
# MAIN
# --------------------------------------------------------------
if __name__ == '__main__':
	import sys

	if len(sys.argv) != 2:
		sys.stderr.write('Usage: %s filename\n' % sys.argv[0])
		raise SystemExit(1)

	lexer = BasicLexer()
	for tok in lexer.tokenize(open(sys.argv[1]).read()):
	sys.stdout.write('%s\n' % tok)
