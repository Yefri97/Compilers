# --------------------------------------------------------------
# compiler: lolaparse.py
#
# Grammar analyzer of lola lenguage
#
# --------------------------------------------------------------

# import modules
from sly import Parser
from lolalex import LolaLexer
from lolaAST import *

# CLASS LolaParser
class LolaParser(Parser):

    def __init__(self):
        self.numerror = 0
    tokens = LolaLexer.tokens

    # debugfile = 'parser.out'
    # Grammar rules and actions

    # program : module;
    @_('module')
    def program(self, p):
        return p[0]

    # expressionListOrEmpty : "(" expressionList ")"
    #                       | empty
    #                       ;
    @_(' "(" expressionList ")" ')
    def expressionListOrEmpty(self, p):
        return ExpressionList(p[1])

    @_('empty')
    def expressionListOrEmpty(self, p):
        return Empty();

    # simpleType  : basicType
    #             | id expressionListOrEmpty
    #             ;
    @_('basicType')
    def simpleType(self, p):
        return p[0]

    @_('id expressionListOrEmpty')
    def simpleType(self, p):
        return p[0].value

    # basicType : "BIT"
    #           | "TS"
    #           | "OC"
    #           ;
    @_('BIT', 'TS', 'OC')
    def basicType(self, p):
        return p[0]

    # expressionList  : expressionList "," expression
    #                 | expression
    #                 ;
    @_('expressionList "," expression')
    def expressionList(self, p):
        p0 = p[0]
        p0.append(p[2])
        return p0

    @_('expressionList error expression')
    def expressionList(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ','")

    @_('expression')
    def expressionList(self, p):
        return [p[0]]

    # parenList : parenList "[" expression "]"
    #           | empty
    #           ;
    @_('parenList "[" expression "]"')
    def parenList(self, p):
        p0 = p[0]
        p0.append(p[2])
        return p0

    @_('"[" expression "]"')
    def parenList(self, p):
        return [p[1]]

    @_('parenList')
    def parenListOrEmpty(self, p):
        return ParenList(p[0])

    @_('empty')
    def parenListOrEmpty(self, p):
        return Empty()

    # type  : parenList simpleType;
    @_('parenListOrEmpty simpleType')
    def type(self, p):
        return Type(p[0], p[1])

    # constDeclaration  : id ":=" expression ";" ;
    @_('id AS expression ";"')
    def constDeclaration(self, p):
        return ConstDec(p[0], p[2], p.lineno)

    @_('error AS expression ";"')
    def constDeclaration(self, p):
        lines = p.lineno
        print ("  Linea",lines," Se espera el ID para asignar")

    @_('id error expression ";"')
    def constDeclaration(self, p):
        lines = p.lineno
        print ("  Linea",lines," Se espera ':=' Error en asignacion.")

    @_('id AS error ";"')
    def constDeclaration(self, p):
        lines = p.lineno
        print ("  Linea",lines," Error en expresion")

    @_('id AS expression error')
    def constDeclaration(self, p):
        lines = p.lineno
        print ("  Linea",lines," Se espera ';' al declarar CONST")

    # varDeclaration  : idList ":" type ";" ;
    @_('idList ":" type ";"')
    def varDeclaration(self, p):
        return VarsDec(IdList(p[0]), p[2], p.lineno)

    @_('error ":" type ";"')
    def varDeclaration(self, p):
        lines = p.lineno
        print ("  Linea",lines," Variables erroneas")

    @_('idList error type ";"')
    def varDeclaration(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ':' al declarar TIPO DATO")

    @_('idList ":" error ";"')
    def varDeclaration(self, p):
        lines = p.lineno
        print ("  Linea",lines," Tipo de dato malo")

    @_('idList ":" type error')
    def varDeclaration(self, p):
        lines = p.lineno
        print ("  Linea",lines," Se espera ';'")

    # idList  : idList "," id
    #         | id
    #         ;
    @_('idList "," id')
    def idList(self, p):
        p0 = p[0]
        p0.append(p[2])
        return p0

    # , no

    @_('idList "," error')
    def idList(self, p):
        lines = p.lineno
        print ("  Linea",lines," ID invalido")

    @_('id')
    def idList(self, p):
        return [p[0]]

    # no
    # selector  : "." id
    #           | "." int
    #           | "[" expression "]"
    #           ;
    @_('"." id', '"." int', '"[" expression "]"')
    def selector(self, p):
        return Selector(p[0], p[1])

    # selectorList  : selectorList selector
    #               | empty
    #               ;
    @_('selectorList selector')
    def selectorList(self, p):
        p0 = p[0]
        p0.append(p[1])
        return p0

    @_('selector')
    def selectorList(self, p):
        return [p[0]]

    @_('selectorList')
    def selectorListOrEmpty(self, p):
        return SelectorList(p[0])

    @_('empty')
    def selectorListOrEmpty(self, p):
        return Empty()

    # factor  : id selectorList
    #         | boolean
    #         | int
    #         | "~" factor
    #         | "↑" factor
    #         | "(" expression ")"
    #         | "MUX" "(" expression ":" expression "," expression ")"
    #         | "REG" "(" expression "," expression ")"
    #         | "LATCH" "(" expression "," expression ")"
    #         | "SR" "(" expression "," expression ")"
    #         ;
    @_('var', 'boolean', 'int')
    def factor(self, p):
        return p[0]

    @_('"~" factor', '"↑" factor')
    def factor(self, p):
        return Modifier(p[0], p[1])

    @_('"(" expression ")"')
    def factor(self, p):
        return p[1]

    @_('MUX "(" expression ":" expression "," expression ")"')
    def factor(self, p):
        return MUX(p[2], p[4], p[6])

    @_('MUX "(" expression error expression "," expression ")"')
    def factor(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ':' en MUX")

    @_('MUX "(" expression ":" expression error expression ")"')
    def factor(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ',' en MUX")

    @_('MUX "(" expression ":" expression "," expression error')
    def factor(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ')' en MUX")

    @_('REG', 'LATCH', 'SR')
    def gate(self, p):
        return p[0]

    @_('gate "(" expression "," expression ")"')
    def factor(self, p):
        return Gate(p[0], p[2], p[4])

    @_('gate error expression "," expression ")"')
    def factor(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera '('")

    @_('gate "(" error "," expression ")"')
    def factor(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera una expresion")

    @_('gate "(" expression error expression ")"')
    def factor(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ','")

    @_('gate "(" expression "," error ")"')
    def factor(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera una expresion")

    @_('gate "(" expression "," expression error')
    def factor(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ')'")

    # op1 : "*"
    #     | "/"
    #     | "DIV"
    #     | "MOD"
    #     ;
    @_('"*"', '"/"', 'DIV', 'MOD')
    def op1(self, p):
        return p[0]

    # term  : term op1 factor
    #       | factor
    #       ;
    @_('term op1 factor')
    def term(self, p):
        return BinOp(p[1], p[0], p[2])

    @_('factor')
    def term(self, p):
        return p[0]

    # op2 : "+"
    #     | "-"
    #     ;
    @_('"+"', '"-"')
    def op2(self, p):
        return p[0]

    # expression  : expression op2 term
    #             | term
    #             ;
    @_('expression op2 term')
    def expression(self, p):
        return BinOp(p[1], p[0], p[2])

    @_('term')
    def expression(self, p):
        return p[0]

    # assignment  : id selectorList ":=" expression ;
    @_('var AS expression')
    def assignment(self, p):
        return Assign(p[0], p[2], p.lineno)

    @_('var error expression')
    def assignment(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera asignacion':='")

    # op3 : "="
    #     | "#"
    #     | "<"
    #     | "<="
    #     | ">"
    #     | ">="
    #     ;
    @_('"="', '"#"', '"<"', 'LE', '">"', 'GE')
    def op3(self, p):
        return p[0]

    @_('error')
    def op3(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ';'")

    # relation  : expression op3 expression ;
    @_('expression op3 expression')
    def relation(self, p):
        return BinOp(p[1], p[0], p[2])

    # elsifStatement  : "ELSIF" relation "THEN" statementSequence ;
    @_('ELSIF relation THEN statementSequence')
    def elsifStatement(self, p):
        return ElsIf(p[1], p[3])

    @_('ELSIF error THEN statementSequence')
    def elsifStatement(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera relacion ELSEIF")

    # elsifStatementList  : elsifStatementList elsifStatement
    #                     | empty
    #                     ;
    @_('elsifStatementList elsifStatement')
    def elsifStatementList(self, p):
        p0 = p[0]
        p0.append(p[1])
        return p0

    @_('elsifStatement')
    def elsifStatementList(self, p):
        return [p[0]]

    @_('elsifStatementList')
    def elsifStatementListOrEmpty(self, p):
        return ElsIfList(p[0])

    @_('empty')
    def elsifStatementListOrEmpty(self, p):
        return Empty()

    # elseStatementOrEmpty : "ELSE" statementSequence
    #                      | empty
    #                      ;
    @_('ELSE statementSequence')
    def elseStatementOrEmpty(self, p):
        return Else(p[1])

    @_('empty')
    def elseStatementOrEmpty(self, p):
        return Empty()

    # ifStatement : "IF" relation "THEN" statementSequence
    #               elsifStatementList
    #               elseStatementOrEmpty
    #               "END"
    #             ;
    @_('IF relation THEN statementSequence elsifStatementListOrEmpty elseStatementOrEmpty END')
    def ifStatement(self, p):
        return If(p[1], p[3], p[4], p[5])

    @_('IF error THEN statementSequence elsifStatementListOrEmpty elseStatementOrEmpty END')
    def ifStatement(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Error relacion IF")

    @_('IF relation THEN error elsifStatementListOrEmpty elseStatementOrEmpty END')
    def ifStatement(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Error relacion IF")

    @_('IF relation THEN statementSequence error elseStatementOrEmpty END')
    def ifStatement(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Error ELSE")

    # forStatement  : "FOR" id ":=" expression ".." expression "DO" statementSequence "END";
    @_('FOR id AS expression TP expression DO statementSequence END')
    def forStatement(self, p):
        return For(p[1], p[3], p[5], p[7], p.lineno)

    @_('FOR error AS expression TP expression DO statementSequence END')
    def forStatement(self, p):
        lines = p.lineno
        print ("    Linea",lines,"Se espera ID en FOR")

    @_('FOR id error expression TP expression DO statementSequence END')
    def forStatement(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Mala asignacion en el FOR")

    @_('FOR id AS expression error expression DO statementSequence END')
    def forStatement(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera '..' en el FOR")

    @_('FOR id AS expression TP expression error statementSequence END')
    def forStatement(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera 'DO' en el FOR")

    # statement : assignment
    #           | unitAssignment
    #           | ifStatement
    #           | forStatement
    #           ;
    @_('assignment', 'unitAssignment', 'ifStatement', 'forStatement')
    def statement(self, p):
        return p[0]

    # statementSequence : statementSequence ";" statement
    #                   | statement
    #                   ;
    @_('statementSequence ";" statement')
    def statementSequence(self, p):
        p0 = p[0]
        p0.append(p[2])
        return p0

    @_('statementSequence error statement')
    def statementSequence(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ';'")

    @_('statement')
    def statementSequence(self, p):
        return [p[0]]

    # typeDeclarationList : typeDeclarationList typeDeclaration ";"
    #                     | empty
    #                     ;
    @_('typeDeclarationList typeDeclaration ";"')
    def typeDeclarationList(self, p):
        p0 = p[0]
        p0.append(p[1])
        return p0

    @_('typeDeclarationList typeDeclaration error')
    def typeDeclarationList(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ';'")

    @_('typeDeclaration ";"')
    def typeDeclarationList(self, p):
        return [p[0]]

    @_('typeDeclarationList')
    def typeDeclarationListOrEmpty(self, p):
        return TypeDecList(p[0])

    @_('empty')
    def typeDeclarationListOrEmpty(self, p):
        return Empty()

    # constDeclarationList : constDeclarationList constDeclaration
    #                      | empty
    #                      ;
    @_('constDeclarationList constDeclaration')
    def constDeclarationList(self, p):
        p0 = p[0]
        p0.append(p[1])
        return p0

    @_('constDeclaration')
    def constDeclarationList(self, p):
        return [p[0]]

    @_('constDeclarationList')
    def constDeclarationListOrEmpty(self, p):
        return ConstDecList(p[0])

    @_('empty')
    def constDeclarationListOrEmpty(self, p):
        return Empty()

    # constDeclarationOrEmpty : "CONST" constDeclarationList
    #                         | empty
    #                         ;
    @_('CONST constDeclarationListOrEmpty')
    def constDeclarationOrEmpty(self, p):
        return p[1]

    @_('empty')
    def constDeclarationOrEmpty(self, p):
        return Empty()

    # varDeclarationList : varDeclarationList varDeclaration
    #                    | empty
    #                    ;
    @_('varDeclarationList varDeclaration')
    def varDeclarationList(self, p):
        p0 = p[0]
        p0.append(p[1])
        return p0

    @_('varDeclaration')
    def varDeclarationList(self, p):
        return [p[0]]

    @_('varDeclarationList')
    def varDeclarationListOrEmpty(self, p):
        return VarDecList(p[0])

    @_('empty')
    def varDeclarationListOrEmpty(self, p):
        return Empty()

    # inDeclarationOrEmpty : "IN" varDeclarationList
    #                      | empty
    #                      ;
    @_('IN varDeclarationListOrEmpty')
    def inDeclarationOrEmpty(self, p):
        return InDec(p[1])

    @_('empty')
    def inDeclarationOrEmpty(self, p):
        return Empty()

    # inoutDeclarationOrEmpty : "INOUT" varDeclarationList
    #                         | empty
    #                         ;
    @_('INOUT varDeclarationListOrEmpty')
    def inoutDeclarationOrEmpty(self, p):
        return InoutDec(p[1])

    @_('empty')
    def inoutDeclarationOrEmpty(self, p):
        return Empty()

    # outDeclarationOrEmpty   : "OUT" varDeclarationList
    #                         | empty
    #                         ;
    @_('OUT varDeclarationListOrEmpty')
    def outDeclarationOrEmpty(self, p):
        return OutDec(p[1])

    @_('empty')
    def outDeclarationOrEmpty(self, p):
        return Empty()

    # varDeclarationOrEmpty   : "VAR" varDeclarationList
    #                         | empty
    #                         ;
    @_('VAR varDeclarationListOrEmpty')
    def varDeclarationOrEmpty(self, p):
        return VarDec(p[1])

    @_('empty')
    def varDeclarationOrEmpty(self, p):
        return Empty()

    # beginDeclarationOrEmpty : "BEGIN" statementSequence
    #                         | empty
    #                         ;
    @_('BEGIN statementSequence')
    def beginDeclarationOrEmpty(self, p):
        return StatementSequence(p[1])

    @_('empty')
    def beginDeclarationOrEmpty(self, p):
        return Empty()

    # module  : "MODULE" id ";"
    #           typeDeclarationList
    #           constDeclarationOrEmpty
    #           inDeclarationOrEmpty
    #           inoutDeclarationOrEmpty
    #           outDeclarationOrEmpty
    #           varDeclarationOrEmpty
    #           beginDeclarationOrEmpty
    #           "END" id "."
    #         ;
    @_('MODULE id ";" typeDeclarationListOrEmpty constDeclarationOrEmpty inDeclarationOrEmpty inoutDeclarationOrEmpty outDeclarationOrEmpty varDeclarationOrEmpty beginDeclarationOrEmpty END id "." ')
    def module(self, p):
        return Module(p[1], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[11], p.lineno)

    @_('MODULE id error typeDeclarationListOrEmpty constDeclarationOrEmpty inDeclarationOrEmpty inoutDeclarationOrEmpty outDeclarationOrEmpty varDeclarationOrEmpty beginDeclarationOrEmpty END id "." ')
    def module(self, p):
        lines = p.lineno
        print ("Error fatal!   Linea",lines,"Se espera un ';' al final de MODULE o ';'")

    @_('MODULE id ";" typeDeclarationListOrEmpty constDeclarationOrEmpty inDeclarationOrEmpty inoutDeclarationOrEmpty outDeclarationOrEmpty varDeclarationOrEmpty beginDeclarationOrEmpty END id error ')
    def module(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera '.' al finalizar programa")

    @_('MODULE id ";" typeDeclarationListOrEmpty constDeclarationOrEmpty inDeclarationOrEmpty inoutDeclarationOrEmpty outDeclarationOrEmpty varDeclarationOrEmpty beginDeclarationOrEmpty END error "." ')
    def module(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Finalice con el ID de MODULE")

    # expressionOrEmpty : expression
    #                   | empty
    #                   ;
    @_('expression')
    def expressionOrEmpty(self, p):
        return Expr(p[0])

    @_('empty')
    def expressionOrEmpty(self, p):
        return Empty()

    # formalParenList   : formalParenList "[" expressionOrEmpty "]"
    #                   | empty
    #                   ;
    @_('formalParenList "[" expressionOrEmpty "]"')
    def formalParenList(self, p):
        p0 = p[0]
        p0.append(p[2])
        return p0

    @_('"[" expressionOrEmpty "]"')
    def formalParenList(self, p):
        return [p[1]]

    @_('formalParenList')
    def formalParenListOrEmpty(self, p):
        return FormalParenList(p[0])

    @_('empty')
    def formalParenListOrEmpty(self, p):
        return Empty()

    # formalType : formalParenList "BIT" ;
    @_('formalParenListOrEmpty BIT')
    def formalType(self, p):
        return Type(p[0], p[1])

    # formalBusType : formalParenList "TS"
    #               | formalParenList "OC"
    #               ;
    @_('formalParenListOrEmpty TS', 'formalParenListOrEmpty OC')
    def formalBusType(self, p):
        return Type(p[0], p[1])

    # asteriskOrEmpty : "*"
    #                 | empty
    #                 ;
    @_('"*"')
    def asteriskOrEmpty(self, p):
        return p[0]

    @_('empty')
    def asteriskOrEmpty(self, p):
        return Empty()

    # idListOrEmpty   : "(" idList ")"
    #                 | empty
    #                 ;
    @_(' "(" idList ")" ')
    def idListOrEmpty(self, p):
        return IdList(p[1])

    @_('empty')
    def idListOrEmpty(self, p):
        return Empty()

    # formalTypeList  : formalTypeList idList ":" formalType ";"
    #                 | empty
    #                 ;
    @_('formalTypeList idList ":" formalType ";"')
    def formalTypeList(self, p):
        p0 = p[0]
        p0.append(VarsDec(IdList(p[1]), p[3], p.lineno))
        return p0

    @_('idList ":" formalType ";"')
    def formalTypeList(self, p):
        return VarsDec(IdList(p[0]), p[2], p.lineno)

    @_('idList error formalType ";"')
    def formalTypeList(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ';'")

    @_('formalTypeList')
    def formalTypeListOrEmpty(self, p):
        return FormalTypeList(p[0])

    @_('empty')
    def formalTypeListOrEmpty(self, p):
        return Empty()

    # inFormalDeclarationOrEmpty  : "IN" formalTypeList
    #                             | empty
    #                             ;
    @_('IN formalTypeListOrEmpty')
    def inFormalDeclarationOrEmpty(self, p):
        return InDec(p[1])

    @_('empty')
    def inFormalDeclarationOrEmpty(self, p):
        return Empty()

    # formalBusTypeList : formalBusTypeList idList ":" formalBusType ";"
    #                   | empty
    #                   ;
    @_('formalBusTypeList idList ":" formalBusType ";"')
    def formalBusTypeList(self, p):
        p0 = p[0]
        p0.append(VarsDec(IdList(p[1]), p[3], p.lineno))
        return p0

    @_('formalBusTypeList idList error formalBusType ";"')
    def formalBusTypeList(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ':'")

    @_('formalBusTypeList idList ":" error ";"')
    def formalBusTypeList(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Error Tipo")

    @_('formalBusTypeList idList ":" formalBusType error')
    def formalBusTypeList(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ':'")

    @_('idList ":" formalBusType ";"')
    def formalBusTypeList(self, p):
        return VarsDec(IdList(p[0]), p[2], p.lineno)

    @_('formalBusTypeList')
    def formalBusTypeListOrEmpty(self, p):
        return FormalBusTypeList(p[0])

    @_('empty')
    def formalBusTypeListOrEmpty(self, p):
        return Empty()

    # inoutFormalDeclarationOrEmpty : "INOUT" formalBusTypeList
    #                               | empty
    #                               ;
    @_('INOUT formalBusTypeListOrEmpty')
    def inoutFormalDeclarationOrEmpty(self, p):
        return InoutDec(p[1])

    @_('empty')
    def inoutFormalDeclarationOrEmpty(self, p):
        return Empty()

    # typeDeclaration : "TYPE" id asteriskOrEmpty idListOrEmpty ";"
    #                   constDeclarationOrEmpty
    #                   inFormalDeclarationOrEmpty
    #                   inoutFormalDeclarationOrEmpty
    #                   outDeclarationOrEmpty
    #                   varDeclarationOrEmpty
    #                   beginDeclarationOrEmpty
    #                   "END" id
    #                 ;
    @_('TYPE id asteriskOrEmpty idListOrEmpty ";" constDeclarationOrEmpty inFormalDeclarationOrEmpty inoutFormalDeclarationOrEmpty outDeclarationOrEmpty varDeclarationOrEmpty beginDeclarationOrEmpty END id')
    def typeDeclaration(self, p):
        return TypeDec(p[1], p[2], p[3], p[5], p[6], p[7], p[8], p[9], p[10], p[12], p.lineno)

    @_('TYPE id asteriskOrEmpty idListOrEmpty error constDeclarationOrEmpty inFormalDeclarationOrEmpty inoutFormalDeclarationOrEmpty outDeclarationOrEmpty varDeclarationOrEmpty beginDeclarationOrEmpty END id')
    def typeDeclaration(self, p):
        lines = p.lineno
        print ("  Linea",lines,"Se espera ';' en TYPE")

    # unitAssignment  : id selectorList "(" expressionList ")" ;
    @_('var "(" expressionList ")" ')
    def unitAssignment(self, p):
        return UnitAssign(p[0], p[2])

    # empty
    @_('')
    def empty(self, p):
        pass

    @_('id selectorListOrEmpty')
    def var(self, p):
        return Var(p[0], p[1])

    # identifier
    @_('IDENTIFIER')
    def id(self, p):
        return Id(p[0])

    # int
    @_('INTEGER')
    def int(self, p):
        return Int(p[0])

    # boolean
    @_('LOGICVALUE')
    def boolean(self, p):
        return Boolean(p[0])

    def error(self, p):
    	if p:
            self.numerror = self.numerror + 1
            print("Error",self.numerror)
            print('  Error de sintaxis antes de', p.type)
            #self.errok()
            self.tokens
    	else:
            print("End of file!")
