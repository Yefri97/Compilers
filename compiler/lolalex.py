# --------------------------------------------------------------
# compiler: lolalex.py
#
# Lexical analyzer of lola lenguage
#
# --------------------------------------------------------------

# import modules
from sly import Lexer

# CLASS LolaLexer
class LolaLexer(Lexer):

	# Set of reserved words
	reserved_words = {
		'BIT', 'TS', 'OC','BEGIN', 'CONST', 'END', 'IN', 'INOUT', 'MODULE',
		'OUT','REG', 'TYPE', 'VAR', 'FOR', 'MUX', 'LATCH', 'SR', 'DIV',
		'MOD', 'IF', 'THEN', 'ELSIF', 'ELSE', 'DO',
	}

	# Set of tokens
	tokens = {
		'IDENTIFIER', 'INTEGER', 'LOGICVALUE', 'LE', 'GE', 'AS', 'TP', *reserved_words
	}

	# Set of literals
	literals = {
		'~', '&', '|', '^', '+', '-', '*', '#', '<', '>', '(', ')', '[', ']',
		'{', '}', '.', ',', ';', ':', '\'', '!' , '↑', '/'
	}

	# Ingone spaces and tabs
	ignore = ' \t'

	# Ignore comments (* Comment *)
	ignore_comment = r'\(\*(([^*])|(\*+[^*)]))*\*+\)'

	# Count newlines
	@_(r'\n')
	def ignore_newline(self, t):
		self.lineno += 1
		return t

	# Rules for tokens
	LE = r'<='
	GE = r'>='
	AS = r':='
	TP = r'\.\.'

	@_(r'\d+')
	def INTEGER(self, t):
		t.value = int(t.value)
		return t

	@_(r'[a-zA-Z][a-zA-Z0-9]*')
	def IDENTIFIER(self, t):
		if t.value in self.reserved_words:
			t.type = t.value
		return t

	@_(r'\'[01]')
	def LOGICVALUE(self, t):
		t.value = int(t.value[1:])
		return t

	# Message error
	def error(self, value):
		print('Line %d: Bad character %r' % (self.lineno, value[0]))
		self.index += 1
