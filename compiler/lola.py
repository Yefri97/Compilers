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
from lolacode import GenerateCode

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

    # Create class that check the program
    check = LolaCheck()

    # Create class that generate the code
    gen = GenerateCode()

    # Menu
    print ("1. Analizador Léxico")
    print ("2. Analizado Sintáctico")
    print ("3. Generar código para árbol en Graphviz")
    print ("4. Analizador Semántico")
    print ("5. Generador de codigo")

    opcion = input()
    if opcion == "1":
        for tok in lexer.tokenize(data):
            sys.stdout.write('%s\n' % tok)
    elif opcion == "2":
        root = parser.parse(lexer.tokenize(data))
        if root:
            root.pprint()
        else:
            print ("No arbol")
    elif opcion == "3":
        # root of the AST
        root = parser.parse(lexer.tokenize(data))
        dot.visit(root)
        print(dot)
    elif opcion == "4":
        # root of the AST
        root = parser.parse(lexer.tokenize(data))
        check.visit(root)
    else:
        # root of the AST
        root = parser.parse(lexer.tokenize(data))
        check.visit(root)
        # print(root.typeDec.list[0].body.list[0].var.type)
        # exit()
        gen.visit(root)

        for inst in gen.code:
            print(inst)
