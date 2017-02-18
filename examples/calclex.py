# calclex.py
# Calculadora Analizador Léxico

from sly import Lexer

class CalcLexer(Lexer):
    # Set of reserved names (language keywords)
    reserved_words = { 'WHILE', 'IF', 'ELSE', 'PRINT' }

    # Set of token names.   This is always required
    tokens = {
        'NUMBER',
        'ID',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'ASSIGN',
        'EQ',
        'LT',
        'LE',
        'GT',
        'GE',
        'NE',
        *reserved_words,
        }

    literals = { '(', ')', '{', '}', ';' }

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ      = r'=='
    ASSIGN  = r'='
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        # Check if name matches a reserved word (change token type if true)
        if t.value.upper() in self.reserved_words:
            t.type = t.value.upper()
        return t

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, value):
        print('Line %d: Bad character %r' % (self.lineno, value[0]))
        self.index += 1

if __name__ == '__main__':
    data = '''
# Counting
x = 0;
while (x < 10) {
    print x:
    x = x + 1;
}
'''
    lexer = CalcLexer()
    for tok in lexer.tokenize(data):
        print(tok)
