# An implementation of Dartmouth BASIC (1964)

from sly import Parser
from baslex import BasicLexer

class BasicParser(Parser):
	debugfile = 'parser.out'

	tokens = BasicLexer.tokens

	# Un programa BASIC es una serie de instrucciones.
	# Representamos el programa como un diccionario de 
	# tuplas indexado por el numero de lineas
	

	# program : program statement
	#         | statement
	
	@_('program statement',
	   'statement')
	def program(self, p):
		pass 
	
	@_('error')
	def program(self, p):
		pass 
	
	# statement : INTEGER command NEWLINE
	
	@_('INTEGER command NEWLINE')
	def statement(self, p):
		pass

	# statement : RUN NEWLINE
	#           | LIST NEWLINE
	#           | NEW NEWLINE
	
	@_('RUN NEWLINE',
	   'LIST NEWLINE',
	   'NEW NEWLINE')
	def statement(self, p):
		pass

	# statement : INTEGER NEWLINE

	@_('INTEGER NEWLINE')
	def statement(self, p):
		pass
	
	# Manejo de errores en instrucciones

	@_('INTEGER error NEWLINE')
	def statement(self, p):
		pass
	
	# statement : NEWLINE

	@_('NEWLINE')
	def statement(self, p):
		pass
	
	# command : LET variable EQUALS expr
	
	@_('LET variable EQUALS expr')
	def command(self, p):
		pass

	@_('LET variable EQUALS error')
	def command(self, p):
		pass

	# command : READ varlist

	@_('READ varlist')
	def command(self, p):
		pass

	@_('READ error')
	def command(self, p):
		pass
	
	# command : DATA numlist

	@_('DATA numlist')
	def command(self, p):
		pass

	@_('DATA error')
	def command(self, p):
		pass

	# command : PRINT plist optend

	@_('PRINT plist optend')
	def command(self, p):
		pass

	@_('PRINT error')
	def command(self, p):
		pass

	# Terminaciones opcionales de PRINT. Puede ser coma (,) o punto y coma (;)
	@_('COMMA', 'SEMI', 'empty')
	def optend(self, p):
		pass

	# command : PRINT
	
	@_('PRINT')
	def command(self, p):
		pass

	# command : GOTO INTEGER

	@_('GOTO INTEGER')
	def command(self, p):
		pass

	@_('GOTO error')
	def command(self, p):
		pass

	# command : IF relexpr THEN INTEGER

	@_('IF relexpr THEN INTEGER')
	def command(self, p):
		pass

	@_('IF error THEN INTEGER')
	def command(self, p):
		pass

	@_('IF relexpr THEN error')
	def command(self, p):
		pass

	# command : FOR ID EQUALS expr TO expr optstep

	@_('FOR ID EQUALS expr TO expr optstep')
	def command(self, p):
		pass

	@_('FOR ID EQUALS error TO expr optstep')
	def command(self, p):
		pass

	@_('FOR ID EQUALS expr TO error optstep')
	def command(self, p):
		pass

	@_('FOR ID EQUALS expr TO expr STEP error')
	def command(self, p):
		pass
	
	# optstep : STEP expr
	#         | empty

	@_('STEP expr',
	   'empty')
	def optstep(self, p):
		pass

	# command : NEXT ID

	@_('NEXT ID')
	def command(self, p):
		pass

	@_('NEXT error')
	def command(self, p):
		pass

	# command : END
	
	@_('END')
	def command(self, p):
		pass

	# command : REM
	
	@_('REM')
	def command(self, p):
		pass
		
	# command : STOP
	
	@_('STOP')
	def command(self, p):
		pass

	# command : DEF ID LPAREN ID RPAREN EQUALS expr
	
	@_('DEF ID LPAREN ID RPAREN EQUALS expr')
	def command(self, p):
		pass
		
	@_('DEF ID LPAREN ID RPAREN EQUALS error')
	def command(self, p):
		pass

	@_('DEF ID LPAREN error RPAREN EQUALS expr')
	def command(self, p):
		pass

	# command : GOSUB INTEGER

	@_('GOSUB INTEGER')
	def command(self, p):
		pass
	
	@_('GOSUB error')
	def command(self, p):
		pass

	# command : RETURN

	@_('RETURN')
	def command(self, p):
		pass

	# command : DIM dimlist

	@_('DIM dimlist')
	def command(self, p):
		pass

	@_('DIM error')
	def command(self, p):
		pass

	# dimlist : dimlist COMMA dimitem
	#         | dimitem	

	@_('dimlist COMMA dimitem',
	   'dimitem')
	def dimlist(self, p):
		pass

	# dimitem : ID LPAREN INTEGER RPAREN
	#         | ID LPAREN INTEGER COMMA INTEGER RPAREN

	@_('ID LPAREN INTEGER RPAREN')
	def dimitem(self, p):
		pass
	
	@_('ID LPAREN INTEGER COMMA INTEGER RPAREN')
	def dimitem(self, p):
		pass
	
	# expr : expr PLUS expr
	#      | expr MINUS expr
	#      | expr TIMES expr
	#      | expr DIVIDE expr
	#      | expr POWER expr
	
	@_('expr PLUS expr',
	   'expr MINUS expr',
	   'expr TIMES expr',
	   'expr DIVIDE expr',
	   'expr POWER expr',)
	def expr(self, p):
		pass
	
	# expr : INTEGER
	#      | FLOAT
	
	@_('INTEGER',
	   'FLOAT')
	def expr(self, p):
		pass
	
	# expr : variable

	@_('variable')
	def expr(self, p):
		pass
	
	# expr : LPAREN expr RPAREN

	@_('LPAREN expr RPAREN')
	def expr(self, p):
		pass

	# expr : MINUS expr
	
	@_('MINUS expr')
	def expr(self, p):
		pass

	# relexpr : expr LT expr
	#         | expr LE expr
	#         | expr GT expr
	#         | expr GE expr
	#         | expr EQUALS expr
	#         | expr NE expr
# ----------------------------------------------------------------------
# NO CAMBIE NADA A PARTIR DE AQUI
# ----------------------------------------------------------------------
if __name__ == '__main__':
	import sys
	
	if len(sys.argv) != 2:
		sys.stderr.write("Usage: %s filename\n" % sys.argv[0])
		raise SystemExit(1)
	
	lexer = BasicLexer()
	parser = BasicParser()
	parser.parse(open(sys.argv[1]).read())
