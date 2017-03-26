# --------------------------------------------------------------
# compiler: lolaparse.py
#
# Grammar analyzer of lola lenguage
#
# --------------------------------------------------------------

# import modules
from sly import Parser
from lolalex import LolaLexer

# CLASS LolaParser
class LolaParser(Parser):

    # Get the token list from the lexer (required)
    tokens = LolaLexer.tokens

    # Grammar rules and actions

    # program : module;
    @_('module')
    def program(self, p):
        pass

    # expressionListOrEmpty : "(" expressionList ")"
    #                       | empty
    #                       ;
    @_(' "(" expressionList ")" ')
    def expressionListOrEmpty(self, p):
        pass

    @_('empty')
    def expressionListOrEmpty(self, p):
        pass

    # simpleType  : basicType
    #             | id expressionListOrEmpty
    #             ;
    @_('basicType')
    def simpleType(self, p):
        pass

    @_('id expressionListOrEmpty')
    def simpleType(self, p):
        pass

    # basicType : "BIT"
    #           | "TS"
    #           | "OC"
    #           ;
    @_('BIT')
    def basicType(self, p):
        pass

    @_('TS')
    def basicType(self, p):
        pass

    @_('OC')
    def basicType(self, p):
        pass

    # expressionList  : expressionList "," expression
    #                 | expression
    #                 ;
    @_('expressionList "," expression')
    def expressionList(self, p):
        pass

    @_('expression')
    def expressionList(self, p):
        pass

    # parenList : parenList "[" expression "]"
    #           | empty
    #           ;
    @_('parenList "[" expression "]"')
    def parenList(self, p):
        pass

    @_('"[" expression "]"')
    def parenList(self, p):
        pass

    @_('parenList')
    def parenListOrEmpty(self, p):
        pass

    @_('empty')
    def parenListOrEmpty(self, p):
        pass

    # type  : parenList simpleType;
    @_('parenListOrEmpty simpleType')
    def type(self, p):
        pass

    # constDeclaration  : id ":=" expression ";" ;
    @_('id AS expression ";"')
    def constDeclaration(self, p):
        pass

    # varDeclaration  : idList ":" type ";" ;
    @_('idList ":" type ";"')
    def varDeclaration(self, p):
        pass

    # idList  : idList "," id
    #         | id
    #         ;
    @_('idList "," id')
    def idList(self, p):
        pass

    @_('id')
    def idList(self, p):
        pass

    # selector  : "." id
    #           | "." int
    #           | "[" expression "]"
    #           ;
    @_('"." id')
    def selector(self, p):
        pass

    @_('"." int')
    def selector(self, p):
        pass

    @_('"[" expression "]"')
    def selector(self, p):
        pass

    # selectorList  : selectorList selector
    #               | empty
    #               ;
    @_('selectorList selector')
    def selectorList(self, p):
        pass

    @_('selector')
    def selectorList(self, p):
        pass

    @_('selectorList')
    def selectorListOrEmpty(self, p):
        pass

    @_('empty')
    def selectorListOrEmpty(self, p):
        pass

    # factor  : id selectorList
    #         | boolean
    #         | int
    #         | "~" factor
    #         | "↑" factor
    #         | "(" expression ")"
    #         | "MUX" "(" expression ":" expression "," expression ")"
    #         | "MUX" "(" expression "," expression ":" expression "," expression ":" expression "," expression ")"
    #         | "REG" "(" expression ")"
    #         | "REG" "(" expression "," expression ")"
    #         | "LATCH" "(" expression "," expression ")"
    #         | "SR" "(" expression "," expression ")"
    #         ;
    @_('id selectorListOrEmpty')
    def factor(self, p):
        pass

    @_('boolean')
    def factor(self, p):
        pass

    @_('int')
    def factor(self, p):
        pass

    @_('"~" factor')
    def factor(self, p):
        pass

    @_('"↑" factor')
    def factor(self, p):
        pass

    @_('"(" expression ")"')
    def factor(self, p):
        pass

    @_('MUX "(" expression ":" expression "," expression ")"')
    def factor(self, p):
        pass

    @_('MUX "(" expression "," expression ":" expression "," expression ":" expression "," expression ")"')
    def factor(self, p):
        pass

    @_('REG "(" expression ")"')
    def factor(self, p):
        pass

    @_('REG "(" expression "," expression ")"')
    def factor(self, p):
        pass

    @_('LATCH "(" expression "," expression ")"')
    def factor(self, p):
        pass

    @_('SR "(" expression "," expression ")"')
    def factor(self, p):
        pass

    # op1 : "*"
    #     | "/"
    #     | "DIV"
    #     | "MOD"
    #     ;
    @_('"*"')
    def op1(self, p):
        pass

    @_('"/"')
    def op1(self, p):
        pass

    @_('DIV')
    def op1(self, p):
        pass

    @_('MOD')
    def op1(self, p):
        pass

    # term  : term op1 factor
    #       | factor
    #       ;
    @_('term op1 factor')
    def term(self, p):
        pass

    @_('factor')
    def term(self, p):
        pass

    # op2 : "+"
    #     | "-"
    #     ;
    @_('"+"')
    def op2(self, p):
        pass

    @_('"-"')
    def op2(self, p):
        pass

    # expression  : expression op2 term
    #             | term
    #             ;
    @_('expression op2 term')
    def expression(self, p):
        pass

    @_('term')
    def expression(self, p):
        pass

    # assignment  : id selectorList ":=" expression ;
    @_('id selectorListOrEmpty AS expression')
    def assignment(self, p):
        pass

    # op3 : "="
    #     | "#"
    #     | "<"
    #     | "<="
    #     | ">"
    #     | ">="
    #     ;
	# Rules for tokens en el analizador lexico
	# LE = r'<='
	# GE = r'>='
    @_('"="')
    def op3(self, p):
        pass

    @_('"#"')
    def op3(self, p):
        pass

    @_('"<"')
    def op3(self, p):
        pass

    @_('LE')
    def op3(self, p):
        pass

    @_('">"')
    def op3(self, p):
        pass

    @_('GE')
    def op3(self, p):
        pass

    # relation  : expression op3 expression ;
    @_('expression op3 expression')
    def relation(self, p):
        pass

    # elsifStatement  : "ELSIF" relation "THEN" statementSequence ;
    @_('ELSIF relation THEN statementSequence')
    def elsifStatement(self, p):
        pass

    # elsifStatementList  : elsifStatementList elsifStatement
    #                     | empty
    #                     ;
    @_('elsifStatementList elsifStatement')
    def elsifStatementList(self, p):
        pass

    @_('elsifStatement')
    def elsifStatementList(self, p):
        pass

    @_('elsifStatementList')
    def elsifStatementListOrEmpty(self, p):
        pass

    @_('empty')
    def elsifStatementListOrEmpty(self, p):
        pass

    # elseStatementOrEmpty : "ELSE" statementSequence
    #                      | empty
    #                      ;
    @_('ELSE statementSequence')
    def elseStatementOrEmpty(self, p):
        pass

    @_('empty')
    def elseStatementOrEmpty(self, p):
        pass

    # ifStatement : "IF" relation "THEN" statementSequence
    #               elsifStatementList
    #               elseStatementOrEmpty
    #               "END"
    #             ;
    @_('IF relation THEN statementSequence elsifStatementListOrEmpty elseStatementOrEmpty END')
    def ifStatement(self, p):
        pass

    # forStatement  : "FOR" id ":=" expression ".." expression "DO" statementSequence "END";
    @_('FOR id AS expression TP expression DO statementSequence END')
    def forStatement(self, p):
        pass

    # statement : assignment
    #           | unitAssignment
    #           | ifStatement
    #           | forStatement
    #           ;
    @_('assignment')
    def statement(self, p):
        pass

    @_('unitAssignment')
    def statement(self, p):
        pass

    @_('ifStatement')
    def statement(self, p):
        pass

    @_('forStatement')
    def statement(self, p):
        pass

    # statementSequence : statementSequence ";" statement
    #                   | statement
    #                   ;
    @_('statementSequence ";" statement')
    def statementSequence(self, p):
        pass

    @_('statement')
    def statementSequence(self, p):
        pass

    # typeDeclarationList : typeDeclarationList typeDeclaration ";"
    #                     | empty
    #                     ;
    @_('typeDeclarationList typeDeclaration ";"')
    def typeDeclarationList(self, p):
        pass

    @_('typeDeclaration ";"')
    def typeDeclarationList(self, p):
        pass

    @_('typeDeclarationList')
    def typeDeclarationListOrEmpty(self, p):
        pass

    @_('empty')
    def typeDeclarationListOrEmpty(self, p):
        pass

    # constDeclarationList : constDeclarationList constDeclaration
    #                      | empty
    #                      ;
    @_('constDeclarationList constDeclaration')
    def constDeclarationList(self, p):
        pass

    @_('constDeclaration')
    def constDeclarationList(self, p):
        pass

    @_('constDeclarationList')
    def constDeclarationListOrEmpty(self, p):
        pass

    @_('empty')
    def constDeclarationListOrEmpty(self, p):
        pass

    # constDeclarationOrEmpty : "CONST" constDeclarationList
    #                         | empty
    #                         ;
    @_('CONST constDeclarationListOrEmpty')
    def constDeclarationOrEmpty(self, p):
        pass

    @_('empty')
    def constDeclarationOrEmpty(self, p):
        pass

    # varDeclarationList : varDeclarationList varDeclaration
    #                    | empty
    #                    ;
    @_('varDeclarationList varDeclaration')
    def varDeclarationList(self, p):
        pass

    @_('varDeclaration')
    def varDeclarationList(self, p):
        pass

    @_('varDeclarationList')
    def varDeclarationListOrEmpty(self, p):
        pass

    @_('empty')
    def varDeclarationListOrEmpty(self, p):
        pass

    # inDeclarationOrEmpty : "IN" varDeclarationList
    #                      | empty
    #                      ;
    @_('IN varDeclarationListOrEmpty')
    def inDeclarationOrEmpty(self, p):
        pass

    @_('empty')
    def inDeclarationOrEmpty(self, p):
        pass

    # inoutDeclarationOrEmpty : "INOUT" varDeclarationList
    #                         | empty
    #                         ;
    @_('INOUT varDeclarationListOrEmpty')
    def inoutDeclarationOrEmpty(self, p):
        pass

    @_('empty')
    def inoutDeclarationOrEmpty(self, p):
        pass

    # outDeclarationOrEmpty   : "OUT" varDeclarationList
    #                         | empty
    #                         ;
    @_('OUT varDeclarationListOrEmpty')
    def outDeclarationOrEmpty(self, p):
        pass

    @_('empty')
    def outDeclarationOrEmpty(self, p):
        pass

    # varDeclarationOrEmpty   : "VAR" varDeclarationList
    #                         | empty
    #                         ;
    @_('VAR varDeclarationListOrEmpty')
    def varDeclarationOrEmpty(self, p):
        pass

    @_('empty')
    def varDeclarationOrEmpty(self, p):
        pass

    # beginDeclarationOrEmpty : "BEGIN" statementSequence
    #                         | empty
    #                         ;
    @_('BEGIN statementSequence')
    def beginDeclarationOrEmpty(self, p):
        pass

    @_('empty')
    def beginDeclarationOrEmpty(self, p):
        pass

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
        pass

    # expressionOrEmpty : expression
    #                   | empty
    #                   ;
    @_('expression')
    def expressionOrEmpty(self, p):
        pass

    @_('empty')
    def expressionOrEmpty(self, p):
        pass

    # formalParenList   : formalParenList "[" expressionOrEmpty "]"
    #                   | empty
    #                   ;
    @_('formalParenList "[" expressionOrEmpty "]"')
    def formalParenList(self, p):
        pass

    @_('"[" expressionOrEmpty "]"')
    def formalParenList(self, p):
        pass

    @_('formalParenList')
    def formalParenListOrEmpty(self, p):
        pass

    @_('empty')
    def formalParenListOrEmpty(self, p):
        pass

    # formalType : formalParenList "BIT" ;
    @_('formalParenListOrEmpty BIT')
    def formalType(self, p):
        pass

    # formalBusType : formalParenList "TS"
    #               | formalParenList "OC"
    #               ;
    @_('formalParenListOrEmpty TS')
    def formalBusType(self, p):
        pass

    @_('formalParenListOrEmpty OC')
    def formalBusType(self, p):
        pass

    # asteriskOrEmpty : "*"
    #                 | empty
    #                 ;
    @_('"*"')
    def asteriskOrEmpty(self, p):
        pass

    @_('empty')
    def asteriskOrEmpty(self, p):
        pass

    # idListOrEmpty   : "(" idList ")"
    #                 | empty
    #                 ;
    @_(' "(" idList ")" ')
    def idListOrEmpty(self, p):
        pass

    @_('empty')
    def idListOrEmpty(self, p):
        pass

    # formalTypeList  : formalTypeList idList ":" formalType ";"
    #                 | empty
    #                 ;
    @_('formalTypeList idList ":" formalType ";"')
    def formalTypeList(self, p):
        pass

    @_('idList ":" formalType ";"')
    def formalTypeList(self, p):
        pass

    @_('formalTypeList')
    def formalTypeListOrEmpty(self, p):
        pass

    @_('empty')
    def formalTypeListOrEmpty(self, p):
        pass

    # inFormalDeclarationOrEmpty  : "IN" formalTypeList
    #                             | empty
    #                             ;
    @_('IN formalTypeListOrEmpty')
    def inFormalDeclarationOrEmpty(self, p):
        pass

    @_('empty')
    def inFormalDeclarationOrEmpty(self, p):
        pass

    # formalBusTypeList : formalBusTypeList idList ":" formalBusType ";"
    #                   | empty
    #                   ;
    @_('formalBusTypeList idList ":" formalBusType ";"')
    def formalBusTypeList(self, p):
        pass

    @_('idList ":" formalBusType ";"')
    def formalBusTypeList(self, p):
        pass

    @_('formalBusTypeList')
    def formalBusTypeListOrEmpty(self, p):
        pass

    @_('empty')
    def formalBusTypeListOrEmpty(self, p):
        pass

    # inoutFormalDeclarationOrEmpty : "INOUT" formalBusTypeList
    #                               | empty
    #                               ;
    @_('INOUT formalBusTypeListOrEmpty')
    def inoutFormalDeclarationOrEmpty(self, p):
        pass

    @_('empty')
    def inoutFormalDeclarationOrEmpty(self, p):
        pass

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
        pass

    # unitAssignment  : id selectorList "(" expressionList ")" ;
    @_('id selectorListOrEmpty "(" expressionList ")" ')
    def unitAssignment(self, p):
        pass

    # empty
    @_('')
    def empty(self, p):
        pass

    # identifier
    @_('IDENTIFIER')
    def id(self, p):
        pass

    # int
    @_('INTEGER')
    def int(self, p):
        pass

    # boolean
    @_('LOGICVALUE')
    def boolean(self, p):
        pass
