# --------------------------------------------------------------
# compiler: lola.py
#
# Compiler of lola lenguage
#
# --------------------------------------------------------------

# import modules
import sys
from lolalex import LolaLexer

# MAIN
if __name__ == '__main__':
    # Verify that the user enters one file
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s filename\n' % sys.argv[0])
        raise SystemExit(1)
    # Load file
    data = open(sys.argv[1]).read()

    # Create lexer
    lexer = LolaLexer()
    for tok in lexer.tokenize(data):
        sys.stdout.write('%s\n' % tok)
