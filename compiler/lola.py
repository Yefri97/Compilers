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

    # Create Parser
    parser = LolaParser()

    # Create class that draw the AST
    dot = DotCode()

    # Menu
    print ("1. Analizador Léxico")
    print ("2. Analizado Sintáctico")
    print ("3. Generar código para árbol en Graphviz")
    print ("4. Analizador Semántico")

    opcion = input()
    if opcion == "1":
        for tok in lexer.tokenize(data):
            sys.stdout.write('%s\n' % tok)
    elif opcion == "2":
            result = parser.parse(lexer.tokenize(data))
            if result:
                result.pprint()
            else:
                print ("No arbol")
    elif opcion == "3":
                root = parser.parse(lexer.tokenize(data))
                dot.visit(root)
                print(dot)
    elif opcion == "4":
        check = LolaCheck()
        check.visit(root)
