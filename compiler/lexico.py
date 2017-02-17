from sly import Lexer

class LexLola(Lexer):

	# Set reserved words
	reserved_words = {
		'BIT', 'TS', 'OC','BEGIN', 'CONST', 'END', 'IN', 'INOUT', 'MODULE',
		'OUT','REG', 'TYPE', 'VAR', 'FOR', 'MUX', 'LATCH', 'SR', 'DIV',
		'MOD', 'IF', 'THEN', 'ELSIF', 'ELSE', 'DO',
	}

	# Set tokens
	token = { 'IDENTIFIER', 'INTEGER', 'LOGICVALUE', *reserved_words }

	# Set literals
    literals = { '~', '&', '|', '^', '+', '-', '*', '=', '#', '<', '<=', '>', '>=',
    '(', ')', '[', ']', '{', '}', '->', '.', ',', ';', ':', ':=', "'", '!' , '↑', '/'}

	# Ingone spaces and tabs
	ignore = ' \t'

	# Rules for tokens
	LOGICVALUE = r'\'[01]'

	@_(r'\d+')
	def INTEGER(self, t):
		t.value = int(t.value)
		return t

	@_(r'[a-zA-Z][A-Z0-9]*')
	def IDENTIFIER(self, t):
		if t.value in self.keywords:
			t.type = t.value
		return t
