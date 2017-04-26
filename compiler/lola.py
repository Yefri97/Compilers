# --------------------------------------------------------------
# compiler: lola.py
#
# Compiler of lola language
#
# --------------------------------------------------------------

# import modules
from lolalex import LolaLexer
from lolaparse import LolaParser
from lolacheck import CheckProgramVisitor as LolaCheck
from lolaDOT import DotCode

# MAIN
if __name__ == '__main__':
    import sys
    # Verify that the user enters one file
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s filename\n' % sys.argv[0])
        raise SystemExit(1)
    # Load file
    data = open(sys.argv[1]).read()

    # Create lexer
    lexer = LolaLexer()
    # Create parser
    parser = LolaParser()
    # Create class that draw the AST
    #dot = DotCode()
    check = LolaCheck()

    root = parser.parse(lexer.tokenize(data))
    check.visit(root)
    #dot.visit(root)

    #print(dot)
