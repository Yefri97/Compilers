# Lola - Dibujar AST + graphviz

from lolaAST import NodeVisitor

class LolaSemantic(NodeVisitor):
    def __init__(self):
        super(LolaSemantic, self).__init__()

    def visit_Module(self, node):
        pass

    def visit_TypeDec(self, node):
        # Crea la tabla de simbolos

        # Activa bandera: Explora la rama de declaración

        # Agrega tabla de simbolos en la pila

        # Desactiva bandera: Explora el nodo StatementSequence

        # Elimina top de la pila de tabla de simbolos

        # Guarda en la tabla de simbolos global el nombre de este tipo


    def visit_Id(self, node):
        # If bandera esta activa
            # Guarde en la tabla de simbolos
        # else
            # Consulte en la pila de tabla de simbolos

    def visit_For(self, node):
        pass

    def visit_StatementSequence(self, node):
        pass

    def generic_visit(self, node):
        self.visit_children(node)
